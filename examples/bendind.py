#!/usr/bin/python

import sys
from numpy import *
from matplotlib.pyplot import *

sys.path.append("../")
from curvature import *
from BendEnergy import *

sigma = logspace(-0.3,1.8,200)
k = curvature(sys.argv[1],sigma)
nmbe  = BendEnergy(k)

plot(log(nmbe.sigma),log(nmbe()),'+')
show()
