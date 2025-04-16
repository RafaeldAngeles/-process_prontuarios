import pdfplumber
import psycopg2
import os
from dotenv import load_dotenv

def dataExtraction(caminho_pdf):
    try:
        # Carrega as variáveis do .env
        load_dotenv()

        conn = psycopg2.connect(
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        cursor = conn.cursor()

        print("Banco de dados:", os.getenv("DATABASE_NAME"))

        # Leitura e extração do PDF
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

        for linha in linhas:
            linha_lower = linha.lower()

            if "nome completo" in linha_lower and ":" in linha:
                dados["full_name"] = linha.split(":", 1)[1].strip()
            elif "data de nascimento" in linha_lower and ":" in linha:
                dados["birth_date"] = linha.split(":", 1)[1].strip()
            elif "endereço" in linha_lower and ":" in linha:
                dados["address"] = linha.split(":", 1)[1].strip()
            elif "profissão" in linha_lower and ":" in linha:
                dados["profession"] = linha.split(":", 1)[1].strip()
            elif "telefone" in linha_lower and ":" in linha:
                dados["phone"] = linha.split(":", 1)[1].strip()
            elif "e-mail" in linha_lower and ":" in linha:
                dados["email"] = linha.split(":", 1)[1].strip()
            elif "nome do pai" in linha_lower and ":" in linha:
                dados["father_name"] = linha.split(":", 1)[1].strip()
            elif "nome da mãe" in linha_lower and ":" in linha:
                dados["mother_name"] = linha.split(":", 1)[1].strip()
            elif "queixa principal" in linha_lower and ":" in linha:
                dados["main_complaint"] = linha.split(":", 1)[1].strip()
            elif "idade:" in linha and ":" in linha:
                if not dados["father_age"]:
                    dados["father_age"] = linha.split(":", 1)[1].strip()
                elif not dados["mother_age"]:
                    dados["mother_age"] = linha.split(":", 1)[1].strip()

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
        print("✅ Dados inseridos com sucesso no banco de dados!")
        print("\n=== DADOS EXTRAÍDOS DO PRONTUÁRIO PSICOLÓGICO ===")
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")

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
