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

			//Default Setting				
	$(".fancybox-thumb").fancybox({
		prevEffect	: 'none',
		nextEffect	: 'none',
		padding : 0,
		afterLoad   : addLinks,
		beforeClose : removeLinks,
		loop		: false,
		helpers : { overlay : { locked : false } },
		beforeShow: function () {
			$("#body").addClass("blur");
			$(".fancybox-skin").css("backgroundColor","transparent");
			$(".fancybox-skin").css("-moz-box-shadow","0 0 0");
			$(".fancybox-skin").css("-webkit-box-shadow","0 0 0");
			$(".fancybox-skin").css("box-shadow","0 0 0");
		},
		afterClose: function () {
			$("#body").removeClass("blur");			
		}
	});



//Autoplay
	$(document).on('click','.button #autoplay',function(event){
		$(".fancybox-thumb").fancybox({
			prevEffect	: 'none',
			nextEffect	: 'none',
			autoPlay: true,
			playSpeed: 5000,
			afterLoad   : addLinks,
			beforeClose : removeLinks,
			loop		: false,
			locked     : false,
			helpers : { overlay : { locked : false } },
			afterShow: function(){          
				if(this.index  == this.group.length - 1){
					setTimeout(closefancybox, 4000);
				}
			},
			beforeShow: function () {
				$("#body").addClass("blur");
				$(".fancybox-skin").css("backgroundColor","transparent");
				$(".fancybox-skin").css("-moz-box-shadow","0 0 0");
				$(".fancybox-skin").css("-webkit-box-shadow","0 0 0");
				$(".fancybox-skin").css("box-shadow","0 0 0");
			},
			afterClose: function () {
				$("#body").removeClass("blur");
			}
		});
		

		var $a = $('.item').find("a")[0].click();	
	});
	function closefancybox(){
		$.fancybox.close();
	}
	
	function addLinks() {
		var list = $("#linkimage");
		
		if (!list.length) {    
			list = $('<ul id="linkimage" class = \"col-md-11 col-lg-10 col-lg-push-1 col-sm-11 col-xs-12\">');
		
			for (var i = 0; i < this.group.length; i++) {
				$('<li data-index="' + i + '"><label></label></li>').click(function() { $.fancybox.jumpto( $(this).data('index'));}).appendTo( list );
			}
			
			list.appendTo( '.fancybox-prev' );
		}

		list.find('li').removeClass('active').eq( this.index ).addClass('active');
	}

	function removeLinks() {
		$("#linkimage").remove();    
	}
	$(document).on('click','.button #star',function(){
        $.ajax({
            type:"POST",
            url:"/stories/add_star/",
            data: {
                    'storyid': $( "#star" ).val()
                  },
            success: function(result){
				$( "#starcount" ).replaceWith(result.string);
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
	$(document).on('click','#oldercomment',function(){
		$data = $( ".comment-item" ).first().attr( "data-id" );
	
        $.ajax({
            type:"POST",
            url:"/load_comment/",
            data: {
					'max-id': $data,
					'id': $( "#oldercomment" ).attr( "value" ),
                  },
            success: function(result){
				$( "#comment" ).prepend(result.string);
            }
		});
	});
	
	$(document).on('click','#delete-submit',function(){
		$id = $( "#delete-submit" ).attr("data-id");
		 $(this).val('Please wait ...')
		.attr('disabled','disabled');
        $.ajax({
            type:"POST",
            url:"/delete_story/",
            data: {
					'id': $id,
                  },
            success: function(result){
				$( "#server-feedback" ).replaceWith(result.string);
				$("#delete-submit").removeAttr('disabled');
            }
		});
	});
	
});