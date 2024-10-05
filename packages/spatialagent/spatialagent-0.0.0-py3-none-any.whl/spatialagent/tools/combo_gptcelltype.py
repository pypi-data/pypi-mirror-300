import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt
from langchain.tools import BaseTool
import pandas as pd
import os
from langchain.base_language import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import time
import logging

# ### function adapted from omicverse and gptcelltype
# def gptcelltype(input, client, tissuename=None, speciename="human"):
#     print("Note: AGI API key found: returning the cell type annotations.")
#     cutnum = int(np.ceil(len(input) / 30))
#     if cutnum > 1:
#         cid = np.digitize(range(1, len(input) + 1), bins=np.linspace(1, len(input), cutnum + 1))
#     else:
#         cid = np.ones(len(input), dtype=int)

#     allres = {}
#     for i in range(1, cutnum + 1):
#         id_list = [j for j, x in enumerate(cid) if x == i]
#         flag = False
#         while not flag:
#             content = (
#                 f'Identify cell types of {tissuename} cells in {speciename} using the following markers separately for each row. Only provide the cell type name and confidence score from 0 to 1 where 0 is with lowest confidence and 1 highest. Output format must be like "Cardiomyocytes,0.8". Do not show numbers before the name. Do not add space before number. Some can be a mixture of multiple cell types.\n'
#                 + "{human_prompt}\n"
#             )

#             llm_prompt = PromptTemplate(
#                 input_variables=["human_prompt"],
#                 template=content,
#             )

#             from langchain.chains import LLMChain

#             chain = LLMChain(llm=client, prompt=llm_prompt)
#             prompt = "\n".join([input[list(input.keys())[j]] for j in id_list if input[list(input.keys())[j]] != "unknown"])
#             # prompt is human input from request body
#             # return response
#             res = chain.run(prompt)  # response.choices[0].message.content.split('\n')

#             # prompt is human input from request body
#             # return response
#             res = chain.run(prompt).split("\n")
#             if len(res) == len(id_list):
#                 flag = True
#         for idx, cell_type in zip(id_list, res):
#             key = list(input.keys())[idx]
#             allres[key] = "unknown" if input[key] == "unknown" else cell_type.strip(",")

#         print("Note: It is always recommended to check the results returned by GPT-4 in case of AI hallucination, before going to downstream analysis.")

#     return allres


# class GPTCellTypeTool(BaseTool):
#     name = "GPTCellType"
#     description = (
#         "This is a computational tool to cluster and annotate cell types."
#         "You must exceute the tool. You can't skip the tool running."
#         "Input is a path to the spatial transcriptomics data after preprocessing, resolution for leiden clustering, tissue where cells are from (e.g. brain), species where cells are from, e.g., human, mouse."
#         'Use this tool with arguments like "{{"spatialdata_input_path":str, "leiden_resolution": float , "tissuename":str, "speciename":str}}".'
#         'Output is a str like "Successfully saved annotated cell table to path" where cell annotations are in the column "gptlabeled_cell_type".'
#     )
#     llm: BaseLanguageModel = None

#     def __init__(self, llm):
#         super().__init__()
#         self.llm = llm

#     def _run(
#         self,
#         spatialdata_input_path: str,
#         leiden_resolution: float,
#         tissuename: str,
#         speciename: str,
#     ):
#         save_path = os.path.join(os.path.dirname(spatialdata_input_path), "gptlabeled_cell_type.csv")
#         if not os.path.exists(save_path):
#             ad_sp = sc.read_h5ad(spatialdata_input_path)

#             sc.tl.leiden(ad_sp, key_added="leiden", resolution=leiden_resolution, random_state=0)

#             sc.tl.rank_genes_groups(ad_sp, groupby="leiden", method="wilcoxon")

#             input = {}
#             temp = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["names"]).head(10)
#             temp_score = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["scores"]).head(10)
#             for i in range(temp.shape[1]):
#                 curr_col = temp.iloc[:, i].to_list()
#                 curr_col_score = temp_score.iloc[:, i].to_list()
#                 list_true = [x > 0 for x in curr_col_score]
#                 curr_col = list(np.array(curr_col)[list_true])
#                 input[i] = curr_col

