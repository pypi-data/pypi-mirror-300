import os, scanpy as sc
from langchain.tools import BaseTool


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


class ScanpyPreprocessTool(BaseTool):
    name = "ScanpyPreprocess"
    description = (
        "This is a computational tool to preprocess spatial transcriptomics data using Scanpy."
        "Input is the path to the raw spatial transcriptomics data."
        'Use this tool with arguments like "{{"spatialdata_input_path":str}}".'
        "Output is a str like 'Successfully saved preprocessed data to path'."
    )
    save_path: str = None

    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path

    def _run(self, spatialdata_input_path: str):
        preprocess_data_save_path = self.save_path + "preprocessed.h5ad"

        if not os.path.exists(preprocess_data_save_path):
            result = scanpy_preprocess(spatialdata_input_path, preprocess_data_save_path)
        else:
            result = True
        if result:
            return "Successfully saved preprocessed data at: " + preprocess_data_save_path
        else:
            return "Failed to save preprocessed data at: " + preprocess_data_save_path

    def _arun(self, input_url):
        raise NotImplementedError("This tool does not support async")
