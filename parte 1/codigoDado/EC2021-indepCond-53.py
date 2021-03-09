from probabilityPlus import *
from prettytable import *
from agents import *
from ipythonblocks import *
from utils import *

def teste():


    T, F = True, False
    burglary = BayesNet([
    ('Burglary', '', 0.001),
    ('Earthquake', '', 0.002),
    ('Alarm', 'Burglary Earthquake',
     {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
    ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
    ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
    ])

    R = burglary
    print("Aceder ao no na posicao 2:")
    print(R.nodes[2])

    print("\nAceder ao nome do no na posicao 2:")
    print(R.variables[2])

    print("\nAceder ao numero de nos da rede")
    print(len(R.nodes))

    print("\nAceder aos nomes dos filhos da posicao 2:")
    print(R.nodes[2].children)

    print("\nAceder aos nos dos filhos da posicao 2:")
    for i in range (len(R.nodes[2].children)): 
        print(R.nodes[2+i+1])



    return cond_indep('Burglary', 'JohnCalls', 'Alarm', burglary)


def cond_indep(X, Y, E, R):
    print("\n\n\n\n")
    
    index = -1 #tem sempre de haver 1 no raiz
    for i in range (len(R.nodes)):
        if(len(R.nodes[i].children) == 0):
            index = index +1
    
    return cond_indepAux(index,X, Y, E, R)


def cond_indepAux(index,X, Y, E, R):

    for i in range (len(R.nodes[index].children)): 
        print(R.nodes[index+i+1])
        cond_indepAux(index+1,X, Y, E, R)

    return 1




def cond_indep_explica(X, Y, E, R):
    return


def odos_cond_indeps(R):
    return





if __name__ == '__main__':
    teste()




