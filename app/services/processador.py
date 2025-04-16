import pdfplumber
import psycopg2
import os
from dotenv import load_dotenv

def dataExtraction(caminho_pdf):
    try:
        load_dotenv()

        conn = psycopg2.connect(
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        cursor = conn.cursor()

        with pdfplumber.open(caminho_pdf) as pdf:
            texto = "\n".join(pagina.extract_text() for pagina in pdf.pages if pagina.extract_text())

        linhas = texto.splitlines()
        dados = {
            "full_name": "",
            "birth_date": "",
            "address": "",
            "profession": "",
            "phone": "",
            "email": "",
            "father_name": "",
            "mother_name": "",
            "main_complaint": "",
            "father_age": "",
            "mother_age": ""
        }
        
        for i, linha in enumerate(linhas):
            linha_lower = linha.lower().strip()

            if linha_lower.startswith("nome completo:"):
                dados["full_name"] = linha.split(":", 1)[1].strip()
            elif linha_lower.startswith("data de nascimento:"):
                dados["birth_date"] = linha.split(":", 1)[1].strip()
            elif linha_lower.startswith("endereço:"):
                dados["address"] = linha.split(":", 1)[1].strip()
            elif linha_lower.startswith("profissão:"):
                dados["profession"] = linha.split(":", 1)[1].strip()
            elif linha_lower.startswith("telefone:"):
                dados["phone"] = linha.split(":", 1)[1].strip()
            elif linha_lower.startswith("e-mail:"):
                dados["email"] = linha.split(":", 1)[1].strip()
            elif linha_lower.startswith("nome do pai:"):
                if i + 1 < len(linhas):
                    dados["father_name"] = linhas[i + 1].strip()
                if i + 2 < len(linhas):
                    dados["father_age"] = linhas[i + 2].strip()
            elif linha_lower.startswith("nome da mãe:"):
                if i + 1 < len(linhas):
                    dados["mother_name"] = linhas[i + 1].strip()
                if i + 2 < len(linhas):
                    dados["mother_age"] = linhas[i + 2].strip()
            elif linha_lower.startswith("queixa principal:"):
                dados["main_complaint"] = linha.split(":", 1)[1].strip()

        print("✅ Dados inseridos com sucesso no banco de dados!\n")
        for k, v in dados.items():
            print(f"{k}: {v}")
        
        cursor.execute("""
            INSERT INTO user_data (
                full_name, birth_date, address, profession, phone,
                email, father_name, mother_name, main_complaint
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dados["full_name"],
            dados["birth_date"],
            dados["address"],
            dados["profession"],
            dados["phone"],
            dados["email"],
            dados["father_name"],
            dados["mother_name"],
            dados["main_complaint"]
        ))

        conn.commit()
        

    except Exception as e:
        print("Erro:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    caminho = "C:/Users/Micro/Desktop/Projetos/prontuario/Prontuarios/prontuario.pdf"
    dataExtraction(caminho)
