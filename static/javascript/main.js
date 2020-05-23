(function timeAgo(selector) {

    var templates = {
        prefix: "",
        suffix: " temu",
        seconds: "%d sek.",
        minute: "%d min.",
        minutes: "%d min.",
        hour: "%d godz.",
        hours: "%d godz.",
        day: "dzień",
        days: "%d dni",
        month: "miesiąc",
        months: "%d msc.",
        year: "rok",
        years: "%d lat"
    };
    var template = function (t, n) {
        return templates[t] && templates[t].replace(/%d/i, Math.abs(Math.round(n)));
    };

    var timer = function (time) {
        if (!time) return;
        time = time.replace(/\.\d+/, ""); // remove milliseconds
        time = time.replace(/-/, "/").replace(/-/, "/");
        time = time.replace(/T/, " ").replace(/Z/, " UTC");
        time = time.replace(/([\+\-]\d\d)\:?(\d\d)/, " $1$2"); // -04:00 -> -0400
        time = new Date(time * 1000 || time);

        var now = new Date();
        var seconds = ((now.getTime() - time) * .001) >> 0;
        var minutes = seconds / 60;
        var hours = minutes / 60;
        var days = hours / 24;
        var years = days / 365;

        return templates.prefix + (
        seconds < 45 && template('seconds', seconds) || seconds < 90 && template('minute', 1) || minutes < 45 && template('minutes', minutes) || minutes < 90 && template('hour', 1) || hours < 24 && template('hours', hours) || hours < 42 && template('day', 1) || days < 30 && template('days', days) || days < 45 && template('month', 1) || days < 365 && template('months', days / 30) || years < 1.5 && template('year', 1) || template('years', years)) + templates.suffix;
    };

    var elements = document.getElementsByClassName('timeago');
    for (var i in elements) {
        var $this = elements[i];
        if (typeof $this === 'object') {
            $this.innerHTML = timer($this.getAttribute('title') || $this.getAttribute('datetime'));
        }
    }
    // update time every minute
    setTimeout(timeAgo, 60000);

})();

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function(){
	var maxLength = 150;
	$(".card-text").each(function(){ //rakowy kod
	    var str = $(this).html();
        var re = /(#[a-z0-9][a-z0-9\-_]*)/ig;
        str = str.replace(re, function(x) { return '<a href="/tag/'+x.substring(1, x.length)+'">' + x + '</a> '; });
        var regex = /(https?:\/\/([-\w\.]+)+(:\d+)?(\/([\w\/_\.]*(\?\S+)?)?)?)/ig;
        var replaced_text = str.replace(regex, "<a href='$1' target='_blank'>$1</a>");
        $(this).html(replaced_text);
		var myStr = $(this).text();
		if($.trim(myStr).length > maxLength){
			var newStr = myStr.substring(0, maxLength);
			var removedStr = myStr.substring(maxLength, $.trim(myStr).length);
			$(this).empty().html(newStr);
			$(this).append('<a href="javascript:void(0);" class="read-more"> Zobacz całość</a>');
			$(this).append('<span class="more-text">'+removedStr+'</span>');
			var str = $(this).html();
            str = str.replace(re, function(x) { return '<a href="/tag/'+x.substring(1, x.length)+'">' + x + '</a> '; });
            var replaced_text = str.replace(regex, "<a href='$1' target='_blank'>$1</a>");
            $(this).html(replaced_text);
		}
	});
	$(".read-more").click(function(){
		$(this).siblings(".more-text").contents().unwrap();
		$(this).remove();
	});
	$('.komentarztresc').each(function(){
        var str = $(this).html();
        var regex = /(https?:\/\/([-\w\.]+)+(:\d+)?(\/([\w\/_\.]*(\?\S+)?)?)?)/ig;
        var replaced_text = str.replace(regex, "<a href='$1' target='_blank'>$1</a>");
        $(this).html(replaced_text);
    });
});
