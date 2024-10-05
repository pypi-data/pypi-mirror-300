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
import shutil
import os
import sys
import anndata as ad
import scanpy as sc
import numpy as np
import pickle
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


class SaveAnnoTool(BaseTool):
    name = "SaveAnno"
    description = (
        "This is a tool to summarize both main-level and sub-level cell type and tissue niche annotations."
        "Input includes (1)a path to the spatial transcriptomics data,"
        "(2)path to annotated sub-level tissue niches, "
        "(3)path to the main level combined table, "
        "(5)column_key of the column where main-level cell type label is, "
        "(6)column_key of the column where main-level tissue niche label is, "
        "(7)column_key of the column where sub-level cell type label is, "
        "(8)column_key of the column where reason for sub-level cell type label is, "
        "(9)column_key of the column where sub-level tissue niche label is, "
        "(10)column_key of the column where reason for sub-level tissue niche label is, "
        'Use this tool with arguments like "{{"spatial_adata_input_url":str,"sub_level_tissue_niche_url":str,"path_main_level_combined_table":str,"main_level_cell_type_key":str,"main_level_tissue_niche_key":str,"sub_level_cell_type_key":str,"sub_level_cell_type_reason_key":str,"sub_level_tissue_niche_key":str,"sub_level_tissue_niche_reason_key":str}}".'
        'Output is a str like "Successfully save summary to path ..." '
    )
    llm: BaseLanguageModel = None
    save_path: str = None

    def __init__(self, llm, save_path):
        super().__init__()
        self.llm = llm
        self.save_path = save_path

    def _run(
        self,
        spatial_adata_input_url: str,
        sub_level_tissue_niche_url: str,
        path_main_level_combined_table: str,
        main_level_cell_type_key: str,
        main_level_tissue_niche_key: str,
        sub_level_cell_type_key: str,
        sub_level_cell_type_reason_key: str,
        sub_level_tissue_niche_key: str,
        sub_level_tissue_niche_reason_key: str,
    ):
        result_path = self.save_path + "final_result.h5ad"
        if not os.path.exists(result_path):
            ad_all = sc.read_h5ad(spatial_adata_input_url)
            pd_sub_level_tissueniche = pd.read_csv(sub_level_tissue_niche_url, index_col=0)
            ad_all.obs = pd_sub_level_tissueniche
            pd_path_main_level_combined_table=pd.read_csv(path_main_level_combined_table,index_col=0)
            ad_all.obs['main_level_celltype_reason'] = pd_path_main_level_combined_table['main_level_celltype_reason']
            ad_all.obs['main_level_tissueniche_reason'] = pd_path_main_level_combined_table['main_level_tissueniche_reason']
            ad_all.write_h5ad(result_path)
            
            dir_path = self.save_path 
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                
                # Skip the file named result.h5ad
                if item == 'final_result.h5ad':
                    continue
                
                # If it's a file, remove it
                if os.path.isfile(item_path):
                    os.remove(item_path)
                # If it's a folder, remove the entire folder
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

            print("Cleanup completed, except for result.h5ad.")



        return (
            "Successfully save final annotated anndata to path:"
            + result_path
            + ", where main-level cell type labels is in column "
            + main_level_cell_type_key
            + ", reason for deciding main-level cell type labels is in column 'main_level_celltype_reason'"
            + ", main-level tissue niche labels is in column"
            + main_level_tissue_niche_key
            + ", reason for deciding main-level tissue niche labels is in column 'main_level_tissueniche_reason'"
            + ", sub-level cell type labels is in column "
            + sub_level_cell_type_key
            + ", reason for deciding sub-level cell type labels is in column"
            + sub_level_cell_type_reason_key
            + ", sub-level tissue niche labels is in column"
            + sub_level_tissue_niche_key
            + ", reason for deciding sub-level tissue niche labels is in column"
            + sub_level_tissue_niche_reason_key
            + "."
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
