import sys
import anndata as ad
import scanpy as sc
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
import sys
from langchain.tools import BaseTool
import pandas as pd
import os
import logging
from langchain.base_language import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from langchain.chains import LLMChain
import time
import pickle

from itertools import combinations
from collections import Counter

from collections import defaultdict
from itertools import combinations
from collections import Counter
from pathlib import Path


def is_n_nearest(first_id, second_id, coordinates, num_nearest=2):
    # Calculate distances from first_id to all other ids
    first_coords = coordinates[first_id]
    distances = {id_: np.linalg.norm(first_coords - coords) for id_, coords in coordinates.items() if id_ != first_id}

    # Sort ids by distance
    sorted_ids = sorted(distances, key=distances.get)

    # Check if second_id is within the num_nearest nearest ids
    return second_id in sorted_ids[:num_nearest]


def find_connected_components(edges, values):
    graph = defaultdict(list)

    for (u, v), val in zip(edges, values):
        if val:  # Only consider edges with True value
            graph[u].append(v)
            graph[v].append(u)

    visited = set()
    components = []

    def dfs(node, component):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.append(current)
                stack.extend(graph[current])

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components


def update_dict_with_components(data_dict, components):
    for component in components:
        # Find the value to assign - using the value of the first node in the component
        common_value = data_dict[component[0]]
        for node in component:
            data_dict[node] = common_value


