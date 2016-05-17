$(function(){

    $(document).on('click','.cont-img',function(){
        var _this = this;
        $(_this).next('ol').show();
        $(_this).hide();
    });
    $(document).on('click','ol',function(){
        var _this = this;
        $(_this).prev('.cont-img').show();
        $(_this).hide();
    });
    $(document).on('click','.reply-button',function(){
        var _this=this,
            _id=$(_this).attr('id');
        console.log(this);
        if($('.involved-reply-hot-'+_id)&& $('.favorite-info-'+_id) && $('.recommend-foot-fa-'+_id)){
            $('.favorite-info-'+_id).hide();
            $('.recommend-foot-fa-'+_id).hide();
            $('.involved-reply-hot-'+_id).hide();
        }

        $('.decorator-foot-'+_id).fadeToggle();
        $('.reply-'+_id).toggle();
        $('.involved-reply-hot-'+_id).slideToggle();


    });




    $(document).on('click','.triger',function(){

        $('.reply').removeClass("hidden")
    });
    $(document).on('click','.n1',function(){
        $('#myModal').modal('show')
    });

    var _that1;
    $(document).on("mouseenter","[data-toggle='popover']", function () {
        var _this = this,

            _id = $(this).attr('id');
        _that1 =_this
        $(_this).popover({
            html: true,
            animation:true,
            placement:"auto bottom",
            trigger:'manual',

            content:'<div class="popo-content">' +'<div class="user-info-num">'+'</div>' +
            '<div class="user-info-img">'+'<span>' +
            '</span>'+'</div>'+
            '</div>',});
        t=setTimeout(function () {

            $(_this).popover("show");
            $(_this).on("shown.bs.popover",function(){
                var result;
                console.log($(_this).attr('class'));
                if ($(_this).attr('class')=='user-box'){
                    $('.arrow').css('left','75%');
                    $('.popover').css({'position':'relative','left':'-250px','top':'-10px','width':'450px'});

                }
                else if ($(_this).attr('class')=='author-info'){
                    $('.arrow').css('left','18%');
                    $('.popover').css({'position':'absolute','left':'-50px'});

                }

                $.ajax({
                    type:'get',
                    url:"/forum/get_user/",
                    data:{
                        'id':_id
                    },
                    // async:false,
                    success : function(data){

                        $(".popover-content .user-info-num").append(
                            '<img style="height:30px;width:30px;" src='+data.avatar+ '>'+'<span>'+'关注'+data.following_num+'</span>'+'<span>'
                            + '文章' +data.article_num+'</span>'+'<span>'+'喜欢'+data.favorite_num+'</span>');
                        if(data.img){
                            for(var i =0; i < data.img.length;i++){
                                $(".popover-content .user-info-img").append('<div style="float:left">'+'<img '+'src='+data.img[i]+ '>'+'<div>')}
                        }
                    },
                });

            }())},700);



    });
     $(document).on("mouseleave", "[data-toggle='popover']",function () {
        clearTimeout(t);

        s=setTimeout(function () {

            if (!$(".popover:hover").length) {
                $("[data-toggle='popover']").popover("hide");

            }}, 100);});
    $(document).on("mouseleave",'.popover', function () {
        console.log($(this))
        setTimeout(function () {
            $("[data-toggle='popover']").popover('hide');},100);
    });
    $('.put').click(function() {

        var _node = $(this);
        var _href = _node.attr('href');
        var _text = _node.attr('id');
        var content = $("input#"+ _text).val();
        var params = '[{"id":"tastId-6653535157","caption":"sdf","ow":440,"oh":587,"raw":"http://imglf2.nosdn.127.net/img/b0FJTHI3SFptWkFnNXdUZ0RVSkNvR3pTa3NQeVVMd3hnelNkTS9hS1QyM0dzTGxMV2JNMmd3PT0.jpg","rw":440,"rh":587,"rotate":0},{"id":"tastId-2372800545","caption":"人格的风格","ow":440,"oh":587,"raw":"http://nos.netease.com/imglf/img/b0FJTHI3SFptWkFnNXdUZ0RVSkNvRWM4L2pJNFlEcWt4UjJKendhMGN6UEN3RDFuKzVxTlFBPT0.jpg","rw":440,"rh":587,"rotate":0},{"id":"tastId-4057654699","caption":"电饭锅电饭锅","ow":440,"oh":587,"raw":"http://nos.netease.com/imglf2/img/b0FJTHI3SFptWkFnNXdUZ0RVSkNvQi9lam1sSWRmQkpsQ2tTT0h1a05Rc3VwcnlUTzZ3NThRPT0.jpg","rw":440,"rh":587,"rotate":0},{"id":"tastId-1107313217","caption":"电饭锅电饭锅","ow":440,"oh":587,"raw":"http://nos.netease.com/imglf0/img/b0FJTHI3SFptWkFnNXdUZ0RVSkNvSlFzdTlxVXNvL3hSZks1UzRTVkdRU3AxT2xCM2pSOG5RPT0.jpg","rw":440,"rh":587,"rotate":0},{"id":"tastId-6515050620","caption":"徐VC","ow":440,"oh":587,"raw":"http://nos.netease.com/imglf2/img/b0FJTHI3SFptWkFnNXdUZ0RVSkNvTXlncmc0R3NDeTlxNlNEckxXVTQ4dWljcldMSUpsQWRBPT0.jpg","rw":440,"rh":587,"rotate":0}]';

        $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
        });
        $.ajax({
            type: 'post',
            dataType: 'json',
            url: _href,

            data: {
                'content': content,
                a: 'asffas',
                photo:params,
            },

            success: function (data) {

                $('input#'+ _text).val("");
                var newcomment = '<li>'+data.content+ '</li>'
                $('div.con'+ _text).append( newcomment);
                alert(data.content)
            }
        });

        return false;
    });

});