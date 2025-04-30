import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
import random as rd
import cv2
import math
import os
import pathlib

def rgb_img (image,
             resize=(1000,1000)) :
    """Resize and split the image in three images (RGB)
    
    Args:
        image : numpy.ndarray
            Original image
        resize : optionnal, tuple
            New size (should be less than original size)
       
    Returns:
        r_img : numpy.ndarray
            Red image
        g_img : numpy.ndarray
            Green image
        b_img : numpy.ndarray
            Blue image
    """
    img = cv2.imread(image)
    img[:,:,[2, 0]] = img[:,:,[0, 2]]
    r_img, g_img, b_img = img[:,:,0],img[:,:,1],img[:,:,2]
    r_img = cv2.resize(r_img, resize, 4, 4)
    g_img = cv2.resize(g_img, resize, 4, 4)
    b_img = cv2.resize(b_img, resize, 4, 4)
    return (r_img,g_img,b_img)

def image_rgb_split(image,
                    r_disp = [0,310],
                    g_disp = [-33,50],
                    b_disp = [0,0],
                    limits = False,
                    resize=(1000,1000)) :
    """Resize and tranform the original image in three images (RGB) and merge
    them together with a displacement of each canal.
    
    Args:
        image : numpy.ndarray
            Original image
        r_disp : optionnal, tuple
            Displacement vector of the Red image
        g_disp : optionnal, tuple
            Displacement vector of the Green image
        b_disp : optionnal, tuple
            Displacement vector of the Blue image
        resize : optionnal, tuple
           New size (should be less than original size)
       
    Returns:
        new_img : numpy.ndarray
            Transformed image
    """
    r_img,g_img,b_img = rgb_img(image,
                                resize = resize)
    ny,nx = r_img.shape
    r0,r1 = r_disp
    g0,g1 = g_disp
    b0,b1 = b_disp
    if limits :
        y_pixel, x_pixel = limits
    else :
        x_pixel = max(abs(r1),abs(g1),abs(b1))
        y_pixel = max(abs(r0),abs(g0),abs(b0))
    new_img = np.zeros((ny+2*y_pixel,nx+2*x_pixel,3), dtype = int)
    new_img[y_pixel+r0:y_pixel+ny+r0,x_pixel+r1:x_pixel+nx+r1,2]=b_img
    new_img[y_pixel+g0:y_pixel+ny+g0,x_pixel+g1:x_pixel+nx+g1,1]=g_img
    new_img[y_pixel+b0:y_pixel+ny+b0,x_pixel+b1:x_pixel+nx+b1,0]=r_img
    new_img = new_img[2*y_pixel:-2*y_pixel,2*x_pixel:2*-x_pixel,:]
    return (new_img)

def ellipse (ab = (1,1),
             center = (0,0),
             Phi = 0,
             n_frames = 20,
             plot = False,
             **kwargs) :
    """Create an elliptic trajectory stack in an numpy array.
    
    Args:
        ab : optionnal,tuple
            Dimensions of the ellipse
        center : optionnal, tuple
            Center of the ellipse
        Phi : optionnal, float
            Rotation of the ellipse (in degree)
        n_frames : optionnal, int
            Number of frames/points of discretisation of the trajectory
        plot : optionnal, boolean
           If True, plot the ellipse trajectory
       
    Returns:
        xy : numpy.ndarray
            All the position of the ellipse trajectory
    """
    alpha = np.arange(n_frames)*2*math.pi/n_frames
    x = []
    y = []
    a,b = ab
    for al in alpha :
        xi = a*math.cos(al)
        yi = b*math.sin(al)
        xphi = xi*math.cos(Phi) + yi*math.sin(Phi) + center[0]
        yphi = yi*math.cos(Phi) - xi*math.sin(Phi) + center[1]
        if plot :
            plt.scatter(xphi, yphi, **kwargs)
        x.append(int(xphi))
        y.append(int(yphi))
    xy = np.asarray([x,y])
    xy = np.transpose(xy)
    return(xy)

