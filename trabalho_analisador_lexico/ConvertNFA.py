import re


class NFA:
    def __init__(self):
        self.estados = set()
        self.estado_inicial = None
        self.estados_finais = set()
        self.transicoes = {}
        self.next_id = 0

    def novo_estado(self):
        estado_id = f"q{self.next_id}"
        self.next_id += 1
        self.estados.add(estado_id)
        return estado_id

    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        if (estado_origem, simbolo) not in self.transicoes:
            self.transicoes[(estado_origem, simbolo)] = set()
        self.transicoes[(estado_origem, simbolo)].add(estado_destino)

    def __str__(self):
        transicoes_str = "\n".join(
            f"({origem}, '{simbolo}') -> {destinos}"
            for (origem, simbolo), destinos in self.transicoes.items()
        )
        return (
            f"Estado Inicial: {self.estado_inicial}\n"
            f"Estados Finais: {self.estados_finais}\n"
            f"Transições:\n{transicoes_str}"
        )


def criar_nfa_combinado(token_types):
    nfa_combinado = NFA()
    estado_inicial = nfa_combinado.novo_estado()
    nfa_combinado.estado_inicial = estado_inicial

    for token, expressao_regular in token_types.items():
        if token == 'PALAVRA_RESERVADA':
            nfa_token = converter_para_nfa_palavras_reservadas(
                expressao_regular)
        else:
            nfa_token = converter_para_nfa(expressao_regular)
        nfa_combinado.adicionar_transicao(
            estado_inicial, '', nfa_token.estado_inicial)
        nfa_combinado.estados.update(nfa_token.estados)
        nfa_combinado.transicoes.update(nfa_token.transicoes)
        nfa_combinado.estados_finais.update(nfa_token.estados_finais)

    return nfa_combinado


def converter_para_nfa_palavras_reservadas(expressao_regular):
    nfa = NFA()
    estado_inicial = nfa.novo_estado()
    nfa.estado_inicial = estado_inicial

    palavras_reservadas = re.findall(r'\b(\w+)\b', expressao_regular)

    for palavra in palavras_reservadas:
        estado_final = nfa.novo_estado()
        nfa.adicionar_transicao(estado_inicial, palavra, estado_final)
        nfa.estados_finais.add(estado_final)

    return nfa


def converter_para_nfa(expressao_regular):
    nfa = NFA()
    estado_inicial = nfa.novo_estado()
    estado_atual = estado_inicial

    i = 0
    while i < len(expressao_regular):
        char = expressao_regular[i]

        if char == '[':  # Início de um conjunto de caracteres
            i += 1
            conjunto = set()
            while expressao_regular[i] != ']':
                if i + 2 < len(expressao_regular) and expressao_regular[i+1] == '-':
                    for c in range(ord(expressao_regular[i]), ord(expressao_regular[i+2]) + 1):
                        conjunto.add(chr(c))
                    i += 3
                else:
                    conjunto.add(expressao_regular[i])
                    i += 1
            estado_novo = nfa.novo_estado()
            for c in conjunto:
                nfa.adicionar_transicao(estado_atual, c, estado_novo)
            estado_atual = estado_novo

        elif char == '\\':  # Tratamento de escape
            i += 1
            estado_novo = nfa.novo_estado()
            nfa.adicionar_transicao(
                estado_atual, expressao_regular[i], estado_novo)
            estado_atual = estado_novo

        # Grupo de não captura
        elif char == '(' and expressao_regular[i+1:i+3] == '?:':
            i += 3
            while expressao_regular[i] != ')':
                if expressao_regular[i] == '\\':
                    i += 1
                estado_novo = nfa.novo_estado()
                nfa.adicionar_transicao(
                    estado_atual, expressao_regular[i], estado_novo)
                estado_atual = estado_novo
                i += 1

        elif char == '\\b':  # Tratamento para borda de palavra
            # Nesse contexto, \b é apenas um delimitador, não adiciona transições.
            i += 1

        else:
            estado_novo = nfa.novo_estado()
            nfa.adicionar_transicao(estado_atual, char, estado_novo)
            estado_atual = estado_novo

        i += 1

    estado_final = estado_atual
    nfa.estado_inicial = estado_inicial
    nfa.estados_finais.add(estado_final)
    return nfa


# Definições de tokens conforme especificado
TOKEN_TYPES = {
    'IDENTIFICADOR': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INTEIRO': r'\d+',
    'STRING': r'"(?:\\.|[^"\\])*"',
    'OPERADOR': r'[+\-*/=<>,]',
    'SEPARADOR': r'[();,]',
    'PALAVRA_RESERVADA': r'\b(int|string)\b'
}

# Criação do NFA combinado
nfa_combinado = criar_nfa_combinado(TOKEN_TYPES)
print(nfa_combinado)
