//  start of w2ui config
var layout = {
        name: 'layout',
        padding: 0,
        panels: [
            { type: 'main', minSize: 400, resizable: true, }
        ]
    };

var grid = { 
        name: 'grid',
        show: {          
            toolbar : true,
            footer : true,
            lineNumbers : true
        },         
        columns: [
            { field: 'complainer', caption: 'complainer', size: '15%', sortable: true, searchable: true },
            { field: 'servant', caption: 'servant', size: '15%', sortable: true, searchable: true },
            { field: 'claim_type', caption: 'claim_type', size: '20%', sortable: true, searchable: true},
            { field: 'text', caption: 'text', size: '35%', searchable: true},
            { field: 'created', caption: 'created', size: '15%', sortable: true},
        ],};

$(function () { 
    $().w2layout(layout);
    $().w2grid(grid);
});
// end of w2ui config

function w2ui_popup() {
    w2popup.open({
        title: 'Claims',
        body: '<div id="main_w2ui" style="position: absolute; left: 0px; top: 0px; right: 0px; bottom: 0px; width: 100%;"></div>',
        width : 1000,
        onOpen  : function (event) {
            event.onComplete = function () {
                $('#w2ui-popup #main_w2ui').w2render('layout');
                w2ui.layout.content('main', w2ui.grid);
            }
        },
    });
}






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
    window.location.hash = "organization=" + org_id; 

        $.ajax({
            type: "GET",
            url: "/get_claims/"  + org_id + "/",
            success: function(data){
                var messages = "";
                var template,
                    message,
                    template_button;

                template = document.getElementById('claim_template_global').innerHTML;
                template_button = document.getElementById('show_all_button_template').innerHTML;
                template_button_grid = document.getElementById('show_all_button_template_grid').innerHTML;
                template_button_add = document.getElementById('show_all_button_template_add').innerHTML.replace('id=""', 'id="open_claim"');
                console.log(template_button_add)

                var records = [];
                var record;
                var count = 0
                for (var i = data.length - 1; i >= 0; i--) {

                    if (count < 4) {
                        message = template.replace('%complainer%', data[i]['complainer']);
                        message = message.replace('%servant%', data[i]['servant']);
                        message = message.replace('%claim_type%', data[i]['claim_type']);
                        message = message.replace('%text%', data[i]['text']);
                        message = message.replace('%created%', data[i]['created']);
                        message = message.replace('%bribe%', data[i]['bribe']);

                        if (data[i]['claim_icon']) {
                            message = message.replace('<div style="float: right"></div>',  '<div style ="float: right"><img src="' + data[i]['claim_icon'] + '" height="50em" width="50em"></div>');
                            console.log (message);
                        }
                        messages += message;
                        count += 1
                    } 
                    record = {recid: i+1, complainer: data[i]['complainer'], servant: data[i]['servant'], claim_type: data[i]['claim_type'],
                                text: data[i]['text'], created: data[i]['created']};
                    records.push(record); 
                }

                w2ui.grid.records = records;

                template_button = template_button.replace('%org_id%', org_id);
                if (messages == "") {
                    messages = 'No claims for this polygon';
                    template_button= '';
                    template_button_grid = ''};            
                $("#target").html(messages + template_button_add + template_button_grid + template_button);

            },
            error: function(data){
                console.log(data.responseText)
            }                
        });
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


    $("#get_claims").click(function() {
        var org_id = $('#org_id').val();
        select_building(org_id);
    });


    $('#organization_name').autocomplete({
        lookup: places,
        onSelect: function (suggestion) {
            $('#org_id').val(suggestion.data);
            update_dropdown(suggestion.org_type_id);
            AddPage.validate();
        }
    });


    $("#claim_form").submit(function(event){
        $('#processing').show();
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
                $('#processing').hide();
                $('#message').html('Thank you for your message');
                window.location.reload();

                // $('#claim_text').val('');
                // $('#servant').val('');
                // if (grecaptcha_reset){
                //     grecaptcha.reset();
                // };
            },
            error: function(data){
                console.log(data.responseText)
            }                
        });
        return false;
    });


    $("#org_form").submit(function(event){
        $('#processing').show();
        event.preventDefault();
        post_data = $('#org_form').serialize() + '&layer_id=' + layer_id;
        console.log(post_data)
        $.ajax({
            type: "POST",
            url: add_org_url,
            data: post_data,

            success: function(data){                 
                $('#processing').hide();           
                window.location.reload();

            },
            error: function(data){
                console.log(data.responseText)
            }                
        });
        return false;
    });

    $( "#open_org" ).click(function() {
      $( "#org_form_block" ).slideToggle( "slow", function() {  
      });
    });

    $( "#open_claim" ).click(function() {
      console.log('claim_form_block togle 0');
      $( "#claim_form_block" ).slideToggle( "slow", function() {  
      });
      console.log('claim_form_block togle');
    });    

    var pair;
    var hash_data = window.location.hash.replace("#", "").split("&");
    for (var i = hash_data.length - 1; i >= 0; i--) {
        pair = hash_data[i].split('=');
        if (pair[0] === 'organization') {
            select_building(pair[1]);
            $('#organization_name').val(get_name_by_id(pair[1]));
            break;
        }
    }
});



