import POsolver as PO
import numpy as np
import matplotlib.pyplot as plt
import time

#Initial Params
filename = "geometries/trihedral.obj"
alpha = 180 #0/180 for V pol; 90/270 for H pol
phi = np.arange(45,135,0.1) #90
theta = 90
freq = 3e9 #np.arange(1e9,4e9,30e6)
raysperlam = 3
bounces = 3
        

v,f = PO.build(filename)
RCS = lambda E_theta,E_phi,r0: 10*np.log10(4*np.pi*r0*r0*((abs(E_theta))**2 + (abs(E_phi))**2))
arr = []

  


tic = time.time()
for ang in phi:
    E1, E2,r0 = PO.simulate(alpha, ang, theta, freq, raysperlam, v, f, bounces)
    arr.append(RCS(E1,E2,r0))
toc = time.time()
print(str(toc-tic) + " seconds")
plt.plot(phi, arr)
plt.show()
