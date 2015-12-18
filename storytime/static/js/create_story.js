$(document).ready(function() {
	var position = 1;
	var previewposition = 1;
	$("#addimage").click(function(event){
		var string = "";
		var id = "id_source" + previewposition;
		$("<div class = \"col-xs-12 col-sm-12  col-md-12 col-lg-12 card\" style = \"overflow: hidden;\"><label for=\"id_source\">Image:</label><input id=\"" + id + "\" name=\"source\" type=\"file\" " + string +  " multiple><br><div id=\"preview" + previewposition + "\"></div> <div class = \"delete col-xs-12 col-sm-12 col-md-12 col-lg-12  btn btn-success\">Delete</div></div>").insertBefore("#choice");
		previewposition++;
		var inputLocalFont = document.getElementById(id);
		inputLocalFont.addEventListener("change",previewImages,false);
	});
	
	$("#addtext").click(function(event){
		$( "<div class = \"col-xs-12 col-sm-12 col-md-12 col-lg-12 card\" > <label for=\"id_text\">Text:</label><br><br><br><textarea class=\"form-control\" rows=\"4\" id=\"id_text\" maxlength=\"200\" name=\"text\" type=\"text\"></textarea><input id=\"id_text_position\" name=\"text_position\" type=\"hidden\" value = " + position +"> <div class = \"delete col-xs-12 col-sm-12 col-md-12 col-lg-12  btn btn-success\">Delete</div></div>" ).insertBefore("#choice");
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

function previewImages(){
    var fileList = this.files;
    var curpos = previewposition - 1;
	var curclass = '#preview' + curpos;
    var anyWindow = window.URL || window.webkitURL;

        for(var i = 0; i < fileList.length; i++){
          var objectUrl = anyWindow.createObjectURL(fileList[i]);
          $(curclass).append('<img style = "margin-bottom:10px; max-height:400px;" class = "img-responsive" src="' + objectUrl + '" />' + "<input id=\"id_position\" name=\"position\" type=\"hidden\" value = " + position + "> ");
          window.URL.revokeObjectURL(fileList[i]);
		  position++;
        }
    
    
}	

});