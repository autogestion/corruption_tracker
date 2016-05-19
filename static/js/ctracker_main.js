
function signup(event){
    $.ajax({
        type: "POST",
        url: api_url + 'sign_up/',
        data: $('#signup_form').serialize(),

        success: function(data){
            console.log(data.username);
            $('#login_form #id_login').val(data.username);
            $( "<p>You can login with</p>" ).insertBefore( "#login_form" );
            $("#registerModal").modal("hide");
            $("#loginModal").modal("show");
            $(".navbar-collapse.in").collapse("hide");
        },
        error: function(data){
            console.log(data.responseText)
            $( "<p>Register error</p>" ).insertBefore( "#claims_list form" );
        }                
    });
    return false;
}



$(document).ready(function () {

    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#back_button").click(function() {
      $("#userclaimsModal").modal("hide");
      $("#claimsModal").modal("show");
      $(".navbar-collapse.in").collapse("hide");
      return false;
    });   


    $("#claim_form").submit(function(event){
        add_claim(event);
    });
    $("#org_form").submit(function(event){
        add_organization(event)
    });


    $("#about-btn").click(function() {
      $("#aboutModal").modal("show");
      $(".navbar-collapse.in").collapse("hide");
      return false;
    });    


    $("#login-btn").click(function() {
      $("#loginModal").modal("show");
      $(".navbar-collapse.in").collapse("hide");
      return false;
    });
    if (login_error) {
        $("#login-error").html(login_error);
        $("#loginModal").modal("show");
        $(".navbar-collapse.in").collapse("hide"); 
    }


    $("#register-btn").click(function() {
      $("#registerModal").modal("show");
      $(".navbar-collapse.in").collapse("hide");
      return false;
    });

});