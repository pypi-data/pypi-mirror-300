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

warnings.simplefilter(action="ignore", category=FutureWarning)
import matplotlib.pyplot as plt
from utag import utag
from langchain.tools import BaseTool
import pandas as pd
import scanpy.external as sce

import numpy as np
from scipy.spatial import KDTree
from collections import Counter

import os, pandas as pd, numpy as np, scanpy as sc
from langchain.tools import BaseTool

import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.stats import mode
from collections import Counter
from pathlib import Path


def fun_rmv_smallcluster(ad_toassign, ad_label, label_key):
    # Sample data
    array1 = ad_toassign.obsm["spatial"]
    array2 = ad_label.obsm["spatial"]
    labels2 = np.array(ad_label.obs[label_key])

    # Initialize the Nearest Neighbors model
    nbrs = NearestNeighbors(n_neighbors=5, algorithm="auto").fit(array2)

    # Find the 5 nearest neighbors for each sample in array1
    _, indices = nbrs.kneighbors(array1)

    # Assign the most frequent label from the neighbors
    assigned_labels = []
    for i in range(array1.shape[0]):
        neighbor_labels = labels2[indices[i]]
        most_frequent_label = Counter(neighbor_labels).most_common(1)[0][0]
        assigned_labels.append(most_frequent_label)

    assigned_labels = np.array(assigned_labels)
    return assigned_labels


def rmv_smallcluster_utag_label(utag_results, label_key, batch_key):
    small_cluster = list(utag_results.obs[label_key].value_counts()[utag_results.obs[label_key].value_counts() < 100].index)
    for batch_i in utag_results.obs[batch_key].unique():
        utag_results_batch = utag_results[utag_results.obs[batch_key] == batch_i]
        ad_toassign = utag_results_batch[utag_results_batch.obs[label_key].isin(small_cluster)]
        ad_label = utag_results_batch[~utag_results_batch.obs[label_key].isin(small_cluster)]

        if ad_toassign.shape[0] != 0:
            if ad_label.shape[0] > 0:
                assigned_labels = fun_rmv_smallcluster(ad_toassign, ad_label, label_key)

                utag_results_batch.obs.loc[utag_results_batch.obs[label_key].isin(small_cluster), label_key] = assigned_labels

                utag_results_batch.obs[label_key] = utag_results_batch.obs[label_key].astype("str")
                utag_results.obs.loc[utag_results.obs[batch_key] == batch_i, label_key] = utag_results_batch.obs[label_key]
            else:
                utag_results.obs[label_key] = "0"
    return utag_results


def utag_compute(ad_sp, batch_key, ref_save_path):
    ### Estimate the distance threshold for UTAG
    ad_onesample = ad_sp[ad_sp.obs[batch_key] == ad_sp.obs[batch_key].unique()[0]]
    cells = ad_onesample[np.random.permutation(ad_onesample.shape[0])[:10000]].obsm["spatial"]
    for distance_threshold in range(10, 1000, 5):
        # Compute the pairwise Euclidean distance matrix
        distance_matrix = np.sqrt(np.sum((cells[:, np.newaxis, :] - cells[np.newaxis, :, :]) ** 2, axis=2))
        counts_within_distance = np.sum(distance_matrix < distance_threshold, axis=1) - 1
        # Calculate the average number of cells within the specified distance
        average_count = np.mean(counts_within_distance)
        # utag_results.obs['UTAG Label_leiden_0.1'].unique()
        if average_count > 3:
            break

    ### Run UTAG on provided data
    for resolution in np.arange(0.05, 0.5, 0.05):
        utag_results = utag(
            ad_sp, slide_key=batch_key, max_dist=distance_threshold, normalization_mode="l1_norm", apply_clustering=True, clustering_method="leiden", resolutions=[resolution]
        )
        if utag_results.obs["UTAG Label_leiden_" + str(resolution)].nunique() > 2:
            utag_results = rmv_smallcluster_utag_label(utag_results, "UTAG Label_leiden_" + str(resolution), batch_key)
            utag_results.obs["utag"] = utag_results.obs["UTAG Label_leiden_" + str(resolution)]
            utag_results.write_h5ad(ref_save_path)
            break
    return utag_results


