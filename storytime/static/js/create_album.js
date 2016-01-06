$(document).ready(function() {
	var position = 2;
	var previewposition = 2;
	var $container = $('#album-content');
	
	
	  $container.masonry({
		columnWidth: '.image-content',
		itemSelector: '.image-content',
		transitionDuration: 0,
	  });   
	  
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
	

	$("#addimage").click(function(event){
		$("#id_source").click();
		var inputLocalFont = document.getElementById("id_source");
		inputLocalFont.addEventListener("change",previewImages,false);
	});
	
	$(document).on('click','.delete',function(event){
		$item =  $(event.target).parent();
		$parent = $item.parent();
		$parent.remove();
	});
	
//Sending data
	$(document).on('click','#submit',function(event){
	var formData = new FormData($("#story")[0]);
	var fileList = this.files;
	var anyWindow = window.URL || window.webkitURL;
	$(this).val('Please wait ...').attr('disabled','disabled');
	$('body').loadingIndicator();
	$('.loading-indicator-wrapper').show();
	$('.loading-indicator-helper').text("Your story is being uploaded. This may take several minutes.");
	if($('#id_Story-title').val().replace(/^\s+/, "") === ""){
		alert("Please insert the title!");
		$(this).val('Upload').removeAttr("disabled");
		$('.loading-indicator-wrapper').hide();
		return;
	}
		$.ajax({
			   type: "POST",
			   url: "/stories/create_album/store_album/",
			   data: formData, // serializes the form's elements.
			   contentType: false,
			   cache:false,
			   processData:false,
			   success: function(data)
			   {
				   var storyid = data.id
				   $('.image-content').append('<input id="story-id" name="storyid" type="hidden" value="' + data.id + '">');
				   for(var i = 0; i < j; i++){
						var id = "#image" + i;
						var idw = "image" + i;
						var formData = new FormData($(id)[0]);	
						if (i == 0){
							formData.append('source',document.getElementById("banner-image").files[0]);
							$.ajax({
								type: "POST",
								url: "/stories/create_album/store_image/",
								data: formData, // serializes the form's elements.
								contentType: false,
								cache:false,
								processData:false,
								enctype: "multipart/form-data",
								success: function(data){
									k++;
									checksend(storyid);
								}
							});
						}else{
							var id = i - 1;
							if (document.getElementById(idw)) {
								formData.append('source',document.getElementById("id_source").files[id]);
								$.ajax({
									type: "POST",
									url: "/stories/create_album/store_image/",
									data: formData, // serializes the form's elements.
									contentType: false,
									cache:false,
									processData:false,
									enctype: "multipart/form-data",
									success: function(data){
										k++;
										checksend(storyid);
									}
								});
							}else{
								k++;
							}
							
						}
					}

			   }
			 });

		
	});
function checksend(storyid){

	if(k == j){
		$.ajax({
			type: "POST",
			url: "/stories/create_album/album_finish/",
			data: {
				'story-id': storyid,
			},
			success: function(data){
				window.location.replace(data.result); 				
			}
		}); 	
	k = 700;
	}
}
var j = 1;
var k = 0;
var pos = 1;
function previewImages(){	
		
    var fileList = this.files;
    var anyWindow = window.URL || window.webkitURL;

        for(var i = 0; i < fileList.length; i++){
          var objectUrl = anyWindow.createObjectURL(fileList[i]);
          $container.append('<form id = "image' + pos + '" action="/stories/create_stories/" method="post" name = "source" enctype = "multipart/form-data">  <input id="id_position" name="position" type="hidden" value="' + pos + '"> <div  class=" col-lg-2 image-content card" style = " padding:0;"><div class = "col-lg-12" style = "padding:3px;"><div class = "col-lg-12 " style = "margin-bottom:2px; padding-top:0; padding-left:0; padding-right:0;"><img style = "border-top-left-radius: 5px; border-top-right-radius: 5px	;" class="img-responsive" src="' + 	objectUrl + '  " alt="Chania" ></div><input class = "col-lg-12" id="id_caption" maxlength="100" name="caption" type="text"></div><div class = \"delete col-xs-12 col-sm-12 col-md-12 col-lg-12  btn btn-success\">Delete</div></div></form>');
          window.URL.revokeObjectURL(fileList[i]);
		  pos++;
		  j++;
        }
		loadimage();

}	
function loadimage(){
	$container.imagesLoaded( function () {		
				
		$container.masonry( 'reloadItems' );
		$container.masonry( 'layout' );
		
	});
}


});
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#banner').css('background', ' url('+e.target.result +')');
			$('#banner').css('background-repeat', 'no-repeat');
			$('#banner').css('background-size', 'cover');
			$('#banner').css('background-attachment', 'fixed');
				
            }
            reader.readAsDataURL(input.files[0]);
		
        }
    }