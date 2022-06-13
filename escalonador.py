# Uma thread pra escalonar e outra pra pegar a entrada do teclado
from queue import Queue
from threading import Thread
from classes.bilhete import Bilhete
from classes.processo import Processo

arquivo_entrada = ''
tempo_cpu = 0

def loteria(lista: list, fracao_cpu: int):
    processos_concluidos = 0
    iteracoes = 0
    for processo in lista:
        processo.gerar_bilhetes()
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(lista) > 0:
            iteracoes += 1
            processo_sorteado = Processo.sortear()
            processo_sorteado.reduz_tempo_execucao(fracao_cpu)
            if processo_sorteado.acabou() and processo_sorteado in lista:
                lista.remove(processo_sorteado)
                tempo_executado = (iteracoes * fracao_cpu) + processo_sorteado.tempo_execucao
                log.write(f"processo {processo_sorteado.nome} finalizado em {tempo_executado} segundos.\n")
                processos_concluidos += 1
        print(f'Foram concluídos {processos_concluidos} processos.')
        return

def alternanciaCircular(fila: Queue, fracao_cpu: int):
    processos_concluidos = 0
    iteracoes = 0
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while not fila.empty():
            iteracoes += 1
            processo = fila.get()
            processo.reduz_tempo_execucao(fracao_cpu)
            if processo.tempo_execucao > 0:
                fila.put(processo)
            else:
                tempo_executado = (iteracoes * fracao_cpu) + processo.tempo_execucao
                log.write(f"processo {processo.nome} finalizado em {tempo_executado} segundos.\n")
                processos_concluidos += 1
        print(f'Foram concluídos {processos_concluidos} processos.')
        return

def prioridades(lista: list, fracao_cpu: int):
    processos_concluidos = 0
    iteracoes = 0
    global arquivo_entrada
    with open(f'log-{arquivo_entrada}.txt', 'w') as log:
        while len(lista) > 0:
            lista.sort(key=lambda x: x.prioridade, reverse=True)
            for processo in lista:
                prioridade_mais_alta = lista[0].prioridade
                if processo.prioridade == prioridade_mais_alta:
                    processo.reduz_tempo_execucao(fracao_cpu)
                    if processo.acabou() and processo in lista:
                        lista.remove(processo)
                        tempo_executado = (iteracoes * fracao_cpu) + processo.tempo_execucao
                        log.write(f"processo {processo.nome} finalizado em {tempo_executado} segundos.\n")
                        processos_concluidos += 1
            iteracoes += 1
        print(f'Foram concluídos {processos_concluidos} processos.')
        return

def escalonar(nome_arquivo: str):
    numero_de_processos = 0
    with open(nome_arquivo, 'r') as arquivo:
        numero_de_processos += len(arquivo.readlines()) - 1
    with open(nome_arquivo, 'r') as arquivo:
        cabecalho = arquivo.readline().split('|')
        algoritmo_escalonamento, fracao_cpu = cabecalho[0], int(cabecalho[1])
        match algoritmo_escalonamento:
            case 'alternanciaCircular':
                fila = Queue()
                while linha := arquivo.readline():
                    linha = linha.strip()
                    linha = linha.split('|')
                    fila.put(Processo(linha[0], int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4]), int(linha[5])))
                alternanciaCircular(fila, fracao_cpu)

            case 'loteria':
                Bilhete.valor_maximo = numero_de_processos
                lista = list()
                while linha := arquivo.readline():
                    linha = linha.strip()
                    linha = linha.split('|')
                    lista.append(Processo(linha[0], int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4]), int(linha[5])))
                loteria(lista, fracao_cpu)

            case 'prioridade':
                lista = list()
                while linha := arquivo.readline():
                    linha = linha.strip()
                    linha = linha.split('|')
                    lista.append(Processo(linha[0], int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4]), int(linha[5])))
                prioridades(lista, fracao_cpu)

            case _:
                print('Algoritmo de escalonamento não reconhecido')    

def main():
    entrada = input().split(' ')
    if comando := entrada[0] == 'escalonar':
        if (nome_arquivo := entrada[1]).endswith('.txt'):
            global arquivo_entrada
            arquivo_entrada = nome_arquivo[:-4]
            escalonar(nome_arquivo)
    return False

if __name__ == '__main__':
    main()