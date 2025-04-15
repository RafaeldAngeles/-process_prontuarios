import pdfplumber
import psycopg2
import os
from dotenv import load_dotenv

def extrair_e_inserir_dados(caminho_pdf):
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
        dados = {}

        def pegar_valor(label):
            for linha in linhas:
                if label.lower() in linha.lower():
                    partes = linha.split(":")
                    if len(partes) > 1:
                        return partes[1].strip()
            return ""

        def pegar_idades():
            idades = [linha.split(":")[1].strip() for linha in linhas if "Idade:" in linha]
            return idades[0], idades[1] if len(idades) >= 2 else ("", "")

        dados["full_name"] = pegar_valor("Nome completo")
        dados["birth_date"] = pegar_valor("Data de nascimento")
        dados["address"] = pegar_valor("Endereço")
        dados["profession"] = pegar_valor("Profissão")
        dados["phone"] = pegar_valor("Telefone")
        dados["email"] = pegar_valor("E-mail")
        dados["father_name"] = pegar_valor("Nome do pai")
        dados["mother_name"] = pegar_valor("Nome da mãe")
        dados["main_complaint"] = pegar_valor("Queixa Principal")
        father_age, mother_age = pegar_idades()
        dados["father_age"] = father_age
        dados["mother_age"] = mother_age

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
    extrair_e_inserir_dados(caminho)
