
function signup(event){
    post_data = $('#signup_form').serialize();
    var username =  $('#signup_form #username').val();

    $.ajax({
        type: "POST",
        url: api_url + 'sign_up/',
        data: post_data,

        success: function(data){
            $("#claims_list").html($("#login_popup_form").html());
            $("#claims_list form").attr('id', 'login_form');
            $('#login_form #id_login').val(username);
            $( "<p>You can login with</p>" ).insertBefore( "#claims_list form" );
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


    $("#claim_form").submit(function(event){
        add_claim(event);
    });
    $("#org_form").submit(function(event){
        add_organization(event)
    });

    // $(".claims_of_user").on('click', function() { 
    //     get_claims_for_user();
    // });


    $("#about").on('click', function() { 
        $("#claims_list").html($("#who_is_there").html())
    });


    $("#login_popup").on('click', function() {
        $("#claims_list").html($("#login_popup_form").html());
        $("#claims_list form").attr('id', 'login_form');
    });
    if (login_error) {        
        $("#claims_list").html($("#login_popup_form").html());
        $("#claims_list form").attr('id', 'login_form');
        $( "<p>Login error</p>" ).insertBefore( "#claims_list form" );
    }


    $("#signup_popup").on('click', function() {
        $("#claims_list").html($("#signup_popup_form").html());
        $("#claims_list form").attr('id', 'signup_form');
    });


    $('#close_claims_list').on('click', function() { 
        $("#claims_list").html('')
    });


});