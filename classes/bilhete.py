from random import randint


class Bilhete:
    total = 0
    dicionario_processos = {}
    bilhetes_de_processos_que_acabaram = []
    # implementar resorteamento de bilhetes de processos que já acabaram

    def sortear():
        return randint(0, Bilhete.total-1)
