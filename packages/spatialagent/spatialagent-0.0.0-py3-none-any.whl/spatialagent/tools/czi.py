import os, time, shutil, logging, requests, cellxgene_census, pandas as pd
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores.chroma import Chroma
from langchain.tools import BaseTool
from langchain.schema import Document
from openai import OpenAIError


CELL_GUIDE_BASE_URI = "https://cellguide.cellxgene.cziscience.com"
LATEST_SNAPSHOT = requests.get(f"{CELL_GUIDE_BASE_URI}/latest_snapshot_identifier").text


### How czi_census_datasets.csv is generated
# test = pd.read_csv('../data/czi_census_datasets.csv')
# import cellxgene_census
# census = cellxgene_census.open_soma(census_version="latest")

# from tqdm import tqdm
# for datasetid in tqdm(test['dataset_id']):

#     organism_key = "Homo sapiens"
#     adata = cellxgene_census.get_anndata(
#         census,
#         organism=organism_key,
#         obs_value_filter=f"dataset_id in {[test['dataset_id'][0]]}",
#     )
#     if adata.shape[0]==0:
#         organism_key = "Mus musculus"

#         adata = cellxgene_census.get_anndata(
#             census,
#             organism=organism_key,
#             obs_value_filter=f"dataset_id in {[datasetid]}",
#         )

#     test.loc[test['dataset_id']==datasetid,'cell_type']=';'.join(list(adata.obs['cell_type'].unique()))
#     test.loc[test['dataset_id']==datasetid,'development_stage']=';'.join(list(adata.obs['development_stage'].unique()))
#     test.loc[test['dataset_id']==datasetid,'tissue']=';'.join(list(adata.obs['tissue'].unique()))
#     test.loc[test['dataset_id']==datasetid,'disease']=';'.join(list(adata.obs['disease'].unique()))
#     test.loc[test['dataset_id']==datasetid,'sex']=';'.join(list(adata.obs['sex'].unique()))
#     test.loc[test['dataset_id']==datasetid,'tissue_general']=';'.join(list(adata.obs['tissue_general'].unique()))
#     test.loc[test['dataset_id']==datasetid,'self_reported_ethnicity']=';'.join(list(adata.obs['self_reported_ethnicity'].unique()))


"""
Function from Isaac Virshup
https://gist.github.com/ivirshup/e7cc5b717bad6fd32460525765e10c9b
"""


def _get_cellguide_file(relpth: str, snapshot: str = LATEST_SNAPSHOT) -> requests.Response:
    req = requests.get(f"{CELL_GUIDE_BASE_URI}/{snapshot}/{relpth}")
    if req.text == "":
        raise ValueError(f"No record found for {snapshot}/{relpth}")
    return req


def get_computational_marker_genes(ontology_id: str, *, snapshot=LATEST_SNAPSHOT) -> pd.DataFrame:
    resp = _get_cellguide_file(f"computational_marker_genes/{ontology_id}.json", snapshot=snapshot)
    return pd.DataFrame.from_records(resp.json(), exclude=["groupby_dims"])


def get_canonical_marker_genes(ontology_id: str, *, snapshot=LATEST_SNAPSHOT) -> pd.DataFrame:
    resp = _get_cellguide_file(f"canonical_marker_genes/{ontology_id}.json", snapshot=snapshot)
    return pd.DataFrame.from_records(resp.json())


def get_description(ontology_id: str, validated=True) -> dict | str:
    if validated:
        subdir = "validated_descriptions"
    else:
        subdir = "gpt_descriptions"

    req = requests.get(f"{CELL_GUIDE_BASE_URI}/{subdir}/{ontology_id}.json")
    if req.text == "":
        raise ValueError(f"No record found for {subdir}/{ontology_id}")
    return req.json()


def save_to_chroma(chunks: list[Document], CHROMA_PATH, embeddings):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    # db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    # db.persist()
    # print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

    # Create a new DB from the documents with retry mechanism
    retry_attempts = 50
    for attempt in range(retry_attempts):
        try:
            db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
            db.persist()
            print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
            break
        except OpenAIError as e:
            if "429" in str(e):
                wait_time = 2**attempt  # Exponential backoff
                logging.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    if db is None:
        raise Exception("Failed to save to Chroma after several attempts due to rate limit errors.")


def fun_czi_retriever_tool(embeddings, czi_file_path, CHROMA_PATH):
    if not os.path.exists(CHROMA_PATH):
        logging.info("Creating new Chroma database from CZI data.")
        loader = CSVLoader(file_path=czi_file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)
        logging.info(chunks[0])
        # vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        save_to_chroma(chunks, CHROMA_PATH, embeddings)

    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()

    description = (
        # "CZI datasets are all processed with cell type annotations and can be used for reference."
        "Use this tool to find one of the best matching single-cell dataset in CZI that matches the query."
        "Input is one str of a comprehensive description including target tissue (brain, liver, eye, etc.), condition (embryo, adult, disease, healthy, etc.), or organism (mouse or human)."
        "Output must be information of reference scRNA-seq data:'The best matching reference Dataset id: ... Dataset title: ... Collection Name: xx'. in JSON format."
        # "Output must be JSON format like this:'The best matching reference Dataset id: ... Dataset title: ... Collection Name: xx'."
        "You must execute the tool. You can't skip the tool running."
    )

    tool = create_retriever_tool(retriever, "RetrieveCZIDataID", description)

    return tool


