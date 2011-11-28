from curvature import *

class BendEnergy(curvature_fft1d):

 def __init__(self,k):
  self.k = k
  self.phi  = zeros((k.sigmas.size),dtype = "float")
  for i  in arange(k.sigmas.size):
   self.phi[i] = (k.perimeter[i]**2)*mean(k(i,k.t)**2)
  self.sigma = 1/k.sigmas

 def __call__(self,i = None):
  if i is not None: 
   return(phi)
  else:
   return(phi[i])
