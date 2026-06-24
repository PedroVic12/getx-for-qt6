from scripts.power_query_MUST_PDF_Tables import power_query, console
from scripts.script_read_text_MUST_PDF import process_PDF_text_folder_pdf, process_PDF_text_single_pdf
from scripts.juntar_resultados_excel_MUST import consolidar_anotacoes, substituir_aba_excel, extrair_cod_ons

import os 
import pandas as pd

from services.DataBaseController import SQLiteController, AccessController
from pathlib import Path


#! Refatorção do Projeto para projeto profissional Python com SQL Alchemy e Pyside com QT Designer MVP
#! Update 22/10/2025
#! Refatorar partindo do banco: Access Microsoft -> Crud - Pyside6 Controle e Gestão Desktop (Deck Builder + Gerador de Relatórios .docx e com AI em HTML) + Site Dashboard Atividades SP com controle aprovação MUST

# Função para conectar com o Banco de dados (apos o Excel consolidado)
def run_database_load_process(input_folder):
    """
    Função chamada pela GUI para carregar os dados nos bancos.
    """
    console.log("Iniciando processo de carregamento para os bancos de dados...", "info")
    
    database_folder = Path(input_folder) / "database"
    source_excel_path = database_folder / "must_tables_PDF_notes_merged.xlsx"
    
    if not source_excel_path.exists():
        console.log(f"ERRO: Arquivo de origem não encontrado: {source_excel_path}", "error")
        return

    df_source = pd.read_excel(source_excel_path)

    # Carregar para SQLite
    sqlite_db_path = database_folder / "database_consolidado.db"
    sqlite_controller = SQLiteController(df_source, sqlite_db_path)
    sqlite_controller.load_data()
    
    # Carregar para Access
    access_db_path = database_folder / "database_consolidado.accdb"
    if access_db_path.exists():
        access_controller = AccessController(df_source, access_db_path)
        access_controller.load_data()
    else:
        console.log(f"AVISO: Banco de dados Access não encontrado em {access_db_path}. Pulei a carga.", "warning")

    console.log("\n✅ Processo de carregamento de banco de dados concluído.", "success")

# Função para tratamento de dados
def consolidate_and_merge_results(input_folder):
    """
    Função principal que orquestra a consolidação das anotações
    e o merge final com as tabelas.
    """
    console.log("Iniciando etapa de consolidação e junção...", "info")
    
    # --- 1. Consolida as anotações ---
    anotacoes_folder = os.path.join(input_folder, "anotacoes_extraidas")
    console.log(f"Lendo anotações da pasta: {anotacoes_folder}", "info")
    df_notes = consolidar_anotacoes(anotacoes_folder)
    
    if df_notes is None or df_notes.empty:
        console.log("Nenhum dado de anotação foi consolidado. Processo interrompido.", "warning")
        return

    # --- 2. Prepara para o Merge ---
    tabelas_folder = os.path.join(input_folder, "tabelas_extraidas")
    database_path = os.path.join(tabelas_folder, "database_must.xlsx")
    
    if not os.path.exists(database_path):
        console.log(f"ERRO CRÍTICO: O arquivo base 'database_must.xlsx' não foi encontrado em {tabelas_folder}", "error")
        return
        
    console.log(f"Lendo banco de dados principal de: {database_path}", "info")
    df_tables = pd.read_excel(database_path, sheet_name="Tabelas Consolidada")

    # --- 3. Limpeza e Merge ---
    console.log("Limpando e padronizando códigos ONS...", "info")
    df_tables["Cód ONS"] = df_tables["Cód ONS"].apply(extrair_cod_ons).str.upper().str.strip()
    df_notes["Cód ONS"] = df_notes["Cód ONS"].apply(extrair_cod_ons).str.upper().str.strip()

    df_notes_filtrado = df_notes[df_notes["num_tabela"] == 1].reset_index(drop=True)

    console.log("Realizando o merge entre tabelas e anotações...", "info")
    df_final_merged = df_tables.merge(
        df_notes_filtrado[["Cód ONS", "Anotacao"]],
        on="Cód ONS",
        how="left"
    )

    # --- 4. Exportação dos Resultados Finais ---
    output_database_folder = os.path.join(input_folder, "database")
    os.makedirs(output_database_folder, exist_ok=True)
    
    final_excel_path = os.path.join(output_database_folder, "must_tables_PDF_notes_merged.xlsx")
    final_json_path = os.path.join(output_database_folder, "must_tables_PDF_notes_merged.json")

    console.log(f"Exportando resultado final para Excel: {final_excel_path}", "info")
    df_final_merged.to_excel(final_excel_path, index=False)
    
    console.log(f"Exportando resultado final para JSON: {final_json_path}", "info")
    df_final_merged.to_json(final_json_path, orient="records", force_ascii=False)

    console.log("✅ Processo de consolidação e junção concluído com sucesso!", "success")


