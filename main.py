#! /usr/bin/python
import sys
import glob
from numpy import *
from scipy.interpolate import interp1d
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import *
from curvature import curvature_fft1d

# s = vetor que armazena diferentes valores de desvio padrao sigma da gaussiana
# utilizada para janela de suavizacao 
sigma_range = linspace(3.,50.,20.)
s = sigma_range

# Le a curvatura analitica do arquivo de entrada
ana = fromfile(sys.argv[2],dtype=float,sep="\n")

tf = arange(ana.size)/float(ana.size-1)

# Instancializa objeto
c = curvature_fft1d(sys.argv[1],sigma_range)

# Curvograma k(sigma,t)
curvs = ndarray((s.size,c.t.size),dtype="float")
for i in arange(s.size):
  curvs[i] = copy(c(i,c.t))

###########################################
# Apresentacao dos resultados em figuras
###########################################
# Figura 1 : Contorno original e reconstruido
# para o menor valor de sigma
###########################################
figure(1)
suptitle('Contour reconstruction, after Frequency-Domain gaussian\'s window smoothing, with energy compensation',fontsize=12)

subplot(331)
plot(c.z.real,c.z.imag)
xlabel('x',fontsize=12)
ylabel('y',fontsize=12)
title('Original',fontsize=12)

subplot(333)
plot(c.t,c.z.real,c.t,c.z.imag)
xlabel('t',fontsize=12)
ylabel('x,y',fontsize=12)

subplot(337)

plot(c.rcountours[4].real,c.rcountours[4].imag)
xlabel('x',fontsize=12)
ylabel('y',fontsize=12)
title('Reconstructed for $\sigma = '+repr(s[4])+'$',fontsize=12)

subplot(339)
plot(c.t,c.rcountours[4].real,c.t,c.rcountours[4].imag)
xlabel('t',fontsize=12)
ylabel('x,y',fontsize=12)

###################################################################################
# Figura 2 : Mostra a curvatura para todas as suavicoes (com compensacao de energia)
####################################################################################
figure(2)
suptitle('Computed curvatures through Costa and Fontoura 1D Fourier method (Costa,1996)',fontsize=12)

subplot(321)
title('Analytical',fontsize=12)
plot(tf,ana)
xlabel('t',fontsize=12)
ylabel('k(t)',fontsize=12)

subplot(322)
title('$\sigma = '+ s[0].__str__()+'$',fontsize=14)
plot(tf,c(0,tf),c.t,c(0,c.t))
xlabel('t',fontsize=12)
ylabel('k(t)',fontsize=12)

subplot(323)
title('$\sigma = '+ s[1].__str__()+'$',fontsize=14)
plot(tf,c(1,tf),c.t,c(1,c.t))
xlabel('t',fontsize=12)
ylabel('k(t)',fontsize=12)

subplot(324)
title('$\sigma = '+ s[2].__str__()+'$',fontsize=14)
plot(tf,c(2,tf),c.t,c(2,c.t))
xlabel('t',fontsize=12)
ylabel('k(t)',fontsize=12)

subplot(325)
title('$\sigma = '+ s[3].__str__()+'$',fontsize=14)
plot(tf,c(3,tf),c.t,c(3,c.t))
xlabel('t',fontsize=12)
ylabel('k(t)',fontsize=12)

subplot(326)
title('$\sigma = '+ s[15].__str__()+'$',fontsize=14)
plot(tf,c(15,tf),c.t,c(15,c.t))
xlabel('t',fontsize=12)
ylabel('k(t)',fontsize=12)

################################################
# Figura 3 : Apresenta curvograma e grafico 3D
################################################
fig = figure(3)
title('Curvograma da imagem da Figura 1',fontsize=12)
ax = Axes3D(fig)
xlabel("t",fontsize=12)
ylabel('$\sigma$',fontsize=14)
x,y = meshgrid(c.t,s)
ax.plot_surface(x,y,curvs,rstride = 20, cstride = 20)
show()
