from langchain.tools import BaseTool
import scanpy as sc
import numpy as np
import pandas as pd
import scanpy.external as sce

import numpy as np
import os, pandas as pd, numpy as np, scanpy as sc
from langchain.tools import BaseTool
from sklearn.neural_network import MLPClassifier


def subset_adata(adata, sample_size):
    df = adata.obs

    # Calculate the number of samples to select for each cell type
    cell_type_counts = df["cell_type"].value_counts()
    scale = sample_size / sum(cell_type_counts)
    samples_per_cell_type = (cell_type_counts * scale).astype(int)

    # Sample cells for each cell type
    sampled_df_list = []
    for cell_type, count in samples_per_cell_type.items():
        cell_type_df = df[df["cell_type"] == cell_type]
        sampled_df = cell_type_df.sample(n=count, random_state=42)  # Set a random_state for reproducibility
        sampled_df_list.append(sampled_df)

    # Combine all sampled DataFrames
    sampled_df = pd.concat(sampled_df_list)

    return adata[sampled_df.index]


def harmony_fun(rawdata_path: str, ref_save_path: str, save_path: str, dataset_id_ind: int):
    np.random.seed(0)

    combine_save_pth = save_path + f"combine_adata_{dataset_id_ind}.h5ad"
    if not os.path.exists(combine_save_pth):
        ad_sp = sc.read_h5ad(rawdata_path)

        sc.pp.scale(ad_sp)
        ad_sp.var.index = ad_sp.var.index.str.upper()

        ad_sc = sc.read_h5ad(ref_save_path)
        if ad_sp.shape[0] < ad_sc.shape[0]:
            ad_sc = subset_adata(ad_sc, ad_sp.shape[0])
        ad_sc.var.index = ad_sc.var["feature_name"].str.upper()
        ad_sc.var_names_make_unique()

        list_of_variable_names = ad_sp.var.index.intersection(ad_sc.var.index)
        adata_subset = ad_sp[:, list_of_variable_names]

        list_of_variable_names = ad_sc.var.index.intersection(ad_sp.var.index)
        adata_sc_subset = ad_sc[:, list_of_variable_names]

        # Normalization scaling sc
        sc.pp.normalize_total(adata_sc_subset)
        sc.pp.log1p(adata_sc_subset)

        # Scale data to unit variance and zero mean
        sc.pp.scale(adata_sc_subset)

        combine_adata = adata_subset.concatenate(adata_sc_subset, batch_key="dataset", batch_categories=["st", "scrna"])
        sc.tl.pca(combine_adata, n_comps=30)
        sce.pp.harmony_integrate(combine_adata, "dataset")

        # sc.pp.neighbors(combine_adata, n_neighbors=50, use_rep="X_pca_harmony")
        # sc.tl.umap(combine_adata)

        # fig,ax = plt.subplots(figsize=(6,6))
        # ax = sc.pl.umap(combine_adata, color="dataset", size=1, ax= ax, show=False)
        # fig.savefig(save_path + f"combine_adata_{dataset_id_ind}_leiden_umap.png")

        combine_adata.write_h5ad(combine_save_pth)

    ### transfer via knn
    # transfer_celltype_save_pth = save_path + f"reference_transfer_{dataset_id_ind}.csv"
    # if not os.path.exists(transfer_celltype_save_pth):
    #     combine_adata = sc.read_h5ad(combine_save_pth)
    #     combine_adata_st = combine_adata[combine_adata.obs["dataset"] == "st", :]
    #     combine_adata_scrna = combine_adata[combine_adata.obs["dataset"] == "scrna", :]

    #     # Example 2D arrays and labels
    #     nacell_location = combine_adata_st.obsm["X_pca_harmony"]
    #     sccell_location = combine_adata_scrna.obsm["X_pca_harmony"]
    #     labels = np.array(combine_adata_scrna.obs["cell_type"])  # Labels for each point in array2

    #     # Build KDTree for array2
    #     tree = KDTree(sccell_location)

    #     # Find the nearest 5 neighbors for each point in array1
    #     num_neighbors = 5
    #     nearest_neighbors = tree.query(nacell_location, k=num_neighbors)

    #     # Assign labels based on the most frequent label among the nearest neighbors
    #     assigned_labels = []

    #     for neighbors in nearest_neighbors[1]:
    #         # Find the labels of the nearest neighbors
    #         neighbor_labels = labels[neighbors]

    #         # Find the most frequent label
    #         most_common_label = Counter(neighbor_labels).most_common(1)[0][0]
    #         assigned_labels.append(most_common_label)

    #     # Convert assigned_labels to numpy array
    #     assigned_labels = np.array(assigned_labels)
    #     combine_adata_st.obs["transfer_labels"] = assigned_labels
    #     combine_adata_st.obs.index = combine_adata_st.obs.index.str.replace("-st", "")
    #     combine_adata_st.obs.to_csv(transfer_celltype_save_pth)

    ### transfer via MLP
    transfer_celltype_save_pth = save_path + f"reference_transfer.csv"
    if not os.path.exists(transfer_celltype_save_pth):
        combine_adata = sc.read_h5ad(combine_save_pth)
        combine_adata_st = combine_adata[combine_adata.obs["dataset"] == "st", :]
        combine_adata_scrna = combine_adata[combine_adata.obs["dataset"] == "scrna", :]

        # Example 2D arrays and labels
        nacell_location = combine_adata_st.obsm["X_pca_harmony"]
        sccell_location = combine_adata_scrna.obsm["X_pca_harmony"]
        labels = np.array(combine_adata_scrna.obs["cell_type"])  # Labels for each point in array2

        clf = MLPClassifier(random_state=1, max_iter=100).fit(sccell_location, labels)

        assigned_labels = clf.predict(nacell_location)

        combine_adata_st.obs["transfer_labels"] = assigned_labels
        combine_adata_st.obs.index = combine_adata_st.obs.index.str.replace("-st", "")
        combine_adata_st.obs.to_csv(transfer_celltype_save_pth)

    return transfer_celltype_save_pth


