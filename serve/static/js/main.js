//字体闪烁
function changeColor(){
    var color="#f00|#0f0|#00f|#880|#808|#088|yellow|green|blue|gray";
    color=color.split("|");
    document.getElementById("blink").style.color=color[parseInt(Math.random() * color.length)];
    }
setInterval("changeColor()",200);
//左侧导航
$(function(){loadMenu(function (id){});});
/*传入一个函数参数为 id 即li上的属性 aid*/
function loadMenu (fun_clickAction) {
  /*事件回调函数*/
  clickAction = fun_clickAction;
  /*一级菜单的样式*/
  $(".lmenu > ul > li > span").prepend('<em class="icoclose"></em>');
  /*二级菜单的样式*/
  $(".lmenu > ul > li > ul > li").each(function(){
    /*检查是否有节点*/
    span = $(this).find("span");
    if ( span.length ){
      //有节点的话
      span.prepend('<em class="icoclose2"></em>');
    }else{
      //无节点的话,绑定事件
      $(this).prepend('<em class="iconleaf"></em>')
           .click(function(){
            clickAction($(this).attr('aid'));
           });
    }
  });
  /*三级菜单的样式*/
  $(".lmenu > ul > li > ul > li > ul > li")
    .prepend('<em class="iconleaf2"></em>')
    .click(function(){
      clickAction($(this).attr('aid'));
    });

  $(".lmenu ul li span").click(function(){
    var ye = $(this).find('em');
    classNama = ye.attr("class");
    if( classNama == 'icoclose'){ye.attr('class','icoopen');}
    else if( classNama == 'icoopen' ){ye.attr('class','icoclose');}
    else if( classNama == 'icoclose2'){ye.attr('class','icoopen2');}
    else if( classNama == 'icoopen2' ){ye.attr('class','icoclose2');}
    $(this).siblings("ul").slideToggle("normal","swing");
  });
}
window.onload=function(){
    //上导航选项弹出
    let menu2=document.querySelector("#menu2");
    let mymenubar2=document.querySelector("#mymenubar2");
    menu2.onmouseenter=function () {
        mymenubar2.style.display="block"
    }
    menu2.onmouseleave=function () {
        mymenubar2.style.display="none"
    }
    //变换皮肤颜色
    let skin=document.querySelectorAll(".skin")
    let darkerSkin=document.querySelectorAll(".darkerSkin")
    let skin1=document.querySelector("#skin1");
    let skin2=document.querySelector("#skin2");
    let skin3=document.querySelector("#skin3");
    let skin4=document.querySelector("#skin4");
    let skin5=document.querySelector("#skin5");
    let skinvalue=localStorage.skinvalue?localStorage.skinvalue:"1";
    skin1.onclick=function () {
        localStorage.skinvalue="1"
        for(let i=0;i<skin.length;i++){
            skin[i].style.backgroundColor="#2F4050";
        }
        for(let i=0;i<darkerSkin.length;i++){
            darkerSkin[i].style.backgroundColor="#263949";
        }
    }
    skin2.onclick=function () {
        localStorage.skinvalue="2"
        for(let i=0;i<skin.length;i++){
            skin[i].style.backgroundColor="#327732";
        }
        for(let i=0;i<darkerSkin.length;i++){
            darkerSkin[i].style.backgroundColor="#245924";
        }
    }
    skin3.onclick=function () {
        localStorage.skinvalue="3"
        for(let i=0;i<skin.length;i++){
            skin[i].style.backgroundColor="#9c6728";
        }
        for(let i=0;i<darkerSkin.length;i++){
            darkerSkin[i].style.backgroundColor="#7f5928";
        }
    }
    skin4.onclick=function () {
        localStorage.skinvalue="4"
        for(let i=0;i<skin.length;i++){
            skin[i].style.backgroundColor="#6c3a88";
        }
        for(let i=0;i<darkerSkin.length;i++){
            darkerSkin[i].style.backgroundColor="#522867";
        }
    }
    skin5.onclick=function s5() {
        localStorage.skinvalue="5"
        for(let i=0;i<skin.length;i++){
            skin[i].style.backgroundColor="#999C9E";
        }
        for(let i=0;i<darkerSkin.length;i++){
            darkerSkin[i].style.backgroundColor="#898c8e";
        }
    }
    if(skinvalue==1){
        skin1.onclick()
    }else if(skinvalue==2){
        skin2.onclick()
    }else if(skinvalue==3){
        skin3.onclick()
    }else if(skinvalue==4){
        skin4.onclick()
    }else if(skinvalue==5){
        skin5.onclick()
    }
    //获取时间
    let myDate = new Date();
    let year = myDate.getFullYear();
    let month = myDate.getMonth()+1;
    let date = myDate.getDate();
    let timestr = year+"年"+month+"月"+date+"日"
    let time = document.querySelector("#time")
    time.innerText=timestr
}
