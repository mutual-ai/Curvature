#!/usr/bin/python

import sys
from curvature import *
from BendEnergy import *
from numpy import *
from matplotlib.pyplot import *

sigma = logspace(-0.8,1.8,10)
k = curvature_fft1d(sys.argv[1],sigma)
nmbe  = BendEnergy(k)

plot(log(nmbe.sigma),log(nmbe()))
show()
