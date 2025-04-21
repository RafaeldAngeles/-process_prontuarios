from .interfaces.i_extractor import IExtractor

class DataExtractor(IExtractor):
    def extract(self, text: str) -> dict:
        linhas = [linha.strip() for linha in text.splitlines() if linha.strip()]
        dados = {
            "full_name": "", "birth_date": "", "address": "", "profession": "",
            "phone": "", "email": "", "father_name": "", "mother_name": "",
            "main_complaint": "", "father_age": "", "mother_age": ""
        }

        try:
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
        except Exception as e:
            print("Erro ao extrair os dados:", e)

        return dados

