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


class InferLRTool(BaseTool):
    name = "InferLRConfidence"
    description = (
        "This is a computational tool to analyze ligand receptor pair information."
        "Input includes (1)a path to the spatial transcriptomics data,"
        "(2) path to saved batch information summary,"
        "(3) the description of the dataset,"
        "(4) the tissue type of the dataset."
        "(5) path to saved cell type information summary,"
        "(6) path to saved tissue region information summary,"
        "(7) the path to saved infered cell-cell communication result"
        'Use this tool with arguments like "{{"spatial_adata_input_url":str,"summary_batch":str, "dataset_description":str,"rule_tissue":str, "summary_celltype":str, "summary_tissueregion":str,"path_cci":str}}".'
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
        spatial_adata_input_url,
        summary_batch, dataset_description, rule_tissue, summary_celltype, summary_tissueregion, path_cci
    ):
        cci=pd.read_csv(path_cci)

        with open(summary_batch) as f:
            summary_batch = json.load(f)

        with open(summary_celltype) as f:
            summary_celltype = json.load(f)   

        with open(summary_tissueregion) as f:
            summary_tissueregion = json.load(f)                        

        unique_sample=list(summary_batch.keys())

        ### analyze unique cell type pair across samples
        unique_source_target={}
        for i in unique_sample:
            cci_i = cci.loc[cci['sample']==i,:]
            test = cci_i.drop_duplicates(subset=['source', 'target'])
            unique_source_target[i] = list(test[['source', 'target']].itertuples(index=False, name=None))

        for i in unique_sample:
            set_slice_1 = set(unique_source_target[i])
            other_sets = set()
            for key, value in unique_source_target.items():
                if key != i:
                    other_sets.update(value)
            unique_to_slice_1 = set_slice_1 - other_sets
            # Display the result
            print(unique_to_slice_1)


        ### find same cell type pair but different ligand receptor pair across samples
        test=cci.drop_duplicates(subset=['source', 'target'])
        all_source_target=list(test[['source', 'target']].itertuples(index=False, name=None))
        for i in all_source_target:
            if all_source_target.count(i)>1:
                print(i)


        p=0

        return (
            "Successfully save a combined table with main-level both cell type and tissue niche labels to path:"
            + ", where main-level cell type labels are"
            + " in column 'main_level_celltype' and main-level tissue niche labels are in column 'main_level_tissueniche'."
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
