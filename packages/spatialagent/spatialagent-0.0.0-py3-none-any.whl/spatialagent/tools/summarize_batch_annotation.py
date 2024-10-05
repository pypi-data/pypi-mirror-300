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


class SummarizeBatchAnnoTool(BaseTool):
    name = "SummarizeBatchAnno"
    description = (
        "This is a tool to summarize batch information of the spatial data."
        "Input includes (1)a path to the spatial transcriptomics data,"
        "(2) the column key of batch,"
        "(3) the description of the dataset,"
        "(4) the tissue type of the dataset."
        'Use this tool with arguments like "{{"spatial_adata_input_url":str,"batch_key":str, "dataset_description":str, "rule_tissue":str}}".'
        'Output is a str like "Successfully save summary to path ..." '
    )


    llm: BaseLanguageModel = None
    save_path: str = None

    def __init__(self, llm, save_path):
        super().__init__()
        self.llm = llm
        self.save_path = save_path

    def _run(self, spatial_adata_input_url, batch_key, dataset_description, rule_tissue):
        summary_save_path = self.save_path + "summary_batch.json"
        if not os.path.exists(summary_save_path):
            ad_sp = sc.read_h5ad(spatial_adata_input_url)
            unique_batch = ad_sp.obs[batch_key].unique()
            content = (
                f"I have spatial transcritpomics samples in {rule_tissue}."
                f"The dataset description is {dataset_description}."
                "Give me analysis of the batch keys."
                "I have these batch keys:{unique_batch}."
                "For each batch, output a description. Output format should be: \n"
                "key 1:xx, description:xx. end."
                "key 2:xx, description:xx. end."
                "key 3:xx, description:xx. end."
            )

            llm_prompt = PromptTemplate(
                input_variables=["human_prompt"],
                template=content,
            )

            chain = LLMChain(llm=self.llm, prompt=llm_prompt)

            res = chain.run(unique_batch) 
            dic_batch={}
            for i in unique_batch:
                dic_batch[i] = res.split(i)[1].split('end')[0]
            ### save results to json
            with open(summary_save_path, 'w') as f:
                json.dump(dic_batch, f)
            
        return (
            "Successfully save summary of batch information to path: " + summary_save_path
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
