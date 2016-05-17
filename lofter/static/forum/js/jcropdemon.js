/**
 * Created by Administrator on 2016-04-02.
 */

$(function () {
    var $ = jQuery,
        $list = $('#fileList'),
    // 优化retina, 在retina下这个值是2
        ratio = window.devicePixelRatio || 1,
    // 缩略图大小
        thumbnailWidth = 300 * ratio,
        thumbnailHeight = 300 * ratio,
    // Web Uploader实例
        uploader,
        jcrop_api,



    // Grab some information about the preview pane
        $preview = $('#preview-pane'),
        $pcnt = $('#preview-pane .preview-container'),
        $mpcnt = $('#preview-pane .mpreview-container'),
        $pimg = $('#preview-pane .preview-container img'),
        $pimg1 = $('#preview-pane .mpreview-container img'),

        xsize = $pcnt.width(),
        ysize = $pcnt.height(),
        mxsize = $mpcnt.width(),
        mysize = $mpcnt.height();


    uploader = WebUploader.create({
        // 选完文件后，是否自动上传。
        auto: true,
        thumb:true,
        duplicate:true,
        // swf文件路径
        swf: '/static/forum/Uploader.swf',

        // 文件接收服务端。
        server: '/forum/post_setting/',

        // 选择文件的按钮。可选。
        // 内部根据当前运行是创建，可能是input元素，也可能是flash.
        pick: $('#filePicker'),

        //只允许选择图片
        accept: {
            title: 'Images',
            extensions: 'gif,jpg,jpeg,bmp,png',
            mimeTypes: 'image/*'
        },

        fileNumLimit:300,

    });

    //初始化结束，开始事件
    //上传一张图片后增加一个更换按钮

    //上传成功以后更换图片
    uploader.on('uploadSuccess', function (file, response) {
        if(response.error){
            alert('no')
        }
        else{
            alert('ok')

            $('#filePicker').remove();
            uploader.addButton({
                id:"#file2",
                innerHTML:"更换图片",
            });
            $('.webuploader-pick').css({'background':'white','color':'gray',
                'left':'3px','top':'-10px','font-size':'0.1em'});

            boundx=response.width;
            boundy=response.height;

            $('#target').Jcrop({
                onChange: updatePreview,
                onSelect: updatePreview,
                aspectRatio: xsize / ysize,
            },function(){
                // Use the API to get the real image size
                // var bounds = this.getWidgetSize();


                // Store the API in the jcrop_api variable
                jcrop_api = this;


                // Move the preview into the jcrop container for css positioning
                $preview.appendTo(jcrop_api.ui.holder);
            });



            jcrop_api.setImage(response.address);
            if (response.width <response.height){
                var left =(450-response.width)/2;
                $('.jcrop-holder').css({'left':left+'px','top':'0px'});
                $('.jcrop-holder #preview-pane ').css({'top':'10px','left':'400px'});
            }
            else{
                var top = (350-response.height)/ 2;
                $('.jcrop-holder').css({'top':top+'px','left':'0px'});
                $('.jcrop-holder #preview-pane ').css({'top':'-70px','left':'480px'});
            }

            $('.jcrop-preview').attr('src',response.address);}
    });
    function updatePreview(c){

        if (parseInt(c.w) > 0) {
            imgwidth = c.w;
            imgheight = c.h ;
            imgmarginLeft = c.x ;
            imgmarginTop = c.y ;
            var rx = xsize / c.w;
            var ry = ysize / c.h;
            var mrx= mxsize / c.w;
            var mry = mysize / c.h;


            /* console.log('boundy:'+boundy);
             console.log("new width:"+Math.round(rx * boundx) );
             console.log("new height:"+Math.round(ry * boundy) );
             console.log("marginLeft:"+Math.round(ry * c.x));
             console.log("marginTOP:"+Math.round(rx * c.y))*/
            $pimg.css({
                width: Math.round(rx * boundx) + 'px',
                height: Math.round(ry * boundy) + 'px',
                marginLeft: '-' + Math.round(rx * c.x) + 'px',
                marginTop: '-' + Math.round(ry * c.y) + 'px'
            });
            $pimg1.css({
                width: Math.round(mrx * boundx) + 'px',
                height: Math.round(mry * boundy) + 'px',
                marginLeft: '-' + Math.round(mrx * c.x) + 'px',
                marginTop: '-' + Math.round(mry * c.y) + 'px'
            });

        }

    };

    $('.post-avatar').on('click',function () {

        avatar_list = new Array();
        var avatar = new Object(),
            user_avatar = $('.jcrop-holder img').attr('src'),
            user_id = $('.user').attr('id');
        avatar.avatar = user_avatar;
        avatar.id = user_id;
        avatar.width = imgwidth;
        avatar.height = imgheight;
        avatar.left = imgmarginLeft;
        avatar.top = imgmarginTop;
        avatar_list.push(avatar);
        $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
        });
        $.ajax({
            type :'post',
            dataType: 'json',
            url:'/forum/set_avatar/',
            data:{
                'content':JSON.stringify(avatar_list)  ,
            },
            success: function (data) {
                var newcomment = '<li>'+data.content+ '</li>'
            }
        });


    });

});
