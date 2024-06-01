import numpy as np
import igl
from rtxpy import RTX, has_cupy
import rtxpy
import matplotlib.pyplot as plt



optix = RTX()



#helper fns
cosd = lambda x : np.cos(np.deg2rad(x))
sind = lambda x : np.sin(np.deg2rad(x))

def ortho_set(phi, theta):
    right = [0,0,0]; up = [0,0,0]; normal = [0,0,0];

    normal[0] = sind(theta)*cosd(phi)
    normal[1] = sind(theta)*sind(phi)
    normal[2] = cosd(theta)
    
    right[0] = sind(phi)
    right[1] = -cosd(phi)
    up = np.cross(right, normal)

    return np.array(normal), up, np.array(right)

def polarise(pol, k_inc, k_ref, normal):
    e_perp = np.cross(k_inc, normal)/(np.linalg.norm(np.cross(k_inc, normal),axis = 1).reshape(-1,1))

    e_par = np.cross(k_inc, e_perp)/(np.linalg.norm(np.cross(k_inc, e_perp),axis = 1).reshape(-1,1))
    
    e_ref_perp = e_perp
    
    e_ref_par = np.cross(k_ref, e_ref_perp)/(np.linalg.norm(np.cross(k_ref, e_ref_perp),axis = 1).reshape(-1,1))

    E_par = (pol*e_par).sum(1).reshape(-1,1) #I guessed this
    E_perp = (pol*e_perp).sum(1).reshape(-1,1) #I guessed this

    
    return e_ref_par*E_par - e_ref_perp*E_perp
    

def build(filename):

    #Read file, extract vertices and faces, build env in OptiX
    v, f = igl.read_triangle_mesh(filename)

    verts = v.flatten()
    verts = np.float32(verts)
    triangles = f.flatten()
    triangles = np.int32(triangles)



    res = optix.build(0, verts, triangles) #PASS 2 GPU
    assert res == 0
    return v,f

def shoot_and_record(hits_1, ray_pos, ray_dict, numrays):
        
        
    ray_temp = ray_pos[hits_1[:, 0] > 0, :]
    hit_temp = hits_1[hits_1[:, 0] > 0, :]
    o = ray_temp[:,0:3]
    k = ray_temp[:,4:7]
    n = hit_temp[:,1:4]
    p = (o + hit_temp[:,0:1]*k) + 1e-6 * n
    direction = k - 2* ((k*n).sum(1)).reshape(-1,1) *n
    ray_pos[hits_1[:, 0] > 0,0:3] = p
    ray_pos[hits_1[:, 0] > 0,4:7] = direction
         

    #update dictionary
    ray_dict[hits_1[:, 0] > 0,0] += hits_1[hits_1[:, 0] > 0,0]
    newpol = polarise(ray_dict[hits_1[:, 0] > 0, 1:4], k, direction, n)
    

    ray_dict[hits_1[:, 0] > 0, 1:4] = newpol
          
    numrays_1 = np.count_nonzero(hits_1[:, 0]>0)


    if numrays_1 > 0:
        hits = [[0,0,0,0] for i in range(numrays*numrays)]
        hits = np.float32(hits)
        hits = hits.flatten()

        rays = np.float32(ray_pos)
        rays = rays.flatten()

        res = optix.trace(rays,  hits, numrays*numrays)#PASS 2 GPU
        assert res == 0
        
        hits_1 = hits.reshape(numrays*numrays,4)
    
    return hits_1, ray_pos, ray_dict

def PO_Integral(ray_pos, r, pol, direction, tubediam, lam, dir_phi, dir_theta, dir_r):
    
    k = 2*np.pi/lam
    rayArea = tubediam*tubediam
    r_vec = k * dir_r
    
    E_ap = pol * np.exp(-1j * k*r)
    
    H_ap = np.cross(direction, E_ap)

    B_theta = ((np.cross(-dir_phi, E_ap) + np.cross(dir_theta, H_ap))*direction).sum(1)
    B_phi = ((np.cross(dir_theta, E_ap) + np.cross(dir_phi, H_ap))*direction).sum(1)

    factor = 1j*(k/(4*np.pi)) * rayArea * np.exp(1j*(r_vec*ray_pos).sum(1))

    E_theta = factor*B_theta
    E_phi = factor*B_phi

    return E_theta, E_phi    

