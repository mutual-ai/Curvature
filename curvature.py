from numpy import *
import scipy
from scipy.interpolate import *
from cv import *


 #  curvature_fft1d : 
 #  class to compute curvature for a given contour
 #  fname :  filename for contour extraction. Must be binary image  
 #  sigma_range :  Gaussian window's standard deviation (LPF bandwidth) for frequency domain contour smoothing.
 #                when zero no filtering is applied to contour
 #  method : Calculation method string. Currently only "fft1d" is supported

class curvature:
 # Gaussian smoothing function 
  def _G(self):
    return (1/(self._sig*(2*pi)**0.5))*exp(-(self.freq-self._mi)**2/(2*(self._sig**2)))

 # Auxiliary method to calculate perimeter 
  def _L(self):
   return (2*pi*sum(abs(self.zd))/float(self.zd.size))

 # Perform computation stuff   
  def _Calcula_Curvograma(self):
   N = self.z.size
   self.t = linspace(0,1,N)
   self.freq = fft.fftfreq(N,1./float(N))  
   # Compute FFT
   _F = fft.fft(self.z)
   
   self.curvs = ndarray((self.sigmas.size,self.t.size),dtype = "float")
   self.rcontours = ndarray((self.sigmas.size,self.t.size),dtype = "complex") 
   self.perimeter = ndarray((self.sigmas.size),dtype = "float")

   # Calcula energia da imagem atraves de seu espectro de Fourier
   _E  = sum(_F * conjugate(_F))   
   # Limita banda utilizando Filtro Gaussiano
   _F_filtr = copy(_F)  
   
   # Energy compensation because LPF decreases signal energy  
   for self._sig,i in zip(self.sigmas,arange(self.sigmas.size)):
     if self._sig != 0:  
      _F_filtr = _F * self._G()
      # Calcula novo valor de energia apos filtragem
      _Eg  = sum(_F_filtr * conjugate(_F_filtr))
      _k = sqrt(_E/_Eg)
     else: 
      _k = 1.
     
     # Resconstructed contour after LPF in frequency domain
     self.rcontours[i] = copy(fft.ifft(_F_filtr)*_k) 

     # Calcula derivadas 1st and 2nd no dominio da frequencia
     _Fd = complex(0,1) * 2 * pi * self.freq * _F_filtr
     _Fdd = - (2 * pi * self.freq)**2 * _F_filtr
     # Retorna ao dominio espacial 
     self.zd = fft.ifft(_Fd)*_k
     _zd   =  self.zd
     self.zdd = fft.ifft(_Fdd)*_k
     _zdd  = self.zdd

     # Calcula o perimetro do contorno
     self.perimeter[i] = copy(self._L())

     # Calcula curvatura 
     _curv = _zd * conjugate(_zdd)
     _curv = -_curv.imag
     _curv = _curv/(abs(_zd)**3)

     # Array bidimensional curvs = Curvature Function k(sigma,t) 
     self.curvs[i] = scipy.atan(_curv)*self.perimeter[i]   
 
  # Contructor 
  def __init__(self,fn = None,sigma_range = linspace(2,30,10), method = "fft1d"):
  # Carrega imagem
   if type(fn) is str:
    im = LoadImageM(fname,CV_LOAD_IMAGE_GRAYSCALE)
    # Extrai contorno da imagem
    seq = FindContours(im, CreateMemStorage(),CV_RETR_LIST,CV_CHAIN_APPROX_NONE)
    # z = Pontos do contorno, representados na forma complexa, extraidos da imagem 
    # na qual se deseja determinar a funcao de curvatura
    self.z = ndarray(len(seq),dtype='complex')
    for c,i in zip(seq,arange(self.z.size)):
     re,im = c[1],c[0] 
     self.z[i] = complex(re,im)
   elif (type(fn) is ndarray) and (fn.dtype is dtype("complex")):
    self.z = copy(fn)

   self._mi = 0;
   self.sigmas = sigma_range
  
   self._Calcula_Curvograma()

 # Function to compute curvature
 # It is called into class constructor
  def __call__(self,sig_idx,t= None):
    if t is not None:
     _curv = interp1d(self.t,y = self.curvs[sig_idx],kind='quadratic')
     return(_curv(t))
    else:
     return(self.curvs[sig_idx])
   
