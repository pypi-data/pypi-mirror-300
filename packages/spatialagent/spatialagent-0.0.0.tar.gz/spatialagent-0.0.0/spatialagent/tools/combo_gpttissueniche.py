import scanpy as sc
import matplotlib.pyplot as plt
import numpy as np
import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
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

warnings.simplefilter(action="ignore", category=FutureWarning)

# from IPython.display import Image, display, Audio, Markdown
import base64
import matplotlib.pyplot as plt


# Open the image file and encode it as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def gpt_tissue_vision(ad_toano, tissue_cluster_key, focus_niche, data_info, image_path, llm, save_path):
    print("annotate niche label ...")
    dict_niche = {}

    plt.ioff()
    scale = (max(ad_toano.obsm["spatial"][:, 0]) - min(ad_toano.obsm["spatial"][:, 0])) / (max(ad_toano.obsm["spatial"][:, 1]) - min(ad_toano.obsm["spatial"][:, 1]))
    plt.figure(figsize=(5, 5 / scale))
    plt.scatter(ad_toano.obsm["spatial"][:, 0], ad_toano.obsm["spatial"][:, 1], s=0.1, c="lightgrey")
    plt.scatter(
        ad_toano.obsm["spatial"][ad_toano.obs[tissue_cluster_key] == focus_niche, 0],
        ad_toano.obsm["spatial"][ad_toano.obs[tissue_cluster_key] == focus_niche, 1],
        s=0.1,
        c="r",
    )
    plt.axis("off")
    plt.savefig(save_path + "/zone_cluster_0.png", bbox_inches="tight")
    plt.close()

    base64_image = encode_image(image_path)

    image_path1 = save_path + "/zone_cluster_0.png"
    base64_image1 = encode_image(image_path1)

    messages = [
        {"role": "system", "content": f"You are a expert in {data_info}."},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "You need to describe the anatomic regions in the first image and red molecular region niche in the second image based on following information."
                        "The first image shows locations of anatomical tissue regions of the tissue."  # One anatomical region may correspond to multiple molecular regions. Molecular regions may be subregions of anatomical regions."
                        "First, describe the location of anatomical regions in the first image. e.g., Right ventricle: lower right; ..."
                        "Do not mistake the names with real location from the viewer's perspective. For example, 'Left xx' can be on the right side of the image."
                        "Second, describe the spatial location of the majority location of red molecular region niche in the second image in details, like upper left, upper middle, etc. Don't add other locations where have only a small part."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image1}"},
                },
            ],
        },
    ]

    ai_message = llm.invoke(messages)
    print(focus_niche, ai_message.content)
    return ai_message.content


def gpt_tissue_all(focus_niche, response_location, llm, data_info, czi_all_tissueniche, region_gene_list, region_celltype_composition):
    print("annotate niche label ...")
    celltype_gene_infor = ""
    celltype_gene_infor += f"The main-level cell type composition in niche {focus_niche} is:"
    for j in region_celltype_composition.columns:
        if region_celltype_composition.loc[focus_niche, j] > 0:
            celltype_gene_infor += f"{j}:{round(region_celltype_composition.loc[focus_niche,j],2)}" + ";"
    celltype_gene_infor += f"The enriched genes in this niche are: {region_gene_list[int(focus_niche)]} \n"

    prev_info = response_location

    messages = [
        {"role": "system", "content": f"You are a expert in {data_info}."},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "You need to decide the name of the red molecular region niche in the second image based on following information."
                        f"{prev_info}"
                        "Additional information of cell types and enriched genes in this niche are:{celltype_gene_infor}."
                        "Based on previous location description and additional information, reason the most possible tissue niche name of the red region."
                        # f"The tissue niche names should come from possible tissues: {czi_all_tissueniche}.\n"
                        "You must output the tissue niche name of the red molecular region niche in the second image in the format: 'Name:...;Score:...;Reason:...'. Do not add space between the colon and the name or elsewhere. Don't add other information after it. Score is your confidence score from 0 to 1 where 0 is with lowest confidence and 1 highest, and reason is reason why you decide the name from multimodal information.\n"
                        # "If you are not sure about the decision, additional information of cell types and enriched genes in this niche are:{celltype_gene_infor}."
                        # "Output should only be the molecular region niche name like: 'Name'. Don't output other information."
                    ),
                },
            ],
        },
    ]

    ai_message = llm.invoke(messages)
    print(focus_niche, ai_message.content)
    # dict_niche[focus_niche]=ai_message.content
    Name_response, Score_response, Reason_response = ai_message.content.split(";")
    Name_response = Name_response.split("Name:")[1]
    Score_response = Score_response.split("Score:")[1]
    Reason_response = Reason_response.split("Reason:")[1]
    return Name_response, Score_response, Reason_response


