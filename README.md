# PO-SBR-Python
A python implementation of shooting and bouncing rays (PO-SBR), accelerated using OptiX. 
If you have any suggestions/questions, feel free to email me at yftan@nus.edu.sg

# How to use
Place POsolver.py into the working folder, and use the functions.   
Examples are given in Test_RCS for RCS, and Test_range for radar range profile.  

# Functions that you really need to care about
1. ```build(filename)``` takes in the filename of the geometry. Supported file formats inherit from libigl: ```obj, off, stl, wrl, ply, mesh```. Returns vertices and faces ```v,f```  
2. ```simulate(alpha, phi, theta, freq, raysperlam, v, f)```. This simulates monostatic radar. (receive = transmit angle)  
   ```alpha``` is the angle the E vector makes with the theta vector. 0/180 degrees is V pol, 90/270 degrees is H pol.  
   ```phi``` is the phi angle of observation/transmission.  
   ```theta``` is the theta angle of observation/transmission.  
   ```freq``` is the simulation frequency in Hz  
   ```raysperlam``` is the number of rays per lambda. 3 would give 9 rays in an area of lambda^2, 4 would give 16, etc.  
   ```v,f``` are the vertices and faces obtained through ```build(filename)```. Pass ```v,f``` from ```build``` to these parameters in ```simulate```
     
Examples are provided in TestRCS.py, and TestRange.py.
  
   
# Dependencies
numpy: https://numpy.org/  
libigl: https://libigl.github.io/libigl-python-bindings/  
rtxpy (MODIFIED VERSION):   
Grab the modified rtxpy and follow instructions here: https://github.com/pingpongballz/rtxpy  
Original: https://github.com/makepath/rtxpy  
DO NOT USE THE ORIGINAL rtxpy. The original does NOT take into account of inward or outward mesh normals.  


# Results
Simulation on RTX4070 SUPER, i7-14700k  
Flat plate at boreside. x-axis: degree(angle). y-axis: RCS(dBm^2)  
Flat plate dimensions: 1.5m *1.5m.  
Angular step: 45 to 135 degrees, 0.1 degree step  
Operating frequency: 3GHz  
Time to complete: 5.02 seconds  
Theoretical boresight maximum: 38.0dB. Simulated: 38.0dB  
![image](https://github.com/pingpongballz/PO-SBR-Python/assets/74599812/8a49788c-7ac9-4485-8ae6-1fb469643d7c)


  
Dihedral at boreside. x-axis: degree(angle). y-axis: RCS(dBm^2)  
Dihedral dimensions: 1.5m *1.5m plates at 90 degree angles to each other.  
Angular step: 45 to 135 degrees degrees, 0.1 degree step  
Operating frequency: 3GHz  
Time to complete: 11.3 seconds  
Theoretical boresight maximum: 41.0dB. Simulated: 41.1dB  
![image](https://github.com/pingpongballz/PO-SBR-Python/assets/74599812/70424d6e-5c71-42d8-8389-ee52f6deb619)


    
Trihedral at boreside. x-axis: degree(angle). y-axis: RCS(dBm^2)  
Trihedral dimensions: 1.5m interior length.  
Angular step: 45 to 135 degrees degrees, 0.1 degree step  
Operating frequency: 3GHz  
Time to complete: 14.6 seconds  
Theoretical boresight maximum: 33.3dB. Simulated: 33.2dB  
![image](https://github.com/pingpongballz/PO-SBR-Python/assets/74599812/57f95e3a-95b6-4a2a-805a-888e21fdf004)


# References
[1] R. Bhalla and H. Ling, "Image domain ray tube integration formula for the shooting and bouncing ray technique," in Radio Science, vol. 30, no. 5, pp. 1435-1446, Sept.-Oct. 1995.  
[2] S. W. Lee, H. Ling and R. Chou, "Ray-tube integration in shooting and bouncing ray method", Microwave and Optical Technology Letters, vol. 1, no. 8, pp. 286-289, October 1988.  