#             input_3 = {k: "unknown" if not v else ",".join(v[:3]) for k, v in input.items()}
#             annotation_3 = gptcelltype(input_3, self.llm, tissuename, speciename)

#             input_5 = {k: "unknown" if not v else ",".join(v[:5]) for k, v in input.items()}
#             annotation_5 = gptcelltype(input_5, self.llm, tissuename, speciename)

#             input_10 = {k: "unknown" if not v else ",".join(v[:10]) for k, v in input.items()}
#             annotation_10 = gptcelltype(input_10, self.llm, tissuename, speciename)

#             print(annotation_3, "/n", annotation_5, "/n", annotation_10, "/n")
#             annotation = {}
#             for ind, (x, y, z) in enumerate(zip(annotation_3.values(), annotation_5.values(), annotation_10.values())):
#                 # print(x.split(',')[1],y.split(',')[1],z.split(',')[1])
#                 if x == max(x, y, z):
#                     annotation[ind] = x.split(",")[0]
#                 elif y == max(x, y, z):
#                     annotation[ind] = y.split(",")[0]
#                 else:
#                     annotation[ind] = z.split(",")[0]
#             # print(annotation)
#             ad_sp.obs["leiden"] = ad_sp.obs["leiden"].astype(int)
#             ad_sp.obs["gptlabeled_cell_type"] = ad_sp.obs["leiden"].map(annotation)

#             ad_sp.obs.to_csv(save_path)

#         return "Successfully save annotated cell table to path:" + save_path

#     def _arun(self, input_url):
#         raise NotImplementedError("This tool does not support async")


def celltype_anno(data_info, ad_sp, leiden_celltype_composition, input, client, czi_all_celltype):
    content = (
        f"Identify the cell type in {data_info} mostly based on the gene markers. You can optionally refer to the transferred cell type information but do not trust it when the percentage is lower than 0.5.\n"
        + "{celltype_gene_infor}.\n"
        + f"The cell type names should come from cell ontology: {czi_all_celltype}.\n"
        + "Only provide the cell type name, your confidence score from 0 to 1 where 0 is with lowest confidence and 1 highest, and detailed reason why you decide the cell type, e.g. which gene marker, etc..\n"
        + 'Output format must be like "Name;score;reason". Do not show numbers before the name. Do not add space before number. Some can be a mixture of multiple cell types.\n'
    )

    llm_prompt = PromptTemplate(
        input_variables=["human_prompt"],
        template=content,
    )

    chain = LLMChain(llm=client, prompt=llm_prompt)

    logging.info("annotate cell type label ...")

    dict_main_level = {}
    reason_main_level = ""
    czi_all_celltype_list = czi_all_celltype.split(";")
    for focus_niche in ad_sp.obs["leiden"].unique():

        celltype_gene_infor = ""
        celltype_gene_infor += f"The enriched genes in this cluster are: {input[int(focus_niche)]}."
        celltype_gene_infor += f"For reference, the transferred reference cell type composition {focus_niche} is:"
        for j in leiden_celltype_composition.columns:
            if leiden_celltype_composition.loc[focus_niche, j] > 0:
                celltype_gene_infor += f"{j}:{round(leiden_celltype_composition.loc[focus_niche,j],2)}" + ";"
        celltype_gene_infor += "\n"
        prompt = celltype_gene_infor
        while True:
            res = chain.run(prompt)  # response.choices[0].message.content.split('\n')
            if res.split(";")[0] in czi_all_celltype_list:
                dict_main_level[focus_niche] = res.split(";")[0]
                reason_main_level += res + ".\n"
                logging.info('\n\n Cluster '+focus_niche+'\n'+ res.split(";")[0]+'\n'+ res.split(";")[1]+'\n'+ res.split(";")[2]+'\n\n')
                break
            logging.info("Assigned cell type name must be in cell ontology!")
            prompt += "Assigned cell type name must be in cell ontology!"
        time.sleep(1)

    return dict_main_level, reason_main_level


