# Uma thread pra escalonar e outra pra pegar a entrada do teclado
from queue import Queue
from threading import Thread
from classes.bilhete import Bilhete
from classes.processo import Processo


arquivo_entrada = ''
algoritmo_escalonamento = ''
estrutura_de_dados = None
tempo_cpu = 0
escalonador_acabou = False

def loteria(fracao_cpu: int):
    global estrutura_de_dados
    processos_concluidos = 0
    iteracoes = 0
    for processo in estrutura_de_dados:
        processo.gerar_bilhetes()
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(estrutura_de_dados) > 0:
            iteracoes += 1
            processo_sorteado = Processo.sortear()
            processo_sorteado.reduz_tempo_execucao(fracao_cpu)
            if processo_sorteado.acabou() and processo_sorteado in estrutura_de_dados:
                estrutura_de_dados.remove(processo_sorteado)
                tempo_executado = (iteracoes * fracao_cpu) + processo_sorteado.tempo_execucao
                log.write(f"processo {processo_sorteado.nome} finalizado em {tempo_executado} segundos.\n")
                processos_concluidos += 1
        print(f'Foram concluídos {processos_concluidos} processos.')
        return

def alternanciaCircular(fracao_cpu: int):
    global estrutura_de_dados
    processos_concluidos = 0
    iteracoes = 0
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while not estrutura_de_dados.empty():
            iteracoes += 1
            processo = estrutura_de_dados.get()
            processo.reduz_tempo_execucao(fracao_cpu)
            if processo.tempo_execucao > 0:
                estrutura_de_dados.put(processo)
            else:
                tempo_executado = (iteracoes * fracao_cpu) + processo.tempo_execucao
                log.write(f"processo {processo.nome} finalizado em {tempo_executado} segundos.\n")
                processos_concluidos += 1
        print(f'Foram concluídos {processos_concluidos} processos.')
        return

def prioridades(fracao_cpu: int):
    global estrutura_de_dados
    processos_concluidos = 0
    iteracoes = 0
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(estrutura_de_dados) > 0:
            estrutura_de_dados.sort(key=lambda x: x.prioridade, reverse=True)
            for processo in estrutura_de_dados:
                prioridade_mais_alta = estrutura_de_dados[0].prioridade
                if processo.prioridade == prioridade_mais_alta:
                    processo.reduz_tempo_execucao(fracao_cpu)
                    if processo.acabou() and processo in estrutura_de_dados:
                        estrutura_de_dados.remove(processo)
                        tempo_executado = (iteracoes * fracao_cpu) + processo.tempo_execucao
                        log.write(f"processo {processo.nome} finalizado em {tempo_executado} segundos.\n")
                        processos_concluidos += 1
            iteracoes += 1
        print(f'Foram concluídos {processos_concluidos} processos.')
        return

def escalonar(nome_arquivo: str):
    global escalonador_acabou
    with open(nome_arquivo, 'r') as arquivo:
        global algoritmo_escalonamento
        global estrutura_de_dados
        cabecalho = arquivo.readline().split('|')
        algoritmo_escalonamento, fracao_cpu = cabecalho[0], int(cabecalho[1])
        match algoritmo_escalonamento:
            case 'alternanciaCircular':
                estrutura_de_dados = Queue()
                while linha := arquivo.readline():
                    linha = linha.strip()
                    linha = linha.split('|')
                    estrutura_de_dados.put(Processo(linha[0], int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4]), int(linha[5])))
                alternanciaCircular(fracao_cpu)

            case 'loteria':
                estrutura_de_dados = list()
                while linha := arquivo.readline():
                    linha = linha.strip()
                    linha = linha.split('|')
                    estrutura_de_dados.append(Processo(linha[0], int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4]), int(linha[5])))
                loteria(fracao_cpu)

            case 'prioridade':
                estrutura_de_dados = list()
                while linha := arquivo.readline():
                    linha = linha.strip()
                    linha = linha.split('|')
                    estrutura_de_dados.append(Processo(linha[0], int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4]), int(linha[5])))
                prioridades(fracao_cpu)

            case _:
                print('Algoritmo de escalonamento não reconhecido')    
    escalonador_acabou = True

def on_press():
    global estrutura_de_dados
    global escalonador_acabou
    global algoritmo_escalonamento
    
    while not escalonador_acabou:
        novo_processo = input()
        novo_processo = novo_processo.split('|')
        novo_processo = Processo(f'{novo_processo[0]}', int(novo_processo[1]), int(novo_processo[2]), int(novo_processo[3]), int(novo_processo[4]), int(novo_processo[5]))
        if algoritmo_escalonamento == 'loteria':
            novo_processo.gerar_bilhetes()
        if type(estrutura_de_dados) == Queue:
            estrutura_de_dados.put(novo_processo)
        elif type(estrutura_de_dados) == list:
            print(novo_processo)
            estrutura_de_dados.append(novo_processo)
        else:
            print('Algoritmo de escalonamento não reconhecido')



def main():
    thread_principal = None
    entrada = input().split(' ')

    if (comando := entrada[0] == 'escalonar') and (nome_arquivo := entrada[1]).endswith('.txt'):
            global arquivo_entrada
            arquivo_entrada = nome_arquivo[:-4]
            thread_principal = Thread(target=escalonar, args=(nome_arquivo,))
    else:
        print('Comando não reconhecido')
        return -1

    thread_teclado = Thread(target=on_press)
    
    thread_principal.start()
    thread_teclado.start()

    thread_principal.join()
    thread_teclado.join()

if __name__ == '__main__':
    main()