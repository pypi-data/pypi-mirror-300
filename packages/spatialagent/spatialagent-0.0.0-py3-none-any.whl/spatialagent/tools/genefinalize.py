import os, re, pandas as pd
from typing import List, Dict, Any
from langchain.tools import BaseTool
from langchain.base_language import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain_experimental.tools import PythonREPLTool
from langchain_core.output_parsers import StrOutputParser


def sanitize_filename(filename):
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


class GeneImportanceTool(BaseTool):
    name = "GeneImportanceTool"
    # description = (
    #     "If you have collected information about specific cell types and marker genes in the target tissue, use this tool to estimate the importance of each gene marker."
    #     "Input is file_path of where previous information is saved, iter_round as current iteration round, all_num_gene of the number of target genes that user requested."
    #     'Output is a str like "Successfully generated the importance score ..."'
    #     # 'You can only execute the tool one time with one corresponding iteration round number.'
    # )
    description = """
If you have collected information about specific cell types and marker genes in the target tissue, use this tool to estimate the importance of each gene marker.

Input:
    - file_path: Path where previous information about cell types and marker genes is saved.
    - iter_round: Current iteration round (integer).
    - all_num_gene: Number of target genes requested by the user.

Output:
    A string confirming successful generation of importance scores, including the path to the output file, like "Successfully generated the importance score ..."
"""
    llm: BaseLanguageModel = None

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm

    def _run(self, file_path, iter_round, all_num_gene):

        table1 = pd.read_csv(f"{file_path}/read_czi_reference_celltype_{iter_round}.csv")
        table2 = pd.read_csv(f"{file_path}/read_pangdb_celltype_{iter_round}.csv")
        table3 = pd.read_csv(f"{file_path}/read_cellmarker2_celltype_{iter_round}.csv") if os.path.exists(f"{file_path}/read_cellmarker2_celltype_{iter_round}.csv") else None

        num_each = int(all_num_gene / table1.shape[0] * 4)  # 4 is the number of cell types

        system_prompt = self._get_system_prompt(num_each)
        reformat_prompt = self._get_reformat_prompt()
        parser = {"str": StrOutputParser()}
        prompttt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{question}")])
        chain = prompttt | self.llm | parser

        csv_file_path = f"{file_path}/iter{iter_round}_importance_score_output.csv"
        if not os.path.exists(csv_file_path):
            self._process_cell_types(table1, table2, table3, iter_round, file_path, chain, reformat_prompt)
            self._combine_output_tables(table1, iter_round, file_path, csv_file_path)

        return f"Successfully generated the importance score of first {num_each} important genes of each cell type as a table in {csv_file_path}."

    def _get_system_prompt(self, num_each: int) -> str:
        return f"""
Understand the information, your task is to output a list of most important {num_each} genes for this cell type with the highest importance score.
You must follow the following rules to decide the importance score ranging from 0 to 1 (with 0 is least important and 1 is most important) of each gene.
1. each cell type has unique marker genes which are important.
2. When a gene is used to name this cell type and marked as its unique marker, such marker gene is very important. You must include this gene in any case. For example, gene 'Pvalb' is unique marker for cell type 'pvalb GABAergic cortical interneuron'.
3. When a gene appears in multiple database resources like all CZI, Pang, and CellMarker2 databases, it has a higher confidence to be a valid and important marker.
4. When a gene appears as marker in multiple cell types, it is important. However, it may less useful for differentiate the two cell types so in this case you need additional unique markers.
5. choose the genes that are nonrepeatable.
6. You must provide the correct number of genes as requested.
After choosing genes, you must examine if the genes are selected based on the above rules.
You must return the gene list in the following format:
1:[gene name]...
Importance Score: ...
Reason: ...
2:[gene name]...
Importance Score: ...
Reason: ...
Continue ...
"""

    def _get_reformat_prompt(self) -> str:
        return """
You are a helpful assistant. You will be provided with a path to a text that contains information of gene names and importance score in a structured format. 
Your task is to generate a Python code that read the content of the text, parse this text and convert it into a pandas DataFrame and save the table at {save_path}.
Here is the first 2000 letters of text:
{content}
The table must at lease include columns 'Gene Name', 'Importance Score', 'Reason'.
The 'Gene Name' can not start with numbers like '1.' or only be numbers like '1'. The 'Gene Name' must be only gene names like 'Slc17a7'.
Here is the path to the text file: {input_path}
Write only the Python code to achieve this.
"""

    def _process_cell_types(self, table1: pd.DataFrame, table2: pd.DataFrame, table3: pd.DataFrame, iter_round: int, file_path: str, chain, reformat_prompt: str):
        for i in range(table1.shape[0]):
            cell_info = self._get_cell_info(table1, table2, table3, i)
            a = sanitize_filename(cell_info["cell_type"])
            txt_path = f"{file_path}/iter{iter_round}_{a}.txt"
            save_path = f"{file_path}/iter{iter_round}_{a}.csv"

            if not os.path.exists(save_path):
                self._generate_and_save_importance(cell_info, txt_path, save_path, chain, reformat_prompt)
            else:
                print(f"Final gene panel already exists as a table in {save_path}.")

    def _get_cell_info(self, table1: pd.DataFrame, table2: pd.DataFrame, table3: pd.DataFrame, i: int) -> Dict[str, Any]:
        info = {
            "cell_type": table1["cell_type"][i],
            "description": table1["description"][i],
            "czi_marker_genes": table1["marker_genes"][i],
            "czi_cano_marker_genes": table1["cano_marker_genes"][i],
            "pangdb_cell_type": table2["cell_type_pangdb"][i],
            "pangdb_marker_genes": table2["marker_genes"][i],
        }
        if table3 is not None:
            info.update(
                {
                    "cellmarker2_cell_type": table3["cell_type_cellmarker2"][i],
                    "cellmarker2_marker_genes": table3["marker_genes"][i],
                }
            )
        return info

    def _generate_and_save_importance(self, cell_info: Dict[str, Any], txt_path: str, save_path: str, chain, reformat_prompt: str):
        while True:
            query = self._format_query(cell_info)
            answer = chain.invoke({"question": query})
            llm_output = answer["str"]
            with open(txt_path, "w") as file:
                file.write(llm_output)

            # Create the LLMChain with the prompt template and the LLM
            prompt = PromptTemplate(template=reformat_prompt, input_variables=["text"])
            llm_chain = LLMChain(prompt=prompt, llm=self.llm)

            # Generate the code
            generated_code = llm_chain.run(
                {
                    "input_path": txt_path,
                    "save_path": save_path,
                    "content": llm_output[:2000],
                }
            )

            result = PythonREPLTool().run(generated_code)
            if result == "":
                try:
                    _ = pd.read_csv(save_path)
                    print(f"Saved the gene panel at {self._short(save_path)}.")
                    os.remove(txt_path)
                    break
                except:
                    print("result is good but gene panel is missing")
            else:
                print("result:", result)

    def _short(self, path):
        memory_data_index = path.find("memory_data")
        if memory_data_index != -1:
            return path[memory_data_index:]
        return path

    def _format_query(self, cell_info: Dict[str, Any]) -> str:
        query = (
            f"The cell type in reference dataset is {cell_info['cell_type']}.\n"
            f"Description of this cell type is {cell_info['description']}.\n"
            f"Computational marker gene of this cell type in CZI database is {cell_info['czi_marker_genes']}, with their expression from high to low.\n"
            f"Canonical marker gene of this cell type in CZI database is {cell_info['czi_cano_marker_genes']}.\n"
            f"The best matched cell type of this cell type in Pang database is {cell_info['pangdb_cell_type']} with marker genes {cell_info['pangdb_marker_genes']}.\n"
        )

        if "cellmarker2_cell_type" in cell_info:
            query += (
                f"The best matched cell type of this cell type in CellMarker2 database is {cell_info['cellmarker2_cell_type']} "
                f"with marker genes {cell_info['cellmarker2_marker_genes']}.\n"
            )

        return f"Here is the information I collected: {query}"

    def _combine_output_tables(self, table1: pd.DataFrame, iter_round: int, file_path: str, csv_file_path: str):
        output_table = []
        for i in range(table1.shape[0]):
            a = sanitize_filename(table1["cell_type"][i])
            save_path = f"{file_path}/iter{iter_round}_{a}.csv"
            table_i = pd.read_csv(save_path)
            table_i["cell type"] = a
            output_table.append(table_i)
            os.remove(save_path)

        output_table = pd.concat(output_table)
        output_table.to_csv(csv_file_path, index=False)


