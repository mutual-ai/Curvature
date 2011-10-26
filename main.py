#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# Script para cálculo do erro quadrático médio
# embutido no cálculo computacional de 
# descritores de curvatura de imagens 
# Recebe como parâmetro de entrada
# o diretório raiz da onde se encontra o banco de imagens 
# e os valores analíticos de referência para comparação do cálculo 

import sys
import os
import shutil
from os.path import *
from re import *
from numpy import *
from scipy.interpolate import interp1d
from curvature import curvature_fft1d

# Esta função é chamada pelo método os.path.walk()
# Coloca em três listas (arg[0], arg[1] e arg[2]) 
# os nomes dos arquivos das figuras que calcularemos a curvatura
# , os respetivos dados para curvaturas analíticas e o nome para
# o arquivo de armazenamento das saídas.
# Qualdo o método os.path.walk() executa, este se encarrega de visitar
# cada diretório abaixo da raíz fornecida chamando esta função. 
# Antes de chamar visit() os.path.walk() passa como parâmetro, em d,
# o nome do diretório visitado e em fl uma lista de arquivos
# contidos neste mesmo diretório 
def visit(arg,d,fl):
  for f in fl:
   aux = join(d,f)   
   if isfile(aux):
    r = compile("K_ana.dat")
    if r.search(aux):
      # arquivo .dat (curvatura analítica)
      arg[0].append(aux)
    else:
     r = compile("bmp$")
     if r.search(aux):
       # arquivo .bmp (imagem para calculo da curvatura)
       arg[1].append(aux)
      # nome do arquivo .dat para saída
       aux = r.sub("dat",aux)
       r = compile(d)
       aux = r.sub("./"+OUTPUTDIR,aux)
       arg[2].append(aux)

# Esta funcao auxiliar calcula o erro RMS entre dois vetores
# de mesmo tamanho
def rms_err(a,b):
  e = diff(array([a,b]),axis = 0)
  n = float(e.size)
  e = sqrt(sum(square(e))/n)
  return(e)


#######################################
#                                     #
#       Programa Principal            #
#                                     #
#######################################
OUTPUTDIR = "saida"

# s : Faixa de valores e número de pontos para o
# desvio padrão do filtro passa baixas Gaussiano.
# Este fator determina a frequência de corte deste
# filtro, que é aplicado antes de se calcular a curvatura.
# Quanto mais pontos mais curvaturas serão calculadas por imagem  

sigma_range = logspace(-0.7,2,40.,endpoint = True)
# s  é apenas um apelido para sigma_range
s = sigma_range

# lista para armazenamento do nome dos arquivos
# de entrada e saída 
# lista_de_arquivos[0] -> Lista dos nomes dos arquivos de imagens de entrada
# lista_de_arquvos[1] ->  Lista dos nomes dos arquivos de curvaturas analíticas correspondentes na forma de vetor coluna.
# lista_de_arquivos[2] -> Lista dos nomes Arquivos de saída para armazenamento do  erro calculado 
lista_de_arquivos = [[],[],[]]

# Obtém listas dos nomes dos arquivos a partir da 
# raiz fornecida ao script
if sys.argv[1]: 
 walk(sys.argv[1],visit,lista_de_arquivos)
else: os.exit(-1)

# Loop externo para cada imagem
#  Computa curvatura e calcula o erro quadrático médio
#  em relacao a resposta  analitica
for ana_str,im_str,fout_str in zip(lista_de_arquivos[0],lista_de_arquivos[1],lista_de_arquivos[2]):
 print im_str
 # Leitura dos dados para Vetor com reposta analítica
 ana = fromfile(ana_str,sep="\n")
 # arquivo de saída 
 fout = open(fout_str,"w")
 # Instancializa objeto para calculo de curvaturas
 c = curvature_fft1d(im_str,s)
 # curvs -> Curvograma k(sigma,t)
 curvs = ndarray((s.size,c.t.size),dtype="float")
 # Erro quadrático médio do calculo da curvatura 
 # da forma sob análise para cada valor de sigma
 err =  ndarray((s.size),dtype="float")
 # Parâmetro t para interpolação da função curvatura
 # para reamostragem com  o mesmo número de pontos que 
 # a resposta analítica
 tf = linspace(0,1,ana.size)
 # Interage para cada valor de sigma
 print >> fout,"sigma\terr_rms\n"
 for i in arange(s.size):
   # obtém curvaturas para o curvograma
   #curvs[i] = c(i,c.t)
   # obtém o erro quadrático médio entre curvatura analítica
   # e a reamostrada 
   aux = c(i,tf)
   err[i] = rms_err(ana,aux)
   print "sigma = {0}, err_rms = {1}".format(s[i],err[i])
  
   print >> fout,"{0}\t{1}".format(s[i],err[i])
 fout.close()

 
 
