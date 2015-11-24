$(document).ready(function() {
	var position = 1;
	$("#addimage").click(function(event){
		var string = "onchange = \"$('#preview" + position + "')[0].src = window.URL.createObjectURL(this.files[0])\"";
		$("<div class = \"col-xs-12 col-sm-12  col-md-4 col-lg-4 item\" style = \"overflow: hidden;\"><label for=\"id_source\">Image:</label><input id=\"id_source\" name=\"source\" type=\"file\" " + string +  " ><br><img id=\"preview" + position + "\" style=\"max-height:300px;\"  class = \"img-responsive\"/> <input id=\"id_position\" name=\"position\" type=\"hidden\" value = " + position + "></div>").insertBefore("#choice");
		if(position%3 == 0)
			$("<div class = \"col-xs-12 col-sm-12 col-md-12 col-lg-12\"><br></div>").insertBefore("#choice");
		position++;
	});
	
	$("#addtext").click(function(event){
		$( "<div class = \"col-xs-12 col-sm-12 col-md-4 col-lg-4 item\" > <label for=\"id_text\">Text:</label><br><br><br><textarea class=\"form-control\" rows=\"9\" id=\"id_text\" maxlength=\"200\" name=\"text\" type=\"text\"></textarea><input id=\"id_text_position\" name=\"text_position\" type=\"hidden\" value = " + position +"> </div>" ).insertBefore("#choice");
		if(position%3 == 0)
			$("<div class = \"col-xs-12 col-sm-12 col-md-12 col-lg-12\"><br></div>").insertBefore("#choice");
		position++;
	});
});