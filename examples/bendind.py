#!/usr/bin/python

import sys
import os
from os.path import *
from re import *
from numpy import *
from matplotlib.pyplot import *
import matplotlib.image as img

sys.path.append("../")
from curvature import *
from BendEnergy import *

figure()
ax = subplot(121)
sigma = logspace(-0.3,1.8,200)
for im_file in sys.argv[1:]:
 if isfile(im_file):
  k = curvature(im_file,sigma)
  nmbe  = BendEnergy(k)
  ax.plot(log(nmbe.sigma),log(nmbe()),linewidth = 3.0,label = im_file)
  r = compile("bmp$")
  if r.search(im_file):
   aux = r.sub("dat",im_file) 
   fout = open(aux,"w")
   print >>fout,"%",im_file,"\n"
   print >>fout,"Col1 : nmbe   Col2: log(nmbe)\n\n"
   for a in nmbe.phi:
    print >> fout,"{0}\t{1}".format(a,log(a))
   fout.close() 
h,l = ax.get_legend_handles_labels()
ax.legend(h[::-1],l[::-1],loc=3)
ylabel('NMBE',fontsize=15)
xlabel('Scale',fontsize=15)
img = img.imread("./misc_cells.bmp")
bx = subplot(122)
gray()
imshow(img[::-1])
    

show()
