
$(document).ready(function() {
	$('input').attr("value","");
    $('.page2').hide();
});
$(document).ready(function() {
	$('.loader').remove();
});

$(".scroler").click(function() {
    $('.page2').show();
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
$(".scrolerBack").click(function() {
    $("#wrapper").animate(
        {"top": "+=100%"},
        1500);
    $("#main").animate(
        {"top": "+=100%"},
        1500);
    $("#bg").animate(
        {"top": "+=100%"},
        1500);
    $("#overlay").animate(
        {"top": "+=100%"},
        1500);
});
