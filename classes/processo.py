from .bilhete import Bilhete

class Processo:
    # implementar resorteamento de bilhetes de processos que já acabaram
    dicionario_bilhetes = {}

    def __init__(self, nome: str, PID: int, tempo_execucao: int, prioridade: int, UID: int, quantidade_de_memoria: int):
        self.nome = nome
        self.PID = PID
        self.tempo_execucao = tempo_execucao
        self.prioridade = prioridade
        self.UID = UID
        self.quantidade_de_memoria = quantidade_de_memoria
        self.bilhetes = []
    
    def __str__(self):
        return f"{self.nome}|{self.PID}|{self.tempo_execucao}|{self.prioridade}|{self.UID}|{self.quantidade_de_memoria}"
    
    def __repr__(self):
        return self.__str__()

    def reduz_tempo_execucao(self, fracao_cpu: int):
        self.tempo_execucao -= fracao_cpu
    
    def acabou(self):
        return self.tempo_execucao <= 0
    
    def gerar_bilhetes(self):
        numero_de_bilhetes = self.prioridade
        for numero_bilhete in range(Bilhete.total, Bilhete.total+numero_de_bilhetes):
            Processo.dicionario_bilhetes[numero_bilhete] = self
            self.bilhetes.append(numero_bilhete)
        Bilhete.dicionario_processos[self] = self.bilhetes
        Bilhete.total += numero_de_bilhetes
    
    def sortear():
        return Processo.dicionario_bilhetes[Bilhete.sortear()]
