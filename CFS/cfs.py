import sys

#### Implementação da árvore vermelha e preto ####
# Node creation
class Node():
    def __init__(self, item):
        self.item = item
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1


class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    # Preorder
    def pre_order_helper(self, node):
        if node != TNULL:
            sys.stdout.write(node.item + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    # Inorder
    def in_order_helper(self, node):
        if node != TNULL:
            self.in_order_helper(node.left)
            sys.stdout.write(node.item + " ")
            self.in_order_helper(node.right)

    # Postorder
    def post_order_helper(self, node):
        if node != TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            sys.stdout.write(node.item + " ")

    # Procura de nó na árvore
    def search_tree_helper(self, node, key):
        if node == TNULL or key == node.item:
            return node

        if key < node.item:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # Balanceamento da árvore pós inserção 
    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Exclusão de nó
    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.item == key:
                z = node

            if node.item <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    # Balanceamento da árvore após inserção
    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    # Imprimindo a árvore
    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.item) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def searchTree(self, k):
        return self.search_tree_helper(self.root, k)

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self,  x):
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.item = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.item < x.item:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.item < y.item:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def get_root(self):
        return self.root
        #return self.root.item

    def delete_node(self, item):
        self.delete_node_helper(self.root, item)
    
    def print_tree(self):
      self.__print_helper(self.root, "", True)

    #percorrer nó mais a esquerda da árvore
    def menorNodo(self,node):
      while node.left != self.TNULL:
        node = node.left
      return node.item

######### fim da árvore ############

#execução do escalonamento

arquivo = open('cfs.txt', 'r')
total_list = []

#inserção de todos os processos em uma lista
unit_list = []
for line in arquivo:
  a = line.split("|")
  unit_list.append(a)

for i in range(len(unit_list)):
  unit_list[i].append(0)

#inicialização de árvore e
#inserção do tempo de uso nos nós da árvore
bst = RedBlackTree()
for i in range(len(unit_list)):
    no = unit_list[i][2]
    bst.insert(int(no)) 

#inicialização da execução de processos
while int(len(unit_list)) != 0:   
    
  #busca pelo nó mais a esquerda da árvore
  b = bst.get_root()
  mostleft = int(bst.menorNodo(b))
  tempo = int(mostleft)
  bst.delete_node(tempo)

  #seleção de processos que possuem o mesmo tempo de execução
  em_exc = []
  for i in range(len(unit_list)):
    if unit_list[i][2] == str(mostleft):
      em_exc.append(unit_list[i])


  #verificação adicional/exclusão de itens desnecessários
  #nota: todos os processos ainda sim são executados, pois
  #o while é encerrado
  while len(em_exc) == 0:
    bst.delete_node(tempo)
    mostleft = int(bst.menorNodo(b))
    tempo = int(mostleft)
    
    em_exc = []
    for i in range(len(unit_list)):
        if unit_list[i][2] == str(mostleft):
            em_exc.append(unit_list[i])    
               
  #seleção do processo que possue maior prioridade         
  maior_prioridade = []
  a = 0
  for i in range(len(em_exc)):
    if int(em_exc[i][3]) > a:
      a = int(em_exc[i][3])
      maior_prioridade.append(em_exc[i])
      
        
  maior_prioridade = maior_prioridade[-1]
  

  #remoção do processo de maior prioridade
  #da lista de processos totais
  for i in range(len(unit_list)):
    if unit_list[i] == maior_prioridade:
      unit_list.remove(unit_list[i])
      break

  #execução do processo pós verificações 
  fcpu = 10 #fração de cpu(pré-estabelecida)
  prc_exec = []
  cont = 0
  while cont != fcpu:
    if tempo == 0:
      maior_prioridade[-1] =  int(maior_prioridade[-1]) + (fcpu * int(maior_prioridade[3])) 
      prc_exec.append(maior_prioridade[0])
      print(maior_prioridade[0], ' executado!')
      print('tempo de execução: ',maior_prioridade[-1])
      break
    else:
      maior_prioridade[-1] =  int(maior_prioridade[-1]) + (fcpu * int(maior_prioridade[3])) 
      tempo -= 1
    cont += 1 
    
    
  #caso o processo ainda tenha tempo de uso:
  if tempo != 0:
    maior_prioridade[2] = str(tempo)
    unit_list.append(maior_prioridade)
    
    for i in range(len(unit_list)):
        no = unit_list[i][2]
        bst.insert(int(no)) 


