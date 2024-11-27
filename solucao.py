from datetime import timedelta, datetime

def ler_propostas(caminho_arquivo):
    propostas = []
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.rsplit(' ', 1)
            titulo = partes[0].strip()
            duracao_str = partes[1].strip()
            if duracao_str == "lightning":
                duracao = 5
            else:
                duracao = int(duracao_str.replace("min", ""))
            propostas.append((titulo, duracao))
    return propostas

def merge_sort(propostas):
    if len(propostas) <= 1:
        return propostas
    meio = len(propostas) // 2
    esquerda = merge_sort(propostas[:meio])
    direita = merge_sort(propostas[meio:])
    return merge(esquerda, direita)

def merge(esquerda, direita):
    lista_ordenada = []
    while esquerda and direita:
        if esquerda[0][1] > direita[0][1]:
            lista_ordenada.append(esquerda.pop(0))
        else:
            lista_ordenada.append(direita.pop(0))
    lista_ordenada.extend(esquerda or direita)
    return lista_ordenada

def organizar_sessoes(propostas):
    sessao_manha = preencher_sessao(propostas, 180)  
    sessao_tarde = preencher_sessao(propostas, 240)  
    return sessao_manha, sessao_tarde

def preencher_sessao(propostas, duracao_maxima):
    sessao = []
    tempo_total = 0
    propostas_restantes = []
    for proposta in propostas:
        if tempo_total + proposta[1] <= duracao_maxima:
            sessao.append(proposta)
            tempo_total += proposta[1]
        else:
            propostas_restantes.append(proposta)
    propostas[:] = propostas_restantes  
    return sessao

def formatar_cronograma(sessoes):
    cronograma = []
    horario_atual = datetime.strptime("09:00", "%H:%M")
    for nome_sessao, sessao in sessoes:
        cronograma.append(nome_sessao)
        for titulo, duracao in sessao:
            cronograma.append(f"{horario_atual.strftime('%H:%M')} {titulo} {duracao}min")
            horario_atual += timedelta(minutes=duracao)
        if "manhã" in nome_sessao:
            cronograma.append("12:00 Almoço")
            horario_atual = datetime.strptime("13:00", "%H:%M")
        else:
            cronograma.append("16:00 Evento de Networking")
    return "\n".join(cronograma)

def main():
    propostas = ler_propostas("mini-conferencia.txt")
    propostas_ordenadas = merge_sort(propostas)
    
    sessao_manha, sessao_tarde = organizar_sessoes(propostas_ordenadas)
    
    sessoes = [
        ("Trilha 1 - Sessão da manhã", sessao_manha),
        ("Trilha 2 - Sessão da tarde", sessao_tarde)
    ]
    
    cronograma = formatar_cronograma(sessoes)
    print(cronograma)

if __name__ == "__main__":
    main()