class GeneVotingTool(BaseTool):
    name = "GeneVotingTool"
    # description = (
    #     "If you have collected multiple rounds of marker genes in the target tissue, use this tool to vote the final gene panel."
    #     "Input is file_path of where iter3_importance_score_output.csv is saved, all_num_gene of the number of target genes that user requested."
    #     'For example, table iter3_importance_score_output.csv is saved in "/hoxxme/sd/d/sd/cx/sd/iter3_importance_score_output.csv", file_path should be "/hoxxme/sd/d/sd/cx/sd/".'
    #     'Output is a str like "Successfully saved ... and the path to where results are saved as a csv."'
    # )
    description = """
Vote for the final gene panel based on multiple rounds of marker genes in the target tissue.

Input:
- file_path: Path where iter3_importance_score_output.csv is saved. Example: If the file is at '/hoxxme/sd/d/sd/cx/sd/iter3_importance_score_output.csv', file_path should be '/hoxxme/sd/d/sd/cx/sd/'.
- all_num_gene: Number of target genes requested by the user.

Output:
A string confirming successful saving of the results, including the path to the saved CSV file. Example: 'Successfully saved the gene panel at memory_data/2023-08-20/final_gene_panel.csv'

This tool combines multiple rounds of gene importance scores, aggregates the data, and produces a final gene panel that ensures representation of all cell types.
"""
    llm: BaseLanguageModel = None

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm

    def _run(self, file_path: str, all_num_gene: int) -> str:
        important = self._load_and_combine_tables(file_path)
        sorted_df = self._aggregate_and_sort(important, all_num_gene)

        try:
            sorted_df.index = range(1, 1 + all_num_gene)
        except ValueError:
            return (
                "The number of genes you selected is not correct. You must exit and go back to planning stage "
                "to use other tools that re-design the gene panel and give annotations and reasons."
            )

        output_path = f"{file_path}/final_gene_panel.csv"
        sorted_df.to_csv(output_path, index=False)
        self._cleanup_files(file_path)

        return f"Saved the gene panel at {self._short(output_path)}."

    def _short(self, path):
        memory_data_index = path.find("memory_data")
        if memory_data_index != -1:
            return path[memory_data_index:]
        return path

    def _load_and_combine_tables(self, file_path: str) -> pd.DataFrame:
        tables = [pd.read_csv(f"{file_path}/iter{i}_importance_score_output.csv") for i in range(1, 4) if os.path.exists(f"{file_path}/iter{i}_importance_score_output.csv")]
        important = pd.concat(tables)
        important["Gene Name"] = important["Gene Name"].str.upper()
        return important

    def _aggregate_and_sort(self, important: pd.DataFrame, all_num_gene: int) -> pd.DataFrame:
        while True:
            aggregated_df = (
                important.groupby("Gene Name")
                .agg(
                    {
                        "Importance Score": "sum",
                        "Reason": lambda x: "; ".join(x),
                        "cell type": lambda x: "; ".join(x),
                    }
                )
                .reset_index()
            )
            sorted_df_all = aggregated_df.sort_values(by="Importance Score", ascending=False)
            sorted_df = sorted_df_all.iloc[:all_num_gene, :]

            if self._check_cell_type_coverage(sorted_df, sorted_df_all, important):
                print(f"All cell types are included in the top {all_num_gene} genes.")
                break

        return sorted_df

    def _check_cell_type_coverage(self, sorted_df: pd.DataFrame, sorted_df_all: pd.DataFrame, important: pd.DataFrame) -> bool:
        for cell_type in important["cell type"].unique():
            if sorted_df["cell type"].str.contains(cell_type).sum() < 1:
                high_gene_name = sorted_df_all.loc[sorted_df_all["cell type"].str.contains(cell_type), "Gene Name"].values[0]
                important.loc[important["Gene Name"] == high_gene_name, "Importance Score"] += 1
                print(cell_type)
                return False
        return True

    def _cleanup_files(self, file_path: str):
        for iteration_rounds in range(1, 4):
            rm_pth = f"{file_path}/read_czi_reference_adata_{iteration_rounds}.h5ad"
            if os.path.exists(rm_pth):
                os.remove(rm_pth)


