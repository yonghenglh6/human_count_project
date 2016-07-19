import configLoad
#import crash_on_ipy
import CheckNewImage
import NdetectPerson
import maineval_voc
import time
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import boxTu
run=True;

net=maineval_voc.initNet();

source_flag=configLoad.source_flag;
result_flag=configLoad.result_flag;
boundingbox_flag=configLoad.boundingbox_flag

while run:
    configLoad.load_cameras();
    configLoad.load_camera_config();
    for camera in configLoad.globalConfig['cameras']:
        #check max number;
        #camera
        #
        frames_path=camera['frame_path'];
        if camera.has_key('savedProgress'):
            oneImage=CheckNewImage.get_last_new_image(frames_path,filter=source_flag,saved_progress=camera['savedProgress']);
        else:
            oneImage=CheckNewImage.get_last_new_image(frames_path,filter=source_flag);
        if oneImage=='':
            continue;
        originimage = Image.open(frames_path+'/'+oneImage)
        print 'dealing:' + oneImage
        midImage=maineval_voc.processImage(net,originimage)
        #origin = np.array(originimage, dtype=np.uint8)
        originimage=np.array(originimage, dtype=np.uint8);

        density=maineval_voc.getSoftMaxDensity(midImage);
        area=maineval_voc.getPersonArea(midImage);
        mix=maineval_voc.mixPicutre2(originimage,area,0,5);


        #plt.imsave(camera['result_softdensity_path']+'/'+oneImage.replace('.source.','.fcn_sm.'),density)
        #plt.imsave(camera['result_personarea_path']+'/'+oneImage.replace('.source.','.fcn_pa.'),area)

        density=density*255;
        area[area==15]=30;

        #densityImage=Image.open(camera['result_softdensity_path']+'/'+oneImage);
        #areaImage=Image.open(camera['result_personarea_path']+'/'+oneImage);
        #print area.shape;
        #print np.max(area);
        #print density.shape;
        #print np.max(density);
        #frames=NdetectPerson.detectPersons(areaImage=areaImage,densityImage=densityImage);
        frames=NdetectPerson.detectPersons(area=area,cameraconfig=camera, density=density);

        image_with_frame=boxTu.boxTu(mix,frames)
        plt.imsave(camera['result_personarea_path']+'/'+oneImage.replace(source_flag,result_flag),image_with_frame);

        with open(camera['result_person_box_path']+'/'+oneImage.replace(source_flag,boundingbox_flag),'w') as fframes:
            for frame in frames:
                oneline='';
                for fvalue in frame:
                    oneline+=str(fvalue)+' ';
                fframes.writelines(oneline+'\n');

        print frames;

        camera['savedProgress']=oneImage;
        #print oneImage;
    configLoad.save_camera_config();
    time.sleep(5);
    print 'one circle is done.'