class HarmonyTransferTool(BaseTool):
    name = "HarmonyTransfer"
    description = (
        "This is a computational tool to transfer CZI reference dataset cell types to query data."
        # 'Input must be the (1-3) dataset id 1, 2, and 3 and (4) organism key of the CZI reference datasets and (5) the path to the preprocessed spatial transcriptomics data.'
        "Input must be the path to the preprocessed spatial transcriptomics data."
        # '"dataset_id" must be real dataset id and not be something like "Dataset ID from Step 1.1 output". The organism must be one of "Homo sapiens or "Mus musculus.'
        'The "preprocessed_adata_path" must be path to the preprocessed spatial transcriptomics data, not raw data.'
        # "Input is a path to the spatial transcriptomics data after preprocessing, resolution for leiden clustering, tissue where cells are from (e.g. brain), species where cells are from, e.g., human, mouse."
        'Use this tool with arguments like "{{ "preprocessed_adata_path":str}}".'
        'Output is a str like "Successfully save transferred cell type labels to path" where transferred cell type labels are in the column "transfer_labels".'
    )
    save_path: str = None

    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path

    def _run(self, preprocessed_adata_path: str):
        directory_path = self.save_path + "/czi_reference"
        file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        for dataset_id_ind, file_name in enumerate(file_names):
            transfer_celltype_save_pth = harmony_fun(preprocessed_adata_path, directory_path + "/" + file_name, self.save_path, dataset_id_ind)

        # ad_sp = sc.read_h5ad(preprocessed_adata_path)
        # for dataset_id_ind, _ in enumerate(file_names):
        #     transfer_celltype_save_pth = self.save_path + f"reference_transfer_{dataset_id_ind}.csv"
        #     transfer1 = pd.read_csv(transfer_celltype_save_pth, index_col=0)
        #     ad_sp.obs[f"transfer_labels"] = transfer1["transfer_labels"]

        # transfer_final_save_pth = self.save_path + "reference_transfer.csv"
        # ad_sp.obs.to_csv(transfer_final_save_pth)

        return "Successfully save transferred cell type labels to path:" + transfer_celltype_save_pth + 'where transferred cell type labels are saved in the column "transfer_labels".'

    def _arun(self):
        raise NotImplementedError("This tool does not support async")