# def clean_string(s):
#     # Remove spaces, hyphens, newlines, and asterisks from the beginning and end of the string
#     return s.strip(" -*\n:")

# def reformat_gene_list(content):
#     pattern = re.compile(
#         r"\d+\.\s*([^\n]+)\n\s*([^\n]+)\n\s*([^\n]+)\n\s*([^\n]+)",
#         re.MULTILINE
#     )
#     # Find all matches
#     matches = pattern.findall(content)

#     for i in range(len(matches)):
#         # Clean up each match
#         matches[i] = [clean_string(x) for x in matches[i]]
#         matches[i] = [x.replace('*','') for x in matches[i]]

#     # Create a DataFrame
#     if len(matches[0])==5:
#         data = pd.DataFrame(matches, columns=['Gene', 'Cell type', 'Reason', 'Annotation', 'Reference'])
#     else:
#         data = pd.DataFrame(matches, columns=['Gene', 'Reason', 'Annotation', 'Reference'])

#     for column_name in data.columns:
#         data[column_name] = data[column_name].str.replace(column_name, '')
#     for column_name in ['Reason', 'Annotation', 'Reference']:
#         data[column_name] = data[column_name].str.lstrip('-*\n:').str.rstrip('-*\n:')
#     try:
#         data['Gene'] = data['Gene'].str.split(':').str[1].str.strip()
#     except AttributeError:
#         pass

