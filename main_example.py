import transformations_library as tl
import os

if __name__ == '__main__' :    
    img = 'Img_expl.png'
    saving_folder = os.getcwd()+'\\result_expl\\'
    frames = 30
    r_dict = {'ab' : (10, 0),
             'center' : (0,0),
             'Phi' : 0,
             'n_frames' : frames,
             'p' : 0.05}
    g_dict = {'ab' : (50,60),
             'center' : (0,10),
             'Phi' : 0,
             'n_frames' : frames,
             'p' : 0.05}
    b_dict = {'ab' : (5,15),
             'center' : (60,0),
             'Phi' : 1/2,
             'n_frames' : frames,
             'p' : 0.05}
    tl.animation_image(img,
                       r_dict,
                       g_dict,
                       b_dict,
                       saving_folder = saving_folder,
                       t_frame = 5,
                       n_lines = 30,
                       p_black_line = 0.2,
                       p_color_exchange = 0.2,
                       p_full_black = 0.1,
                       p_full_negative = 0.1,
                       resize = (600,600))
