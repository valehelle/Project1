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
	var $numtracker = 1;
	$(document).on('click',' #readmore',function(){
		$data = $( ".story-item" ).last().attr( "data-id" );
			$.ajax({
				type:"POST",
				url:"/discovery/previous/",
				data: {
						'max-id': $data
					  },
				success: function(result){
					var div = document.createElement("div");
					var idname = "new" + $numtracker;
					div.id = idname;
					idname = "#" + idname;
					$container.append(div);
					$(idname).css('visibility','hidden');	
					$(idname).append(result.string);							
					$container.imagesLoaded( function () {			
						$container.masonry( 'reloadItems' );
						$container.masonry( 'layout' );
						$container.append(div);
						$(idname).css('visibility','visible');
						$numtracker++;
					});
				}
			});
		
	});
	
	var $container = $('#feedcontent');
	$container.imagesLoaded( function () {
	  $container.masonry({
		columnWidth: '.story-item',
		itemSelector: '.story-item',
		transitionDuration: 0,
	  });   
	  
	});

});