#-------------------------------------------------------------------------------------------------------------------------------
#! SCRIPT DE AUTOMAÇÂO COMPLETO VIA TERMINAL

# ETL (Extract, Transform, Load): Você extrai o conteúdo dos PDFs, imediatamente o limpa, estrutura e valida (Transform), e então carrega os dados já limpos e estruturados no banco de dados final (Load). Este é o modelo mais tradicional.

# EXTL (Extract, Load, Transform): Você extrai o conteúdo bruto dos PDFs (Extract), carrega esse conteúdo bruto (por exemplo, o texto completo de cada página) em uma área de preparação (staging area) no seu banco de dados ou em um Data Lake (Load), e só então executa rotinas (com SQL, Python, etc.) para limpar e estruturar os dados em tabelas finais (Transform). Este modelo é mais moderno e flexível.

def run_extract_PDF_tables(input_folder, pdf_files_to_process, intervalos_paginas_to_process, mode = "folder" ):
 
    
    print("\nIniciando extração de tabelas de PDFs...\n")
   
    output_folder = os.path.join(input_folder, "tabelas_extraidas")
    os.makedirs(output_folder, exist_ok=True)
    
    
    try:
        pdf_files = pdf_files_to_process # Usa a lista de arquivos passadas
        intervalos_paginas = intervalos_paginas_to_process # Usa a lista de intervalos passadas

        if len(pdf_files) != len(intervalos_paginas):
            console.log("ERRO CRÍTICO: O número de arquivos PDF e intervalos não corresponde.", "error")
            return
        mapeamento = dict(zip(pdf_files, intervalos_paginas))
        console.log("Mapeamento de arquivos e páginas criado com sucesso.", "success")
    except Exception as e:
        console.log(f"ERRO ao preparar mapeamento de arquivos e intervalos: {e}", "error")
        return

    # O modo "single" não será mais usado da mesma forma, já que estamos operando em uma lista selecionada
    # Se um único PDF foi selecionado na GUI, ele estará em pdf_files_to_process
    power_query.run_folder_mode( input_folder, output_folder, mapeamento)


def extract_text_from_must_tables(input_folder, pdf_files_to_process, mode = "folder"):

    print("\nIniciando extração de texto dos PDFs MUST...\n")

    # Pasta para salvar os resultados
    output_folder = os.path.join(input_folder, "anotacoes_extraidas")
    os.makedirs(output_folder, exist_ok=True) # Garante que a pasta exista

    # Execução para os arquivos selecionados
    for pdf_file_name in pdf_files_to_process:
        pdf_path = os.path.join(input_folder, pdf_file_name)
        if os.path.exists(pdf_path):
            process_PDF_text_single_pdf(pdf_path, output_folder) # process_PDF_text_single_pdf já lida com um único PDF
        else:
            print(f"AVISO: O arquivo '{pdf_file_name}' não foi encontrado na pasta de entrada. Pulando.")

    print("\n🔚 Script concluído.")



# Main da automação 
# if __name__ == "__main__":

#     run_extract_PDF_tables(intervalos_paginas, mode="folder")

#     extract_text_from_must_tables(mode ="folder")
    

