import os
from pdf_processor.reader import PDFReader
from pdf_processor.extractor import DataExtractor
from pdf_processor.repository import PostgreSQLRepository

def process_all_pdfs(folder_path: str):
    reader = PDFReader()
    extractor = DataExtractor()
    repository = PostgreSQLRepository()

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            print(f"📄 Processando: {file}")
            try:
                text = reader.read(file_path)
                data = extractor.extract(text)
                repository.save(data)
                print("✅ Sucesso ao salvar:", data["full_name"])
            except Exception as e:
                print(f"❌ Erro ao processar {file}: {e}")

if __name__ == "__main__":
    pasta_pdfs = os.path.join("data", "prontuarios")
    process_all_pdfs(pasta_pdfs)
