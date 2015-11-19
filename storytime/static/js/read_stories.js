$(document).ready(function() {

	// using jQuery
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	
	function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});


	$(".item").click(function(event){
		var $div = $(this).next();
		var $a = $($div).find("a");
		$a.trigger('click');
	});
				
	$(document).ready(function() {
		$(".fancybox-thumb").fancybox({
			prevEffect	: 'none',
			nextEffect	: 'none',
			helpers	: {
				title	: {
					type: 'outside'
				},
				thumbs	: {
					width	: 500,						
					height	: 500
				}
			}
		});
	});

	$(document).on('click','.button #star',function(){
        $.ajax({
            type:"POST",
            url:"/stories/add_star",
            data: {
                    'storyid': $( "#star" ).val()
                  },
            success: function(result){
				$( "#star" ).replaceWith(result.string);
            }
		});
	});

	$(document).on('click','.button #id_submit',function(){
	    $.ajax({
			type: "POST",
			data: $('#comment_form form').serialize(),
			url: "/comments/post/",
			cache: false,
			success: function(result) {
				$( "#comment" ).append(result.string);
				$( "#id_comment" ).val("");
			 }
		});
		return false;
	});
	number = 2;
	$(document).on('click','.button #oldercomment',function(){
        $.ajax({
            type:"POST",
            url:"/load_comment/",
            data: {
                    'number': number,
					'id': $( "#oldercomment" ).val(),
                  },
            success: function(result){
				$( "#comment" ).prepend(result.string);
				number++;

            }
		});
	});
});