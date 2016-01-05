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


	$(document).on('click','.button #notificationbutton',function(){
        $.ajax({
            type:"POST",
            url:"/profile/update_seen/",
            data: {
                    'username': 1
                  },
            success: function(result){
				$( "#count" ).replaceWith("<span id = \"count\">0</span>");

            }
		});
	});

	$(document).on('click','#feedback-submit',function(){
		$feedback = $("#text-feedback").val();
		 $(this).val('Please wait ...')
		.attr('disabled','disabled');
        $.ajax({
				type:"POST",
				url:"/feedback/",
				data: {
						'feedback': $feedback
					  },
				success: function(result){
					$( "#server-feedback" ).replaceWith(result.string);
					$("#feedback-submit").removeAttr('disabled');
				}
			});
	});
	
	$(document).on('click',' #search',function(){
		$string = "/profile?u=" + $( "#search_input" ).val();
		window.location.replace($string)
	});
	

	
});
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65260175-2', 'auto');
  ga('send', 'pageview');