def fun_czi_retriever3_tool(embeddings, czi_file_path, CHROMA_PATH):
    if not os.path.exists(CHROMA_PATH):
        logging.info("Creating new Chroma database from CZI data.")
        loader = CSVLoader(file_path=czi_file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)
        logging.info(chunks[0])
        # vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        save_to_chroma(chunks, CHROMA_PATH, embeddings)

    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()

    description = (
        # "CZI datasets are all processed with cell type annotations and can be used for reference."
        "Use this tool to find three of the best matching single-cell dataset in CZI that matches the query."
        "Input is one str of a description including target tissue (brain, liver, eye, etc.), condition (embryo, adult, disease, healthy, etc.), and organism (mouse or human)."
        "Output must be JSON format like this:'The three best matching reference Dataset id: ... Dataset title: ... Collection Name: xx'."
        "You must execute the tool. You can't skip the tool running."
    )

    tool = create_retriever_tool(retriever, "RetrieveCZIDataID", description)

    return tool


class ReadCZIDataTOOL(BaseTool):
    name = "ReadCZIData"
    description = (
        "You must use this tool to read the reference single cell dataset in CZI database given the input query."
        'Input need to be the dataset id, organism key, and the number of target genes that user wanted. "dataset_id_list" must be real dataset id and not be something like "Dataset ID from Step 1.1 output". The organism must be one of "Homo sapiens or "Mus musculus. iter_round as current iteration round.'
        'Use this tool with arguments like "{{"dataset_id_list":str, "organism_key":str,"num_gene":int,"iter_round": int}}".'
        'Output must be in JSON format, as a str like "Successfully saved ... and the path to where results are saved."'
    )

    desired_path: str = None

    def __init__(self, desired_path):
        super().__init__()
        self.desired_path = desired_path

    def _run(self, dataset_id_list: str, organism_key: str, num_gene: str, iter_round: int):
        # print(args)
        # print(kwargs)
        # dataset_id_list = dict_input1[0]
        # organism_key = dict_input2[1]
        # print(dataset_id_list)

        file_folder = self.desired_path
        save_path = file_folder + f"read_czi_reference_adata_{iter_round}.h5ad"
        save_csv = file_folder + f"read_czi_reference_celltype_{iter_round}.csv"

        if not os.path.exists(save_path):
            census = cellxgene_census.open_soma(census_version="latest")
            census_info = census["census_info"]["summary_cell_counts"].read().concat().to_pandas()
            adata = cellxgene_census.get_anndata(
                census,
                organism=organism_key,
                obs_value_filter=f"dataset_id in {[dataset_id_list]}",
            )
            census.close()
            adata.write_h5ad(save_path)

            dic_cell_gene = {
                "cell_type": [],
                "description": [],
                "marker_genes": [],
                "cano_marker_genes": [],
            }

            # top_marker_genes = 10
            # if num_gene / len(list(adata.obs["cell_type"].unique())) > 10:
            #     top_marker_genes = (
            #         int(num_gene / len(list(adata.obs["cell_type"].unique()))) + 5
            #     )
            # logging.info(f"\nNumber of top marker genes used: {top_marker_genes}.\n")

            for i in list(adata.obs["cell_type"].unique()):
                if i == "unknown":
                    continue
                ontology_term_id = census_info.loc[
                    (census_info["label"] == i) & (census_info["organism"] == organism_key),
                    "ontology_term_id",
                ]
                ontology_term_key = list(ontology_term_id)[0].replace(":", "_")
                try:
                    res_compu = get_computational_marker_genes(ontology_term_key)
                    if organism_key == "Homo sapiens":
                        res_compu = res_compu.loc[res_compu["gene_ontology_term_id"].str.contains("ENSG"), :]
                    else:
                        res_compu = res_compu.loc[res_compu["gene_ontology_term_id"].str.contains("ENSMUSG"), :]
                except:
                    res_compu = {}
                    res_compu["symbol"] = []
                try:
                    id_description = get_description(ontology_term_key)
                    id_description = id_description["description"]
                except ValueError:
                    id_description = get_description(ontology_term_key, validated=False)
                try:
                    res_cano = get_canonical_marker_genes(ontology_term_key)
                    marker_caon = res_cano["symbol"].tolist()
                except ValueError:
                    marker_caon = []

                dic_cell_gene["cell_type"].append(i)
                dic_cell_gene["description"].append(id_description)
                dic_cell_gene["marker_genes"].append(res_compu["symbol"].tolist())
                dic_cell_gene["cano_marker_genes"].append(marker_caon)

            dic_cell_gene = pd.DataFrame(dic_cell_gene)
            dic_cell_gene.to_csv(save_csv)

        else:
            print("Reference data already exist!")
        output = f"Successfully read reference data and extract unique cell types and corresponding marker genes in the reference. The path to file folder where reference data is saved as anndata and unique cell types and corresponding marker genes are saved as csv is {file_folder}."
        return output

    def _arun(self, input_url):
        raise NotImplementedError("This tool does not support async")


