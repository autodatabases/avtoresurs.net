function showFlashMessage(message) {
    //var template = "{% include 'alert.html' with message='" + message + "' %}";
    var template = "<div class='flash-message-alert'><div class='col-sm-6 div-flash'>" +
        "<div class='alert alert-info alert-dismissible' role='alert'>" +
        "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
        "<span aria-hidden='true'>&times;</span></button>" +  message + "</div></div></div>";
    $(template).insertAfter("#add-form");
    $(".flash-message-alert").fadeIn();
    setTimeout(function () {
        $(".flash-message-alert").fadeOut()
    }, 1800);
    setTimeout(function(){
        $(".flash-message-alert").remove()
    }, 1900);

}