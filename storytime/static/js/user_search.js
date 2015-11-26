$(document).ready(function() {
	$(document).on('click',' #search',function(){
		$string = "/profile?u=" + $( "#search_input_form" ).val();
		window.location.replace($string)
	});
	
});