class ReadCZIData3TOOL(BaseTool):
    name = "ReadCZIData"
    description = (
        "You must use this tool to read the reference single cell dataset in CZI database given the input query."
        # 'Input need to be the dataset id, organism key, and the number of target genes that user wanted. "dataset_id_list" must be real dataset id and not be something like "Dataset ID from Step 1.1 output". The organism must be one of "Homo sapiens or "Mus musculus. iter_round as current iteration round.'
        'Input must be the dataset id 1, 2, and 3, organism key, and the number of target genes that user wanted. "dataset_id_list" must be real dataset id and not be something like "Dataset ID from Step 1.1 output". The organism must be one of "Homo sapiens or "Mus musculus. iter_round as current iteration round.'
        'Use this tool with arguments like "{{"dataset_id_1":str, "dataset_id_2":str, "dataset_id_3":str, "organism_key":str,"num_gene":int,"iter_round": int}}".'
        'Output must be in JSON format, as a str like "Successfully saved ... and the path to where results are saved."'
    )
    desired_path: str = None

    def __init__(self, desired_path):
        super().__init__()
        self.desired_path = desired_path

    def _run(self, dataset_id_1: str, dataset_id_2: str, dataset_id_3: str, organism_key: str, num_gene: str, iter_round: int):

        file_folder = self.desired_path
        dataset_id_list = [dataset_id_1, dataset_id_2, dataset_id_3]
        save_path = file_folder + f"read_czi_reference_adata_{iter_round}.h5ad"
        save_csv = file_folder + f"read_czi_reference_celltype_{iter_round}.csv"

        if not os.path.exists(save_path):
            census = cellxgene_census.open_soma(census_version="latest")
            census_info = census["census_info"]["summary_cell_counts"].read().concat().to_pandas()
            adata = cellxgene_census.get_anndata(
                census,
                organism=organism_key,
                obs_value_filter=f"dataset_id in {dataset_id_list}",
            )
            census.close()
            adata.write_h5ad(save_path)

            dic_cell_gene = {
                "cell_type": [],
                "description": [],
                "marker_genes": [],
                "cano_marker_genes": [],
            }

            # top_marker_genes = 10
            # if num_gene / len(list(adata.obs["cell_type"].unique())) > 10:
            #     top_marker_genes = (int(num_gene / len(list(adata.obs["cell_type"].unique()))) + 5)
            # logging.info(f"\nNumber of top marker genes used: {top_marker_genes}.\n")

            for i in list(adata.obs["cell_type"].unique()):
                if i == "unknown":
                    continue
                ontology_term_id = census_info.loc[
                    (census_info["label"] == i) & (census_info["organism"] == organism_key),
                    "ontology_term_id",
                ]
                ontology_term_key = list(ontology_term_id)[0].replace(":", "_")
                try:
                    res_compu = get_computational_marker_genes(ontology_term_key)
                    if organism_key == "Homo sapiens":
                        res_compu = res_compu.loc[res_compu["gene_ontology_term_id"].str.contains("ENSG"), :]
                    else:
                        res_compu = res_compu.loc[res_compu["gene_ontology_term_id"].str.contains("ENSMUSG"), :]
                except:
                    res_compu = {}
                    res_compu["symbol"] = []
                try:
                    id_description = get_description(ontology_term_key)
                    id_description = id_description["description"]
                except ValueError:
                    id_description = get_description(ontology_term_key, validated=False)
                try:
                    res_cano = get_canonical_marker_genes(ontology_term_key)
                    marker_caon = res_cano["symbol"].tolist()
                except ValueError:
                    marker_caon = []

                dic_cell_gene["cell_type"].append(i)
                dic_cell_gene["description"].append(id_description)
                dic_cell_gene["marker_genes"].append(res_compu["symbol"].tolist())
                dic_cell_gene["cano_marker_genes"].append(marker_caon)

            dic_cell_gene = pd.DataFrame(dic_cell_gene)
            dic_cell_gene.to_csv(save_csv)

        else:
            print("Reference data already exist!")
        output = f"Successfully read reference data and extract unique cell types and corresponding marker genes in the reference. The path to file folder where reference data is saved as anndata and unique cell types and corresponding marker genes are saved as csv is {file_folder}."
        return output

    def _arun(self, **kwargs):
        raise NotImplementedError("This tool does not support async")