def random_list_insert (t_list,
                        p = 0.1,
                        r = 1) :
    """Introduce chaos in any trajectory list.
    
    Args:
        t_list : list
            Trajectory list (of the ellipse function mostly)
        p : optionnal, float
            Probability to insert a chaotic movement in each frame
        r : optionnal, float
            Max radius of the chaos introduced
       
    Returns:
        new_list : numpy.ndarray
            All the position of the ellipse trajectory (chaotic)
    """
    n = len(t_list)
    c_range = r*np.max(t_list)
    new_list = t_list
    nb_chaos = int(p*n)
    for j in range (nb_chaos) :
        i = rd.randint(0,n)
        new_list = np.append(new_list, np.array([rd.randint(0,c_range),rd.randint(0,c_range)]))
        new_list = np.reshape(new_list, (n+j+1,2))
        new_list[[-1, i],:] = new_list[[i, -1],:]
    new_list = new_list[:n]
    return(new_list)

def random_black_line_vertical_horizontal(img,
                                          p = (0.1, 0.1, 0.1),
                                          line_thickness = 2) :
    """Introduce black lines on an image.
    
    Args:
        img : np.ndarray
            Original image
        p : optionnal, tuple
            Probability to insert a chaotic line for each color (RGB)
        line_thickness : optionnal, float
            Thickness of each line
       
    Returns:
        new_img : numpy.ndarray
            Transformed image
    """
    m,n,_ = img.shape
    new_img = img
    for color in range(3) :
        for e in range (int(p[color]*n)) :
            i = rd.randint(0,n-1)
            for line in range(line_thickness) :
                try :
                    new_img[:,i+line,color] = 0
                except :
                    ()
        for e in range (int(p[color]*m)) :
            i = rd.randint(0,m-1)
            for line in range(line_thickness) :
                try :
                    new_img[i+line,:,color] = 0
                except :
                    ()
    return(new_img)

def random_black_line(img,
                      n_lines = 10,
                      p = 0.1) :
    """Introduce black lines on an image.
    
    Args:
        img : np.ndarray
            Original image
        n_lines : optionnal, int
            Number of random test
        p : optionnal, tuple
            Probability to insert a chaotic line for each color (RGB)

    Returns:
        new_img : numpy.ndarray
            Transformed image
    """
    new_img = img
    for _ in range (n_lines) :
        if rd.randint(1,int(1/p)) == 1 :
            mask = np.ones(new_img.shape)
            n,m,l = mask.shape
            a1 = rd.randint(0,n)
            a2 = rd.randint(0,n)
            b1 = rd.randint(0,m)
            b2 = rd.randint(0,m)
            size = rd.randint(0,100)
            for i in range (n) :
                for j in range (m) :
                    try :
                        distance = (i-a1)*(j-b2)-(i-a2)*(j-b1)
                    except :
                        distance = size * 2
                    if abs(distance) < size :
                        if (i-a1) :
                            mask[i,j,:] = 0
            new_img = new_img*mask
    return(new_img)


def random_color_exchange (img,
                           p = 0.1) :
    """Introduce color swap (RG or RB or GB) on an image.
    
    Args:
        img : np.ndarray
            Original image
        p : optionnal, tuple
            Probability to insert a chaotic color exchange (RGB)

    Returns:
        new_img : numpy.ndarray
            Transformed image
    """
    new_img = img
    if rd.randint(1,int(2/(3*p))) == 1 :
        i = rd.randint(0,2)
        j = rd.randint(0,2)
        new_img[:,:,[i, j]] = new_img[:,:,[j, i]]
    return(new_img)
    
def random_full_black (img,
                       p = 0.1) :
    """Introduce black image.
    
    Args:
        img : np.ndarray
            Original image
        p : optionnal, tuple
            Probability to insert a chaotic black image

    Returns:
        new_img : numpy.ndarray
            Transformed image
    """
    new_img = img
    if rd.randint(1,int(1/p)) == 1 :
        new_img = new_img*0
    return(new_img)
    
