function update_dropdown (org_type_id){
    console.log(org_type_id)
    var $dropdown = $("#claim_type");
    $dropdown.empty();

    if (claim_types[org_type_id]){
        console.log(claim_types[org_type_id])
    $.each(claim_types[org_type_id], function(key, value) {
      $dropdown.append($("<option></option>")
         .attr("value", value.id).text(value.value));
    });    
    }
}


function get_name_by_id (org_id) {
    for (var i = places.length - 1; i >= 0; i--) {
        if (places[i].data === parseInt(org_id)){
            update_dropdown (places[i].org_type_id)
            return places[i].value;
        }
    }
    return "Name not found"
}


function select_building (org_id) {
    $('#org_id').val(org_id);
    $('#organization_name').val(get_name_by_id(org_id));
}


var AddPage = {
    // 50 too much for testing        
    min_claim_text_len: 10,
    init: function (){
        $('#org_id').on('change', function(){
            AddPage.validate();
        });
        $('#claim_text').on('change', function(){
            AddPage.validate();
        });

		/*
        $('#organization_name').autocomplete({
            lookup: places,
            onSelect: function (suggestion) {
                $('#org_id').val(suggestion.data);
                update_dropdown(suggestion.org_type_id);
                AddPage.validate();
            }
        });
		*/
		
        $("#claim_form").submit(function(event){
            AddPage.show_processing();
            event.preventDefault();
            $.ajax({
                type: "POST",
                url: add_claim_url,
                data: $('#claim_form').serialize(),
                statusCode: {
                    200: function (response) {
                        //
                    },
                    201: function (response) {
                        //
                    },
                    400: function (response) {
                        //
                    },
                    403: function (response) {
                        alert("Too much claims. Please wait an hour and try again.");
                    }
                },
                success: function(data){
                    $('#message').html('Thank you for your message');
                    $('#claim_text').val('');
                    $('#servant').val('');
                    if (grecaptcha_reset){
                        grecaptcha.reset();
                    };
                  
                    AddPage.hide_processing();
                },
                error: function(data){
                    console.log(data.responseText)
                }                
            });
            return false;
        });

    },
    inputs_to_validate: [
        // $('#organization_name'),
        $('#claim_text'),
        $('#org_id'),
    ],
    show_processing: function (){
        $('#processing').show();
    },
    hide_processing: function (){
        $('#processing').hide();
    },
    validate: function (){       
        var org_id = $('#org_id').val();
        if (org_id.length < 0) {
            $('#org_id').addClass('incorrect');
            $('#org_id_error').html("Choose organization to claim");
        } else {
            $('#org_id').removeClass('incorrect');
        }
        AddPage.show_submit();

        // Claim text
        var claim_text = $('#claim_text').val();
        if (claim_text.length < AddPage.min_claim_text_len) {
            $('#claim_text').addClass('incorrect');
            $('#claim_text_error').html(AddPage.min_claim_text_len + " characters is minimum length of claim message");

        } else {
            $('#claim_text').removeClass('incorrect');
        }
        AddPage.show_submit();

    },
    is_valid: function (){
        for (var i = AddPage.inputs_to_validate.length - 1; i >= 0; i--) {
            if (AddPage.inputs_to_validate[i].hasClass('incorrect')) {
                return false;
            }
        };
        return true;
    },
    show_submit: function (){
        if (AddPage.is_valid()) {
            $('#submit_add').prop('disabled', false);
        } else {
            $('#submit_add').prop('disabled', true);
        }
    },
};

$(document).ready(function() {

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

    // Main page logic
    AddPage.init();

});