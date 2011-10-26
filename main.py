#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# Script para c�lculo do erro quadr�tico m�dio
# embutido no c�lculo computacional de 
# descritores de curvatura de imagens 
# Recebe como par�metro de entrada
# o diret�rio raiz da onde se encontra o banco de imagens 
# e os valores anal�ticos de refer�ncia para compara��o do c�lculo 

import sys
import os
import shutil
from os.path import *
from re import *
from numpy import *
from scipy.interpolate import interp1d
from curvature import curvature_fft1d

# Esta fun��o � chamada pelo m�todo os.path.walk()
# Coloca em tr�s listas (arg[0], arg[1] e arg[2]) 
# os nomes dos arquivos das figuras que calcularemos a curvatura
# , os respetivos dados para curvaturas anal�ticas e o nome para
# o arquivo de armazenamento das sa�das.
# Qualdo o m�todo os.path.walk() executa, este se encarrega de visitar
# cada diret�rio abaixo da ra�z fornecida chamando esta fun��o. 
# Antes de chamar visit() os.path.walk() passa como par�metro, em d,
# o nome do diret�rio visitado e em fl uma lista de arquivos
# contidos neste mesmo diret�rio 
def visit(arg,d,fl):
  for f in fl:
   aux = join(d,f)   
   if isfile(aux):
    r = compile("K_ana.dat")
    if r.search(aux):
      # arquivo .dat (curvatura anal�tica)
      arg[0].append(aux)
    else:
     r = compile("bmp$")
     if r.search(aux):
       # arquivo .bmp (imagem para calculo da curvatura)
       arg[1].append(aux)
      # nome do arquivo .dat para sa�da
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

# s : Faixa de valores e n�mero de pontos para o
# desvio padr�o do filtro passa baixas Gaussiano.
# Este fator determina a frequ�ncia de corte deste
# filtro, que � aplicado antes de se calcular a curvatura.
# Quanto mais pontos mais curvaturas ser�o calculadas por imagem  

sigma_range = logspace(-0.7,2,40.,endpoint = True)
# s  � apenas um apelido para sigma_range
s = sigma_range

# lista para armazenamento do nome dos arquivos
# de entrada e sa�da 
# lista_de_arquivos[0] -> Lista dos nomes dos arquivos de imagens de entrada
# lista_de_arquvos[1] ->  Lista dos nomes dos arquivos de curvaturas anal�ticas correspondentes na forma de vetor coluna.
# lista_de_arquivos[2] -> Lista dos nomes Arquivos de sa�da para armazenamento do  erro calculado 
lista_de_arquivos = [[],[],[]]

# Obt�m listas dos nomes dos arquivos a partir da 
# raiz fornecida ao script
if sys.argv[1]: 
 walk(sys.argv[1],visit,lista_de_arquivos)
else: os.exit(-1)

# Loop externo para cada imagem
#  Computa curvatura e calcula o erro quadr�tico m�dio
#  em relacao a resposta  analitica
for ana_str,im_str,fout_str in zip(lista_de_arquivos[0],lista_de_arquivos[1],lista_de_arquivos[2]):
 print im_str
 # Leitura dos dados para Vetor com reposta anal�tica
 ana = fromfile(ana_str,sep="\n")
 # arquivo de sa�da 
 fout = open(fout_str,"w")
 # Instancializa objeto para calculo de curvaturas
 c = curvature_fft1d(im_str,s)
 # curvs -> Curvograma k(sigma,t)
 curvs = ndarray((s.size,c.t.size),dtype="float")
 # Erro quadr�tico m�dio do calculo da curvatura 
 # da forma sob an�lise para cada valor de sigma
 err =  ndarray((s.size),dtype="float")
 # Par�metro t para interpola��o da fun��o curvatura
 # para reamostragem com  o mesmo n�mero de pontos que 
 # a resposta anal�tica
 tf = linspace(0,1,ana.size)
 # Interage para cada valor de sigma
 print >> fout,"sigma\terr_rms\n"
 for i in arange(s.size):
   # obt�m curvaturas para o curvograma
   #curvs[i] = c(i,c.t)
   # obt�m o erro quadr�tico m�dio entre curvatura anal�tica
   # e a reamostrada 
   aux = c(i,tf)
   err[i] = rms_err(ana,aux)
   print "sigma = {0}, err_rms = {1}".format(s[i],err[i])
  
   print >> fout,"{0}\t{1}".format(s[i],err[i])
 fout.close()

 
 
