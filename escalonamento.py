import random
import queue

def escalonar(nome_arquivo: str):
    arquivo = open(nome_arquivo, 'r')
    cabecalho = arquivo.readline().split('|')
    linha_atual = arquivo.readline().split('|')
    nomeProcesso, PID, tempo, prioridade, UID, qtmemoria = linha_atual[2], linha_atual[3], linha_atual[4], linha_atual[5], linha_atual[6], linha_atual[7]
    algorimo_escalonamento, fracao_cpu = cabecalho[0], cabecalho[1]
    for i in range(0, 100):
        print(arquivo.readline())
    if cabecalho[0] == 'alternanciaCircular':
        alt_circ()
    if cabecalho[0] == 'loteria':
        loteria()
    if cabecalho[0] == 'prioridade':
        prioridade()
    
def alt_circ():
    queue = [] 
    for i in range (0, 100):
        queue.append(arquivo.readline())
    for j in range (0, len(queue)):
        queue[j].linha_atual[4] = linha_atual[4] - cabecalho[1]
        queue.append(queue[j])

def prioridade():
    

def loteria():






if __name__ == "__main__":

    print("Bem-vindo ao gerador de arquivos de entrada para o escalonador!")
    print("Escolha o algoritmo: 1: alternancia circular, 2: prioridade, 3: loteria")
    alg = int(input())
    print("Informe a fracao de CPU que cada processo tera direito por vez")
    clock = int(input())
    print("Informe o numero de processos a serem criados")
    numProcessos = int(input())
    
    if alg == 1:
        A = "alternanciaCircular"
    elif alg == 2:
        A = "prioridade"
    elif alg == 3:
        A = "loteria"
    else:
        print("O algoritmo informado nao existe")
        exit()

    out = open("entradaEscalonador.txt", 'w')

    out.write(A+"|"+str(clock)+"\n")

    for i in range (0, numProcessos):
        tempo = random.randrange(1,10)*clock
        prioridade = random.randrange(1, 100)
        UID = random.randrange(1,10)
        memoria = random.randrange(1,10)*1024
        out.write("processo-"+str(i)+"|"+str(i)+"|"+str(tempo)+"|"+str(prioridade)+"|"+str(UID)+"|"+str(memoria)+"\n")

    out.close()