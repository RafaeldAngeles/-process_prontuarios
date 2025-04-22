from .interfaces.i_extractor import IExtractor

class DataExtractor(IExtractor):
    def extract(self, text: str) -> dict:
        linhas = [l.strip() for l in text.splitlines() if l.strip()]
        for idx, l in enumerate(linhas):
            print(f"{idx:02d}: {l}")

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

            if "nome completo" in linha_lower:
                dados["full_name"] = self.extract_value(linha)

            elif "data de nascimento" in linha_lower:
                dados["birth_date"] = self.formatar_data(self.extract_value(linha))

            elif "endereço" in linha_lower:
                dados["address"] = self.extract_value(linha)

            elif "profissão" in linha_lower:
                dados["profession"] = self.extract_value(linha)

            elif "telefone" in linha_lower:
                dados["phone"] = self.extract_value(linha)

            elif "e-mail" in linha_lower:
                dados["email"] = self.extract_value(linha)

            elif "nome do pai" in linha_lower:
                dados["father_name"] = self.extract_value(linha)

            elif "idade" in linha_lower and not dados["father_age"]:
                dados["father_age"] = self.extract_value(linha)

            elif "nome da mãe" in linha_lower:
                dados["mother_name"] = self.extract_value(linha)

            elif "idade" in linha_lower and not dados["mother_age"]:
                dados["mother_age"] = self.extract_value(linha)

            elif "queixa principal" in linha_lower:
                if not dados["main_complaint"]:
                    dados["main_complaint"] = self.extract_value(linha)

        return dados

    def extract_value(self, linha: str) -> str:
        """Extraí o valor após o ":" e remove espaços em branco extras."""
        try:
            return linha.split(":", 1)[1].strip() if ":" in linha else ""
        except IndexError:
            return ""

    def formatar_data(self, data_br: str) -> str:
        """Formata a data do formato DD/MM/AAAA para YYYY-MM-DD."""
        try:
            dia, mes, ano = data_br.split("/")
            return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
        except:
            return ""
