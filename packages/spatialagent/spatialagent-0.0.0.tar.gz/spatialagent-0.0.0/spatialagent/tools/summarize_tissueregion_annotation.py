import scanpy as sc
import matplotlib.pyplot as plt
import numpy as np
import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import scipy as sp
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import silhouette_score
import os
import scanpy as sc
import pandas as pd
import warnings
import sys
import anndata as ad
import scanpy as sc
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
import json
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

warnings.simplefilter(action="ignore", category=FutureWarning)


class SummarizeTissueRegionAnnoTool(BaseTool):
    name = "SummarizeTissueRegionAnno"
    description = (
        "This is a tool to summarize tissue region information of the spatial data."
        "Input includes (1)a path to the spatial transcriptomics data,"
        "(2) path to saved batch information summary,"
        "(3) the description of the dataset,"
        "(4) the tissue type of the dataset."
        "(5) the column key of batch,"
        "(6) the column key of cell type,"
        "(7) the column key of tissue region,"
        'Use this tool with arguments like "{{"spatial_adata_input_url":str,"summary_batch":str, "dataset_description":str,"rule_tissue":str, "batch_key":str, "cell_type_key":str,"tissue_region_key":str}}".'
        'Output is a str like "Successfully save summary to path ..." '
    )
    #     args = parser.parse_args()
    # args.rule = (f"I want to infer cell-cell communications or interactions in a spatial transcriptomics experiment of {args.rule_tissue}."
    #              f"Path of labeled data is {args.rule_labeleddata_path} where column {args.batch_key} is different batches of samples,"
    #              f"column {args.cell_type_key} is cell types, and column {args.tissue_niche_key} is tissue niches."
    #              f"The sample description is in {args.sample_description}"
    #              f"The cell type label description is in {args.label_description}"

    llm: BaseLanguageModel = None
    save_path: str = None

    def __init__(self, llm, save_path):
        super().__init__()
        self.llm = llm
        self.save_path = save_path

    def _run(self, spatial_adata_input_url, summary_batch, dataset_description, rule_tissue, batch_key, cell_type_key, tissue_region_key):
        allsample_tissueregion_save_path = self.save_path + "allsample_tissueregion.json"
        if not os.path.exists(allsample_tissueregion_save_path):
            ad_sp = sc.read_h5ad(spatial_adata_input_url)
            unique_sample = ad_sp.obs[batch_key].unique()

            ### read json file
            with open(summary_batch) as f:
                summary_batch = json.load(f)

            ### get each sample, each tissue region
            persample_tissueregion_save_path = self.save_path + "persample_tissueregion.json"
            if not os.path.exists(persample_tissueregion_save_path):
                content = (
                    f"I have spatial transcritpomics samples in {rule_tissue}."
                    f"The dataset description is {dataset_description}."
                    "Give me analysis of the tissue region, especially in terms of their features and functions."
                    "Now I'm analyzing cells in batch {batch_id} sample."
                    # "Prior information of labels is: {info_str}"
                    "Percentage of cell types in this tissue region is:{celltype_tissue_composition_str}"
                    "For each tissue region, think step by step:"
                    "1. what is the tissue region's cell type composition: (1) have specificity in one cell type (with more than 80%), (2) specific in two or three cell type (sum up to 90%), (3) mixed or evenly distributed of cell type (where the highest percentage is lower than 10%)?"
                    "2. from the annotations, give potential reasons of the tissue region's cell type specificity, e.g. the tissue region's functions related to in this sample."
                    "3. is there any interesting or special findings?"
                    "Be concise."
                )

                llm_prompt = PromptTemplate(
                    input_variables=["human_prompt"],
                    template=content,
                )

                chain = LLMChain(llm=self.llm, prompt=llm_prompt)                
                tissue_region_summary={}
                for sample_i in unique_sample:
                    tissue_region_summary[sample_i]={}
                    ad_sp_i=ad_sp[ad_sp.obs[batch_key]==sample_i]
                    unique_tissue_region_i=ad_sp_i.obs[tissue_region_key].unique()

                    celltype_tissue_composition = (
                        ad_sp_i.obs.groupby(tissue_region_key)[cell_type_key].value_counts(normalize=True).unstack().fillna(0)
                    )
                    for focus in unique_tissue_region_i:
                        celltype_tissue_composition_str=''
                        celltype_tissue_composition_str += (
                            f"The cell type distribution of tissue region {focus} is:"
                        )
                        for j in celltype_tissue_composition.columns:
                            if celltype_tissue_composition.loc[focus, j] > 0:
                                celltype_tissue_composition_str += (
                                    f"{j}:{round(celltype_tissue_composition.loc[focus,j],2)}" + ";"
                                )
                        celltype_tissue_composition_str += "\n"

                        args={"batch_id":summary_batch[sample_i],"celltype_tissue_composition_str":celltype_tissue_composition_str}
                        res = chain.run(args) 
                        tissue_region_summary[sample_i][focus]=res
                ### write json file
                with open(persample_tissueregion_save_path, "w") as f:
                    json.dump(tissue_region_summary, f)
            else:
                with open(persample_tissueregion_save_path) as f:
                    tissue_region_summary = json.load(f)

            ### get each cell type, across samples
            batch_info=''
            for i in summary_batch.keys():
                batch_info+=i+":"+summary_batch[i]+"."
            content = (
                f"I have spatial transcritpomics samples in {rule_tissue}."
                f"The dataset description is {dataset_description}."
                "Give me analysis of the tissue region features and patterns."
                f"The batch information is {batch_info}."
                "The tissue region information is {tissue_region_across_sample}."
                "Think step by step:"
                "1.what is pattern of each tissue region's cell type composition change?"
                "2.what is possible region behind the changes?"
                "3.Is there any interesting or special findings?"
                "Be concise."
            )
            llm_prompt = PromptTemplate(
                input_variables=["human_prompt"],
                template=content,
            )
            chain = LLMChain(llm=self.llm, prompt=llm_prompt)


            tissue_region_summary_all={}
            unique_tissue_region=ad_sp.obs[tissue_region_key].unique()
            for focus in unique_tissue_region:
                tissue_region_across_sample=''
                for i in unique_sample:
                    if focus in tissue_region_summary[i].keys():
                        tissue_region_across_sample+=i+":"+tissue_region_summary[i][focus]+".\n"

                args={"tissue_region_across_sample":tissue_region_across_sample}
                res = chain.run(args) 
                tissue_region_summary_all[focus]=res

            ### write json file
            with open(allsample_tissueregion_save_path, "w") as f:
                json.dump(tissue_region_summary_all, f)
           
        return (
            "Successfully save summary of tissue region information to path: " + allsample_tissueregion_save_path
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
