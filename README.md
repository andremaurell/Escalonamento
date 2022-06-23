# Escalonamento
Algoritmos de escalonamento, funcionando como um escalonador de um Sistema Operacional.
Para seu uso, é necessário ter o python 3.10.4 instalado e abrir um terminal na mesma pasta que o arquivo _escalonador.py_, e executar o comando:
```
python3 escalonador.py
```
e, após, seguir as instruções escritas no terminal para executá-lo.

## Arquivos
Os arquivos _loteria.txt_, _prioridades.txt_ e _alternancia.txt_ são os processos pedidos para serem executados por cada tipo de escalonamento, respectivo
a seu nome.

A pasta classes possui dois códigos distintos: _bilhete.py_, para auxiliar na lógica dos bilhetes, e _processos.py_, para auxiliar na lógica dos processos.

A pasta CFS condiz ao escalonador Completely Fair Scheduler, do Linux. Há dois arquivos dentro dela: _cfs.py_ e _cfs.txt_, sendo possível executar o _cfs.py_, utilizando _python3 cfs.py_ para simular o escalonador utilizado no Linux. Esta pasta não é necessária para o funcionamento do escalonador.

O arquivo _escalonador.py_ é o escalonador propriamente dito, e o código princial que deve ser executado para tudo funcionar corretamente.

