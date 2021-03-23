"""
Grupo53 
Ana Alburquerque 53512
Gonçalo Antunes 52831
Tiago Cabrita 52741
"""

from prettytable import *
from utils import *
from utils import *
from probabilityPlus import *
from itertools import *

def cond_indep(x,y,e,rede):   
    if isinstance(e, str):
        e=e.split(" ")
    dic=graphToDic(rede)
    caminhos=find_all_paths(dic,x,y,[])
    inativosCaminho=[]
    for i in caminhos:
        temInativos=False
        if i:
            triplos=triplosEmCaminho(i)
            for t in triplos:
                for j in e:
                    if j in t:
                        temInativos=True
        inativosCaminho.append(temInativos)
    for i in inativosCaminho:
        if i==False:
            return False
    return True

def cond_indep_explica(x,y,e,rede):   
    dic=graphToDic(rede)
    caminhos=find_all_paths(dic,x,y,[])
    triplos=[]
    resposta=[]
    for i in range(0,len(caminhos)):
        triplos=triplosEmCaminho(caminhos[i])
        for triplo in triplos:
            resposta.append((i,checkTriplo(triplo,e,rede)))
    explicacao=""
    for i in range(0,len(caminhos)):
        inicio=0
        for j in range(0,len(resposta)):
            if j==0:
                explicacao=explicacao+ 'No '+str(i+1)+'º caminho, '
            if resposta[j][0]==i:
                inicio=inicio+1
                explicacao=explicacao+'o '+str(inicio)+'º triplo é '+resposta[j][1]+', '
    cond=cond_indep(x,y,e,rede)
    if cond:
        explicacao+='logo X e Y são condicionalmente independentes, porque todos os caminhos são inativos.'
    else:       
        explicacao+='logo X e Y não são condicionalmente independentes, porque existe pelo menos um caminho ativo.'
    return (cond,explicacao)

def todos_cond_indeps(rede):
    var=set(rede.variables)
    lista=[]
    for x in var:
        otherX=var-{x}
        for y in otherX:
            allE=all_possible_e(rede,x,y)
            for z in allE:
                i=cond_indep(x,y,z,rede)
                if i and checkAlreadyIn(x,y,z,lista):
                    lista.append((x,y,z))
    return lista

"""
Funções Auxiliares
"""
def checkAlreadyIn(x,y,z,lista):
    for i in range(0,len(lista)):
        cond=set(z)==set(lista[i][2])
        if x in lista[i] and y in lista[i] and cond:
            return False    
    
    return True

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def graphToDic(rede):
    var=set(rede.variables)
    myDict={}
    for v in var:
        myDict[v]=rede.variable_node(v).parents+rede.variable_node(v).children
    return myDict

def all_possible_e(rede,x,y):
    var=set(grafo.variables)
    lista=[]
    var=var-{x}-{y}
    for i in var:
        lista.append(i)
    for i in range(2,len(var)+1):
        perm = permutations(var, i)
        for j in perm:
            lista.append(j)
    return lista

def triplosEmCaminho(caminho):
    triplos=[]
    for i in range(0,len(caminho)):
        if i+2>len(caminho)-1:
            return triplos
        triplos.append((caminho[i],caminho[i+1],caminho[i+2]))
        
def checkTriplo(triplo,e,rede):
    pais1=rede.variable_node(triplo[0]).parents
    pais2=rede.variable_node(triplo[1]).parents
    pais3=rede.variable_node(triplo[2]).parents
    explicacao=""

    if triplo[0] in pais2 and triplo[1] in pais3:
        explicacao += "Cadeia Causal "
    if triplo[0] in pais2 and triplo[2] in pais2:
        explicacao += "Efeito Comum "
    if triplo[1] in pais1 and triplo[1] in pais3:
        explicacao += "Causa Comum "
    for i in e:
        if i in triplo:
            return explicacao + "inativo"
    return explicacao + "ativo"
