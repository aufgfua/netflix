## Codigo adaptado de https://medium.com/odscjournal/binary-search-tree-implementation-in-python-5f8a50341eaf

# DADO NA ABP NO FORMATO:
# { ID : ID , DADO1: _ , DADO2: _ }


#lista = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

import math
class Abp:
    
    """
    Constructor with vaue we are going 
    to insert in tree with assigning
    left and right child with default None 
    """
    
    def __init__(self, data):
        self.data = data
        self.Left_child = None
        self.Right_child = None
        
    """
    If the data we are inserting already 
    present in tree it will not add it 
    to avoid the duplicate values
    """
        
    def Add_Node(self, data):
        if data['id'] == self.data['id']:
            return # node already exist

        """
        If the data we are inserting is Less
        than the value of the current node, then
        data will insert in Left node
        """
        
        if data['id'] < self.data['id']:
            if self.Left_child:
                self.Left_child.Add_Node(data)
            else:
                self.Left_child = Abp(data)
         
            """
            If the data we are inserting is Greater
            than the value of the current node, then
            data will insert in Right node
            """
            
        else:
            if self.Right_child:
                self.Right_child.Add_Node(data)
            else:
                self.Right_child = Abp(data)


    def Find_Node(self, val):
        
        """
        If current node is equal to 
        data we are finding return true
        """
        
        if self.data['id'] == val:
            return self.data
        
        """
        If current node is lesser than 
        data we are finding we have search 
        in Left child node
        """

        if val < self.data['id']:
            if self.Left_child:
                return self.Left_child.Find_Node(val)
            else:
                return False
        
        """
        If current node is Greater than 
        data we are finding we have search 
        in Right child node
        """

        if val > self.data['id']:
            if self.Right_child:
                return self.Right_child.Find_Node(val)
            else:
                return False
            
    """
    First it will visit Left node then
    it will visit Root node and finally 
    it will visit Right and display a
    list in specific order
    """        

    def In_Order_Traversal_id(self):
        elements = []
        if self.Left_child:
            elements += self.Left_child.In_Order_Traversal_id()

        elements.append(self.data['id'])

        if self.Right_child:
            elements += self.Right_child.In_Order_Traversal_id()

        return elements

    def In_Order_Traversal_data(self):
        elements = []
        if self.Left_child:
            elements += self.Left_child.In_Order_Traversal_data()

        elements.append(self.data)

        if self.Right_child:
            elements += self.Right_child.In_Order_Traversal_data()

        return elements
    
    """
    First it will visit Left node then
    it will visit Right node and finally 
    it will visit Root node  and display a
    list in specific order
    """ 
    
    def Post_Order_Traversal_id(self):
        elements = []
        if self.Left_child:
            elements += self.Left_child.Post_Order_Traversal_id()
        if self.Right_child:
            elements += self.Right_child.Post_Order_Traversal_id()

        elements.append(self.data['id'])

        return elements
    
    def Post_Order_Traversal_data(self):
        elements = []
        if self.Left_child:
            elements += self.Left_child.Post_Order_Traversal_data()
        if self.Right_child:
            elements += self.Right_child.Post_Order_Traversal_data()

        elements.append(self.data)

        return elements
    
    """
    First it will visit Root node then
    it will visit Left node and finally 
    it will visit Right node  and display a
    list in specific order
    """   
    
    def Pre_Order_Traversal_id(self):
        elements = [self.data['id']]
        if self.Left_child:
            elements += self.Left_child.Pre_Order_Traversal_id()
        if self.Right_child:
            elements += self.Right_child.Pre_Order_Traversal_id()

        return elements

    def Pre_Order_Traversal_data(self):
        elements = [self.data]
        if self.Left_child:
            elements += self.Left_child.Pre_Order_Traversal_data()
        if self.Right_child:
            elements += self.Right_child.Pre_Order_Traversal_data()

        return elements
    
    """
    This method will give
    the Max value of tree
    """ 
    
    def Find_Maximum_Node(self):
        if self.Right_child is None:
            return self.data
        return self.Right_child.Find_Maximum_Node()
    
    """
    This method will give
    the Min value of tree
    """ 
    
    def Find_Minimum_Node(self):
        if self.Left_child is None:
            return self.data
        return self.Left_child.Find_Minimum_Node()
    
    """
    This method will give
    the Total Sum value of tree
    """  
    
    def calculate_Sum_Of_Nodes(self):
        left_sum = self.Left_child.calculate_Sum_Of_Nodes() if self.Left_child else 0
        right_sum = self.Right_child.calculate_Sum_Of_Nodes() if self.Right_child else 0
        return self.data['id'] + left_sum + right_sum



