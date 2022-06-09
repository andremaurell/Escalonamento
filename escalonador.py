# Uma thread pra escalonar e outra pra pegar a entrada do teclado
from queue import Queue
from random import randint
from re import A, X
from threading import Thread

class Bilhete:
    bilhetes = []
    valor_maximo = 0

    def __init__(self):
        pass
#    ''' def gerar(self, lista:list):
#         for i in range(0, len(lista))
#         processo.prioridade

#     def gerar(self):
#         while (bilhete := randint(0, Bilhete.valor_maximo)) in Bilhete.bilhetes_gerados:
#             bilhete = randint(1, Bilhete.valor_maximo)
#         self.numero = bilhete
#         Bilhete.bilhetes_gerados.append(bilhete)
#         Bilhete.ordenar()
#         return'''
    def __str__(self):
        return str(self.numero)
    
    def __repr__(self):
        return self.__str__
    
    def ordenar():
        Bilhete.bilhetes_gerados.sort()

tempo_executado = 0

class Processo:
    def __init__(self, nome: str, PID: int, tempo_execucao: int, prioridade: int, UID: int, quantidade_de_memoria: int, bilhete: Bilhete = None):
        self.nome = nome
        self.PID = PID
        self.tempo_execucao = tempo_execucao
        self.prioridade = prioridade
        self.UID = UID
        self.quantidade_de_memoria = quantidade_de_memoria
        self.bilhete = bilhete

        

    def relogio(self, fracao_cpu):
        global tempo_executado
        if self.tempo_execucao - fracao_cpu > 0:
            tempo_executado += fracao_cpu
        elif self.tempo_execucao - fracao_cpu < 0:
            tempo_executado += self.tempo_execucao
    
    def __str__(self):
        return f"{self.nome}|{self.PID}|{self.tempo_execucao}|{self.prioridade}|{self.UID}|{self.quantidade_de_memoria}"
    
    def __repr__(self):
        return self.__str__()

    def reduz_tempo_execucao(self, fracao_cpu: int):
        self.tempo_execucao -= fracao_cpu
    
    def acabou(self):
        return self.tempo_execucao <= 0

def loteria(lista: list, fracao_cpu: int):
    processos_concluidos = 0
    dicionario_processos = {}
    dicionario_bilhetes = {}
    # gerar os bilhetes
    total = 0
    for i in range(0, len(lista)):
        num_bilhetes = lista[i].prioridade
        for x in range(total, total+num_bilhetes):
            dicionario_processos[lista[i]] = x
            dicionario_bilhetes[x] = lista[i]
        total+=num_bilhetes
    while len(lista) > 0:
        Num_sort = randint(0, total-1)
        processo = dicionario_bilhetes[Num_sort]
        processo.reduz_tempo_execucao(fracao_cpu)
        processo.relogio(fracao_cpu)
        if processo.acabou():
            if processo in lista:
                lista.remove(processo)
                print(f"processo {processo.nome} finalizado em {tempo_executado} segundos.")
                processos_concluidos += 1
                
        
        
    print(f'Foram concluídos {processos_concluidos} processos.')
    return

def alternanciaCircular(fila: Queue, fracao_cpu: int):
    processos_concluidos = 0
    while not fila.empty():
        processo = fila.get()
        processo.reduz_tempo_execucao(fracao_cpu)
        processo.relogio(fracao_cpu)
        if processo.tempo_execucao > 0:
            fila.put(processo)
        else:
            print(f"processo {processo.nome} finalizado em {processo.tempo_executado} segundos.")
            processos_concluidos += 1
    print(f'Foram concluídos {processos_concluidos} processos.')
    return

def prioridades():
    
    pass

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
                #for elemento in lista:
                    #print(elemento)
                loteria(lista, fracao_cpu)

            case 'prioridades':
                pass

            case _:
                print('Algoritmo de escalonamento não reconhecido')    
        


def main():
    entrada = input().split(' ')
    if comando := entrada[0] == 'escalonar':
        if (nome_arquivo := entrada[1]).endswith('.txt'):
            escalonar(nome_arquivo)
    return False

    # arquivo = open('loteria.txt', 'r')
    # arquivo.readlines()

if __name__ == '__main__':
    main()