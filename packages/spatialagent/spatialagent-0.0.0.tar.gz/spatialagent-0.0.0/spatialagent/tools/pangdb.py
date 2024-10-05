import os, pandas as pd, numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from langchain.tools import BaseTool
from langchain.base_language import BaseLanguageModel


def get_embeddings(embeddings, texts):
    response = embeddings.embed_documents(texts)
    return np.array(response)


def find_most_similar(embeddings, query, descriptions):
    # Get embeddings for the query and all descriptions
    embeddings = get_embeddings(embeddings, query + descriptions)
    query_embedding = embeddings[: len(query)]
    description_embeddings = embeddings[len(query) :]

    # Calculate cosine similarity
    pangdb_matched_cell_type_name = []
    for i in range(len(query)):
        similarities = cosine_similarity([query_embedding[i]], description_embeddings)[0]

        # Find the index of the most similar description
        most_similar_index = np.argmax(similarities)
        print(
            query[i],
            "----->",
            descriptions[most_similar_index],
            similarities[most_similar_index],
        )
        pangdb_matched_cell_type_name.append(descriptions[most_similar_index])
    return pangdb_matched_cell_type_name


class PangDBSEARCHTool(BaseTool):
    name = "SearchPangDBMarker"
    description = (
        "For each cell types identified in a study of a tissue or organ in human or mouse, this tool searches for marker genes of each cell type in the Pang database."
        "Input is the path to the folder where the reference data is saved, the organism of target cell types: from human (Hs) or mouse (Mm), and the tissue of target cell types: e.g. brain, liver, Pancreas, Vasculature. iter_round as current iteration round,"
        'Output is a str like "Successfully saved ..."'
    )
    embeddings: BaseLanguageModel = None

    desired_path: str = None

    def __init__(self, embeddings, desired_path):
        super().__init__()
        self.embeddings = embeddings
        self.desired_path = desired_path
        # self.df=pd.read_csv(dataPath)
        # self.

    def _run(self, file_folder, organism_key, tissue_key, iter_round):
        save_csv = file_folder + f"read_pangdb_celltype_{iter_round}.csv"

        if not os.path.exists(save_csv):
            df_czi = pd.read_csv(file_folder + f"read_czi_reference_celltype_{iter_round}.csv")
            df_panglab = pd.read_csv(self.desired_path + "/data/PanglaoDB_markers_27_Mar_2020.csv")
            df_panglab = df_panglab[df_panglab["species"].str.contains(organism_key, na=False)]

            df_czi["description_all"] = organism_key + " " + df_czi["cell_type"].astype("str") + " " + tissue_key
            czi_unique_celltypes = df_czi["cell_type"].unique()

            df_panglab["description_all"] = df_panglab["species"].astype("str") + " " + df_panglab["cell type"].astype("str") + " " + df_panglab["organ"].astype("str")
            pang_unique_celltypes = df_panglab["description_all"].unique()

            # Example usage
            descriptions = list(pang_unique_celltypes)
            query = list(czi_unique_celltypes)

            pangdb_matched_cell_type_name = find_most_similar(self.embeddings, query, descriptions)

            dic_cell_gene = {
                "cell_type_czi": [],
                "cell_type_pangdb": [],
                "marker_genes": [],
            }
            for i, j in zip(query, pangdb_matched_cell_type_name):
                dic_cell_gene["cell_type_czi"].append(i)
                dic_cell_gene["cell_type_pangdb"].append(j)
                dic_cell_gene["marker_genes"].append(df_panglab.loc[df_panglab["description_all"] == j, "official gene symbol"].tolist())

            dic_cell_gene = pd.DataFrame(dic_cell_gene)
            dic_cell_gene.to_csv(save_csv)
        else:
            print("Pang db data already exist!")

        output = "Successfully saved the matched cell types and marker genes in the PangDB to the file folder."
        print(output)
        return output
