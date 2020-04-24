$(document).ready(function() {
    $(document).on("click", ".lajkbtn", function() {
        var post_id = $(this).attr('post_id');
        var $btn = $(this);
        $.ajax({
            url : '/like',
            type : 'POST',
            data : { postid : post_id },
        success: function(data) {
            $btn.removeClass('btn btn-success btn-sm lajkbtn').addClass('btn btn-danger btn-sm unlajkbtn');
            $btn.text("Odlub");
            $('.likes' + post_id).text(data.likes);
        }
        });
    });
    $(document).on("click", ".unlajkbtn", function() {
        var post_id = $(this).attr('post_id');
        var $btn = $(this);
        $.ajax({
            url : '/unlike',
            type : 'POST',
            data : { postid : post_id },
            success: function(data) {
                $btn.removeClass('btn btn-danger btn-sm unlajkbtn').addClass('btn btn-success btn-sm lajkbtn');
                $btn.text("Polub");
                $('.likes' + post_id).text(data.likes);
            }
        });
    });
    $(document).on("click", ".usunwpis", function() {
        var post_id = $(this).attr('post_id');
        $.ajax({
            type: "POST",
            url: "/remove",
            data: { post_id : post_id },
            success: function() {
                $("#wpis"+post_id).remove();
            },
            error: function() {
                alert("Wystąpił błąd");
            }
        });
    });
    $(document).on("click", ".usunkomentarz", function() {
        var kom_id = $(this).attr('kom_id');
        $.ajax({
            type: "POST",
            url: "/removekom",
            data: { kom_id : kom_id },
            success: function() {
                $(".komentarz"+kom_id).remove();
            },
            error: function() {
                alert("Wystąpił błąd");
            }
        });
    });
    $(document).on("click", ".dodajkomentarz", function() {
        var post_id = $(this).attr('post_id');
        var inputvalue = $("#komentarz"+post_id).val();

        $.ajax({
            type: "POST",
            url: "/dodajkomentarz",
            data: { post_id : post_id, inputvalue : inputvalue },
            success: function(data) {
                $("#komentarz"+post_id).val("");
                   var span = $('<span />',{
                        class:'usunkomentarz' ,
                        kom_id: data.komid,
                        html:'&times;'
                    });
                if($(".autorwpisu"+post_id).text() === data.autor) {
                    var div = $('<div />',{
                        class:'komentarz'+data.komid ,
                        html:'<b>'+data.autor+'</b>: '+data.tresc
                    });
                    $(".komentarze"+post_id).prepend(div);
                    span.appendTo('.komentarz'+data.komid);
                }
                else {
                    $(".komentarze"+post_id).prepend($('<div>', {class: 'komentarz'+data.komid, text: data.autor+": "+data.tresc}));
                    span.appendTo('.komentarz'+data.komid);
                }
            },
            error: function() {
                alert("Wystąpił błąd, minimalna długość komentarza to 2 znaki, a maksymalna 50 znaków");
            }
        });
    });
});
