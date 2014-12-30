
$(document).ready(function() {
	$('input').attr("value","");
});

$(".scroler").click(function() {
    $("#wrapper").fadeOut(500);
    $("#main").fadeOut(500);
    $("#bg").fadeOut(500);
    $("#overlay").fadeOut(500);
});