$(document).ready(function() {
	var position = 2;
	var previewposition = 2;
	$("#addimage").click(function(event){
		var string = "";
		var id = "id_source" + previewposition;
		$("<div class = \"col-xs-12 col-sm-12  col-md-12 col-lg-12 \" style = \"margin-top:35px; text-overflow: ellipsis;\"><div class = \"card col-xs-12 col-md-8 col-md-push-2 col-lg-6 col-lg-push-3\"><label for=\"id_source\">Image:</label><input style = \"overflow: hidden;\" id=\"" + id + "\" name=\"source\" type=\"file\" " + string +  " multiple><br><div id=\"preview" + previewposition + "\"></div> <div class = \"delete col-xs-12 col-sm-12 col-md-12 col-lg-12  btn btn-success\">Delete</div></div></div>").insertBefore("#choice");
		previewposition++;
		var inputLocalFont = document.getElementById(id);
		inputLocalFont.addEventListener("change",previewImages,false);
	});
	
	$("#addtext").click(function(event){
		$( "<div class = \"col-xs-12 col-sm-12  col-md-12 col-lg-12 \" style = \"padding-top:25px; overflow:hidden; \" ><div class = \"col-xs-12 col-md-8 col-md-push-2 col-lg-6 col-lg-push-3 card\"><textarea class = \"col-lg-12\" rows=\"4\" id=\"id_text\" maxlength=\"200\" name=\"text\" type=\"text\" placeholder = \"Insert text here\" style = \"border-color:transparent;\"></textarea><input id=\"id_text_position\" name=\"text_position\" type=\"hidden\" value = " + position +"> <div class = \"delete col-xs-12 col-sm-12 col-md-12 col-lg-12  btn btn-success\">Delete</div></div></div>" ).insertBefore("#choice");
		position++;
	});
	$(document).on('click','.delete',function(event){
		$item =  $(event.target).parent();
		$item.remove();
	});

	$(document).on('click','#submit',function(event){
		$('body').loadingIndicator();
		$('.loading-indicator-helper').text("Your story is being uploaded. This may take several minutes.");
	});
var j = 1;
function previewImages(){
    var fileList = this.files;
    var curpos = previewposition - 1;
	var curclass = '#preview' + curpos;
    var anyWindow = window.URL || window.webkitURL;
	
        for(var i = 0; i < fileList.length; i++){
		  var reader = new FileReader();
          reader.onload = function (e) {
		  $(curclass).append('<div class = "background-image" id =' + 'background' + curpos + j + ' style = "margin-bottom:10px; min-height:400px;">' + "<input id=\"id_position\" name=\"position\" type=\"hidden\" value = " + position + "> </div>");

          var back =  'background' + curpos + j;
		 
		  var idback = '#'+back;
		  $(idback).css('background', ' url('+e.target.result +')');
		  $(idback).css('background-repeat', 'no-repeat');
	      $(idback).css('background-size', 'contain');
		   j++;
		   position++;
		  }
		  reader.readAsDataURL(fileList[i]);
 
		  
        }
    
    
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