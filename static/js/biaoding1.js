
var points=new Array();
var sign=0;
var c;
var cxt;
var img;


function PrePage(){
    if(pagenum<=0){
        alert("已经到第一张了");
    }
    else{
        pagenum=pagenum-1;
        a = points.join();
        $.post("biaoding.html?action=postpoints&points="+a,{},function(data,status){
        alert(data);
        });
        loadurl(window.subpage,pagenum);
    }
}

function AfterPage(){
    if(pagenum>=sumpage-1){
        alert("已经到最后一张了");
    }
    else{
        pagenum=pagenum+1;
        a = points.join();
        $.post("biaoding.html?action=postpoints&points="+a,{},function(data,status){
        alert(data);
        });
        loadurl(window.subpage,pagenum);
    }
}

function loadurl(subpage,pagenum){
     if(subpage==window.subpage){
        //alert("biaoding.html?subpage="+subpage+"&pagenum="+pagenum+"&taskid="+taskid);
        window.open("biaoding.html?subpage="+subpage+"&pagenum="+pagenum+"&taskid="+taskid,'_self');
     }
}

function submitPage(){
    $.post("biaoding.html?action=Calculation",{},function(data,status){
        //alert(data);
        var arrayObj = new Array();
        arrayObj =data.split(",");
        document.getElementById("vanishing").innerHTML=arrayObj[0];
        document.getElementById("rateing").innerHTML=arrayObj[1];
        //alert(arrayObj[1]);
     });
}

//侧栏切换效果
$(document).ready(function(e) {
    subpage=window.subpage;
            $(".tabItemContainer>li>a").removeClass("tabItemCurrent");
			$(".tabBodyItem").removeClass("tabBodyCurrent");
    if(subpage==0){
			$($(".tabItemContainer>li")[0]).find("a").addClass("tabItemCurrent");
			$($(".tabBodyItem")[0]).addClass("tabBodyCurrent");

    }else if(subpage==1){
			$($(".tabItemContainer>li")[1]).find("a").addClass("tabItemCurrent");
			$($(".tabBodyItem")[1]).addClass("tabBodyCurrent");
			$(".subcamera_or_not").show();
    }
//    else if (subpage==2){
//			$($(".tabItemContainer>li")[2]).find("a").addClass("tabItemCurrent");
//			$($(".tabBodyItem")[1]).addClass("tabBodyCurrent");
//    }
});
function getTop(e){
    var offset=e.offsetTop;
    if(e.offsetParent!=null) offset+=getTop(e.offsetParent);
    return offset;
}
//获取元素的横坐标
function getLeft(e){
    var offset=e.offsetLeft;
    if(e.offsetParent!=null) offset+=getLeft(e.offsetParent);
    return offset;
}

//计算所画点的坐标并添加到数组
//	document.getElementById("myCanvas").onclick = function(){positionObj(event,"myCanvas")};
function positionObj(event,id){
    var thisX = getLeft(document.getElementById(id));
    var thisY = getTop(document.getElementById(id));
    subpage=window.subpage;

    x = event.clientX - thisX;
    y = event.clientY - thisY;
    //document.getElementById("signal_x").innerHTML=x;
    //document.getElementById("signal_y").innerHTML=y;

    points[sign]=new Array();
    points[sign][0]=x;
    points[sign][1]=y;
    sign+=1;
    if (subpage == 1){
        drawlines();
    }
//		var imageData = cxt.getImageData(0,0,640,480);
//		var i=y*640*4+x*4;
//		imageData.data[i]=255;
//		imageData.data[i+1]=0;
//		imageData.data[i+2]=0;
//		imageData.data[i+3]=255;
//		cxt.putImageData(imageData,0,0);
}

//画点程序
function drawpoints(){
    cxt.fillStyle="ffffff";
    cxt.fillRect(0,0,640,480);
    cxt.drawImage(img,0,0);
    for(var i=0;i<sign;i++){
        cxt.beginPath();
        cxt.fillStyle="#FF0000";
        cxt.arc(points[i][0],points[i][1],2,0,Math.PI*2,true);
        cxt.closePath();
        cxt.fill();
    }
}

function drawlines(){
    cxt.fillStyle="ffffff";
    cxt.fillRect(0,0,640,480);
    cxt.drawImage(img,0,0);
    if(sign <2){
        return 0;
    }
    if (sign % 2 == 0){
        for(var i=0;i<sign;i++){
        cxt.beginPath();
        cxt.fillStyle="#FF0000";
        cxt.moveTo(points[i][0],points[i][1]);
        cxt.lineTo(points[i+1][0],points[i+1][1]);
        cxt.lineWidth = 2;
        cxt.strokeStyle="red";
        cxt.stroke();
        i += 1;
        }
    }else if(sign % 2 == 1){
        for(var i=0;i<sign-1;i++){
        cxt.beginPath();
        cxt.fillStyle="#FF0000";
        cxt.moveTo(points[i][0],points[i][1]);
        cxt.lineTo(points[i+1][0],points[i+1][1]);
        cxt.lineWidth = 2;
        cxt.strokeStyle="red";
        cxt.stroke();
        i += 1;
        }
    }
}

window.onload = function(){
    points;
    sign=0;
    c=document.getElementById("myCanvas");
    cxt=c.getContext("2d");
    img=new Image()
    img.src=window.IImagePath;
    /*img.src = "http://localhost:8080/static/data/malldata/seq_000003.jpg";*/
    //img.src="static/data/1.jpg";
    img.onload=function(){
        cxt.drawImage(img,0,0);
   }

    //？？？
    document.oncontextmenu = function(event){
           event.preventDefault();
    };

    //左键，右键单击事件流
    document.getElementById("myCanvas").onmousedown = function(event){
        subpage=window.subpage;
        if(event.button == 2)
        {
            if(sign!=0){
                sign-=1;
            }
            if (subpage == 1){
               drawlines();
            }
        }else if(event.button == 0){
            positionObj(event,"myCanvas");
        }
        return true;
    }
}


