#!/usr/bin/env python
# coding: utf-8
import web
import pickle
import os
import string
import configLoad

urls = ("/", "index",
		"/index\.html", "index",
        "/calibration\.html", "calibration",
        "/ranking\.html", "show_brief_result",)

render = web.template.render('templates/')
app = web.application(urls, globals())
points = []

class index:
    def GET(self):

        #files = os.listdir("static/camera")
        #print len(files)
        return render.index()

class calibration:
    def GET(self):
        #__init__
        picurl=''
        taskid='';
        name='';
        subpage=0;
        mfiles=[];
        pagenum=1;
        width=640;
        height=480;

        configLoad.load_cameras()
        configLoad.load_camera_config()
        i = web.input(subpage="0")
        subpage=int(i.subpage);

        if (subpage<0):
            return "error"

        name = []
        output = {}
        if subpage==0:
            for camera in configLoad.globalConfig['cameras']:
                name.append(camera['uid']);
        elif subpage==1:
            i = web.input(taskid="none", pagenum="0")
            pagenum = int(i.pagenum)
            taskid = i.taskid
            if (taskid != 'none'):
                mCameraConfig=None;
                for camera in configLoad.globalConfig['cameras']:
                    if taskid == camera['uid']:
                        mCameraConfig=camera;
                        break;
                if mCameraConfig is not None:
                    biaodingdir = mCameraConfig['frame_path'] +'/';
                    files = os.listdir(biaodingdir)
                    mfiles = [biaodingdir + '/' + mfile for mfile in files if configLoad.source_flag in mfile]
                    picurl = mfiles[pagenum]
                    print mCameraConfig['config']['config']
                    width=int(mCameraConfig['config']['config']['width']);
                    height = int(mCameraConfig['config']['config']['height']);


        output['IImagePath'] ='static/'+ picurl
        output['taskid'] = taskid
        output['name'] = name
        output['subpage'] = subpage
        output['sumpage'] = len(mfiles)
        output['pagenum'] = pagenum
        output['width'] = width
        output['height'] = height
        #return "hello"
        return render.calibration(output)

    def POST(self):
        def POST(self):
            i = web.input(action="")
            if i.action == "postpoints":
                i = web.input(action="", points="")
                if i.action == "postpoints":
                    arr = i.points.split(',')
                    for i in range(0, len(arr)):
                        arr[i] = int(arr[i])
                    global flag
                    global points
                    for i in range(0, len(arr), 2):
                        if i < len(arr) - 1:
                            a = [arr[i], arr[i + 1]]
                            points.append(a)
                    print points
                    return 'success'
                return "failure"

            if i.action == "Calculation":
                m = len(points)
                print m
                matrix = []
                vanish = []
                rate = []
                for i in range(0, m, 2):
                    j = 1
                    if points[i][j] > points[i + 1][j]:
                        b = points[i][j] - points[i + 1][j]
                        c = [points[i][j], b]
                        matrix.append(c)
                    else:
                        b = points[i + 1][j] - points[i][j]
                        c = [points[i + 1][j], b]
                        matrix.append(c)
                p = len(matrix)
                for i in range(0, p):
                    for j in range(i + 1, p):
                        b = (matrix[i][0] * matrix[j][1] - matrix[j][0] * matrix[i][1]) / (matrix[j][1] - matrix[i][1])
                        vanish.append(b)
                        c = (matrix[i][1] / (matrix[i][0] - b) + matrix[j][1] / (matrix[j][0] - b)) / 2
                        rate.append(c)
                print vanish
                print rate
                f = file("data.txt", "w")
                li = ["Vanishing point = " + str(sum(vanish) / len(vanish)) + "\n",
                      "Rate of change = " + str(sum(rate) / len(rate)) + "\n"]
                f.writelines(li)
                f.close()
                outstr = str(sum(vanish) / len(vanish)) + "," + str(sum(rate) / len(rate))
                return outstr
        return "failure"


source_flag=configLoad.source_flag;
result_flag=configLoad.result_flag;
boundingbox_flag=configLoad.boundingbox_flag
class show_brief_result:
    def GET(self):
        configLoad.load_cameras();
        configLoad.load_camera_config();
        result_to_show=[];
        for camera in configLoad.globalConfig['cameras']:
            frames_path=camera['frame_path'];

            if camera.has_key('savedProgress'):
                cameradata={};
                cameradata['uid']=camera['uid'];
                oneImage=camera['savedProgress'];
                resimage_path=camera['result_personarea_path']+'/'+oneImage.replace(source_flag,result_flag);
                #resimage = Image.open(camera['result_personarea_path']+'/'+oneImage.replace(source_flag,result_flag))
                cameradata['image']=resimage_path;
                frames=[];
                with open(camera['result_person_box_path']+'/'+oneImage.replace(source_flag,boundingbox_flag)) as fframes:
                    for line in fframes:
                        values=line.split(' ');
                        frames.append((int(values[0]),int(values[1]),int(values[2]),int(values[3]),float(values[4])));
                cameradata['frames']=frames;

                
                result_to_show.append(cameradata);
        i = web.input(orderby="default");
        if i.orderby=='count':
            #print len(result_to_show[0]['frames'])
            result_to_show.sort(key=lambda x:len(x['frames']),reverse=True);
        return render.mainpage(result_to_show);



if __name__ == "__main__":
    app.run()