def sub_celltype_anno(unique_celltype_i, data_info, llm, dict_subtype, czi_all_celltype, spec_threshold=0.8):
    # content = (
    #     f"You must think step by step to provide fine-grained annotation of sub-level cell types in this format: [main-level cell types]-[sub-level cell types]-[specificity, e.g. spatial distribution, unique cell state or function]-[marker gene].\n"
    #     + "{dict_subtype_i}\n"
    #     + f"The tissue region distribution is the percentage of each subtype in spatial tissue niches. The enriched genes are the top 5 genes that are most enriched in this subtype compared to other subtypes in {unique_celltype_i}.\n"
    #     + f"First, is there any identified genes that are unique gene markers of {unique_celltype_i} in {data_info}? If yes, please add provide the gene name and its specificity in this subtype. If not, do not add gene in the name.\n"
    #     + f"Second, check distribution in each main-level tissue niche and find if there is one single tissue region with more than {spec_threshold} of this subtype. If yes, please provide the region name. Do not change the region name. If no, continue.\n"
    #     + 'Note that slightly different regions names means different regions. For example, "Left Ventricle-0" and "Left Ventricle-1" are different regions.\n'
    #     + f"Third, if in second step, no single tissue region has over {spec_threshold} percentage of the subtype, check the first two regions with highest percentage and if they have common in names, if yes, you can combine them as one general region."
    #     + f'For example, combine "Left Ventricle-5" and "Left Ventricle or Right Ventricle-10" as "Left Ventricle"; combine "Left Ventricle" and "Right Ventricle" as "Ventricle". If the combined general region together with more than {spec_threshold} of this subtype, please provide the combined general region name and its specificity in this subtype.\n'
    #     + f"If in second or third step, no single tissue region or general region has over {spec_threshold} percentage, do not add region name in the annotation, keep name it as {unique_celltype_i}."
    #     + f'If there is region or gene in the above step, you can add "xx gene-specific {unique_celltype_i}" or "xx region-specific {unique_celltype_i}" to this subtype based on above result.'
    #     + f"The sub-level cell type names should come from cell ontology: {czi_all_celltype}.\n"

    #     + f'Finally, you must output "Subtype x:...;Reason:...". Do not add numbers, space, """, "." or any other characters after the Name.'
    # )
    content = (
        f"You must think step by step to provide fine-grained annotation of sub-level cell types."
        'You must output "Subtype annotation:...;Reason:...". Do not add numbers, space, """, "." or any other characters after the annotation.'
        "The Subtype annotation must be in this format: [main-level cell types]-[specificity, e.g. spatial distribution, unique cell state or function]-[marker gene].\n"
        f"1.The main-level cell type is: {unique_celltype_i}.\n"
        f"Decide annotation for the sub-level cluster based on the following info:"
        + "{dict_subtype_i}\n"
        + f"The tissue region distribution is the percentage of each subtype in spatial tissue niches. The enriched genes are the top 5 genes that are most enriched in this subtype compared to other subtypes in {unique_celltype_i}.\n"
        + f"The sub-level cell type names should come from cell ontology: {czi_all_celltype}.\n"
        + f"2.Check distribution in each main-level tissue niche and find if there is one single tissue region with more than {spec_threshold} of this subtype. If yes, please provide the region name. Do not change the region name. If no, continue.\n"
        + 'Note that slightly different regions names means different regions. For example, "Left Ventricle-0" and "Left Ventricle-1" are different regions.\n'
        + f"If no single tissue region has over {spec_threshold} percentage of the subtype, check the first two regions with highest percentage and if they have common in names, if yes, you can combine them as one general region."
        + f'For example, combine "Left Ventricle-5" and "Left Ventricle or Right Ventricle-10" as "Left Ventricle"; combine "Left Ventricle" and "Right Ventricle" as "Ventricle". If the combined general region together with more than {spec_threshold} of this subtype, please provide the combined general region name and its specificity in this subtype.\n'
        + f"If no single tissue region or general region has over {spec_threshold} percentage, do not add region name in the annotation."
        + f"3.Is there any identified genes that are well-known gene markers for this subtype of {unique_celltype_i} in {data_info}? If yes, please add the gene as marker gene. If not, do not add gene in the annotation.\n"
        # + f"4.Based on above annotations, find a best matching sub-level cell type for this subtype of {unique_celltype_i} from cell ontology. The sub-level cell type one type must be in {data_info}, not just relavant. Don't propose a subtype of other tissue types or organisms.\n"
    )
    llm_prompt = PromptTemplate(
        input_variables=["human_prompt"],
        template=content,
    )

    chain = LLMChain(llm=llm, prompt=llm_prompt)

    content2 = (
        f"You must think step by step to decide a best matching sub-level cell type of the subcluster in {unique_celltype_i}."
        'You must output "Subtype name:...;Reason:...". Do not add numbers, space, """, "." or any other characters after the Name.'
        "The Subtype x annotation in this format [main-level cell types]-[specificity, e.g. spatial distribution, unique cell state or function]-[marker gene] is {past_response}\n."
        + f"The sub-level cell type names should come from cell ontology: {czi_all_celltype}.\n"
        + f"The sub-level cell type must be in specific tissue type and organism as {data_info}, not just relavant. Don't propose a subtype of other tissue types or organisms.\n"
    )
    llm_prompt2 = PromptTemplate(
        input_variables=["human_prompt"],
        template=content2,
    )
    chain2 = LLMChain(llm=llm, prompt=llm_prompt2)

    res = []
    reason = []
    for i in range(len(dict_subtype)):
        while True:
            prompt = dict_subtype[i]
            try:
                response = chain.run(prompt)
            except:
                time.sleep(6)
            time.sleep(1)
            try:
                subtype_annotation = response.split(f"Subtype annotation:")[1].split(";Reason")[0]
                break
            except:
                prompt += 'You must output "Subtype annotation:...;Reason:...".'

        while True:
            try:
                response_final = chain2.run(response)
            except:
                time.sleep(6)
            time.sleep(1)
            try:
                subtype_name = response_final.split("Subtype name:")[1].split(";Reason")[0]
                break
            except:
                response += 'You must output "Subtype annotation:...;Reason:...".'
        subtype_all = subtype_name + "-" + subtype_annotation
        subtype_all = subtype_all.strip()

        parts = subtype_all.split("-")
        formatted_parts = [f"[{part.strip()}]" for part in parts]
        formatted_str = "-".join(formatted_parts)
        logging.info(f"\n\n----- Subcluster {i} in " + unique_celltype_i + "-----")
        logging.info("\n\n" + formatted_str + "\n" + response.split(f"Subtype annotation:")[1].split(";Reason:")[1])
        res.append(formatted_str)
        reason.append(response.split(f"Subtype annotation:")[1].split(";Reason:")[1])
    return res, reason


def scanpy_gene_marker(ad_sp):
    input_genemarker = {}
    temp = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["names"]).head(3)
    temp_score = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["scores"]).head(3)
    for i in range(temp.shape[1]):
        curr_col = temp.iloc[:, i].to_list()
        curr_col_score = temp_score.iloc[:, i].to_list()
        list_true = [x > 0 for x in curr_col_score]
        curr_col = list(np.array(curr_col)[list_true])
        input_genemarker[i] = curr_col
    return input_genemarker


