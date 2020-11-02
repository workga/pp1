import numpy as np
import imgaug
from imgaug import augmenters as I

#......................PARAMETERS...........................#

train_A = 'config_train'
train_B = 'config_train'

test_A  = 'config_test'
test_B  = 'config_test'

seed    = 0;

aug_n   = 0;
augs    = [[I.Grayscale(alpha=1.0),
            I.KMeansColorQuantization(n_colors=3)],
           [I.KMeansColorQuantization(n_colors=3)]]

#...........................................................#

if (seed != 0):
    imgaug.seed(seed)
else:
    imgaug.seed(np.random.randint(0, 100000))

def get_aug():
    return I.Sequential(augs[aug_n]).augment_image

    
