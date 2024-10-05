import argparse
from enum import Enum
from typing import Dict, Any


class TaskType(Enum):
    TASK1 = "task1"
    TASK2 = "task2"
    TASK3 = "task3"
    TASK_TOOL_TESTING = "tool_test"


class ModelType(Enum):
    GPT4 = "gpt-4"
    GPT4O = "gpt-4o"
    GPT35TURBO = "gpt-35-turbo"
    GPT4VISION = "gpt-4-vision-preview"
    TEXTEMBEDDING3LARGE = "text-embedding-3-large"
    TEXTEMBEDDINGADA002 = "text-embedding-ada-002"
    TEXTEMBEDDING3SMALL = "text-embedding-3-small"
    GENIE = "genie"
    CLAUDE3 = "claude-3-opus"
    LLAMA3_405B = "llama3-405b"
    LLAMA3_8B = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    MISTRAL_7B_INSTRUCTv03 = "mistralai/Mistral-7B-Instruct-v0.3"
    DATABRICKS_MPT_7B = "mosaicml/mpt-7b"
    DATABRICKS_MPT_7B_INSTRUCT = "mosaicml/mpt-7b-instruct"
    # DATABRICKS_MPT_30B = "mosaicml/mpt-30b"
    # DATABRICKS_MPT_30B_INSTRUCT = "mosaicml/mpt-30b-instruct"


class ObservationRuleType(Enum):
    TASK1_2DB = "task1_2db_observation_rule"
    TASK1_3DB = "task1_3db_observation_rule"
    TASK2 = "task2_observation_rule"
    TASK3 = "task3_observation_rule"
    TASK_TOOL_TESTING = "task_testing_tool_observation_rule"


OBSERVATION_RULES = {
    ObservationRuleType.TASK1_2DB.value: """
You need to finish the design of the target gene panel step by step.
The task rule includes the target cell type, tissue, organ, species, or condition information.
Typical steps include:
Iterate step 1.1 to 1.4 three rounds to get multiple rounds of output.
In each round of iteration, you can only execute each step one time with the corresponding iteration round number.
Step 1.1 first, you must search one public single-cell database to find one of the best matching datasets as reference. 
Step 1.2 next, you must find the cell types to be covered and corresponding annotated marker genes based on the reference dataset.
Step 1.3 next, for each cell type, you must find additional marker genes from another database, like PangDB.
Step 1.4 next, you must estimate the importance score of each genes according to previous collected information and rules.
After three rounds of iterations above, you combine the results of multiple rounds to get the final target gene panel.
These are the minimum steps you need to follow to finish the task. Do not skip any step.""",
    ObservationRuleType.TASK1_3DB.value: """
You need to finish the design of the target gene panel step by step.
The task rule includes the target cell type, tissue, organ, species, or condition information.
Typical steps include:
Iterate step 1.1 to 1.5 three rounds to get multiple rounds of output.

In each round of iteration, you can only execute each step one time with the corresponding iteration round number.
Step 1.1 first, you must search one public single-cell dataset to find one of the best matching datasets in CZI databse as reference. Find the datasetid to locate the reference dataset.
Step 1.2 next, you must find the cell types to be covered and corresponding annotated marker genes based on the reference dataset.
Step 1.3 next, for each cell type, you must find additional marker genes from the second database, like PangDB.
Step 1.4 next, for each cell type, you must find additional marker genes from the third database, like CellMarker2.
Step 1.5 next, you must estimate the importance score of each genes according to previous collected information and rules.
After three rounds of iterations above, you combine the results of multiple rounds to get the final target gene panel.
These are the minimum steps you need to follow to finish the task. Do not skip any step.
""",
    ObservationRuleType.TASK2.value: """
You need to finish the annotation of cell types and tissue niches in a spatial transcriptomics dataset step by step.
The annotations are twofold: cell types and tissue niches.

Typical steps include:
Step 1 first, you must preprocess the raw data.
Step 2 next, you must decide main-level cell types.
To do main-level cell type annotation, follow the steps below:
Step 2.1 first, you find one best matching dataset in CZI database as reference dataset.
Step 2.2 next, you get related information from CZI database.
Step 2.3 next, you get transferred cell types from the CZI reference labels. 
Step 2.4 next, you cluster cells on the preprocessed data and use marker genes in each cluster and transferred cell type to annotate main-level cell types.

Step 3 next, you must decide main-level tissue niches.
To do main-level tissue niche annotation, follow the steps below:
Step 3.1 first, you cluster cells to find spatial neighborhood expression coherent clusters and save clusters.
Step 3.2 next, you annotate each cluster a tissue niche name based on multimodal information including anatomical imaging, main-level cell types, marker genes, etc..

Step 4 next, you must decide sub-level cell types.
To do sub-level cell type annotation, follow the steps below:
Step 4.1 first, you cluster main-level cell types and annotate sub-level cell types.

Step 5 next, you must decide sub-level tissue niches.
To do sub-level tissue niche annotation, follow the steps below:
Step 5.1 first, you find sub-level tissue niche clusters based on both expression and spatial distributions.
Step 5.2 next, you annotate each sub-level cluster a tissue niche name based on multimodal information including anatomical imaging, sub-level cell types, marker genes, etc..

Step 6 finally, you must summarize all annotations.

These are the minimum steps you need to follow to finish the task. Do not skip any step.
""",
    ObservationRuleType.TASK3.value: """
You need to finish the inference of cell cell communications or interactions in a spatial transcriptomics dataset step by step.

Typical steps include:
Step 1 first, you must summarize an understanding of the dataset.
Step 1.1 first, summarize batch information.
Step 1.2 first, summarize cell types information.
Step 1.3 next, summarize tissue niches information.

Step 2 next, you must use tools to infer potential cell-cell communications. 

Step 3 next, you must give confidence score for each ligand receptor pair.

Step 4 finally, you must provide report of what you find.

These are the minimum steps you need to follow to finish the task. Do not skip any step.
""",
    ObservationRuleType.TASK_TOOL_TESTING.value: """
You are an AI assistant tasked with testing specific tools used in spatial transcriptomics analysis. Your goal is to thoroughly test the functionality of each tool, ensuring it performs as expected under various conditions. Follow these general guidelines for all tool testing:

1. Start by understanding the tool's purpose and expected inputs/outputs.
2. Test the tool with valid inputs and verify the outputs are correct.
3. Document any unexpected behavior or potential improvements.

For each test case, document the input provided, the expected output, and the actual output. Note any discrepancies or unexpected behaviors. After testing each tool, provide a summary of its performance, including any limitations or potential improvements identified during testing.
""",
}


