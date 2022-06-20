from time import sleep
from queue import Queue
from threading import Thread
from classes.processo import Processo

# ========================================================================= #
#                                                                           #
#     Constantes que podem ser ajustadas manualmente, caso necessário       #
#                                                                           #
# ========================================================================= #
QUEUE = 'Queue'
LIST = 'list'
ALTERNANCIA_CIRCULAR = 'alternanciaCircular'
LOTERIA = 'loteria'
PRIORIDADE = 'prioridade'
DELAY = 0.0005

# ========================================================================= #
#                                                                           #
#          Variáveis globais que serão manipuladas pelas funções            #
#                                                                           #
# ========================================================================= #
arquivo_entrada = ''
algoritmo_escalonamento = ''
estrutura_de_dados = []
processos_concluidos = 0
tempo_cpu = 0
fracao_cpu = 0
iteracoes = 0
escalonador_acabou = False


# ========================================================================= #
#                                                                           #
#           Algoritmo de escalonamento de processos por loteria             #
#                                                                           #
# ========================================================================= #
def loteria():
    global estrutura_de_dados
    global fracao_cpu
    global processos_concluidos
    global iteracoes
    global arquivo_entrada
    for processo in estrutura_de_dados:
        processo.gerar_bilhetes()
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(estrutura_de_dados) > 0:
            iteracoes += 1
            processo_sorteado = Processo.sortear()
            processo_sorteado.reduz_tempo_execucao(fracao_cpu)
            if (processo_sorteado.acabou() and
                    processo_sorteado in estrutura_de_dados):
                estrutura_de_dados.remove(processo_sorteado)
                tempo_executado = ((iteracoes * fracao_cpu) +
                                   processo_sorteado.tempo_execucao)
                log.write(
                    f"processo {processo_sorteado.nome} finalizado em" +
                    f" {tempo_executado} segundos.\n")
                processos_concluidos += 1
            sleep(DELAY)
    return


# ========================================================================= #
#                                                                           #
#     Algoritmo de escalonamento de processos por alternância circular      #
#                                                                           #
# ========================================================================= #
def alternanciaCircular():
    global estrutura_de_dados
    global fracao_cpu
    global processos_concluidos
    global iteracoes
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(estrutura_de_dados) > 0:
            iteracoes += 1
            processo = estrutura_de_dados.pop(0)
            processo.reduz_tempo_execucao(fracao_cpu)
            if processo.tempo_execucao > 0:
                estrutura_de_dados.append(processo)
            else:
                tempo_executado = ((iteracoes * fracao_cpu) +
                                   processo.tempo_execucao)
                log.write(
                    f"processo {processo.nome} finalizado em" +
                    f" {tempo_executado} segundos.\n")
                processos_concluidos += 1
            sleep(DELAY)
    return


# ========================================================================= #
#                                                                           #
#         Algoritmo de escalonamento de processos por prioridades           #
#                                                                           #
# ========================================================================= #
def prioridades():
    global estrutura_de_dados
    global fracao_cpu
    global processos_concluidos
    global iteracoes
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(estrutura_de_dados) > 0:
            iteracoes += 1
            estrutura_de_dados.sort(key=lambda x: x.prioridade, reverse=True)
            for processo in estrutura_de_dados:
                prioridade_mais_alta = estrutura_de_dados[0].prioridade
                if processo.prioridade == prioridade_mais_alta:
                    processo.reduz_tempo_execucao(fracao_cpu)
                    if processo.acabou() and processo in estrutura_de_dados:
                        estrutura_de_dados.remove(processo)
                        tempo_executado = ((iteracoes * fracao_cpu) +
                                           processo.tempo_execucao)
                        log.write(
                            f"processo {processo.nome} finalizado em" +
                            f" {tempo_executado} segundos.\n")
                        processos_concluidos += 1
            sleep(DELAY)
    return


# ========================================================================= #
#                                                                           #
#     Escalonador de processos, que recebe o arquivo de entrada,            #
#     seta algumas variáveis globais e chama a função de escalonamento      #
#     apropriada, conforme estabelecido no arquivo. (Também é a thread      #
#     principal).                                                           #
#                                                                           #
# ========================================================================= #
def escalonar(nome_arquivo: str):
    global escalonador_acabou
    global algoritmo_escalonamento
    global estrutura_de_dados
    global fracao_cpu
    global processos_concluidos
    with open(nome_arquivo, 'r') as arquivo:
        cabecalho = arquivo.readline().split('|')
        algoritmo_escalonamento = str(cabecalho[0])
        fracao_cpu = int(cabecalho[1])
        while linha := arquivo.readline():
            linha = linha.strip()
            linha = linha.split('|')
            estrutura_de_dados.append(
                Processo(
                    nome=linha[0],
                    PID=int(linha[1]),
                    tempo_execucao=int(linha[2]),
                    prioridade=int(linha[3]),
                    UID=int(linha[4]),
                    quantidade_de_memoria=int(linha[5])
                )
            )
        match algoritmo_escalonamento:
            case str(ALTERNANCIA_CIRCULAR):
                alternanciaCircular()
            case str(LOTERIA):
                loteria()
            case str(PRIORIDADE):
                prioridades()
            case _:
                print('Algoritmo de escalonamento não reconhecido')
    print(f'Foram concluídos {processos_concluidos} processos.')
    escalonador_acabou = True
    return


# ========================================================================= #
#                                                                           #
#     Função que é recebe inputs infinitos do usuário, até que a thread     #
#     principal acabe. (Thread secundária).                                 #
#                                                                           #
# ========================================================================= #
def ao_pressionar():
    global estrutura_de_dados
    global escalonador_acabou
    global algoritmo_escalonamento

    while not escalonador_acabou:
        novo_processo = str(input())
        if novo_processo == '':
            continue
        novo_processo = novo_processo.split('|')
        novo_processo = Processo(
            nome=novo_processo[0],
            PID=int(novo_processo[1]),
            tempo_execucao=int(novo_processo[2]),
            prioridade=int(novo_processo[3]),
            UID=int(novo_processo[4]),
            quantidade_de_memoria=int(novo_processo[5])
        )
        if algoritmo_escalonamento == 'loteria':
            novo_processo.gerar_bilhetes()
        if type(estrutura_de_dados) == Queue:
            estrutura_de_dados.put(novo_processo)
        elif type(estrutura_de_dados) == list:
            estrutura_de_dados.append(novo_processo)
        else:
            print('Algoritmo de escalonamento não reconhecido')


# ========================================================================= #
#                                                                           #
#     Função principal que ativa as threads e faz a leitura do arquivo      #
#     de processos a serem escalonados.                                     #
#                                                                           #
# ========================================================================= #
def main():
    thread_principal = None

    entrada = input().split(' ')
    if ((comando := entrada[0] == 'escalonar') and
            (nome_arquivo := entrada[1]).endswith('.txt')):
        global arquivo_entrada
        arquivo_entrada = nome_arquivo[:-4]
        thread_principal = Thread(target=escalonar, args=(nome_arquivo,))
    else:
        print('Comando não reconhecido')
        return -1

    thread_teclado = Thread(target=ao_pressionar)

    thread_principal.start()
    thread_teclado.start()

    thread_principal.join()
    thread_teclado.join()


if __name__ == '__main__':
    main()
