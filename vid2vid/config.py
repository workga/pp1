import numpy as np
import imgaug
from imgaug import augmenters as I

#......................PARAMETERS...........................#

path_A = "config_test"
path_B = "config_test"
seed   = 0;
seq    = [I.Grayscale(alpha=1.0),
          I.KMeansColorQuantization(n_colors=3)]

#...........................................................#

if (seed != 0):
    imgaug.seed(seed)
else:
    imgaug.seed(np.random.randint(0, 100000))

def get_aug():
    return I.Sequential(seq).augment_image

def get_path_A():    
    return path_A

def get_path_B():    
    return path_B

    