def create_base_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Spatial Transcriptomics Task Parser")
    parser.add_argument("--task_id", type=str, required=True, choices=[t.value for t in TaskType])
    parser.add_argument("--model", type=str, choices=[m.value for m in ModelType], default=ModelType.GPT4.value)
    parser.add_argument("--model_name", type=str)  # Required for locally served LLM
    parser.add_argument("--emb_model", type=str, default="text-embedding-3-small")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--name", type=str, default="Spatial transcriptomics agent")
    parser.add_argument("--all_steps", type=int, default=50)
    parser.add_argument("--model_cost", type=str, default="gpt-4")
    return parser


def parse_task1_args(parser: argparse.ArgumentParser) -> Dict[str, Any]:
    parser.add_argument("--game_name", type=str, default="Design target gene panel")
    parser.add_argument("--rule_tissue", type=str, default="Dorsolateral prefrontal cortex")
    parser.add_argument("--rule_num", type=int, default=50)
    parser.add_argument("--observation_rule_key", type=str, default=ObservationRuleType.TASK1_2DB.value)

    args = parser.parse_args()
    args.rule = f"I want to design a spatial transcriptomics experiment of {args.rule_tissue}. Choose {args.rule_num} target genes for me."
    args.observation_rule = OBSERVATION_RULES[args.observation_rule_key]

    return args


def parse_task2_args(parser: argparse.ArgumentParser) -> Dict[str, Any]:
    parser.add_argument("--game_name", type=str, default="Annotate cell types and tissue niches")
    parser.add_argument("--rule_tissue", type=str, default="Developing human heart")
    parser.add_argument("--rule_rawdata_path", type=str, default="/home/wangh256/STAgent/input_data/developing_human_heart/merfish_raw_test.h5ad")
    parser.add_argument("--batch_key", type=str, default="batch")
    parser.add_argument("--rule_anatomica_tissue_path", type=str, default="/home/wangh256/STAgent/input_data/developing_human_heart/AnaImage.png")
    parser.add_argument("--observation_rule_key", type=str, default=ObservationRuleType.TASK2.value)

    args = parser.parse_args()
    args.rule = (
        f"I want to annotate cells of {args.rule_tissue}. "
        f"Path of raw data is {args.rule_rawdata_path} where column {args.batch_key} shows different batches of sample. "
        f"Path of anatomical tissue image is {args.rule_anatomica_tissue_path}."
    )
    args.observation_rule = OBSERVATION_RULES[args.observation_rule_key]

    return args


