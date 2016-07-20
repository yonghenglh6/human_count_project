import ConfigParser
import string
import os
globalConfig = {}
source_flag='.src.jpg';
result_flag='.rs.jpg';
boundingbox_flag='.bbox.txt'

def load_cameras():
    globalConfig['cameras'] = [];
    camera_dirs=os.listdir('camera');
    for camera_dir in camera_dirs:
        if os.path.isdir('camera/'+camera_dir):
            cameramm = {'uid': camera_dir,
                         'base_path': 'camera/'+camera_dir+'/',
                         'config_path': 'camera/'+camera_dir+'/'+'config/',
                         'frame_path': 'camera/'+camera_dir+'/',
                         'result_softdensity_path': 'camera/'+camera_dir+'/',
                         'result_personarea_path': 'camera/'+camera_dir+'/',
                         'result_person_path': 'camera/'+camera_dir+'/',
                         'result_person_box_path':'camera/'+camera_dir+'/'};
            globalConfig['cameras'].append(cameramm);


def load_camera_config():
    for camera in globalConfig['cameras']:
        configPath = camera['config_path'];

        camera['config'] = {};
        camera['config']['config']={};
        camera['config']['config']['mainBoxThreshold']='5';
        camera['config']['config']['maxBoxNumPerImage']='200';
        camera['config']['config']['showResult']='0';
        camera['config']['config']['areaFilter']='True';
        camera['config']['config']['areaFilterThreshold']='26';
        camera['config']['config']['width']=640;
        camera['config']['config']['height']=480;

        if os.path.exists(configPath+'baseconfig'):
            #Base config
            baseconfig = ConfigParser.ConfigParser()
            baseconfig.read(configPath+'baseconfig')

            for section in baseconfig.sections():
                if not camera['config'].has_key(section):
                    camera['config'][section] = {};
                for option in baseconfig.options(section):
                    camera['config'][section][option] = baseconfig.get(section, option);

        if os.path.exists(configPath+'vanishpoint'):
            #vanishpoint config
            with open(configPath+'vanishpoint') as vf:
                data=vf.readline().split(' ');
                camera['vanishPoint']=string.atof(data[0].strip());
                camera['rate1']=string.atof(data[1].strip());
                camera['bodyRate']=string.atof(data[2].strip());

        if os.path.exists(configPath+'savedprocess'):
            #savedProgress config
            with open(configPath+'savedprocess') as vf:
                data=vf.readline();
                camera['savedProgress']=data;


def save_camera_config():
    for camera in globalConfig['cameras']:
        configPath = camera['config_path'];
        if camera.has_key('savedProgress'):
            if os.path.exists(configPath):
                #savedProgress config
                with open(configPath+'savedprocess','w') as vf:
                    vf.writelines(camera['savedProgress']);
            else:
                print "ERROR,configPath not exists!";
#load_cameras();
#load_camera_config();
