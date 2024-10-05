import os, pandas as pd, numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from langchain.tools import BaseTool
from langchain.base_language import BaseLanguageModel

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_experimental.tools import PythonAstREPLTool
# from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser


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


# panglaodb='/home/hey92/scratch/STAgent/data/PanglaoDB_markers_27_Mar_2020.csv'


class CellMarker2Tool(BaseTool):
    name = "SearchCellMarker2"
    description = (
        "For each cell types identified in a study of a tissue or organ in human or mouse, this tool searches for marker genes of each cell type in the Cell Marker 2 database."
        "Input is the path to the folder where the reference data is saved, the organism of target cell types: from human ('Human') or mouse ('Mouse'), the tissue of target cell types: e.g. brain, liver, Pancreas, Vasculature, the cell type: 'Normal cell' or 'Cancer cell', the number of target genes that user wanted, and iter_round as current iteration round,"
        'Output is a str like "Successfully saved ..."'
    )
    embeddings: BaseLanguageModel = None

    desired_path: str = None

    def __init__(self, embeddings, desired_path):
        super().__init__()
        self.embeddings = embeddings
        self.desired_path = desired_path

    def _run(self, file_folder, organism_key, tissue_key, cell_type, num_gene: int, iter_round):
        save_csv = file_folder + f"read_cellmarker2_celltype_{iter_round}.csv"

        if not os.path.exists(save_csv):
            df_czi = pd.read_csv(file_folder + f"read_czi_reference_celltype_{iter_round}.csv")

            # top_marker_genes = 10
            # if num_gene / df_czi.shape[0] > 10:
            #     top_marker_genes = int(num_gene / df_czi.shape[0]*2)

            df_cellmarker2 = pd.read_csv(self.desired_path + "/data/CellMarker2/Cell_marker_All.csv", index_col=0)
            df_cellmarker2 = df_cellmarker2[df_cellmarker2["species"].str.contains(organism_key, na=False)]

            df_czi["description_all"] = organism_key + " " + cell_type + " " + df_czi["cell_type"].astype("str") + " " + tissue_key
            czi_unique_celltypes = df_czi["cell_type"].unique()

            df_cellmarker2["description_all"] = df_cellmarker2[["species", "cell_type", "cell_name", "tissue_class", "tissue_type"]].astype(str).agg(" ".join, axis=1)

            cellmarker2_unique_celltypes = df_cellmarker2["description_all"].unique()

            # Example usage
            descriptions = list(cellmarker2_unique_celltypes)
            query = list(czi_unique_celltypes)

            pangdb_matched_cell_type_name = find_most_similar(self.embeddings, query, descriptions)

            dic_cell_gene = {
                "cell_type_czi": [],
                "cell_type_cellmarker2": [],
                "marker_genes": [],
            }
            for i, j in zip(query, pangdb_matched_cell_type_name):
                dic_cell_gene["cell_type_czi"].append(i)
                dic_cell_gene["cell_type_cellmarker2"].append(j)
                dic_cell_gene["marker_genes"].append(df_cellmarker2.loc[df_cellmarker2["description_all"] == j, "Symbol"].tolist())

            dic_cell_gene = pd.DataFrame(dic_cell_gene)
            dic_cell_gene.to_csv(save_csv)
        else:
            print("CellMarker2 data already exist!")

        output = "Successfully saved the matched cell types and marker genes in the CellMarker2 to the file folder."
        print(output)
        return output
