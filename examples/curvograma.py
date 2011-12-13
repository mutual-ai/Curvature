#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import glob
from numpy import *
from scipy.interpolate import interp1d
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import *

sys.path.append("../")
from curvature import *

lwidth = 2.
fsize = 20
# s = vetor que armazena diferentes valores de desvio padrao sigma da gaussiana
# utilizada para janela de suavizacao 
sigma_range = linspace(0.5,30.0,20)
s = sigma_range

# Le a curvatura analitica do arquivo de entrada
ana = fromfile(sys.argv[1],dtype=float,sep="\n")

tf = arange(ana.size)/float(ana.size-1)

# Instancializa objeto
c = curvature(sys.argv[2],sigma_range)

# Curvograma k(sigma,t)
curvs = ndarray((s.size,c.t.size),dtype="float")
for i in arange(s.size):
  curvs[i] = copy(c(i))

###########################################
# Apresentacao dos resultados em figuras
###########################################
# Figura 1 : Contorno original e reconstruido
# para o menor valor de sigma
###########################################
figure(1)

subplot(331)
plot(c.z.real,c.z.imag,lw=lwidth)
xlabel('x',fontsize=fsize)
ylabel('y',fontsize=fsize)
title('Analitica',fontsize=fsize)

subplot(333)
plot(c.t,c.z.real,c.t,c.z.imag,lw=lwidth)
xlabel('t',fontsize=fsize)
ylabel('x,y',fontsize=fsize)

subplot(337)

plot(c.rcontours[10].real,c.rcontours[10].imag,lw=lwidth)
xlabel('x',fontsize=fsize)
ylabel('y',fontsize=fsize)
title('Reconstruida ($\sigma = '+repr(s[10])+'$)',fontsize=fsize)

subplot(339)
plot(c.t,c.rcontours[10].real,c.t,c.rcontours[10].imag,lw=lwidth)
xlabel('t',fontsize=fsize)
ylabel('x,y',fontsize=fsize)
###################################################################################
# Figura 2 : Mostra a curvatura para todas as suavicoes (com compensacao de energia)
####################################################################################
figure(2)
suptitle('Curvatura $k(t)$',fontsize=fsize)

subplot(331)
title('Analitica',fontsize=fsize)
plot(tf,ana,lw=lwidth)
xlabel('t',fontsize=fsize)
ylabel('$k(t)$',fontsize=fsize)

subplot(333)
title('$\sigma = '+ repr(s[19])+'$',fontsize=fsize)
plot(tf,c(19,tf),lw=lwidth)
xlabel('t',fontsize=fsize)
ylabel('$k(t)$',fontsize=fsize)


subplot(337)
title('$\sigma = '+ repr(s[10])+'$',fontsize=fsize)
plot(tf,c(10,tf),lw=lwidth)
xlabel('t',fontsize=fsize)
ylabel('$k(t)$',fontsize=fsize)

subplot(339)
title('$\sigma = '+ repr(s[5])+'$',fontsize=fsize)
plot(tf,c(5,tf),lw=lwidth)
xlabel('t',fontsize=fsize)
ylabel('$k(t)$',fontsize=fsize)


figure(3)
suptitle("Contorno reconstruido para diversos valores de $\sigma \in [0.5,30.0]$",fontsize=fsize)
subplot(441)
plot(c.z.real,c.z.imag,lw=lwidth)

subplot(442)
plot(c.rcontours[15].real,c.rcontours[15].imag,lw=lwidth)

subplot(443)
plot(c.rcontours[14].real,c.rcontours[14].imag,lw=lwidth)

subplot(444)
plot(c.rcontours[13].real,c.rcontours[13].imag,lw=lwidth)

subplot(445)
plot(c.rcontours[12].real,c.rcontours[12].imag,lw=lwidth)

subplot(446)
plot(c.rcontours[11].real,c.rcontours[11].imag,lw=lwidth)

subplot(447)
plot(c.rcontours[10].real,c.rcontours[10].imag,lw=lwidth)

subplot(448)
plot(c.rcontours[9].real,c.rcontours[9].imag,lw=lwidth)

subplot(449)
plot(c.rcontours[8].real,c.rcontours[8].imag,lw=lwidth)

subplot(4,4,10)
plot(c.rcontours[7].real,c.rcontours[7].imag,lw=lwidth)

subplot(4,4,11)
plot(c.rcontours[6].real,c.rcontours[6].imag,lw=lwidth)

subplot(4,4,12)
plot(c.rcontours[4].real,c.rcontours[4].imag,lw=lwidth)

subplot(4,4,13)
plot(c.rcontours[3].real,c.rcontours[3].imag,lw=lwidth)

subplot(4,4,14)
plot(c.rcontours[2].real,c.rcontours[2].imag,lw=lwidth)

subplot(4,4,15)
plot(c.rcontours[1].real,c.rcontours[1].imag,lw=lwidth)

subplot(4,4,16)
plot(c.rcontours[0].real,c.rcontours[0].imag,lw=lwidth)

################################################
# Figura 3 : Apresenta curvograma e grafico 3D
################################################

fig = figure(4)
title('Curvograma',fontsize=fsize)
ax = Axes3D(fig)
xlabel("t",fontsize=fsize)
ylabel('$\sigma$',fontsize=fsize)

x,y = meshgrid(c.t,s)
ax.plot_surface(x,y,curvs,rstride = 20, cstride = 20,lw=lwidth)
show()