#     return data


# class GeneDesignTool(BaseTool):
#     name='GeneDesignTool'
#     description = ('If you have collected information about specific cell types and marker genes in the target tissue, use this tool to design the final gene panel and give annotations and reasons. After this step, you should reformat the result into a table.'
#                     'Input must be a str to a path where the collected information is saved, and a query of the question, for example:"I want to design a spatial transcriptomics experiment of [target tissue, organ, species]. Choose [number] target genes for me, and new_infor from previous trials."'
#                     'Output is a str like "Successfully saved ... and the path to where results are saved as a txt."')
#     llm: BaseLanguageModel = None

#     def __init__(self, llm):
#         super().__init__()
#         self.llm=llm
#         # query='I want to design a spatial transcriptomics experiment of Dorsolateral prefrontal cortex. Choose 50 target genes for me.'

#     def _run(self, file_path, query, new_infor=None):
#         table1 = pd.read_csv(file_path+'read_czi_reference_celltype.csv')
#         table2 = pd.read_csv(file_path+'read_pangdb_celltype.csv')
#         # table3 = pd.read_csv(file_path+'persist_gene_list.csv')
#         # persist_genes=table3['feature_name'].to_list()

#         current_infor=[]
#         for i in range(table1.shape[0]):
#             a,b,c,d,e,f = table1['cell_type'][i], table1['description'][i], table1['marker_genes'][i], table1['cano_marker_genes'][i], table2['cell_type_pangdb'][i], table2['marker_genes'][i]
#             new_infor=( f'The {i}th cell type in reference dataset is {a}.\n'
#                         f'Description of this cell type is {b}.\n'
#                         f'Computational marker gene of this cell type in CZI database is {c}, with their expression from high to low.\n'
#                         f'Canonical marker gene of this cell type in CZI database is {d}.\n'
#                         f'The best matched cell type of this cell type in Pang database is {e} with marker genes {f}.\n\n')
#             current_infor.append(new_infor)
#         # new_infor= f'An optional reference gene list is selected by a computational tool a unsupervised way: {persist_genes}.'
#         # current_infor.append(new_infor)