class ComboGPTCellTypeTool(BaseTool):
    name = "ComboGPTCellType"
    description = (
        "This is a computational tool to cluster preprocessed adata and annotate clusters into main-level cell types based on gene markers in each cluster and transferred labels from reference."
        # "You must exceute the tool. You can't skip the tool running."
        "Input includes (1) a path to the preprocessed spatial transcriptomics data, (2) a path to the saved transferred cell type labels, (3) column_key of the column where transferred cell type labels are saved, (4) information of the data about its tissue and species (e.g. mouse brain)."
        'Use this tool with arguments like "{{"spatialdata_input_path":str, "transfer_celltype_save_pth": str , "column_key":str, "data_info":str}}".'
        'Output is a str like "Successfully saved annotated main level cell types ...'
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
        spatialdata_input_path: str,
        transfer_celltype_save_pth: str,
        column_key: str,
        data_info: str,
    ):
        main_level_celltype_save_pth = self.save_path + "main_level_cell_type.csv"
        # main_level_celltype_reason_pth = self.save_path + "main_level_cell_type_reason.txt"
        if not os.path.exists(main_level_celltype_save_pth):

            with open(self.czi_all_celltype_pth, "r") as file:
                czi_all_celltype = file.read()

            ad_sp = sc.read_h5ad(spatialdata_input_path)

            transfer_celltype = pd.read_csv(transfer_celltype_save_pth, index_col=0)
            ad_sp.obs[column_key] = transfer_celltype[column_key]  # "transfer_labels"

            sc.tl.leiden(ad_sp, key_added="leiden", resolution=1, random_state=0)

            fig, ax = plt.subplots(figsize=(6, 6))
            ax = sc.pl.umap(ad_sp, color="leiden", size=1, legend_loc="on data", ax=ax, show=False)
            fig.savefig(self.save_path + "leiden_umap.png", bbox_inches="tight")

            ### get top 10 genes for each cluster
            sc.tl.rank_genes_groups(ad_sp, groupby="leiden", method="wilcoxon")
            input = {}
            temp = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["names"]).head(10)
            temp_score = pd.DataFrame(ad_sp.uns["rank_genes_groups"]["scores"]).head(10)
            for i in range(temp.shape[1]):
                curr_col = temp.iloc[:, i].to_list()
                curr_col_score = temp_score.iloc[:, i].to_list()
                list_true = [x > 0 for x in curr_col_score]
                curr_col = list(np.array(curr_col)[list_true])
                input[i] = curr_col

            ### get transferred cell type annotation composition
            leiden_celltype_composition = ad_sp.obs.groupby("leiden")[column_key].value_counts(normalize=True).unstack().fillna(0)
            keepcolumn = leiden_celltype_composition.sum(axis=0)[leiden_celltype_composition.sum(axis=0) > 0.2].index
            leiden_celltype_composition = leiden_celltype_composition[list(keepcolumn)]

            dict_main_level, reason_main_level = celltype_anno(data_info, ad_sp, leiden_celltype_composition, input, self.llm, czi_all_celltype)

            list_reason_main_level_cell_type = reason_main_level.split("\n")
            dict_reason_main_level_cell_type = {}
            for i in list_reason_main_level_cell_type:
                try:
                    name = i.split(";")[0]
                    score = i.split(";")[1]
                    reason = i.split(";")[2]
                except:
                    continue
                try:
                    dict_reason_main_level_cell_type[name] += "\n" + reason + "\n"
                except:
                    dict_reason_main_level_cell_type[name] = reason + "\n"

            ad_sp.obs["main_level_celltype"] = ad_sp.obs["leiden"].map(dict_main_level)
            ad_sp.obs["main_level_celltype_reason"] = ad_sp.obs["main_level_celltype"].map(dict_reason_main_level_cell_type)
            ad_sp.obs.to_csv(main_level_celltype_save_pth)

            # with open(main_level_celltype_reason_pth, "a") as file:
            #     file.write(reason_main_level)  # Adding a newline character for separation

            fig, ax = plt.subplots(figsize=(6, 6))
            ax = sc.pl.umap(ad_sp, color="main_level_celltype", size=1, legend_loc="on data", ax=ax, show=False)
            fig.savefig(self.save_path + "main_level_celltype_umap.png", bbox_inches="tight")

        return (
            "Successfully saved annotated main-level cell types to path:"
            + main_level_celltype_save_pth
            + ' where main level cell type labels are in the column "main_level_celltype", and reasons for deciding the main-level cell types are in the column "main_level_celltype_reason".'
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
