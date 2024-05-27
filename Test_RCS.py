import POsolver as PO
import numpy as np
import matplotlib.pyplot as plt
import time

#Initial Params
#filename = "C:/Users/e0406331/Downloads/libigl-tutorial-data-master/cube.obj"
filename = "geometries/dihedral.obj"
alpha = 180 #0/180 for V pol; 90/270 for H pol
phi = np.arange(30,150,0.5) #90
theta = 90
freq = 5.405e9 #np.arange(1e9,4e9,30e6)
raysperlam = 3
        

v,f = PO.build(filename)
RCS = lambda E_theta,E_phi: 10*np.log10(4*np.pi*np.abs(E_theta)**2)
arr = []

  


tic = time.time()
for ang in phi:
    E1, E2,r0 = PO.simulate(alpha, ang, theta, freq, raysperlam, v, f)
    arr.append(RCS(E1,E2))
toc = time.time()
print(str(toc-tic) + " seconds")
plt.plot(phi, arr)
plt.ylim(0,50)
plt.show()
