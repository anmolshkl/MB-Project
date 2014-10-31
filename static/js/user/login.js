$(document).ready(function(){
	$(".placeholder-input").on("blur", function() {
  		$(this).toggleClass("not-empty", !!$(this).val());
	});
});
$(document).ready(function() {
	$('input').val('');
});