def merge_dicts(original_dict):
    merged_dict = {}

    for main_key, sub_dict in original_dict.items():
        for sub_key, sub_value in sub_dict.items():
            if sub_key not in merged_dict:
                merged_dict[sub_key] = set()
            merged_dict[sub_key].add(sub_value)

    # Convert sets to the desired string format
    for sub_key in merged_dict:
        unique_values = merged_dict[sub_key]
        merged_dict[sub_key] = " or ".join(sorted(unique_values))

    return merged_dict


class ComboGPTTissueNicheTool(BaseTool):
    name = "ComboGPTTissueNiche"
    description = (
        "This is a computational tool to annotate main-level tissue niches based on multimodal information."
        # "You must exceute the tool. You can't skip the tool running."
        "Input includes (1)a path to the spatial transcriptomics data after preprocessing,"
        "(2)a path to the annotated main level cell type labels,"
        "(3)column_key of the column where annotated main level cell type labels are in,"
        "(4)column_key of the column where reason for annotated main level cell type labels are in,"
        "(5)a path to the main-level utag results of tissue niches clusters,"
        "(6)column_key of the column where main-level utag results of tissue niches clusters are in,"
        "(7)batch_key where the sample names are in in spatial transcriptomics data,"
        "(8)information of the data about its tissue and species (e.g. mouse brain),"
        "and (9) a path to saved possible tissues."
        'Use this tool with arguments like "{{"spatial_processed_input_url":str, "main_level_celltype_url": str , "main_level_celltype_key":str, "main_level_celltype_reason_key":str,"main_level_utag_url":str, "main_level_utag_key":str,"batch_key":str,"data_info":str,"possible_tissue_path":str}}".'
        'Output is a str like "Successfully save a main-level combined table with both cell type and tissue niche labels to path ..." '
    )
    llm: BaseLanguageModel = None
    llm_4o: BaseLanguageModel = None
    save_path: str = None
    acaimage_path: str = None

    def __init__(self, llm, llm_4o, save_path, acaimage_path):
        super().__init__()
        self.llm = llm
        self.llm_4o = llm_4o
        self.save_path = save_path
        self.acaimage_path = acaimage_path

    def _run(self, spatial_processed_input_url, main_level_celltype_url, main_level_celltype_key, main_level_celltype_reason_key, main_level_utag_url, main_level_utag_key, batch_key, data_info, possible_tissue_path):
        tissueniche_save_path = self.save_path + "main_level_all.csv"
        # tissueniche_reason_save_path = self.save_path + "main_level_tissue_niche_reason.pkl"
        if not os.path.exists(tissueniche_save_path):

            with open(possible_tissue_path, "r") as file:
                czi_all_tissueniche = file.read()

            ad_sp = sc.read_h5ad(spatial_processed_input_url)
            pd_celltype = pd.read_csv(main_level_celltype_url)
            ad_sp.obs[main_level_celltype_key] = list(pd_celltype[main_level_celltype_key])
            ad_sp.obs[main_level_celltype_reason_key] = list(pd_celltype[main_level_celltype_reason_key])
            pd_utag = pd.read_csv(main_level_utag_url)
            ad_sp.obs[main_level_utag_key] = list(pd_utag[main_level_utag_key])
            ad_sp.obs[main_level_utag_key] = ad_sp.obs[main_level_utag_key].astype("str")

            sampleid_all = ad_sp.obs[batch_key].unique()
            if not os.path.exists(self.save_path + "combo_tissueniche_dict_niche_all.json"):

                dict_niche_all = {}
                dict_reason_all = {}
                for sampleid_i in sampleid_all:
                    print("---------------- Sample ", sampleid_i, "----------------")
                    ad_toano = ad_sp[ad_sp.obs[batch_key] == sampleid_i]
                    print("compute enriched genes ...")
                    ad_toano.obs[main_level_utag_key] = ad_toano.obs[main_level_utag_key].astype("str")
                    sc.tl.rank_genes_groups(ad_toano, groupby=main_level_utag_key, method="wilcoxon")
                    region_gene_list = {}
                    temp = pd.DataFrame(ad_toano.uns["rank_genes_groups"]["names"]).head(10)
                    temp_score = pd.DataFrame(ad_toano.uns["rank_genes_groups"]["scores"]).head(10)
                    for i in range(temp.shape[1]):
                        curr_col = temp.iloc[:, i].to_list()
                        curr_col_score = temp_score.iloc[:, i].to_list()
                        list_true = [x > 0 for x in curr_col_score]
                        curr_col = list(np.array(curr_col)[list_true])
                        region_gene_list[i] = curr_col

                    print("compute cell type compositions ...")
                    region_celltype_composition = ad_toano.obs.groupby(main_level_utag_key)[main_level_celltype_key].value_counts(normalize=True).unstack().fillna(0)

                    all_niche = ad_toano.obs[main_level_utag_key].unique()
                    response_dic = {}
                    score_dic = {}
                    reason_dic = {}
                    for focus_niche in all_niche:
                        print(focus_niche)

                        response_location = gpt_tissue_vision(ad_toano, main_level_utag_key, focus_niche, data_info, self.acaimage_path, self.llm_4o, self.save_path)

                        Name_response, Score_response, Reason_response = gpt_tissue_all(
                            focus_niche, response_location, self.llm, data_info, czi_all_tissueniche, region_gene_list, region_celltype_composition
                        )
                        response_dic[focus_niche] = Name_response
                        score_dic[focus_niche] = Score_response
                        reason_dic[focus_niche] = Reason_response
                        print("\n\n\n")

                    dict_niche_all[sampleid_i] = response_dic
                    dict_reason_all[sampleid_i] = reason_dic

                with open(self.save_path + "combo_tissueniche_dict_niche_all.json", "w") as json_file:
                    json.dump(dict_niche_all, json_file)
                with open(self.save_path + "combo_tissueniche_dict_reason_all.json", "w") as json_file:
                    json.dump(dict_reason_all, json_file)
            else:
                with open(self.save_path + "combo_tissueniche_dict_niche_all.json", "r") as json_file:
                    dict_niche_all = json.load(json_file)
                with open(self.save_path + "combo_tissueniche_dict_reason_all.json", "r") as json_file:
                    dict_reason_all = json.load(json_file)

            ### save reason as pickle
            # merged_dict_reason = {}
            # for i in dict_reason_all.keys():
            #     # print(i)
            #     for j in dict_reason_all[i].keys():
            #         try:
            #             merged_dict_reason[merged_dict[j]] += i + ":" + dict_reason_all[i][j] + "\n"
            #         except:
            #             merged_dict_reason[merged_dict[j]] = i + ":" + dict_reason_all[i][j] + "\n"
            list_leiden_reason={}
            for i in ad_sp.obs[main_level_utag_key].unique():
                list_leiden_reason[i]=''
                for key_i in dict_reason_all.keys():
                    if i in dict_reason_all[key_i].keys():
                        list_leiden_reason[i]+=key_i+': '
                        list_leiden_reason[i]+=dict_reason_all[key_i][i]+'\n'
            ad_sp.obs["main_level_tissueniche_reason"] = ad_sp.obs[main_level_utag_key].map(list_leiden_reason)


            merged_dict = merge_dicts(dict_niche_all)
            for key_i, value_i in zip(merged_dict.keys(), merged_dict.values()):
                merged_dict[key_i] = key_i + "-" + value_i

            ad_sp.obs[main_level_utag_key] = ad_sp.obs[main_level_utag_key].map(merged_dict)
            ad_sp.obs["main_level_tissueniche"] = ad_sp.obs[main_level_utag_key].copy()

            ad_sp.obs = ad_sp.obs.drop(main_level_utag_key, axis=1)
            ad_sp.obs.to_csv(tissueniche_save_path)

            ### plot spatial distribution
            for sampleid_i in sampleid_all:
                print("---------------- Sample ", sampleid_i, "----------------")
                ad_toano = ad_sp[ad_sp.obs[batch_key] == sampleid_i]
                fig, ax = plt.subplots(figsize=(6, 6))
                ax = sc.pl.embedding(ad_toano, basis="spatial", color="main_level_tissueniche", size=10, ax=ax, show=False)
                fig.savefig(self.save_path + f"main_level_tissueniche_{sampleid_i}.png", bbox_inches="tight")

        return (
            "Successfully save a main-level combined table with both cell type and tissue niche labels to path:"
            + tissueniche_save_path
            + ", where main-level cell type labels are"
            + " in column 'main_level_celltype' and main-level tissue niche labels are in column 'main_level_tissueniche'."
            + " and reason for deciding main-level tissue niches are in the column 'main_level_tissueniche_reason'."
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
