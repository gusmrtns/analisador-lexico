import re

class LexicalAnalyzer:
    def __init__(self):
        # Definindo padrões para tokens conhecidos
        self.patterns = [
            (r'\bint\b', 'INT'),
            (r'\bstring\b', 'STRING'),
            (r'=', 'EQ'),
            (r'\d+', 'NUM'),
            (r'"[^"]*"', 'CONST'),
            (r'\+', 'ADD'),
            (r';', 'SEMICOLON'),
            (r'[a-zA-Z_][a-zA-Z_0-9]*', 'VAR'),  # Identificador
        ]
        # Lista de palavras-chave válidas
        self.keywords = {"int", "string"}

    def tokenize(self, code):
        tokens = []
        for line in code.splitlines():
            token_list = self._tokenize_line(line.strip())
            tokens.append(" ".join(token_list))
        return "\n".join(tokens)

    def _tokenize_line(self, line):
        tokens = []
        pos = 0
        length = len(line)

        while pos < length:
            matched = False
            for pattern, token_type in self.patterns:
                regex = re.compile(pattern)
                match = regex.match(line, pos)

                if match:
                    token = match.group(0).strip()

                    # Se for um identificador, verificar se é uma palavra-chave
                    if token_type == "VAR":
                        if token in self.keywords:
                            tokens.append(token.upper())  # Palavra-chave
                        else:
                            tokens.append("VAR")  # Identificador
                    else:
                        tokens.append(token_type)  # Outro token padrão
                    
                    pos = match.end()
                    matched = True
                    break

            if not matched:
                # Se nenhum padrão foi correspondido, marcar como "ERRO"
                tokens.append("ERRO")
                pos += 1

            # Ignorar espaços entre tokens
            while pos < length and line[pos].isspace():
                pos += 1

        return tokens

# Exemplo de uso
if __name__ == "__main__":
    code = """
    int a = 0 ;
    in b = 5 + a ;
    string c = "teSte" ;
    """

    analyzer = LexicalAnalyzer()
    result = analyzer.tokenize(code.strip())
    print(result)
