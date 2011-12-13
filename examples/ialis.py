#!/usr/bin/python

import sys
sys.path.append("/home/marcelo/curvatura")
import os
from os.path import *
#from re import *
import numpy as np
from curvature import *
#import matplotlib.pyplot as plt

NFIGS = 104
 
def msbe(c,pts,s):
   return (mean(c.curvs[s,pts]**2)) 
 
#######################################
#                                     #
#       Programa Principal            #
#                                     #
#######################################

sigma_range = linspace(3.44,5.00,2)
sigma = 0
str_path = sys.argv[1]
prefix_path = array(["/contornos/","/ground-truth/","/css_mod/","/css_orig/","/lee_mod/","/lee_orig/","/pedrosa/","/proposto/"])
prefix_str =  "forma-"
postfix_str = array(["-css_mod.txt", "-css_orig.txt","-lee_mod.txt","-lee_orig.txt","-pedrosa.txt","-proposto.txt"])
# Arquivos de entrada (in_file_list) terminam com a extensao txt (fornecidos pelo ialis)
# Arquivos de saida (out_file_list) terminam com a extensao out e sao criados nos mesmos diretorios
# aonde foram encontrados os arquivos de entrada
#                 x-contorno  y-contorno    ground-truth   css_mod    css_orig      lee_mod     lee_orig  pedrosa proposto
file_in_list = [          [],     [],             [],        [],        [],            [],        [],        [],      [] ]
#               css_mod          css_orig     lee_mod     lee_orig  pedrosa proposto
file_out_list = []
 
# Monta nome dos arquivos em listas 

# lista com nome dos arquivos de dados de entrada das coordenadas do contorno
for i in arange(1,NFIGS+1):
 xs  = str_path + prefix_path[0] + prefix_str + str(i) + str("x-contorno.txt")
 ys  = str_path + prefix_path[0] + prefix_str + str(i) + str("y-contorno.txt") 
 gt  = str_path + prefix_path[1] + prefix_str + str(i) + str("-ground-truth.txt")
 file_in_list[0].append(xs)
 file_in_list[1].append(ys)
 file_in_list[2].append(gt)

# listas com nome dos arquivos de dados de entrada para cada metodo avaliado
# aproveita tambem pra abrir arquivos com um nome de  arquivo de saida
for fil,i in zip(file_in_list[3:],arange(postfix_str.size)):
 fname = str_path + prefix_path[i+2] + str("out") + postfix_str[i]
 f = open(fname,"w")
 file_out_list.append(f)
 for j in arange(1,NFIGS+1): 
    aux = str_path + prefix_path[i+2] + prefix_str + str(j) + postfix_str[i]
    fil.append(aux)  

# Para cada imagem, coleta dados dos arquivos
for fi_lst,fdo in zip(file_in_list[3:],file_out_list):
 
 for fcx,fcy,fgt,fi in zip(file_in_list[0],file_in_list[1],file_in_list[2],fi_lst):
  # Determina pontos do contorno
 # print "{0}, {1}, {2}, {3}, {4}".format(fcx,fcy,fgt,fi,fo)
  cix = np.genfromtxt(fcx,dtype=int)
  ciy = np.genfromtxt(fcy,dtype=int)
  z = np.ndarray((cix.size),dtype = complex)
  for i,x,y in zip(arange(z.size),cix,ciy):
    z[i] = complex(x,y) 
  # Determina ground truth
  gt  = np.genfromtxt(fgt,dtype=int)
  gt  = gt - 1
  # Determina resposta do metodo
  dm = np.genfromtxt(fi,dtype=int)
  dm = dm - 1
  # Calcula curvatura
  k = curvature(z,sigma_range)
  E_gt = msbe(k,gt,sigma)
  E_metodo = msbe(k,dm,sigma)

  print >> fdo,"{0}\t{1}".format(E_metodo, E_gt)
  #print "{0}, {1}, {2}, {3}, {4} -> E_gt = {5}, E_metodo = {6}".format(fcx,fcy,fgt,fi,fo,E_gt,E_metodo)
  #print "z.size = {0}, k.curvs.shape = {1}".format(z.size,k.curvs.shape)
 fdo.close()
 