#         system = f"""Here is the information I collected for this target: {current_infor}.\n\
#                     Understand the information, your goal is to design a gene list that identify all unique cell types and best show high spatial variance.\n\
#                     You must follow the following rules.\n
#                     1. you must cover at least one marker gene for each unique cell type. All unique cell types are: {table1['cell_type'].to_list()}. \n\
#                     2. for each cell type, based on multiple database resources, decide the importance score of its marker genes.\n
#                     3. When a gene is used to name this cell type and marked as its unique marker, such marker gene is very important. You must include this gene in any case. For example, gene 'Pvalb' is unique marker for cell type 'pvalb GABAergic cortical interneuron'.\n\
#                     4. When a gene appears in multiple database resources like both CZI database and Pang database, it has higher confidence to be a valid and important marker.\n\
#                     5. When a gene appears as marker in multiple cell types, it is important. However, it may less useful for differentiate the two cell types so in this case you need additional unique markers.\n\
#                     6. choose the target genes that are nonrepeatable and give reasoning.\n\
#                     7. You must provide the correct number of genes as user requested.\n\
#                     Some new infromation from previous triales is: {new_infor}.\n\
#                     After choosing genes, you must examine if the genes are selected based on the above rules. \n\
#                     Does the selection fit the rule 1? If not, adjust the gene list. Continue...\n\
#                     You must return the gene list in the following format: \
#                     Gene 1:[gene name]...
#                         Reason: ...
#                         Annotation: ...
#                         Reference: ...
#                     Gene 2:[gene name]...
#                         Reason: ...
#                         Annotation: ...
#                         Reference: ...
#                     Continue ..."""

#         parser = {"str": StrOutputParser()}

#         prompttt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])

#         chain = prompttt | self.llm | parser
#         answer =chain.invoke({"question": query})
#         with open(file_path+'final_output.txt', 'w') as file:
#             file.write(answer['str'])

#         print(answer['str'])

#         # answer_table = reformat_gene_list(answer['str'])
#         # answer_table.to_csv(file_path+'gene_list_output.csv')

#         output_path = file_path+'final_output.txt'
#         output=f'Successfully designed the gene panel. The path to file folder where genes, annotations and reasons are saved as txt is {output_path}.'
#         return output


# # Create a prompt template
# prompt_template = """
# You are a helpful assistant. You will be provided with a path to a text that contains information about genes in a structured format.
# Your task is to generate a Python code that read the content of the text, parse this text and convert it into a pandas DataFrame and save the table at {save_path}.
# Here is the first 2000 letters of text:
# {content}
# The table must at lease include columns 'Gene Name', 'Reason', 'Annotation', 'Reference'.
# The 'Gene Name' can not start with numbers like '1.', should be only genes like Slc17a7.
# Here is the path to the text file: {input_path}
# Write only the Python code to achieve this.
# """


# class GeneReformatTool(BaseTool):
#     name='GeneReformatTool'
#     description = ('If you just designed the final gene panel with annotations and reasons and saved in a txt, use this tool to reformat it into a table as final table. After this step, you should examine the result.'
#                     'Input must be a str to a path where the gene panel txt is saved. For example: "/ds/xx/tt/xx/ee/zz.txt".'
#                     'Output is a str like "Successfully saved the gene panel as a table in ..."')

#     llm: BaseLanguageModel = None

#     def __init__(self, llm):
#         super().__init__()
#         self.llm=llm

#     def _run(self, file_path):

#         # Open the file in read mode
#         with open(file_path, 'r') as file:
#             # Read the entire contents of the file
#             content = file.read()

#         save_path = os.path.dirname(file_path)+'/output_table.csv'

#         # Create the LLMChain with the prompt template and the LLM
#         prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
#         llm_chain = LLMChain(prompt=prompt, llm=self.llm)

#         # Generate the code
#         generated_code = llm_chain.run({'input_path':file_path, 'content': content[:2000], 'save_path': save_path})

#         # Print the generated code
#         print("Generated Python Code:")
#         print(generated_code)

#         # Set up the Python execution environment
#         python_repl = PythonREPLTool()