class MainUTAGTool(BaseTool):
    name = "MainUTAG"
    description = (
        "This is a computational tool to find main-level spatial neighborhood expression coherent clusters using a computational method UTAG."
        "Input includes a path to the spatial transcriptomics data after preprocessing, a path to the annotated main level cell type labels, column_key of the column where annotated main level cell type labels are in, and batch_key where the sample names are in in spatial transcriptomics data."
        'Use this tool with arguments like "{{"spatial_processed_input_url":str, "main_level_celltype_url":str,"main_level_celltype_key":str,"batch_key":str}}".'
        'Output is a str like "Successfully save main-level utag results of tissue niches clusters to path ..." where main-level utag results of tissue niches clusters are in the column "main_level_tissueniche_utag".'
    )
    save_path: str = None

    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path

    def _run(self, spatial_processed_input_url: float, main_level_celltype_url: str, main_level_celltype_key: str, batch_key: str):
        utag_save_path = self.save_path + "main_level_utag_results.h5ad"
        csv_save_path = self.save_path + "main_level_tissueniche_utag.csv"
        if not os.path.exists(csv_save_path):
            ### Read the reference data
            ad_sp = sc.read_h5ad(spatial_processed_input_url)
            pd_celltype = pd.read_csv(main_level_celltype_url)
            ad_sp.obs[main_level_celltype_key] = list(pd_celltype[main_level_celltype_key])

            if not os.path.exists(utag_save_path):
                utag_results = utag_compute(ad_sp, batch_key, utag_save_path)
            else:
                utag_results = sc.read_h5ad(utag_save_path)

            ad_sp.obs["main_level_tissueniche_utag"] = list(utag_results.obs.loc[ad_sp.obs.index, "utag"])
            ad_sp.obs.to_csv(csv_save_path)

        return (
            "Successfully save main-level utag results of tissue niches clusters to path:"
            + csv_save_path
            + ', where main-level utag results of tissue niches clusters are in the column "main_level_tissueniche_utag".'
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")


class SubUTAGTool(BaseTool):
    name = "SubUTAG"
    description = (
        "This is a computational tool to find sub-level spatial neighborhood expression coherent clusters using a computational method UTAG."
        "Input includes (1) a path to the spatial transcriptomics data after preprocessing, "
        "(2) a path to saved annotated sub-level cell types table, "
        "(3) batch_key of the column where batches or samples labels are in, "
        # "(4) column_key of the column where annotated main level cell type labels are in, "
        "(4) and main-level tissue niche column key."
        'Use this tool with arguments like "{{"spatial_processed_input_url":str, "sub_level_celltype_url":str,"batch_key":str,"main_level_tissue_cluster_key":str}}".'
        'Output is a str like "Successfully save sub-level utag results of tissue niches clusters to path ..." where 。。。'
    )
    save_path: str = None

    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path

    def _run(self, 
             spatial_processed_input_url: str, 
             sub_level_celltype_url: str, 
             batch_key: str, 
             main_level_tissue_cluster_key: str):
        Path(self.save_path + "/ad_sub_tissueniche").mkdir(parents=True, exist_ok=True)
        csv_save_path = self.save_path + "/ad_sub_tissueniche/" + "sub_level_tissueniche_utag.csv"

        if not os.path.exists(csv_save_path):
            ### Read the reference data
            ad_all = sc.read_h5ad(spatial_processed_input_url)
            pd_celltype = pd.read_csv(sub_level_celltype_url, index_col=0)
            ad_all.obs = pd_celltype
            ad_all.obs["sub_level_tissueniche_utag"] = "-1"
            unique_main_tissue_region = ad_all.obs[main_level_tissue_cluster_key].unique()

            for unique_main_tissue_region_i in unique_main_tissue_region:
                ad_sp = ad_all[ad_all.obs[main_level_tissue_cluster_key] == unique_main_tissue_region_i]

                h5ad_savepath = self.save_path + "/ad_sub_tissueniche/" + f"ad_sub_utag_{unique_main_tissue_region_i}.h5ad"

                if not os.path.exists(h5ad_savepath):
                    utag_results = utag_compute(ad_sp, batch_key, h5ad_savepath)
                else:
                    utag_results = sc.read_h5ad(h5ad_savepath)

                ad_sp.obs["sub_level_tissueniche_utag"] = list(utag_results.obs.loc[ad_sp.obs.index, "utag"])
                ad_all.obs.loc[ad_all.obs[main_level_tissue_cluster_key] == unique_main_tissue_region_i, "sub_level_tissueniche_utag"] = list(ad_sp.obs["sub_level_tissueniche_utag"])

                # Plot spatial embedding
                ad_sp.obsm["spatial"][ad_sp.obs["sample_id"] == "R77_4C4", 0] = ad_sp.obsm["spatial"][ad_sp.obs["sample_id"] == "R77_4C4", 0] - 8000
                ad_sp.obsm["spatial"][ad_sp.obs["sample_id"] == "R78_4C15", 0] = ad_sp.obsm["spatial"][ad_sp.obs["sample_id"] == "R78_4C15", 0] + 4000
                fig, ax = plt.subplots(figsize=(15, 8))
                plt.style.use("dark_background")
                ax = sc.pl.embedding(ad_sp, basis="spatial", color="sub_level_tissueniche_utag", palette="tab20", size=5, ax=ax, show=False)
                fig.savefig(self.save_path + "/ad_sub_tissueniche/" + f"plot_all_{unique_main_tissue_region_i}.png", bbox_inches="tight")

            # # Plot spatial embedding
            # ad_all.obsm["spatial"][ad_all.obs["sample_id"] == "R77_4C4", 0] = (
            # ad_all.obsm["spatial"][ad_all.obs["sample_id"] == "R77_4C4", 0] - 8000
            # )
            # ad_all.obsm["spatial"][ad_all.obs["sample_id"] == "R78_4C15", 0] = (
            # ad_all.obsm["spatial"][ad_all.obs["sample_id"] == "R78_4C15", 0] + 4000
            #     )
            # fig, ax = plt.subplots(figsize=(15,8))
            # plt.style.use("dark_background")
            # ax = sc.pl.embedding(ad_all, basis="spatial", color="sub_level_tissueniche_utag", palette='tab20',size=5, ax=ax, show=False)
            # fig.savefig(self.save_path  + "/ad_sub_tissueniche/" + f"plot_all.png",bbox_inches='tight')

            ad_all.obs.to_csv(csv_save_path)

        return (
            "Successfully save sub-level utag results of tissue niches clusters to path:"
            + csv_save_path
            + ', where sub-level utag results of tissue niches clusters are in the column "sub_level_tissueniche_utag".'
        )

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