def parse_task3_args(parser: argparse.ArgumentParser) -> Dict[str, Any]:
    parser.add_argument("--game_name", type=str, default="Infer cell-cell communications or interactions")
    parser.add_argument("--rule_tissue", type=str, default="Mouse colitis")
    parser.add_argument("--cell_type_key", type=str, default="xxx")
    parser.add_argument("--tissue_niche_key", type=str, default="xxx")
    parser.add_argument("--batch_key", type=str, default="xxx")
    parser.add_argument("--rule_labeleddata_path", type=str, default="xxx")
    parser.add_argument("--dataset_description", type=str, default="xxx")
    # parser.add_argument("--label_description", type=str, default="xxx")
    parser.add_argument("--observation_rule_key", type=str, default=ObservationRuleType.TASK3.value)

    args = parser.parse_args()
    args.rule = (
        f"I want to infer cell-cell communications or interactions in a spatial transcriptomics experiment of tissue type {args.rule_tissue}."
        f"Path of labeled data is {args.rule_labeleddata_path} where column {args.batch_key} is different batches of samples,"
        f"column {args.cell_type_key} is cell types, and column {args.tissue_niche_key} is tissue niches."
        f"The sample description is in {args.dataset_description}"
        # f"The cell type label description is in {args.label_description}"
    )
    args.observation_rule = OBSERVATION_RULES[args.observation_rule_key]

    return args


def parse_tasktooltest_args(parser: argparse.ArgumentParser) -> Dict[str, Any]:
    parser.add_argument("--game_name", type=str, default="Test spatial transcriptomics tools")
    parser.add_argument("--rule_tissue", type=str, default="Dorsolateral prefrontal cortex")
    parser.add_argument("--rule_num", type=int, default=50)
    parser.add_argument("--tool_to_test", type=str, default="GeneVotingTool")
    parser.add_argument("--observation_rule_key", type=str, default=ObservationRuleType.TASK_TOOL_TESTING.value)

    args = parser.parse_args()
    args.rule = f"I want to test a tool a spatial transcriptomics experiment of {args.rule_tissue}."
    args.observation_rule = OBSERVATION_RULES[args.observation_rule_key]

    return args


def parse_args() -> Dict[str, Any]:
    initial_parser = argparse.ArgumentParser(description="Initial parser to get task_id")
    initial_parser.add_argument("--task_id", type=str, required=True, choices=[t.value for t in TaskType], help="ID of the task to run")
    initial_args, unknown = initial_parser.parse_known_args()

    base_parser = create_base_parser()
    if initial_args.task_id == TaskType.TASK1.value:
        return parse_task1_args(base_parser)
    elif initial_args.task_id == TaskType.TASK2.value:
        return parse_task2_args(base_parser)
    elif initial_args.task_id == TaskType.TASK3.value:
        return parse_task3_args(base_parser)
    elif initial_args.task_id == TaskType.TASK_TOOL_TESTING.value:
        return parse_tasktooltest_args(base_parser)
    else:
        raise ValueError(f"Unknown task ID: {initial_args.task_id}")


# === DEPRECATED ===
# task2_observation_rule = (
#     "You need to finish the annotation of cell types and tissue niches in a spatial transcriptomics dataset step by step.\n"
#     "The annotations are twofold: cell types and tissue niches.\n"
#     "Typical steps include:\n"
#     # "Iterate step 1.1 to 1.5 three rounds to get multiple rounds of output.\n"
#     # "In each round of iteration, you can only execute each step one time with the corresponding iteration round number.\n"
#     # "Step 1.1 first, you must search one public single-cell dataset to find one of the best matching datasets in CZI databse as reference. Find the datasetid to locate the reference dataset.\n"
#     # "Step 1.2 next, you must find the cell types to be covered and corresponding annotated marker genes based on the reference dataset.\n"
#     "Step 1 first, you must preprocess the raw data.\n"
#     "Step 2 next, you must decide main-level cell types.\n"
#     "To do main-level cell type annotation, follow the steps below:\n"
#     "Step 2.1 first, you find one best matching dataset in CZI database as reference dataset.\n"
#     "Step 2.2 next, you get related information from CZI database.\n"
#     "Step 2.3 next, you get transferred cell types from the CZI reference labels. \n"
#     "Step 2.4 next, you cluster cells on the preprocessed data and use marker genes in each cluster and transferred cell type to annotate main-level cell types.\n"
#     # "Step 2.4 next, you analyze distribution of main-level cell types across the tissue to name the tissue.\n"
#     # "Step 3 next, you identify and annotate main-level tissue niches.\n"
#     # "Step 4 next, you cluster and annotate sublevel cell types.\n"
#     # "Step 5 next, you identify and annotate sublevel tissue niches.\n"
#     # "After three rounds of iterations above, you combine the results of multiple rounds to get the final target gene panel.\n"
#     "These are the minimum steps you need to follow to finish the task. Do not skip any step.\n"
# )


if __name__ == "__main__":
    pass
