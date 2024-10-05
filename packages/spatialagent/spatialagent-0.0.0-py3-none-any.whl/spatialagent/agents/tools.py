from spatialx.tools import *
from langchain.base_language import BaseLanguageModel


def make_tools(
    llm: BaseLanguageModel,
    llm_4o: BaseLanguageModel,
    embeddings: BaseLanguageModel,
    base_path: str,
    save_path: str,
    args=None,
):

    czi_file_path = f"{base_path}/data/czi_census_datasets_v2_short.csv"
    chroma_path = f"{base_path}/data/chroma_czi_census_datasets_v3"

    if args.task_id == "task1":
        czi_retriever_tool = fun_czi_retriever3_tool(embeddings, czi_file_path, chroma_path)

        all_tools = [
            czi_retriever_tool,
            ReadCZIData3TOOL(save_path),
            PangDBSEARCHTool(embeddings, base_path),
            CellMarker2Tool(embeddings, base_path),
            GeneImportanceTool(llm),
            GeneVotingTool(llm),
        ]
    elif args.task_id == "task2":
        czi_retriever_tool = fun_czi_retriever_tool(embeddings, czi_file_path, chroma_path)
        czi_all_celltype_pth = f"{base_path}/data/czi_all_celltypes.txt"
        all_tools = [
            czi_retriever_tool,
            ScanpyPreprocessTool(save_path),
            get_czi_info_tool(base_path, save_path, llm),
            HarmonyTransferTool(save_path),
            ComboGPTCellTypeTool(llm, save_path, czi_all_celltype_pth),
            MainUTAGTool(save_path),
            ComboGPTTissueNicheTool(llm, llm_4o, save_path, args.rule_anatomica_tissue_path),
            ComboSUBGPTCellTypeTool(llm, save_path, czi_all_celltype_pth),
            SubUTAGTool(save_path),
            ComboSUBGPTTissueNicheTool(llm, save_path),
            SaveAnnoTool(llm, save_path),
        ]
    elif args.task_id == "task3":
        # all_tools = [czi_retriever_tool]
        all_tools = [
            SummarizeBatchAnnoTool(llm, save_path), 
            SummarizeCellTypeAnnoTool(llm, save_path), 
            SummarizeTissueRegionAnnoTool(llm, save_path), 
            CCITool(llm, save_path),
            InferLRTool(llm, save_path)
            ]

    elif args.task_id == "tool_test":
        if not hasattr(args, "tool_to_test") or not args.tool_to_test:
            raise ValueError("For testing_tool task, you must specify a tool_to_test in args")
        if args.tool_to_test == "GeneVotingTool":
            all_tools = [GeneVotingTool(llm)]
        else:
            raise ValueError(f"Invalid tool_to_test: {args.tool_to_test}")
    else:
        raise ValueError("Invalid taskid")

#     p = 0

#     from langchain import hub
#     from langchain.agents import AgentExecutor, create_openai_tools_agent, create_tool_calling_agent

#     # initialize agent with tools
#     from langchain.agents import initialize_agent
#     from langchain.chains.conversation.memory import ConversationBufferWindowMemory
#     from langchain.schema import AIMessage, HumanMessage, SystemMessage

#     tools = [all_tools[4]]

#     conversational_memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5, return_messages=True)

#     sys_msg = (
#         "You are an action agent helping with the task."
#         "You must execute the tool. You can't skip the tool running"
#         "Judge if the execution is successful. If yes, stop."
#         " Do not change the output or iterate."
#     )
#     system_message = SystemMessage(content=sys_msg)

#     agent = initialize_agent(
#         agent="structured-chat-zero-shot-react-description",
#         tools=tools,
#         llm=llm,
#         verbose=True,
#         max_iterations=3,
#         system_message=system_message,
#         early_stopping_method="generate",
#         memory=conversational_memory,
#     )

#     agent.tools = tools

#     query_input = """ 
#  Use Tool: InferLRConfidence
# Input to the tool: 
# spatial_adata_input_url: "/n/holystore01/LABS/jialiu_lab/Users/yichunhe/STAgent/input_data/colitis/adata_test.h5ad", 
# summary_batch: "/n/holystore01/LABS/jialiu_lab/Users/yichunhe/STAgent/memory_data/2024-09-27_09-10-29/summary_batch.json", 
# dataset_description: "We harvested distal colon prior to treatment (day 0), early in disease (day 3), at peak inflammation (day 9), and after a DSS-free recovery period (day 21).", 
# rule_tissue: "Dextran-sodium-sulfate (DSS)-induced mouse colitis model", 
# summary_celltype: "/n/holystore01/LABS/jialiu_lab/Users/yichunhe/STAgent/memory_data/2024-09-27_09-10-29/allsample_celltype.json", 
# summary_tissueregion: "/n/holystore01/LABS/jialiu_lab/Users/yichunhe/STAgent/memory_data/2024-09-27_09-10-29/allsample_tissueregion.json", 
# path_cci: "/n/holystore01/LABS/jialiu_lab/Users/yichunhe/STAgent/memory_data/2024-09-27_09-10-29/cci_result.csv"
# Expected output: A summary file path indicating successful inference of confidence scores for ligand-receptor pairs.   
# """

#     response = agent(query_input)

#     p = 0

    return all_tools

    """
    # from langchain import hub
    # from langchain_community.llms import OpenAI
    # from langchain.agents import AgentExecutor, create_react_agent
    # prompt = hub.pull("hwchase17/react")
    # tools = [all_tools[2]]  # Include CSVAgent in the tools sequence
    # agent = create_react_agent(llm, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=8,handle_parsing_errors=True )
    # agent_executor.invoke({"input": "What are gene symbols of lamp5 GABAergic cortical interneuron in human?"})
    """

    """
    ### works for tool ReadCZIDataTOOL. Second try don't work.
    # llm_with_tools=llm.bind_tools([all_tools[1]], tool_choice=all_tools[1].name)
    # parser = JsonOutputKeyToolsParser(key_name=all_tools[1].name, first_tool_only=True)
    # system = "You can an action agent helping with the task. Execute the tool to get the output. Judge if the execution is successful. If yes, stop. Do not change the output or iterate."
    # prompttt = ChatPromptTemplate.from_messages([("system", system), ("human", "dataset_id_list:{dataset_id_list} organism_key:{organism_key}")])
    # chain = prompttt | llm_with_tools | parser | all_tools[1]
    # qqq={'dataset_id_list':'c05e6940-729c-47bd-a2a6-6ce3730c4919', 'organism_key':'Homo sapiens'}
    # answer =chain.invoke(qqq)           


    # prompt = hub.pull("hwchase17/openai-tools-agent")
    # agent = create_tool_calling_agent(llm, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools)
    # args = {'dataset_id_list':'c05e6940-729c-47bd-a2a6-6ce3730c4919','organism_key':'Homo sapiens'}
    # result = agent_executor.invoke({"input":'dataset_id_list is c05e6940-729c-47bd-a2a6-6ce3730c4919 and organism_key is Homo sapiens'})
   """