#         # Define a function to execute the code and print the DataFrame
#         result = python_repl.run(generated_code)

#         # time.sleep(5)


#         if result=='':
#             return f'Successfully saved the final gene panel as a table in {save_path}.'
#         else:
#             print('result:',result)
#             return result


# class ResultExamineTool(BaseTool):
#     name='ResultExamineTool'
#     description = ('If you have saved gene panel as a table, use this tool to examine the result and give feedback.'
#                     'Input must be a str to a path where the gene panel table is saved. For example: "/ds/xx/tt/xx/ee/zz.csv". and the number of genes that user requested.'
#                     'Output is a str like "Successfully generated correct results."')


#     def __init__(self):
#         super().__init__()

#     def _run(self, file_path, number_gene):

#         table = pd.read_csv(file_path)
#         if table['Gene Name'].unique().shape[0]!=number_gene:
#             return 'The number of genes you selected is not correct. You must exit and go back to planning stage to use other tools that re-design the gene panel and give annotations and reasons.'
#         else:
#             return 'Successfully generated correct results.'


# class GeneImportanceTool(BaseTool):
#     name = "GeneImportanceTool"
#     description = (
#         "If you have collected information about specific cell types and marker genes in the target tissue, use this tool to estimate the importance of each gene marker."
#         "Input is file_path of where previous information is saved, iter_round as current iteration round, all_num_gene of the number of target genes that user requested."
#         'Output is a str like "Successfully generated the importance score ..."'
#         # 'You can only execute the tool one time with one corresponding iteration round number.'
#     )
#     llm: BaseLanguageModel = None

#     def __init__(self, llm):
#         super().__init__()
#         self.llm = llm

#     def _run(self, file_path, iter_round, all_num_gene):
#         table1 = pd.read_csv(file_path + f"read_czi_reference_celltype_{iter_round}.csv")
#         table2 = pd.read_csv(file_path + f"read_pangdb_celltype_{iter_round}.csv")
#         if os.path.exists(file_path + f"read_cellmarker2_celltype_{iter_round}.csv"):
#             table3 = pd.read_csv(file_path + f"read_cellmarker2_celltype_{iter_round}.csv")

#         num_each = int(all_num_gene / table1.shape[0] * 4)

#         system = f"""Understand the information, your task is to output a list of most important {num_each} genes for this cell type with the highest importance score.\n\
#                     You must follow the following rules to decide the importance score ranging from 0 to 1 (with 0 is least important and 1 is most important) of each gene.\n
#                     1. each cell type has unique marker genes which are important. \n\
#                     2. When a gene is used to name this cell type and marked as its unique marker, such marker gene is very important. You must include this gene in any case. For example, gene 'Pvalb' is unique marker for cell type 'pvalb GABAergic cortical interneuron'.\n\
#                     3. When a gene appears in multiple database resources like all CZI, Pang, and CellMarker2 databases, it has a higher confidence to be a valid and important marker.\n\
#                     4. When a gene appears as marker in multiple cell types, it is important. However, it may less useful for differentiate the two cell types so in this case you need additional unique markers.\n\
#                     5. choose the genes that are nonrepeatable.\n\
#                     6. You must provide the correct number of genes as requested.\n\
#                     After choosing genes, you must examine if the genes are selected based on the above rules. \n\
#                     You must return the gene list in the following format: \
#                     1:[gene name]...
#                     Importance Score: ...
#                     Reason: ...
#                     2:[gene name]...
#                     Importance Score: ...
#                     Reason: ...
#                     Continue ..."""

#         reformat_prompt_template = """
#                 You are a helpful assistant. You will be provided with a path to a text that contains information of gene names and importance score in a structured format.
#                 Your task is to generate a Python code that read the content of the text, parse this text and convert it into a pandas DataFrame and save the table at {save_path}.
#                 Here is the first 2000 letters of text:
#                 {content}
#                 The table must at lease include columns 'Gene Name', 'Importance Score', 'Reason'.
#                 The 'Gene Name' can not start with numbers like '1.' or only be numbers like '1'. The 'Gene Name' must be only gene names like 'Slc17a7'.
#                 Here is the path to the text file: {input_path}
#                 Write only the Python code to achieve this.
#                 """

