
$(document).ready(function() {
	$('input').attr("value","");
});

$(".scroler").click(function() {
    $("#wrapper").fadeOut(500);
    $("#main").fadeOut(500);
    $("#bg").fadeOut(500);
    $("#overlay").fadeOut(500);
});


$("#loginForm").submit(function(event){
    //disable the default form submission
    event.preventDefault();
    if(validate() == true) {
      document.getElementById("loginForm").submit();
    }
});

function validate() {
    var ret=true;
    var msg="";
    var pass = document.getElementById("password");
    if(pass.value == '' ) {
        msg = msg + "Please check the password!<br>";
        $("#password").css({"border-color":"red","box-shadow":"0 0 10px red"});
        ret = false;
    }
    var email = document.getElementById("email");
    if(email.value == '') {
        msg = msg + "Please enter your email ID<br>";
        $("#email").css({"border-color":"red","box-shadow":"0 0 10px red"});
        ret = false;
    }
    else {
        var atpos = email.indexOf("@");
        var dotpos = email.lastIndexOf(".");
        if (atpos< 1 || dotpos<atpos+2 || dotpos+2>=x.length) {
            msg = msg + "Not a valid e-mail address<br>";
            ret = false;
        }
    }
    
    if(ret == false) {
        $("#errModal .modal-body").html(msg);
        $('#errModal').modal('show');
    }
    return ret;
}
$(document).ready(function() {
    $(":input").keypress(function(){
      $(this).css({"border-color":"white","box-shadow":" none"});
    })
});