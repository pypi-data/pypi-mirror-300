import os, scanpy as sc
from langchain.tools import BaseTool
import pandas as pd

from langchain.base_language import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import PromptTemplate
from tqdm import tqdm
from langchain.chains import LLMChain
import time
import cellxgene_census
import numpy as np
from pathlib import Path


def scanpy_preprocess(spatialdata_input_path, save_path):
    ad_sp = sc.read_h5ad(spatialdata_input_path)
    ad_sp.raw = ad_sp

    # ad_sp = ad_sp[np.random.permutation(ad_sp.obs.index)[:5000], :]
    ad_sp.var.index = ad_sp.var.index.str.upper()

    # Preprocessin and dimensionality reduction
    sc.pp.filter_cells(ad_sp, min_genes=5)
    sc.pp.filter_cells(ad_sp, min_counts=10)
    sc.pp.filter_genes(ad_sp, min_cells=5)

    sc.pp.normalize_per_cell(ad_sp)
    sc.pp.log1p(ad_sp)
    # sc.pp.regress_out(ad_sp, ["total_counts"])
    # sc.pp.scale(ad_sp)

    sc.pp.pca(ad_sp)
    sc.pp.neighbors(ad_sp)
    sc.tl.umap(ad_sp)

    # save_path=os.path.join(os.path.dirname(spatialdata_input_path), "preprocessed.h5ad")
    ad_sp.write(save_path)
    return True


class get_czi_info_tool(BaseTool):
    name = "get_czi_info"
    description = (
        "This is a computational tool to get related information from CZI database."
        "Input is tissue type info (e.g., brain, or lung), species type info (must be one of 'Homo sapiens' or 'Mus musculus') of the data, target_disease type info ('normal' and/or specific disease type like 'lung adenocarcinoma'), and the dataset id of the best matching CZI reference dataset."
        "'best_dataset_id' must be real dataset id and not be something like 'Dataset ID from Step 1.1 output'."
        'Use this tool with arguments like "{{"target_tissue":str,"target_species":str, "target_disease":str,"best_dataset_id":str}}".'
        "Output is a str like 'Successfully saved possible cell types to path, and possible tissues to path..."
    )
    desired_path: str = None
    llm: BaseLanguageModel = None
    save_path: str = None

    def __init__(self, desired_path, save_path, llm):
        super().__init__()
        self.desired_path = desired_path
        self.llm = llm
        self.save_path = save_path

    def _run(self, target_tissue: str, target_species: str, target_disease: str, best_dataset_id):
        census_df = pd.read_csv(self.desired_path + "/data/czi_census_datasets_v2.csv", index_col=0)

        all_tissue_general = census_df["tissue_general"].unique()

        content = (
            "Which is the best matching tissue name for {target_tissue} "
            f"in all categories: {all_tissue_general}?\n"
            + "Output format must be only the best matching tissue name. Do not show numbers before the name. Do not add space before number.\n"
        )

        llm_prompt = PromptTemplate(
            input_variables=["human_prompt"],
            template=content,
        )
        chain = LLMChain(llm=self.llm, prompt=llm_prompt)

        res = chain.run(target_tissue)  # response.choices[0].message.content.split('\n')

        census_df = census_df.loc[census_df["tissue_general"] == res, :]
        census_df = census_df.loc[census_df["disease"] == target_disease, :]
        # census_df.to_csv(self.czi_file_path)

        ### read and save data
        Path(self.save_path + "/czi_reference").mkdir(parents=True, exist_ok=True)
        directory_path = self.save_path + "/czi_reference"
        file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        if len(file_names) < 1:
            ### remove the previous files
            # for f in file_names:
            #     os.remove(os.path.join(directory_path, f))

            census = cellxgene_census.open_soma(census_version="latest")

            ref_save_path = self.save_path + f"/czi_reference/sc_reference_{best_dataset_id}.h5ad"
            if not os.path.exists(ref_save_path):
                ad_ref = cellxgene_census.get_anndata(
                    census,
                    organism=target_species,
                    obs_value_filter=f"dataset_id in {[best_dataset_id]}",
                )
                ad_ref = ad_ref[:, np.sum(ad_ref.X, axis=0) > 0]
                ad_ref = ad_ref[ad_ref.obs["cell_type"] != "unknown"]
                ad_ref.write_h5ad(ref_save_path)

            # ind = 0
            # np.random.seed(0)
            # all_dataset_id = np.random.permutation(np.array(census_df["dataset_id"]))
            # for dataset_id in all_dataset_id:
            #     try:
            #         ref_save_path = self.save_path + f"/czi_reference/sc_reference_{dataset_id}.h5ad"
            #         if not os.path.exists(ref_save_path):
            #             ad_ref = cellxgene_census.get_anndata(
            #                 census,
            #                 organism=target_species,
            #                 obs_value_filter=f"dataset_id in {[dataset_id]}",
            #             )
            #             if ad_ref.shape[0] == 0:
            #                 continue
            #             ad_ref = ad_ref[:, np.sum(ad_ref.X, axis=0) > 0]
            #             ad_ref = ad_ref[ad_ref.obs["cell_type"] != "unknown"]
            #             ad_ref.write_h5ad(ref_save_path)
            #             ind += 1
            #     except:
            #         continue
            #     if ind >= 3:
            #         break

            census.close()

        ### if exist file, skip
        file_path_1 = self.save_path + "possible_tissues.txt"
        if not os.path.exists(file_path_1):
            # possible_tissues = census_df["tissue"].unique()
            all_tissue = ", ".join(census_df["tissue"].astype(str))
            all_tissue = all_tissue.split(";")
            all_tissue = set(all_tissue)
            possible_tissues_str = ";".join(all_tissue)
            with open(file_path_1, "a") as file:
                file.write(possible_tissues_str + "\n")  # Adding a newline character for separation

        file_path_2 = self.save_path + "possible_celltypes.txt"
        if not os.path.exists(file_path_2):
            # possible_celltypes = census_df["cell_type"].unique()
            all_cell_type = ", ".join(census_df["cell_type"].astype(str))
            all_cell_type = all_cell_type.split(";")
            all_cell_type = set(all_cell_type)
            possible_celltypes_str = ";".join(all_cell_type)
            with open(file_path_2, "a") as file:
                file.write(possible_celltypes_str + "\n")  # Adding a newline character for separation

        return f"Successfully saved possible cell types to:" + file_path_2 + ", and possible tissues to:" + file_path_1

    def _arun(self, input_url):
        raise NotImplementedError("This tool does not support async")
