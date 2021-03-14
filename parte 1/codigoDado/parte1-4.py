# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 10:01:39 2021

@author: tiago
"""
from prettytable import *
from utils import *
from utils import *
from probabilityPlus import *
from itertools import *


def cond_indep(x,y,e,rede):   
    dic=graphToDic(rede)
    caminhos=find_all_paths(dic,x,y,[])
    inativosCaminho=[]
    for i in caminhos:
        temInativos=False
        if i:
            triplos=triplosEmCaminho(i)
        for j in e:
            for t in triplos:
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
        explicacao=explicacao+ 'No '+str(i+1)+' Caminho, o '
        for j in range(0,len(resposta)):
            if resposta[j][0]==i:
                inicio=inicio+1
                explicacao=explicacao+str(inicio)+' Triplo é '+resposta[j][1]+', '
    cond=cond_indep(x,y,e,rede)
    if cond:
        explicacao+='logo é condicionalmente independente, porque todos os caminhos são inativo'
    else:       
        explicacao+='logo não é condicionalmente independente, porque tem pelo menos um caminho ativo'
    return (cond,explicacao)

  
def todos_cond_indeps(rede):
    var=set(rede.variables)
    lista=[]
    for x in var:
        otherX=var-{x}
        for y in otherX:
            otherY=otherX-{y}
            for z in otherY:
                i=cond_indep(x,y,[z],rede)
                if i:
                    lista.append([x,y,z])
    return lista

def triplosEmCaminho(caminho):
    triplos=[]
    for i in range(0,len(caminho)):
        if i+2>len(caminho)-1:
            return triplos
        triplos.append((caminho[i],caminho[i+1],caminho[i+2]))

 
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

T, F = True, False
burglary = BayesNet([
('Burglary', '', 0.001),
('Earthquake', '', 0.002),
('Alarm', 'Burglary Earthquake',
{(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
('MaryCalls', 'Alarm', {T: 0.70, F: 0.01}),
])


grafo=BayesNet([
    ('A', '', 0.5),
    ('B', 'A', {T: 0.90, F: 0.05}),
    ('D', 'A', {T: 0.90, F: 0.05}),
    ('C', 'B', {T: 0.90, F: 0.05}),
    ('E', 'B D', {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
    ])

print(grafo)
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

lista=[]

            
print("\n----------------------COND_INDEP--------------------------------\n")
print(cond_indep('A', 'C', 'B', grafo))
print(cond_indep('A', 'C', 'E', grafo))

print("\n----------------------COND_EXPLICA--------------------------------\n")
print(cond_indep_explica('A', 'C', 'B', grafo))
print(cond_indep_explica('A', 'C', 'E', grafo))


print("\n----------------------TODOS_COND--------------------------------\n")
print(todos_cond_indeps(grafo))