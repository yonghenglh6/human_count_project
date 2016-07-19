from PIL import Image
import numpy as np
import framebox
import matplotlib.pyplot as plt

def boxTu(image,frames):
    #image=Image.open('camera/001/001.rs.jpg');
    #image=np.array(image,dtype=np.uint8);
    #frames=[(139,127,28,58,29.3)]
    for frame in frames:
        boundingbox=framebox.boundingbox();
        boundingbox.read(frame);
        image[boundingbox.TOP:boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT,:]= 255;
        image[boundingbox.TOP:boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT+boundingbox.WIDTH,:]= 255;
        image[boundingbox.TOP,boundingbox.LEFT:boundingbox.LEFT+boundingbox.WIDTH,:]= 255;
        image[boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT:boundingbox.LEFT+boundingbox.WIDTH,:]= 255;
    return image
#plt.imsave('ssa1.jpg',image);



#boxTu(None,None)