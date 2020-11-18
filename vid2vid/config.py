import numpy as np
import imgaug
from imgaug import augmenters as I

#......................PARAMETERS...........................#

seed    = 0;

augs    = [[I.Grayscale(alpha=1.0),
            I.KMeansColorQuantization(n_colors=5)],

           [I.KMeansColorQuantization(n_colors=8)],

           [I.UniformColorQuantization(n_colors=8, max_size=None)],

           [I.Grayscale(alpha=1.0),
            I.UniformColorQuantization(n_colors=8, max_size=None)],

           [I.UniformColorQuantization(n_colors=8, max_size=None),
            I.Grayscale(alpha=1.0)],

           [I.UniformColorQuantization(n_colors=8, max_size=None)]]

noises  = [[I.AdditiveGaussianNoise(scale=(0, 0.2*255))]]

#...........................................................#

if (seed != 0):
    imgaug.seed(seed)
else:
    imgaug.seed(np.random.randint(0, 100000))

def get_aug(n_aug):
    return I.Sequential(augs[n_aug]).augment_image

def get_noise():
    return I.Sequential(noises[0]).augment_image

    
