from curvature import *

class BendEnergy:

 def __init__(self,k):
  self.k = k
  self.phi  = zeros((k.sigmas.size),dtype = "float")
  for i  in arange(k.sigmas.size):
   self.phi[i] = (k.perimeter[i]**2)*mean(k(i)**2)
  self.sigma = 1/k.sigmas

 def __call__(self,i = None):
  if i is None: 
   _aux = self.phi
  else:
   _aux = self.phi[i]
 
  return (_aux)
