
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import time
#%matplotlib inline
###########
def dealDataset(sourcedir,outputdir,fcnversion='pascalcontext',framename_post="jpg",useCPU=0):
	#sourcedir='/home/user/workspace/liuhao/data/smartcity/uncompressed_baoweibu_2_1280x720_30/'
	#outputdir='output_oldfcn_baoweibu_2_1280x720_30/'
	#fcnversion='pascalcontext'
	#framename_post="jpg"
	#useCPU=0
	###########Init data


	frames=os.listdir(sourcedir);
	frames=[imagename for imagename in frames if imagename.endswith(framename_post)]
	if(len(frames)==0):
		print 'Source dir contains no data.'
		exit();
	imFirst=Image.open(sourcedir+'/'+frames[0]);
	size=imFirst.size;
	imFirst.close()
	##########

	if not os.path.exists(outputdir):
		os.makedirs(outputdir);
	output_dirName={'origin':outputdir+'/origin/','parea':outputdir+'/parea/','mix':outputdir+'/mix/','dens':outputdir+'/dens/','classrs':outputdir+'/classrs/','sdens':outputdir+'/sdens/'};
	for key,value in output_dirName.iteritems():
		if not os.path.exists(value):
			os.makedirs(value);



	if fcnversion=='oldpascal':
		import maineval_oldfcn as maineval
	elif fcnversion=='voc':
		import maineval_voc as maineval
	elif fcnversion=='pascalcontext':
		import maineval_pascalcontext as maineval
	else:
		import maineval_pascalcontext as maineval

	if useCPU==1:
		net=maineval.initNet('cpu');
	else:
		net=maineval.initNet('gpu');

	for imagename in frames:
		imagePathSrc=sourcedir+'/'+imagename;

		im = Image.open(imagePathSrc)
		im = np.array(im, dtype=np.uint8)

		##ProcessImage
		k1=time.time()
		oImage=maineval.processImage(net,im)
		k2=time.time()
		print k2-k1


		##origin
		plt.imsave(output_dirName['origin']+imagename,im)
		##parea
		oimg=maineval.getPersonArea(oImage);
		plt.imsave(output_dirName['parea']+imagename,oimg)
		##mix
		mmimg=maineval.mixPicutre2(im,oimg,0,5);
		plt.imsave(output_dirName['mix']+imagename,mmimg)
		##dens
		I=maineval.getDensity(oImage);
		I8 = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
		img = Image.fromarray(I8)
		img.save(output_dirName['dens']+imagename,)
		##classrs
		oimg=maineval.getArea(oImage);
		plt.imsave(output_dirName['classrs']+imagename,oimg)
		##sdens
		I=maineval.getSoftMaxDensity(oImage);
		I8 = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
		img = Image.fromarray(I8)
		img.save(output_dirName['sdens']+imagename,)