def generate_dict_info(ad_sp, input_genemarker, celltype_region_composition):
    dict_subtype = []
    for focus_niche in tqdm(range(len(ad_sp.obs["leiden"].unique()))):
        focus_niche = str(focus_niche)
        celltype_gene_infor = ""
        celltype_gene_infor += f"The gene markers in subtype {focus_niche} are: {input_genemarker[int(focus_niche)]}.\n"
        celltype_gene_infor += f"The tissue region distribution of the subtype {focus_niche} is:"
        for j in celltype_region_composition.columns:
            if celltype_region_composition.loc[focus_niche, j] > 0:
                celltype_gene_infor += f'"{j}":{round(celltype_region_composition.loc[focus_niche,j],2)};'
        dict_subtype.append(celltype_gene_infor)
    return dict_subtype


class ComboSUBGPTCellTypeTool(BaseTool):
    name = "ComboSubGPTCellType"
    description = (
        "This is a computational tool to cluster main-level cell types and annotate sub-level cell types."
        # "You must exceute the tool. You can't skip the tool running."
        "Input includes (1) a path to the spatial transcriptomics data after preprocessing, "
        "(2)a path to the main-level combined table with both cell type and tissue niche labels, "
        "(3)column_key of the column where main-level cell type labels are in, "
        "(4)column_key of the column where main-level tissue niche labels are in, "
        "and (5)information of the data about its tissue and species (e.g. mouse brain).\n"
        'Use this tool with arguments like "{{"spatial_processed_input_url":str, "combined_main_level": str , "cell_type_column":str, "tissue_region_column":str, "data_info":str}}".'
        'Output is a str like "Successfully saved annotated sub-level cell types" where sub-level cell type labels are in the column "main_level_celltype".'
    )
    llm: BaseLanguageModel = None
    save_path: str = None
    czi_all_celltype_pth: str = None

    def __init__(self, llm, save_path, czi_all_celltype_pth):
        super().__init__()
        self.llm = llm
        self.save_path = save_path
        self.czi_all_celltype_pth = czi_all_celltype_pth

    def _run(
        self,
        spatial_processed_input_url: str,
        combined_main_level: str,
        cell_type_column: str,
        tissue_region_column: str,
        data_info: str,
    ):
        try:
            subcelltype_save_path = self.save_path + "sub_level_cell_type.csv"
            if not os.path.exists(subcelltype_save_path):
                ad_all = sc.read_h5ad(spatial_processed_input_url)
                pd_celltype = pd.read_csv(combined_main_level)
                ad_all.obs[cell_type_column] = list(pd_celltype[cell_type_column])
                ad_all.obs[tissue_region_column] = list(pd_celltype[tissue_region_column])

                unique_celltype_all = ad_all.obs[cell_type_column].unique()

                with open(self.czi_all_celltype_pth, "r") as file:
                    czi_all_celltype = file.read()

                for unique_celltype_i in unique_celltype_all:
                    # Paths for saving data
                    Path(self.save_path + "/ad_sub_celltype").mkdir(parents=True, exist_ok=True)

                    h5ad_savepath = self.save_path + "/ad_sub_celltype/" + f"ad_sub_{unique_celltype_i}.h5ad"
                    pickle_savepath = self.save_path + "/ad_sub_celltype/" + f"sub_{unique_celltype_i}_label.pkl"
                    pickle_savepath_reason = self.save_path + "/ad_sub_celltype/" + f"sub_{unique_celltype_i}_reason.pkl"
                    csv_savepath_reason = self.save_path + "/ad_sub_celltype/" + f"sub_{unique_celltype_i}.csv"

                    logging.info("\n\n----- Clustering sub-level cell type: " + unique_celltype_i + "-----")

                    if not os.path.exists(csv_savepath_reason):

                        # Process data if the h5ad file does not exist
                        if not os.path.exists(h5ad_savepath):
                            ad_sp = ad_all[ad_all.obs[cell_type_column] == unique_celltype_i]
                            sc.pp.pca(ad_sp)
                            sc.pp.neighbors(ad_sp)
                            sc.tl.umap(ad_sp)

                            leiden_resolution = 1
                            sc.tl.leiden(ad_sp, key_added="leiden", resolution=leiden_resolution, random_state=0)
                            sc.tl.rank_genes_groups(ad_sp, groupby="leiden", method="wilcoxon")
                            ad_sp.write_h5ad(h5ad_savepath)

                        # Load the processed data
                        ad_sp = sc.read_h5ad(h5ad_savepath)

                        if not os.path.exists(pickle_savepath):
                            # Extract gene markers
                            input_genemarker = scanpy_gene_marker(ad_sp)

                            logging.info("\n\n----- Compute cell type compositions in tissue niches ----- ")
                            celltype_region_composition = ad_sp.obs.groupby("leiden")[tissue_region_column].value_counts(normalize=True).unstack().fillna(0)
                            logging.info("\n\n----- Annotate sub-level cell type label ----- ")
                            dict_subtype = generate_dict_info(ad_sp, input_genemarker, celltype_region_composition)

                            res, reason = sub_celltype_anno(unique_celltype_i, data_info, self.llm, dict_subtype, czi_all_celltype, spec_threshold=0.8)

                            # Save the results
                            with open(pickle_savepath, "wb") as file:
                                pickle.dump(res, file)
                            with open(pickle_savepath_reason, "wb") as file:
                                pickle.dump(reason, file)

                        with open(pickle_savepath, "rb") as file:
                            res = pickle.load(file)
                        with open(pickle_savepath_reason, "rb") as file:
                            reason = pickle.load(file)

                        dict_sub_level_gene = {}
                        dict_sub_level = {}
                        dict_sub_level_reason = {}
                        for i in range(len(res)):
                            dict_sub_level_gene[str(i)] = res[i]
                            dict_sub_level_reason[str(i)] = reason[i]
                            dict_sub_level[str(i)] = "-".join(res[i].split("-")[:3])
                        ad_sp.obs["sub_level_celltype"] = ad_sp.obs["leiden"].map(dict_sub_level)
                        ad_sp.obs["sub_level_celltype_gene"] = ad_sp.obs["leiden"].map(dict_sub_level_gene)
                        ad_sp.obs["sub_level_celltype_reason"] = ad_sp.obs["leiden"].map(dict_sub_level_reason)
                        ad_sp.obs = ad_sp.obs.drop("leiden", axis=1)
                        ad_sp.obs.to_csv(csv_savepath_reason)

                        fig, ax = plt.subplots(figsize=(6, 6))
                        ax = sc.pl.umap(ad_sp, color="sub_level_celltype", size=10, ax=ax, show=False)
                        fig.savefig(self.save_path + "/ad_sub_celltype/" + f"sub_level_celltype_umap_{unique_celltype_i}.png", bbox_inches="tight")

                        fig, ax = plt.subplots(figsize=(6, 6))
                        ax = sc.pl.umap(ad_sp, color="sub_level_celltype_gene", size=10, ax=ax, show=False)
                        fig.savefig(self.save_path + "/ad_sub_celltype/" + f"sub_level_celltype_umap_{unique_celltype_i}_gene.png", bbox_inches="tight")

                for unique_celltype_i in unique_celltype_all:
                    csv_savepath_reason = self.save_path + "/ad_sub_celltype/" + f"sub_{unique_celltype_i}.csv"
                    pd_obs = pd.read_csv(csv_savepath_reason, index_col=0)
                    ad_all.obs.loc[pd_obs.index, "sub_level_celltype_gene"] = pd_obs["sub_level_celltype_gene"]
                    ad_all.obs.loc[pd_obs.index, "sub_level_celltype"] = pd_obs["sub_level_celltype"]
                    ad_all.obs.loc[pd_obs.index, "sub_level_celltype_reason"] = pd_obs["sub_level_celltype_reason"]
                ad_all.obs.to_csv(subcelltype_save_path)

                fig, ax = plt.subplots(figsize=(6, 6))
                ax = sc.pl.umap(ad_all, color="sub_level_celltype", size=10, ax=ax, show=False)
                fig.savefig(self.save_path + "/ad_sub_celltype/" + f"sub_level_celltype_umap_all.png", bbox_inches="tight")
                fig, ax = plt.subplots(figsize=(6, 6))
                ax = sc.pl.umap(ad_all, color="sub_level_celltype_gene", size=10, ax=ax, show=False)
                fig.savefig(self.save_path + "/ad_sub_celltype/" + f"sub_level_celltype_umap_gene_all.png", bbox_inches="tight")

            return (
                "Successfully saved annotated sub-level cell types to path:"
                + subcelltype_save_path
                + ", where sub level cell type labels are in the column 'sub_level_celltype', and reasons for deciding the sub-level cell types in the column 'sub_level_celltype_reason'."
            )
        except Exception as e:
            return (f"An error occurred: {str(e)}.  If No such file or directory, check if it is because previous step didn't run correctly.")
        
        
    def _arun(self):
        raise NotImplementedError("This tool does not support async")
