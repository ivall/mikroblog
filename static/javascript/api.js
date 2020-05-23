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
    $(document).on("click", ".lajktag", function() {
        var tag = $(this).attr('tag');
        var $btn = $(this);
        $.ajax({
            url : '/obserwuj',
            type : 'POST',
            data : { tag : tag },
        success: function(data) {
            $btn.removeClass('btn btn-success btn-sm lajktag').addClass('btn btn-danger btn-sm unlajktag');
            $btn.text("Przestań obserwować");
        }
        });
    });
    $(document).on("click", ".unlajktag", function() {
        var tag = $(this).attr('tag');
        var $btn = $(this);
        $.ajax({
            url : '/przestan_obserwowac',
            type : 'POST',
            data : { tag : tag },
            success: function(data) {
                $btn.removeClass('btn btn-danger btn-sm unlajktag').addClass('btn btn-success btn-sm lajktag');
                $btn.text("Obserwuj");
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
            url: "/dodaj_komentarz",
            data: { post_id : post_id, inputvalue : inputvalue },
            success: function(data) {
                $("#komentarz"+post_id).val("");
                tresc = data.tresc.replace(/(<([^>]+)>)/ig,"");
                   var span = $('<span />',{
                        class:'usunkomentarz' ,
                        kom_id: data.komid,
                        html:'&times;'
                    });
                   var time = $('<time />', {
                       class:'timeago',
                       html:'chwilę temu'
                   });
                   var datakomentarza = $('<div />', {
                        class:'datakomentarza',
                        html:time
                    });
                if ($.trim($(".autorwpisu"+post_id).text()) === $.trim(data.autor)) {
                    var div = $('<div />', {
                        class:'komentarz'+data.komid,
                        html:'<a href="/profil/'+data.autor+'" style="color: white;"><b>'+data.autor+'</b></a>: '+tresc
                    });
                    $(".komentarze"+post_id).prepend(div);
                    datakomentarza.appendTo('.komentarz'+data.komid);
                    span.appendTo('.komentarz'+data.komid);
                }
                else {
                    var not_author = $('<div />', {
                        class:'komentarz'+data.komid,
                        html:'<a href="/profil/'+data.autor+'" style="color: white;">'+data.autor+'</a>: '+tresc
                    });
                    $(".komentarze"+post_id).prepend(not_author);
                    datakomentarza.appendTo('.komentarz'+data.komid);
                    span.appendTo('.komentarz'+data.komid);
                }
            },
            error: function() {
                alert("Wystąpił błąd, minimalna długość komentarza to 2 znaki, a maksymalna 75 znaków");
            }
        });
    });
    $(document).on("click", ".number-of-likes", function() {
        var post_id = $(this).attr('post-id');
        $("#likesModal").modal("show");
        $.ajax({
            url : '/likes',
            type : 'POST',
            data : { post_id : post_id },
            success: function(data) {
                $('.likes-modal-body').text(data.likes);
            }
        });
    });
});
