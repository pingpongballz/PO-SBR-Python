import POsolver as PO
import numpy as np
import matplotlib.pyplot as plt
import time

#Uncomment/comment geometry u wanna use
#Dihedral at ORIGIN.
#filename = "geometries/dihedral.obj"
#Dihedral at 2m OFFSET.
filename = "geometries/dihedral_offset.obj"

#Initial Params.
alpha = 180 #0/180 for V pol; 90/270 for H pol
phi = 90
theta = 90
freq = np.arange(1,2,0.01)*1e9
raysperlam = 3
bounces = 2
        

v,f = PO.build(filename)
RCS = lambda E_theta,E_phi: 10*np.log10(4*np.pi*np.abs(E_theta)**2)
arr = []


tic = time.time()
for i in freq:
    lam = (3e8)/(i)
    k = 2*np.pi/lam
    E1, E2,r0 = PO.simulate(alpha, phi, theta, i, raysperlam, v, f, bounces)
    factor = ((4*np.pi)/(-1j*k)) #normalisation. See R. Bhalla ISAR ray tube method 
    arr.append(E1)
     

toc = time.time()
print(str(toc-tic) + " seconds")
arr_fft = np.fft.ifftshift(np.fft.ifft(arr)) #get range profile
plt.plot(np.linspace(-7.5,7.5,len(freq)),np.abs(arr_fft))
plt.title("0m offset" if filename == "geometries/dihedral.obj" else "2m offset")
plt.show()