def random_full_negative(img,
                         p = 0.1) :
    """Introduce negative image.
    
    Args:
        img : np.ndarray
            Original image
        p : optionnal, tuple
            Probability to insert a chaotic negative image

    Returns:
        new_img : numpy.ndarray
            Transformed image
    """
    new_img = img
    if rd.randint(1,int(1/p)) == 1 :
        new_img = -new_img+255
    return(new_img)

def animation_image(img,
                    r_dict,
                    g_dict,
                    b_dict,
                    saving_folder = '',
                    t_frame = 5,
                    n_lines = 10,
                    p_black_line = 0.2,
                    p_color_exchange = 0.2,
                    p_full_black = 0.1,
                    p_full_negative = 0.1,
                    resize = (600,600)) :
    """Create .gif video from an image.
    
    Args:
        img : np.ndarray
            Original image
        r_dict : dict
            Red dictionnary
        g_dict : dict
            Green dictionnary
        b_dict : dict
            Blue dictionnary
        saving_folder : optionnal, str
            Folder to save transformed images and .gif
        t_frame : optionnal,float
            Time for each frame
        n_lines : optionnal, int
            Number of random test
        p_black_line : optionnal, float
            Probability to insert a chaotic black lines
        p_color_exchange : optionnal, float
            Probability to insert a chaotic color exchange
        p_full_black : optionnal, float
            Probability to insert a chaotic black image
        p_full_negative : optionnal, float
            Probability to insert a chaotic negative image
        resize : optionnal, tuple
            Size of the new image (Have to be smaller than the original one)
    """
    r_list = ellipse (ab = r_dict['ab'], center = r_dict['center'], Phi = r_dict['Phi'], n_frames = r_dict['n_frames'])
    g_list = ellipse (ab = g_dict['ab'], center = g_dict['center'], Phi = g_dict['Phi'], n_frames = g_dict['n_frames'])
    b_list = ellipse (ab = b_dict['ab'], center = b_dict['center'], Phi = b_dict['Phi'], n_frames = b_dict['n_frames'])
    r_list = random_list_insert(r_list, p=r_dict['p'])
    g_list = random_list_insert(g_list, p=g_dict['p'])
    b_list = random_list_insert(b_list, p=b_dict['p'])
    limits = [int(np.max(abs(np.asarray([r_list[:,0],g_list[:,0],b_list[:,0]])))),
              int(np.max(abs(np.asarray([r_list[:,1],g_list[:,1],b_list[:,1]]))))]
    n_frames = r_dict['n_frames']
    n_frames2 = g_dict['n_frames']
    n_frames3 = b_dict['n_frames']
    if n_frames!=n_frames2 or n_frames!=n_frames3 :
        print('n_frames is not the same for all coloors dict. The chosen one is from r_dict = ', n_frames)
    def update (i) :
        print('Image ' + str(i+1) + '/' + str(n_frames))
        new_img = image_rgb_split(img,
                                  r_disp = r_list[i],
                                  g_disp = g_list[i],
                                  b_disp = b_list[i],
                                  limits = limits,
                                  resize = resize)
        new_img[:,:,[2, 0]] = new_img[:,:,[0, 2]]
        new_img = random_black_line(new_img, n_lines = n_lines, p = p_black_line)
        new_img = random_color_exchange(new_img, p = p_color_exchange)        
        new_img = random_full_black(new_img, p = p_full_black)        
        new_img = random_full_negative(new_img, p = p_full_negative)
        return(new_img)
    if not os.path.exists(saving_folder) :
        P = pathlib.Path(saving_folder)
        pathlib.Path.mkdir(P, parents = True)
    iio_imgs = []
    for i in range(n_frames):
        new_img = update(i)
        numname = str(i+1)
        l10 = int(np.log10(i+1))
        for e in range (int(np.log10(n_frames))-l10) :
            numname = '0'+ numname
        name = saving_folder +numname+".png"
        cv2.imwrite(name, new_img) 
        iio_imgs.append(iio.imread(name))
    iio.imwrite(saving_folder+'result.gif',
                iio_imgs,
                duration = t_frame*n_frames,
                loop = 0)

def zoom(img,
         position = False,
         magnification = 2) :
    ()