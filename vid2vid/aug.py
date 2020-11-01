import numpy as np
import imgaug
from imgaug import augmenters as I

SEED = np.random.randint(0, 100000)

imgaug.seed(SEED)#set integer or SEED here

def get_aug():
    seq = I.Sequential([I.Grayscale(alpha=1.0),
                        I.KMeansColorQuantization(n_colors=3)])


    
    return seq.augment_image
    