def populaAbpBalanceada(lista, abp, inicio, fim):
    if(fim-inicio == 1):  # 2 dados (inicio e fim)
        dado_esq = {}
        dado_esq['id'] = inicio
        dado_esq['data'] = lista[inicio]

        dado_dir = {}
        dado_dir['id'] = fim
        dado_dir['data'] = lista[fim]

        abp.Add_Node(dado_esq)
        abp.Add_Node(dado_dir)
        return

    if(fim-inicio == 0): # 1 dado (inicio = fim)
        dado = {}
        dado['id'] = inicio
        dado['data'] = lista[inicio]

        abp.Add_Node(dado)
        return
    if(fim-inicio < 0): # n sei, garantia
        return

    
    meio = inicio + math.floor((fim - inicio) / 2) # adicionar dado do meio

    dado_meio = {}
    dado_meio['id'] = meio
    dado_meio['data'] = lista[meio]
    
    abp.Add_Node(dado_meio)

    populaAbpBalanceada(lista, abp, inicio, meio - 1) # dados esquerda
    populaAbpBalanceada(lista, abp, meio + 1, fim) # dados direita

    return





# DADO NA ABP NO FORMATO:
# { ID : ID , DADO1: _ , DADO2: _ }


#lista = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
def createAbp(lista):
    tamanho_lista = len(lista)
    meio = math.floor(tamanho_lista / 2)

    data_raiz = {}
    data_raiz['id'] = meio
    data_raiz['data'] = lista[meio]

    abp = Abp(data_raiz)

    populaAbpBalanceada(lista, abp, 0, meio - 1)
    populaAbpBalanceada(lista, abp, meio + 1, len(lista) - 1)

    return abp













def createAbp_FILME(lista):
    tamanho_lista = len(lista)
    meio = math.floor(tamanho_lista / 2)

    data_raiz = {}
    data_raiz['id'] = lista[meio]['id']
    data_raiz['data'] = lista[meio]

    abp = Abp(data_raiz)

    populaAbpBalanceada_FILME(lista, abp, 0, meio - 1)
    populaAbpBalanceada_FILME(lista, abp, meio + 1, len(lista) - 1)

    return abp




def populaAbpBalanceada_FILME(lista, abp, inicio, fim):
    if(fim-inicio == 1):  # 2 dados (inicio e fim)
        dado_esq = {}
        dado_esq['id'] = lista[inicio]['id']
        dado_esq['data'] = lista[inicio]

        dado_dir = {}
        dado_dir['id'] = lista[fim]['id']
        dado_dir['data'] = lista[fim]

        abp.Add_Node(dado_esq)
        abp.Add_Node(dado_dir)
        return

    if(fim-inicio == 0): # 1 dado (inicio = fim)
        dado = {}
        dado['id'] = lista[inicio]['id']
        dado['data'] = lista[inicio]

        abp.Add_Node(dado)
        return
    if(fim-inicio < 0): # n sei, garantia
        return

    
    meio = inicio + math.floor((fim - inicio) / 2) # adicionar dado do meio

    dado_meio = {}
    dado_meio['id'] = lista[meio]['id']
    dado_meio['data'] = lista[meio]
    
    abp.Add_Node(dado_meio)

    populaAbpBalanceada_FILME(lista, abp, inicio, meio - 1) # dados esquerda
    populaAbpBalanceada_FILME(lista, abp, meio + 1, fim) # dados direita

    return