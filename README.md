# PO-SBR-Python
A python implementation of shooting and bouncing rays (PO-SBR), accelerated using OptiX

# How to use
Place POsolver.py into the working folder, and use the functions.  
I am too lazy to make a module sooo yeah :/  
Examples are given in Test_RCS for RCS, and Test_range for radar range profile.  

# Results
Flat plate at boreside. x-axis: degree(angle). y-axis: RCS(dBm^2)  
Flat plate dimensions: 1.5m *1.5m.  
Angular step: 45 to 135 degrees, 0.1 degree step  
Operating frequency: 3GHz  
Time to complete: 22.0 seconds  
Theoretical boresight maximum: 38.0dB. Simulated: 38.0dB  
![image](https://github.com/pingpongballz/PO-SBR-Python/assets/74599812/e2ad1b65-5907-4515-a8dd-c4683defaf0a)

  
Dihedral at boreside. x-axis: degree(angle). y-axis: RCS(dBm^2)  
Dihedral dimensions: 1.5m *1.5m plates at 90 degree angles to each other.  
Angular step: 45 to 135 degrees degrees, 0.1 degree step 
Operating frequency: 3GHz  
Time to complete: 31.2 seconds  
Theoretical boresight maximum: 41.0dB. Simulated: 41.1dB  
![image](https://github.com/pingpongballz/PO-SBR-Python/assets/74599812/cb28e0f3-d2a4-4dfa-8e7c-87b0f77b8058)

    
Trihedral at boreside. x-axis: degree(angle). y-axis: RCS(dBm^2)  
Trihedral dimensions: 1.5m interior length.  
Angular step: 45 to 135 degrees degrees, 0.1 degree step  
Operating frequency: 3GHz  
Time to complete: 32.8 seconds  
Theoretical boresight maximum: 33.3dB. Simulated: 33.2dB  
![image](https://github.com/pingpongballz/PO-SBR-Python/assets/74599812/9b51a234-1a67-4b93-bd4c-811c856ab430)