#         parser = {"str": StrOutputParser()}
#         prompttt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])
#         chain = prompttt | self.llm | parser

#         csv_file_path = file_path + f"iter{iter_round}_importance_score_output.csv"
#         if not os.path.exists(csv_file_path):
#             for i in range(table1.shape[0]):
#                 if os.path.exists(file_path + f"read_cellmarker2_celltype_{iter_round}.csv"):
#                     a, b, c, d, e, f, g, h = (
#                         table1["cell_type"][i],
#                         table1["description"][i],
#                         table1["marker_genes"][i],
#                         table1["cano_marker_genes"][i],
#                         table2["cell_type_pangdb"][i],
#                         table2["marker_genes"][i],
#                         table3["cell_type_cellmarker2"][i],
#                         table3["marker_genes"][i],
#                     )
#                 else:
#                     a, b, c, d, e, f = (
#                         table1["cell_type"][i],
#                         table1["description"][i],
#                         table1["marker_genes"][i],
#                         table1["cano_marker_genes"][i],
#                         table2["cell_type_pangdb"][i],
#                         table2["marker_genes"][i],
#                     )
#                 a = sanitize_filename(a)
#                 txt_path = file_path + f"iter{iter_round}_{a}.txt"
#                 save_path = file_path + f"iter{iter_round}_{a}.csv"
#                 if not os.path.exists(save_path):
#                     while True:
#                         print(a)
#                         if os.path.exists(file_path + f"read_cellmarker2_celltype_{iter_round}.csv"):
#                             new_infor = (
#                                 f"The {i}th cell type in reference dataset is {a}.\n"
#                                 f"Description of this cell type is {b}.\n"
#                                 f"Computational marker gene of this cell type in CZI database is {c}, with their expression from high to low.\n"
#                                 f"Canonical marker gene of this cell type in CZI database is {d}.\n"
#                                 f"The best matched cell type of this cell type in Pang database is {e} with marker genes {f}.\n\n"
#                                 f"The best matched cell type of this cell type in CellMarker2 database is {g} with marker genes {h}.\n\n"
#                             )
#                         else:
#                             new_infor = (
#                                 f"The {i}th cell type in reference dataset is {a}.\n"
#                                 f"Description of this cell type is {b}.\n"
#                                 f"Computational marker gene of this cell type in CZI database is {c}, with their expression from high to low.\n"
#                                 f"Canonical marker gene of this cell type in CZI database is {d}.\n"
#                                 f"The best matched cell type of this cell type in Pang database is {e} with marker genes {f}.\n\n"
#                             )
#                         query = f"Here is the information I collected: {new_infor}."
#                         answer = chain.invoke({"question": query})

#                         with open(txt_path, "w") as file:
#                             file.write(answer["str"])

#                         llm_output = answer["str"]

#                         # Create the LLMChain with the prompt template and the LLM
#                         prompt = PromptTemplate(template=reformat_prompt_template, input_variables=["text"])
#                         llm_chain = LLMChain(prompt=prompt, llm=self.llm)

#                         # Generate the code
#                         generated_code = llm_chain.run(
#                             {
#                                 "input_path": txt_path,
#                                 "content": llm_output[:2000],
#                                 "save_path": save_path,
#                             }
#                         )
#                         python_repl = PythonREPLTool()
#                         result = python_repl.run(generated_code)

#                         if result == "":
#                             try:
#                                 test_table = pd.read_csv(save_path)
#                                 print(f"Successfully saved the final gene panel as a table in {save_path}.")
#                                 os.remove(txt_path)
#                                 break
#                             except:
#                                 print("result is good but table is wrong")

#                         else:
#                             print("result:", result)
#                 else:
#                     print(f"Final gene panel already exists as a table in {save_path}.")

#             output_table = []
#             for i in range(table1.shape[0]):
#                 a = table1["cell_type"][i]
#                 a = sanitize_filename(a)
#                 save_path = file_path + f"iter{iter_round}_{a}.csv"
#                 table_i = pd.read_csv(save_path)
#                 table_i["cell type"] = a
#                 output_table.append(table_i)
#             output_table = pd.concat(output_table)
#             output_table.to_csv(csv_file_path, index=False)

