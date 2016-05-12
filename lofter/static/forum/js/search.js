$(function(){
    $('#search').keyup(function(event){
        var query,
            _this=$(this);
        query = $(_this).val();

        t=setTimeout(function () {
            query = $(_this).val();},2000);
        if (query){
            $.get('/forum/search/', {search: query}, function(data){
                $('.dropdown-menu1').html(data);
                var cat=$('.reminder').find(".search-items");
                cat.each(function(){
                    var text = $(this).text().replace(query,"<strong>"+query+"</strong>");
                    $(this).html(text);
                });

            });
        }
        else{
            $.get('/forum/subscript/', function(data){
                $('.dropdown-menu1').html(data);

            });
        }

    });
    $('.form-group').click(function(){

        var _this=this;
        $('.dropdown-menu1').slideDown();

    });
    $(document).click(function(e){   e = window.event||e;
        obj = e.srcElement ? e.srcElement : e.target;
        var id = obj.id;
        if(id != 'search'){ // 如果不是点击输入框
            $('.dropdown-menu1').slideUp(); // $comboContent是下拉框部分
            return;
        }
    });
    $(document).on('click','.edit',function(){
        var id = $(this).attr('id');
        $.get("/forum/get_div/",{'id':id},function(data){
            $('body').css('overflow','hidden');

            $('body').append(data);

        });
    });

    $(document).on('click','.remove',function(){
        $('.ceshi').remove();
        $('body').css("overflow",'auto')
    });
    $(document).on("mouseover",".img-small img",function(){
               $(this).next(".img-operator").show();

    });
        $(document).on("mouseleave",".img-small",function(){
        $(".img-operator").hide();
    });


});