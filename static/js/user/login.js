$(document).ready(function(){
	$(".placeholder-input").on("blur", function() {
  		$(this).toggleClass("not-empty", !!$(this).val());
	});
});
$(document).ready(function() {
	$('input').attr("value","");
});
$(document).ready(function() {
	$('.loader').remove();
});

$("#scroler").click(function() {
    $("#main").animate(
        {"top": "-=100%"},
        1500);
    $("#bg").animate(
        {"top": "-=100%"},
        1500);
    $("#overlay").animate(
        {"top": "-=100%"},
        1500);
    $('.loader').remove();
});