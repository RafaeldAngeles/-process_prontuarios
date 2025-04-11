import pdfplumber

def processar_prontuario_psicologico(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"

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
        if len(idades) >= 2:
            return idades[0], idades[1]
        return "", ""

    # Mapeamento dos campos
    dados["full_name"] = pegar_valor("Nome completo")
    dados["birth_date"] = pegar_valor("Data de nascimento")
    dados["address"] = pegar_valor("Endereço")
    dados["profession"] = pegar_valor("Profissão")
    dados["phone"] = pegar_valor("Telefone")
    dados["email"] = pegar_valor("E-mail")
    dados["father_name"] = pegar_valor("Nome do pai")
    dados["mother_name"] = pegar_valor("Nome da mãe")
    dados["main_complaint"] = pegar_valor("Queixa Principal")

    # Idades separadas
    father_age, mother_age = pegar_idades()
    dados["father_age"] = father_age
    dados["mother_age"] = mother_age

    return dados


if __name__ == "__main__":
    caminho = "C:/Users/Micro/Desktop/Projetos/prontuario/Prontuarios/prontuario.pdf"  
    dados = processar_prontuario_psicologico(caminho)

    print("\n=== DADOS EXTRAÍDOS DO PRONTUÁRIO PSICOLÓGICO ===\n")
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")



# 🔜 Próximos passos (anotado pra amanhã):
# Criar uma nova tabela no PostgreSQL com os campos ajustados ao novo modelo de prontuário psicológico

# Automatizar a leitura de arquivos da pasta (ex: ler tudo de ./Prontuarios/ em loop)

# Inserir os dados extraídos direto no banco

# (Se quiser mais pra frente) Criar uma API com FastAPI pra expor esses dados