$(document).ready(function() {
    $(document).on("click", ".lajkbtn", function() {
        var lajki = $(this).attr('post_id');
        var $btn = $(this);


        $.ajax({
            url : '/like',
            type : 'POST',
            data : { postid : lajki },
        success: function(data) {
            $btn.removeClass('btn btn-success btn-sm lajkbtn').addClass('btn btn-danger btn-sm unlajkbtn');
            $btn.text("Odlub");
            $('.likes' + lajki).text(data.lajkixd);
        }
        });
    });
    $(document).on("click", ".unlajkbtn", function() {
        var lajki = $(this).attr('post_id');
        var $btn = $(this);
        $.ajax({
            url : '/unlike',
            type : 'POST',
            data : { postid : lajki },
            success: function(data) {
                $btn.removeClass('btn btn-danger btn-sm unlajkbtn').addClass('btn btn-success btn-sm lajkbtn');
                $btn.text("Polub");
                $('.likes' + lajki).text(data.lajkixd);
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
});
