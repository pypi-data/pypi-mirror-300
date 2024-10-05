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
from langchain.base_language import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from langchain.chains import LLMChain

from itertools import combinations
from collections import Counter

from collections import defaultdict
from itertools import combinations
from collections import Counter
from pathlib import Path
import pickle
import logging


def get_sublevel_annotation(llm, unique_main_level_i, sample_info, possible_tissue_description, region_celltype_composition, region_gene_list, spec_threshold=0.8):

    content = (
        f"You must think step by step to provide fine-grained annotation of this sub-level tissue cluster under main-level {unique_main_level_i} in the {sample_info}.\n"
        'You must output "Sub-level tissue niche annotation:...;Reason:...". Do not add numbers, space, """, "." or any other characters after the annotation.'
        "The Sub-level tissue niche annotation must be in this format: [main-level tissue niche]/[specificity, e.g. unique cell state or function]/[marker gene].\n"
        f"1.The main-level cell type is: {unique_main_level_i}.\n"
        f"Decide annotation for the sub-level cluster based on the enriched gene markers and sub-level cell type composition in this tissue cluster:"
        + "{celltype_gene_infor}\n"
        + f"2.Check distribution in each sub-level cell type and find if there is one single sub-level cell type with more than {spec_threshold} of this subtype. If yes, please provide the cell type name. Do not change the cell type name. If no, leave the cell type name blank and continue.\n"
        + "Note that slightly different sub-level cell type means different types. \n"
        + f"3.Is there any identified genes that are well-known gene markers for this subtype of {unique_main_level_i} in {sample_info}? If yes, please add the gene as marker gene. If not, do not add gene in the annotation.\n"
        + f"All possible tissues in {sample_info} and their descriptions are {possible_tissue_description}."
        + "Output must be in the format: Sub-level tissue niche annotation:...;Reason:... Do not change any format like adding or deleting space or other symbols.\n"
    )

    llm_prompt = PromptTemplate(
        input_variables=["human_prompt"],
        template=content,
    )
    chain = LLMChain(llm=llm, prompt=llm_prompt)

    res_all = {}
    reason_all = {}
    for ind, i in enumerate(region_gene_list.keys()):

        celltype_gene_infor = ""
        celltype_gene_infor += f"The enriched genes in this niche are: {region_gene_list[i]} .\n"

        celltype_gene_infor += f"The sub-level cell type composition in niche is:"
        for j in region_celltype_composition.columns:
            if region_celltype_composition.loc[i, j] > 0.01:
                celltype_gene_infor += f"{j}:{round(region_celltype_composition.loc[i,j],2)}" + ";"
        celltype_gene_infor + ".\n"

        res = chain.run(celltype_gene_infor)
        logging.info(res.split(";Reason:")[0].split("Sub-level tissue niche annotation:")[-1])
        logging.info("\n")
        logging.info(res.split(";Reason:")[1])
        logging.info("\n\n")
        res_all[i] = res.split(";Reason:")[0].split("Sub-level tissue niche annotation:")[-1]
        reason_all[i] = res.split(";Reason:")[1]

    return res_all, reason_all


