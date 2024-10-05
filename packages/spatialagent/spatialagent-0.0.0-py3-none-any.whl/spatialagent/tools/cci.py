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
import base64
import matplotlib.pyplot as plt
import liana as li
from liana.method import cellphonedb

def contains_only_integers(arr):
    # Check if all values are whole numbers, even if they are floats
    return np.all(arr % 1 == 0)


class CCITool(BaseTool):
    name = "Infer_cell_cell_interaction_cellphonedb"
    description = (
        "This is a computational tool CellPhoneDB to infer cell-cell communication."
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
    llm: BaseLanguageModel = None
    save_path: str = None

    def __init__(self, llm, save_path):
        super().__init__()
        self.llm = llm
        self.save_path = save_path

    def _run(
        self,
        spatial_adata_input_url,
        summary_batch, dataset_description, rule_tissue, batch_key, cell_type_key, tissue_region_key
    ):
        cci_result = self.save_path + 'cci_result.csv'
        if not os.path.exists(cci_result):
            ad_sp = sc.read_h5ad(spatial_adata_input_url)
            unique_sample = ad_sp.obs[batch_key].unique()

            ### set database of cellphonedb
            content = (
                f"Is this sample from mouse or human? Only output mouse or human."
                "I have spatial transcritpomics samples in {rule_tissue}."
                "The dataset description is {dataset_description}."                                    
            )
            llm_prompt = PromptTemplate(
                input_variables=["human_prompt"],
                template=content,
            )
            chain = LLMChain(llm=self.llm, prompt=llm_prompt)     
            resource_name = chain.run({'rule_tissue': rule_tissue, 'dataset_description': dataset_description}) 
            if 'mouse' in resource_name:
                ### homology mapping
                resource = li.rs.select_resource('consensus')
                map_df = li.rs.get_hcop_orthologs(url='https://ftp.ebi.ac.uk/pub/databases/genenames/hcop/human_mouse_hcop_fifteen_column.txt.gz',
                                                columns=['human_symbol', 'mouse_symbol'],
                                                # NOTE: HCOP integrates multiple resource, so we can filter out mappings in at least 3 of them for confidence
                                                min_evidence=3
                                                )
                # rename the columns to source and target, respectively for the original organism and the target organism
                map_df = map_df.rename(columns={'human_symbol':'source', 'mouse_symbol':'target'})
                # We will then translate
                mouse = li.rs.translate_resource(resource,
                                                map_df=map_df,
                                                columns=['ligand', 'receptor'],
                                                replace=True,
                                                # Here, we will be harsher and only keep mappings that don't map to more than 1 mouse gene
                                                one_to_many=1
                                                )
            df_all=[]
            for sample in unique_sample:
                ad_sample = ad_sp[ad_sp.obs[batch_key] == sample]

                if contains_only_integers(ad_sample.X):
                    sc.pp.normalize_total(ad_sample)
                    sc.pp.log1p(ad_sample)

                # run cellphonedb
                if 'mouse' in resource_name:
                    cellphonedb(ad_sample,
                                groupby=cell_type_key,
                                resource=mouse,
                                expr_prop=0.1,
                                use_raw=False,
                                verbose=True, key_added='cpdb_res')
                else:
                    cellphonedb(ad_sample,
                                groupby=cell_type_key,
                                expr_prop=0.1,
                                use_raw=False,
                                verbose=True, key_added='cpdb_res')
                    
                pd_sc_lr_cpdb=ad_sample.uns['cpdb_res']
                pd_sc_lr_cpdb = pd_sc_lr_cpdb.loc[pd_sc_lr_cpdb['cellphone_pvals']<=0.05,:]
                pd_sc_lr_cpdb['sample']=sample
                df_all.append(pd_sc_lr_cpdb)
            df_all=pd.concat(df_all)
            df_all.to_csv(cci_result)
        return  "Successfully save infered cell-cell communication result to path:" + cci_result 

    def _arun(self):
        raise NotImplementedError("This tool does not support async")


