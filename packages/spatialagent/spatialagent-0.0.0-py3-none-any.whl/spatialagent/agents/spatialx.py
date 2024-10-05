import time, logging
from datetime import datetime
from typing import List, Optional, Tuple
from pydantic.v1 import BaseModel, Field
from langchain.schema import SystemMessage
from langchain.agents import initialize_agent
from langchain import LLMChain, PromptTemplate
from langchain.base_language import BaseLanguageModel
from langchain_community.callbacks import get_openai_callback
from tokencost import calculate_prompt_cost, calculate_completion_cost
from langchain.chains.conversation.memory import ConversationBufferWindowMemory


class SpatialX(BaseModel):
    """Spatial Transcriptomics Agent"""

    name: str
    game_name: str
    observation_rule: str
    base_path: str
    status: str
    llm: BaseLanguageModel

    # Configuration settings
    verbose: bool = False
    reflection_threshold: Optional[float] = None
    current_plan: List[str] = []
    belief: str = ""
    pattern: str = ""
    long_belief: str = ""
    counter_belief: str = ""
    plan: str = ""
    high_plan: str = ""

    # Memory components
    memory: List = [""]
    plan_memory: List = [""]
    episodic_memory: List = [""]
    semantic_memory: List = [""]
    summary: str = ""
    summary_refresh_seconds: int = 3600
    last_refreshed: datetime = Field(default_factory=datetime.now)
    memory_importance: float = 0.0
    rule: str = ""

    # Cost related attributes
    max_tokens_limit: int = 1200
    read_observation: str = ""
    prompt_cost: float = 0.0
    completion_cost: float = 0.0
    total_cost: float = 0.0
    model_cost: str = "gpt-4"  # "azure/gpt-4"

    class Config:
        arbitrary_types_allowed = True

    def planning(self, tools: list, last_k: int = 10) -> str:
        """Generate a planning prompt and compute associated costs."""

        prompt = PromptTemplate.from_template(
            " Please understand all current knowledge about the {game_name}: {semantic_memory}.\n"
            " My previous plan is {plan}."
            " My 10 previous steps of actions and conversations are: {episodi_memory}.\n"
            " My last step of actions and conversations is: {most_recent_episodi_memory}"
            " Is the overal task and goal finished? If the overal task and goalis complete, return with [STOP]."
            " If not, understanding the task goal, your previous plan, previous actions and observations, can you do following things? "
            " Do I have a previous plan? If I did't plan anything, make reasonable plans: Please plan several steps according to actions {valid_action_list} you can do now to finish the finally whole {game_name} task step by step. "
            "Plan: "
            "Step 1:  If I execute Step 1, what tools should I use? Do I have the input ? If not, what should I do? "
            "What is the expected output? Is it what is needed now?"
            "Step 2: If I execute Step 2, what is the input ... continue .."
            "Step 3: .. Continue ... "
            " If I had previous plans, have I taken any steps? What is the last round of step I just took? Is the result as expected? If the result is not as expected, re-take the previous step. If the result is as expected, continue to the next step. "
            "Current status thinking and step selection:"
            "What is current iteration round? Which next step should I take? What is the input to this step? What is the expected output?"
            "You must give detailed input information to the tool of this step. For example, you can't say input is 'path of previous step' or 'Extracted from the output of Step'. You must give the absolute file path or accurate information. If no accurate information is available from the previous step, you must re-take the previous step."
            ""
        )

        all_episodic_str = "\n\n".join([o for o in self.episodic_memory[-last_k:]])
        all_semantic_memory_str = "\n\n".join([o for o in self.semantic_memory])

        kwargs = dict(
            episodi_memory=all_episodic_str,
            semantic_memory=all_semantic_memory_str,
            plan=self.plan_memory[-1],
            most_recent_episodi_memory=self.episodic_memory[-1],
            agent_name=self.name,
            game_name=self.game_name,
            rule=self.rule,
            valid_action_list=tools,
        )

        """ === Syntax in Langchain v0.1 === """
        # belief_prediction_chain = LLMChain(llm=self.llm, prompt=prompt)
        # self.belief = belief_prediction_chain.run(**kwargs)

        """ === Syntax in Langchain v0.2 ==="""
        # REF: https://api.python.langchain.com/en/latest/chains/langchain.chains.llm.LLMChain.html
        from langchain_core.output_parsers import StrOutputParser

        chain = prompt | self.llm | StrOutputParser()
        self.belief = chain.invoke(kwargs)

        # Calculate cost
        prompt_string = prompt.format(**kwargs)
        self.total_cost += float(calculate_prompt_cost(prompt_string, self.model_cost))
        self.total_cost += float(calculate_completion_cost(self.belief, self.model_cost))

        return self.belief.strip()

    def action_decision(self, valid_action_list: List[str], promp_head: str, act: str = None, last_k=10) -> Tuple[str, str]:
        """React to a given observation."""
        prompt = PromptTemplate.from_template(
            promp_head
            + "\nYour plan is: {plan}\n"
            # + " Your previous progress summarization including actions and conversations is: {episodi_memory}\n"
            # + "\n Based on the plan, please select the current tool from the available action list: {valid_action_list}. Output need be the following format:"
            + "Extract information of current step to take. Don't change information. Reformat it to the following format:\n"
            + "Use Tool: ..."
            + "Input to the tool: ..."
            + "Expected output: ..."
            + "\n\n"
        )

        all_episodic_str = "\n\n".join([o for o in self.episodic_memory[-last_k:]])

        kwargs = dict(
            valid_action_list=valid_action_list,
            episodi_memory=all_episodic_str,
            plan=self.plan,
        )
        action_prediction_chain = LLMChain(llm=self.llm, prompt=prompt)
        result = action_prediction_chain.run(**kwargs)

        # Calculate cost
        prompt_string = prompt.format(**kwargs)
        self.total_cost += float(calculate_prompt_cost(prompt_string, self.model_cost))
        self.total_cost += float(calculate_completion_cost(result, self.model_cost))

        if "|" in result:
            result, result_comment = result.split("|", 1)
        else:
            result_comment = ""
        return result.strip(), result_comment.strip()

    def make_act(self, tools):
        """Generate action based on observation and available tools."""
        self.plan = self.planning(tools)
        if "[STOP]" in self.plan:
            return "STOP"

        logging.info(f"\033[31mPlan: \033[0m \n{self.plan}\n\n")

        time.sleep(2)
        self.add_plan_memory(self.plan)
        use_tool, comment = self.action_decision(valid_action_list=tools, promp_head="")

        logging.info(f"\033[95mCurrent act:\033[0m {use_tool}")
        logging.info(comment)
        return use_tool

    def match_tools(self, action, all_tools):
        """Match the action with available tools and execute it."""
        matched = False
        action_tool = action.split("Use Tool")[1].split("Input")[0]
        for tool in all_tools:
            if tool.name in action_tool:
                logging.info(f"\n\n Calling tool: {tool.name} ... \n")
                conversational_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5, return_messages=True)

                sys_msg = (
                    " You are an action agent helping with the task."
                    " You must execute the tool at least once. You can't skip the tool running."
                    " You can only act once. Do not use Observation and start a second new round of Action."
                    # " Judge if the execution is successful. If yes, stop."
                    " Do not change the output or iterate."
                    " Return the last round of Observation in the output."
                )
                system_message = SystemMessage(content=sys_msg)

                agent = initialize_agent(
                    agent="structured-chat-zero-shot-react-description",
                    tools=[tool],
                    llm=self.llm,
                    verbose=True,
                    max_iterations=5,
                    system_message=system_message,
                    early_stopping_method="generate",
                    memory=conversational_memory,
                )
                agent.tools = [tool]

                with get_openai_callback() as cb:
                    # NOTE: places that generate colorful blocks in console
                    try:
                        result = agent(action)
                    except Exception as e:
                        return (f"An error occurred: {str(e)}.")
        
                    self.total_cost += cb.total_cost

                logging.info(f"\033[95mExecution result: \033[0m{result['output']}")
                matched = True
                break

        if not matched:
            raise ValueError("No such tool found in the tool list.")
        return result["output"]

    def execute_act(self, use_tool: str, all_tools: List) -> str:
        """Execute the chosen action using available tools."""
        return self.match_tools(use_tool, all_tools)

    def get_summarization(self, long_memory: str) -> str:
        """Summarize long-term memory to save costs."""
        prompt = PromptTemplate.from_template(
            " Please understand all current knowledge about the {game_name}: {semantic_memory}.\n"
            + " Understanding the task rule, observation conversion rules and task history and your knowledge about the {game_name}, can you do following things:"
            + " History summarization: summary the last round memory of {long_memory} with action, observation, and results information."
            + " Response and results in the last round actions is key information, you must memorize all the key information all the time, like the dataset id, dataset title, collection name, url, cell types, marker genes."
            + " Use the templete, and respond shortly: In the round xx, I have taken action .... response is ..."
        )

        all_semantic_memory_str = "\n\n".join([o for o in self.semantic_memory])
        reflection_chain = LLMChain(llm=self.llm, prompt=prompt, verbose=self.verbose)
        kwargs = dict(
            semantic_memory=all_semantic_memory_str,
            long_memory=long_memory,
            game_name=self.game_name,
        )

        self.long_belief = reflection_chain.run(**kwargs).strip()
        return self.long_belief

    def add_long_memory(self, memory_content: str) -> List[str]:
        """Add an observation or memory to the agent's memory."""
        self.memory.append(memory_content)
        return self.memory

    def add_semantic_memory(self, memory_content: str) -> List[str]:
        """Add an observation or memory to the agent's memory."""
        self.semantic_memory.append(memory_content)
        return self.semantic_memory

    def add_episodic_memory(self, memory_content: str) -> List[str]:
        """Add an observation or memory to the agent's memory."""
        self.episodic_memory.append(memory_content)
        return self.episodic_memory

    def add_plan_memory(self, memory_content: str) -> List[str]:
        """Add an observation or memory to the agent's memory."""
        self.plan_memory.append(memory_content)
        return self.plan_memory