class ComboSUBGPTTissueNicheTool(BaseTool):
    name = "ComboSubGPTTissueNiche"
    description = (
        "This is a computational tool to annotation sub-level tissue niches based on multimodal information."
        # "You must exceute the tool. You can't skip the tool running."
        "Input includes (1)a path to the spatial transcriptomics data after preprocessing, "
        "(2)a path to the sub-level utag results of tissue niche clusters, "
        "(3)column_key of the column where main-level tissue niche labels are in the ub-level utag results, "
        "(4)column_key of the column where sub-level cell type labels are in the ub-level utag results, "
        "(5)column_key of the column where sub-level utag tissue niche clusters are in the ub-level utag results, "
        "(6)a path to saved possible tissues, "
        "(7)and information of the data about its tissue and species (e.g. mouse brain). "
        'Use this tool with arguments like "{{"spatialdata_input_path":str, "utag_cluster_path": str , "main_level_tissue_niche_key":str, "sub_level_cell_type_key":str, "sub_level_utag_key":str,"possible_tissue_path":str,"sample_info":str}}".'
        'Output is a str like "Successfully saved annotated sub level tissue niches in path ... where ...'
    )
    llm: BaseLanguageModel = None
    save_path: str = None

    def __init__(self, llm, save_path):
        super().__init__()
        self.llm = llm
        self.save_path = save_path

    def _run(
        self,
        spatialdata_input_path: str,
        utag_cluster_path: str,
        main_level_tissue_niche_key: str,
        sub_level_cell_type_key: str,
        sub_level_utag_key: str,
        possible_tissue_path: str,
        sample_info: str,
    ):

        Path(self.save_path + "/ad_sub_tissueniche_anno").mkdir(parents=True, exist_ok=True)
        csv_savepath_all = self.save_path + "/ad_sub_tissueniche_anno/" + f"sub_level_tissue_niche.csv"
        if not os.path.exists(csv_savepath_all):
            ad_all = sc.read_h5ad(spatialdata_input_path)
            pd_utag = pd.read_csv(utag_cluster_path, index_col=0)
            ad_all.obs = pd_utag
            ad_all.obs[sub_level_utag_key] = ad_all.obs[sub_level_utag_key].astype("str")

            ### refine main_level_tissue_niche name
            unique_main_level_tissue_niche = ad_all.obs[main_level_tissue_niche_key].unique()

            ### get llm description for possible tissues
            with open(possible_tissue_path, "r") as file:
                possible_tissues = file.read()
            content = (
                "Search literature to provide the spatial location, gene markers and unique features of these tissue regions:\n"
                "{possible_tissues}.\n" + "Output must be in format: Tissue region;gene markers;features.\n"
            )
            llm_prompt = PromptTemplate(
                input_variables=["human_prompt"],
                template=content,
            )
            chain = LLMChain(llm=self.llm, prompt=llm_prompt)
            possible_tissue_description = chain.run(possible_tissues)

            ### annotate each main level tissue niche
            for unique_main_level_i in unique_main_level_tissue_niche:
                logging.info("\n\n----- Annotating sub-level tissue niche of: " + unique_main_level_i + "-----")
                # pickle_savepath_reason = self.save_path  + "/ad_sub_tissueniche_anno/" + f"sub_{unique_main_level_i}_reason.pkl"
                csv_savepath_reason = self.save_path + "/ad_sub_tissueniche_anno/" + f"sub_{unique_main_level_i}.csv"

                if not os.path.exists(csv_savepath_reason):
                    ad_sp = ad_all[ad_all.obs[main_level_tissue_niche_key] == unique_main_level_i]

                    sc.tl.rank_genes_groups(ad_sp, groupby=sub_level_utag_key, method="wilcoxon")
                    region_gene_list = {}
                    temp = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["names"]).head(5)
                    temp_score = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["scores"]).head(5)
                    for i in range(temp.shape[1]):
                        curr_col = temp.iloc[:, i].to_list()
                        curr_col_score = temp_score.iloc[:, i].to_list()
                        list_true = [x > 0 for x in curr_col_score]
                        curr_col = list(np.array(curr_col)[list_true])
                        region_gene_list[temp.columns[i]] = curr_col

                    region_celltype_composition = ad_sp.obs.groupby(sub_level_utag_key)[sub_level_cell_type_key].value_counts(normalize=True).unstack().fillna(0)
                    res_all, reason_all = get_sublevel_annotation(self.llm, unique_main_level_i, sample_info, possible_tissue_description, region_celltype_composition, region_gene_list)

                    ad_sp.obs["sub_level_tissueniche"] = ad_sp.obs[sub_level_utag_key].map(res_all)
                    ad_sp.obs["sub_level_tissueniche_reason"] = ad_sp.obs[sub_level_utag_key].map(reason_all)
                    ad_sp.obs.to_csv(csv_savepath_reason)

            for unique_main_level_i in unique_main_level_tissue_niche:
                csv_savepath_reason = self.save_path + "/ad_sub_tissueniche_anno/" + f"sub_{unique_main_level_i}.csv"
                pd_obs = pd.read_csv(csv_savepath_reason, index_col=0)
                ad_all.obs.loc[pd_obs.index, "sub_level_tissueniche"] = pd_obs["sub_level_tissueniche"]
                ad_all.obs.loc[pd_obs.index, "sub_level_tissueniche_reason"] = pd_obs["sub_level_tissueniche_reason"]

            ad_all.obs.to_csv(csv_savepath_all)

        return (
            "Successfully saved annotated sub-level tissue niches to path:"
            + csv_savepath_all
            + ", where sub level tissue niches are in the column 'sub_level_tissueniche', and reasons for deciding the sub-level tissue niches in the column 'sub_level_tissueniche_reason'."
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