def simulate(alpha, phi, theta, freq, raysperlam, v, f):

    lam = (3e8)/(freq)
    k = 2*np.pi/lam
    tubediam = lam/raysperlam
    
    #Get polarisation of wave
    polX = cosd(phi)*cosd(theta)*cosd(alpha)-sind(phi)*sind(alpha)
    polY = sind(phi)*cosd(theta)*cosd(alpha)+cosd(phi)*sind(alpha)
    polZ = -sind(theta)*cosd(alpha)
    pol = np.array([polX,polY, polZ]).T #initial pol

    #get bounding box
    bv,_  = igl.bounding_box(v)
    bbcentre = (np.max(bv, axis = 0) + np.min(bv, axis = 0))/2
    bbradius = igl.bounding_box_diagonal(v)/2


    #observation direction
    obsX = sind(theta)*cosd( phi )
    obsY = sind(theta)* sind( phi )
    obsZ = cosd(theta)
    ray_dir = -np.array([obsX,obsY,obsZ])


    #create initial ray pool
    #ant_centre = bbcentre - ray_dir*(bbradius+1)
    ant_centre =  0 - ray_dir*(bbradius+1)
    numrays = int(((bbradius*2))/(tubediam))
    _, up, right = ortho_set(phi, theta)
    pool_min =  ant_centre - ( right +up ) * bbradius

    up_step = tubediam * up
    right_step = tubediam * right

    pool_begin = pool_min + ( up_step + right_step ) / 2.0
    '''This is a naive implementation. A much faster way below.'''
    '''
    ray_pos = []


    for i in range(numrays):
        for j in range(numrays):
            temp = pool_begin + up_step*i + right_step*j
            ray_pos.append([temp[0], temp[1], temp[2], 0, ray_dir[0], ray_dir[1], ray_dir[2], 10000])
    '''
    
    '''Faster way using numpy arrays'''
    xx, yy = np.meshgrid(np.linspace(0, numrays-1, numrays), np.linspace(0, numrays-1, numrays))
    zz0 = (pool_begin[0] + up_step[0]*xx + right_step[0]*yy).reshape(-1)
    zz1 = (pool_begin[1] + up_step[1]*xx + right_step[1]*yy).reshape(-1)
    zz2 = (pool_begin[2] + up_step[2]*xx + right_step[2]*yy).reshape(-1)
    ray_pos = np.tile([0,0,0,0,ray_dir[0], ray_dir[1], ray_dir[2], 10000],(numrays*numrays,1))
    
    ray_pos[:,0] = zz0
    ray_pos[:,1] = zz1
    ray_pos[:,2] = zz2
    
    
    ray_pos = np.array(ray_pos)
    rays = np.float32(ray_pos)
    rays = rays.flatten()

    ray_dict = np.array([[0, pol[0], pol[1], pol[2]] for i in range(numrays*numrays)]) #index, distance, pol

    '''THIS IS THE BEGINNING SHOOTING'''

    #setup initial rays
    pol = np.tile(pol, (numrays*numrays,1))
    hits = [[0,0,0,0] for i in range(numrays*numrays)]
    hits = np.float32(hits)
    hits = hits.flatten()


    #perform ray trace
    res = optix.trace(rays,  hits, numrays*numrays)#PASS 2 GPU
    assert res == 0

    hits_1 = hits.reshape(numrays*numrays,4)


    

    hits_1, ray_pos, ray_dict = shoot_and_record(hits_1, ray_pos, ray_dict, numrays)
    hits_1, ray_pos, ray_dict = shoot_and_record(hits_1, ray_pos, ray_dict, numrays)
    hits_1, ray_pos, ray_dict = shoot_and_record(hits_1, ray_pos, ray_dict, numrays)
    hits_1, ray_pos, ray_dict = shoot_and_record(hits_1, ray_pos, ray_dict, numrays)

    dir_phi = np.array([-sind(phi)  , cosd(phi), 0])
    dir_theta = np.array([cosd(theta)*cosd(phi), cosd(theta)*sind(phi), -sind(theta)])
    dir_r = np.array([sind(theta)*cosd(phi)  , sind(theta)*sind(phi), cosd(theta)])

    r0 = np.linalg.norm(ant_centre)

    #Perform PO integral
    rays_tbc = ray_dict[ray_dict[:, 0] > 0]
    ray_pos_tbc = ray_pos[ray_dict[:, 0] > 0]
    r_prime = ray_pos_tbc[:,0:3]
    ray_pol = rays_tbc[:,1:4]
    direction = ray_pos_tbc[:,4:7]
    dist = rays_tbc[:,0:1]  - r0 #remove initial travel distance
    E_theta_comp, E_phi_comp = PO_Integral(r_prime, dist , ray_pol, direction ,tubediam, lam, dir_phi, dir_theta, dir_r)
    
    E_theta_sum = np.sum(E_theta_comp)
    E_phi_sum = np.sum(E_phi_comp)
    
    
        
    return E_theta_sum, E_phi_sum, r0


        









    


