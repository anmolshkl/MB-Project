$(".placeholder-input").on("blur", function() {
  $(this).toggleClass("not-empty", !!$(this).val());
});