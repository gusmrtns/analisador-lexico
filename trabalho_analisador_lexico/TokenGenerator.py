import re

# Definindo os tipos de tokens
# Cada entrada no dicionário 'TOKEN_TYPES' associa um nome de token a uma expressão regular
TOKEN_TYPES = {
    # Identificadores começam com uma letra ou '_', seguidos por letras, números ou '_'
    'IDENTIFICADOR': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INTEIRO': r'\d+',  # Inteiros são sequências de dígitos (0-9)
    # Strings são delimitadas por aspas duplas e permitem escapes (ex: \" dentro da string)
    'STRING': r'"(?:\\.|[^"\\])*"',
    # Operadores incluem os caracteres +, -, *, /, =, <, >, ou ,
    'OPERADOR': r'[+\-*/=<>,]',
    'SEPARADOR': r'[();,]',  # Separadores incluem os caracteres ;, (, ) e ,
    # Palavras reservadas como 'int' e 'string', delimitadas por \b para garantir que são palavras completas
    'PALAVRA_RESERVADA': r'\b(int|string)\b'
}

# Função para gerar tokens a partir de um código-fonte


def gerar_tokens(codigo):
    # Cria uma expressão regular combinando todas as regexes definidas em 'TOKEN_TYPES'
    # A função 'join' combina todos os padrões de regex em uma única expressão regular, onde cada padrão é nomeado
    token_regex = '|'.join(
        f'(?P<{tipo}>{regex})' for tipo, regex in TOKEN_TYPES.items())

    # Compila a expressão regular combinada para ser usada na correspondência de tokens
    token_re = re.compile(token_regex)

    tokens = []

    # Itera sobre o código-fonte para identificar tokens
    # O método 'finditer' retorna um iterador sobre todas as correspondências encontradas no 'codigo'
    for match in token_re.finditer(codigo):
        # 'lastgroup' retorna o nome do grupo correspondente (o tipo do token)
        tipo = match.lastgroup
        # 'group' retorna o valor correspondente ao padrão do token no código-fonte
        valor = match.group(tipo)

        # Verifica se o token é uma palavra reservada
        if tipo == 'PALAVRA_RESERVADA':
            # Adiciona o token à lista com o tipo 'PALAVRA_RESERVADA'
            tokens.append((tipo, valor))
        elif tipo == 'IDENTIFICADOR' and valor in ['int', 'string']:
            # Trata palavras reservadas identificadas como 'IDENTIFICADOR'
            tokens.append(('PALAVRA_RESERVADA', valor))
        else:
            # Adiciona o token à lista com o tipo e valor identificados
            tokens.append((tipo, valor))

    return tokens

# Função para imprimir os tokens


def imprimir_tokens(tokens):
    for tipo, valor in tokens:
        print(f'Tipo: {tipo}, Valor: {valor}')


def test(codigo_fonte):
    tokens = gerar_tokens(codigo_fonte)
    imprimir_tokens(tokens)


if __name__ == '__main__':
    codigo_fonte = """
        int x = 10;
        string y = "hello";
        int z = x + 20;
    """
    test(codigo_fonte)
