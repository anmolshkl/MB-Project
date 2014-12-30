
$(document).ready(function() {
	$('input').attr("value","");
});

$(".scroler").click(function() {
    $("#wrapper").animate(
        {"top": "-=100%"},
        1500);
    $("#main").animate(
        {"top": "-=100%"},
        1500);
    $("#bg").animate(
        {"top": "-=100%"},
        1500);
    $("#overlay").animate(
        {"top": "-=100%"},
        1500);
});