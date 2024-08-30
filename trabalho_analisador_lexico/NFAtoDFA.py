from collections import defaultdict


class NFA:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = defaultdict(lambda: defaultdict(set))
        self.estado_inicial = None
        self.estados_finais = set()

    def adicionar_estado(self, estado, final=False, inicial=False):
        self.estados.add(estado)
        if final:
            self.estados_finais.add(estado)
        if inicial:
            self.estado_inicial = estado

    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        self.transicoes[estado_origem][simbolo].add(estado_destino)
        if simbolo != '':
            self.alfabeto.add(simbolo)

    def __str__(self):
        result = "Estados: " + str(self.estados) + "\n"
        result += "Estado Inicial: " + str(self.estado_inicial) + "\n"
        result += "Estados Finais: " + str(self.estados_finais) + "\n"
        result += "Transições:\n"
        for origem, transicoes in self.transicoes.items():
            for simbolo, destinos in transicoes.items():
                result += f"  {origem} --{simbolo}--> {destinos}\n"
        return result


class DFA:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = defaultdict(dict)
        self.estado_inicial = None
        self.estados_finais = set()

    def adicionar_estado(self, estado, final=False, inicial=False):
        self.estados.add(estado)
        if final:
            self.estados_finais.add(estado)
        if inicial:
            self.estado_inicial = estado

    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        self.transicoes[estado_origem][simbolo] = estado_destino

    def __str__(self):
        result = "Estados: " + str(self.estados) + "\n"
        result += "Estado Inicial: " + str(self.estado_inicial) + "\n"
        result += "Estados Finais: " + str(self.estados_finais) + "\n"
        result += "Transições:\n"
        for origem, transicoes in self.transicoes.items():
            for simbolo, destino in transicoes.items():
                result += f"  {origem} --{simbolo}--> {destino}\n"
        return result


def epsilon_closure(nfa, estados):
    """
    Calcula o epsilon-closure de um conjunto de estados do NFA.
    """
    stack = list(estados)
    closure = set(estados)

    while stack:
        estado = stack.pop()
        for next_estado in nfa.transicoes[estado]['']:
            if next_estado not in closure:
                closure.add(next_estado)
                stack.append(next_estado)

    return closure


def mover(nfa, estados, simbolo):
    """
    Move para o conjunto de estados alcançáveis usando o símbolo fornecido.
    """
    next_estados = set()
    for estado in estados:
        if simbolo in nfa.transicoes[estado]:
            next_estados.update(nfa.transicoes[estado][simbolo])
    return next_estados


def nfa_para_dfa(nfa):
    """
    Converte um NFA para um DFA usando o algoritmo de subset construction.
    """
    dfa = DFA()
    estado_inicial = epsilon_closure(nfa, {nfa.estado_inicial})
    estados_processados = {}
    estados_ativos = [estado_inicial]
    estados_nomes = {frozenset(estado_inicial): "Q0"}
    dfa.adicionar_estado(
        estados_nomes[frozenset(estado_inicial)], inicial=True)
    dfa.alfabeto = nfa.alfabeto

    while estados_ativos:
        atual = estados_ativos.pop()
        atual_nome = estados_nomes[frozenset(atual)]

        for simbolo in dfa.alfabeto:
            next_estados = epsilon_closure(nfa, mover(nfa, atual, simbolo))
            if not next_estados:
                continue

            next_nome = estados_nomes.get(frozenset(next_estados))
            if next_nome is None:
                next_nome = f"Q{len(estados_nomes)}"
                estados_nomes[frozenset(next_estados)] = next_nome
                dfa.adicionar_estado(next_nome)
                estados_ativos.append(next_estados)

            dfa.adicionar_transicao(atual_nome, simbolo, next_nome)

        if atual & nfa.estados_finais:
            dfa.estados_finais.add(atual_nome)

    return dfa


# Exemplo de uso
def teste_nfa_com_epsilon():
    # Definição do NFA de exemplo
    nfa = NFA()
    nfa.adicionar_estado('q0', inicial=True)
    nfa.adicionar_estado('q1')
    nfa.adicionar_estado('q2', final=True)

    nfa.adicionar_transicao('q0', 'a', 'q1')
    nfa.adicionar_transicao('q1', 'b', 'q1')
    nfa.adicionar_transicao('q1', '', 'q2')  # transição epsilon

    print("NFA:")
    print(nfa)

    # Converta o NFA para DFA
    dfa = nfa_para_dfa(nfa)

    print("\nDFA:")
    print(dfa)


def teste_nfa_com_simbolos_diferentes():
    nfa = NFA()
    nfa.adicionar_estado('q0', inicial=True)
    nfa.adicionar_estado('q1')
    nfa.adicionar_estado('q2', final=True)

    nfa.adicionar_transicao('q0', 'a', 'q1')
    nfa.adicionar_transicao('q0', 'c', 'q2')
    nfa.adicionar_transicao('q1', 'b', 'q2')

    print("NFA (com transições para diferentes símbolos):")
    print(nfa)

    dfa = nfa_para_dfa(nfa)

    print("\nDFA (convertido do NFA com diferentes símbolos):")
    print(dfa)


def teste_nfa_com_varios_estados_finais():
    nfa = NFA()
    nfa.adicionar_estado('q0', inicial=True)
    nfa.adicionar_estado('q1')
    nfa.adicionar_estado('q2', final=True)
    nfa.adicionar_estado('q3', final=True)

    nfa.adicionar_transicao('q0', 'a', 'q1')
    nfa.adicionar_transicao('q1', 'b', 'q2')
    nfa.adicionar_transicao('q1', 'c', 'q3')

    print("NFA (com vários estados finais):")
    print(nfa)

    dfa = nfa_para_dfa(nfa)

    print("\nDFA (convertido do NFA com vários estados finais):")
    print(dfa)


def teste_nfa_com_multiplas_transicoes():
    nfa = NFA()
    nfa.adicionar_estado('q0', inicial=True)
    nfa.adicionar_estado('q1')
    nfa.adicionar_estado('q2', final=True)

    nfa.adicionar_transicao('q0', 'a', 'q1')
    nfa.adicionar_transicao('q0', 'a', 'q2')

    print("NFA (com múltiplas transições para o mesmo símbolo):")
    print(nfa)

    dfa = nfa_para_dfa(nfa)

    print("\nDFA (convertido do NFA com múltiplas transições):")
    print(dfa)


if __name__ == "__main__":
    print("Teste 1: NFA com transições epsilon\n")
    teste_nfa_com_epsilon()

    print("\nTeste 2: NFA com múltiplas transições para o mesmo símbolo\n")
    teste_nfa_com_multiplas_transicoes()

    print("\nTeste 3: NFA com transições para diferentes símbolos\n")
    teste_nfa_com_simbolos_diferentes()

    print("\nTeste 4: NFA com vários estados finais\n")
    teste_nfa_com_varios_estados_finais()