#             for i in range(table1.shape[0]):
#                 a = table1["cell_type"][i]
#                 a = sanitize_filename(a)
#                 save_path = file_path + f"iter{iter_round}_{a}.csv"
#                 os.remove(save_path)

#         output = f"Successfully generated the importance score of first {num_each} important genes of each cell type as a table in {csv_file_path}."
#         return output


# class GeneVotingTool(BaseTool):
#     name = "GeneVotingTool"
#     description = (
#         "If you have collected multiple rounds of marker genes in the target tissue, use this tool to vote the final gene panel."
#         "Input is file_path of where iter3_importance_score_output.csv is saved, all_num_gene of the number of target genes that user requested."
#         'For example, table iter3_importance_score_output.csv is saved in "/hoxxme/sd/d/sd/cx/sd/iter3_importance_score_output.csv", file_path should be "/hoxxme/sd/d/sd/cx/sd/".'
#         'Output is a str like "Successfully saved ... and the path to where results are saved as a csv."'
#     )
#     llm: BaseLanguageModel = None

#     def __init__(self, llm):
#         super().__init__()
#         self.llm = llm

#     def _run(self, file_path, all_num_gene):
#         important_table1 = pd.read_csv(file_path + "/iter1_importance_score_output.csv")
#         important_table2 = pd.read_csv(file_path + "/iter2_importance_score_output.csv")
#         if os.path.exists(file_path + "/iter3_importance_score_output.csv"):
#             important_table3 = pd.read_csv(file_path + "/iter3_importance_score_output.csv")
#             important = pd.concat([important_table1, important_table2, important_table3])
#         else:
#             important = pd.concat([important_table1, important_table2])
#         important["Gene Name"] = list(important["Gene Name"].str.upper())

#         # aggregated_df = important.groupby('Gene Name').agg({
#         #     'Importance Score': 'sum',
#         #     'Reason': lambda x: '; '.join(x),
#         #     'cell type': lambda x: '; '.join(x)
#         # }).reset_index()
#         # sorted_df = aggregated_df.sort_values(by='Importance Score', ascending=False)
#         # sorted_df = sorted_df.iloc[:all_num_gene,:]

#         while True:
#             # Group by 'Gene Name' and aggregate
#             _dict = {
#                 "Importance Score": "sum",
#                 "Reason": lambda x: "; ".join(x),
#                 "cell type": lambda x: "; ".join(x),
#             }
#             aggregated_df = important.groupby("Gene Name").agg(_dict).reset_index()
#             sorted_df_all = aggregated_df.sort_values(by="Importance Score", ascending=False)
#             sorted_df = sorted_df_all.iloc[:all_num_gene, :]

#             check = 0
#             for i in important["cell type"].unique():
#                 if sorted_df["cell type"].str.contains(i).sum() < 1:
#                     corre_high_gene_name = sorted_df_all.loc[sorted_df_all["cell type"].str.contains(i), "Gene Name"].values[0]
#                     important.loc[important["Gene Name"] == corre_high_gene_name, "Importance Score"] += 1
#                     print(i)
#                     check = 1
#             if check == 0:
#                 print(f"All cell types are included in the top {all_num_gene} genes.")
#                 break

#         try:
#             sorted_df.index = range(1, 1 + all_num_gene)
#         except ValueError:
#             print(
#                 "The number of genes you selected is not correct. You must exit and go back to planning stage to use other tools that re-design the gene panel and give annotations and reasons."
#             )
#             return

#         sorted_df.to_csv(file_path + "/final_gene_panel.csv", index=False)

#         for iteration_rounds in range(1, 4):
#             rm_pth = file_path + f"/read_czi_reference_adata_{iteration_rounds}.h5ad"
#             if os.path.exists(rm_pth):
#                 os.remove(rm_pth)

#         output = f"Successfully saved the final gene panel as a table in {file_path}/final_gene_panel.csv."
#         return output
