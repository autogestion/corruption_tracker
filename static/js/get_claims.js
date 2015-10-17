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


function get_name_by_id (org_id) {
        for (var i = places.length - 1; i >= 0; i--) {
            if (places[i].data === parseInt(org_id)){
                return places[i].value;
            }
        }
        return 'Name not found'
    }


function select_building (org_id) {
    window.location.hash = "organization=" + org_id;  

    $.get("/get_claims/"  + org_id + "/", function(data) {
        var messages = "";
        var template,
            message,
            template_button;

        template = document.getElementById('claim_template_global').innerHTML;
        template_button = document.getElementById('show_all_button_template').innerHTML;
        template_button_grid = document.getElementById('show_all_button_template_grid').innerHTML;

        var records = [];
        var record;

        for (var i = data.length - 1; i >= 0; i--) {
            message = template.replace('%complainer%', data[i]['complainer']);
            message = message.replace('%servant%', data[i]['servant']);
            message = message.replace('%claim_type%', data[i]['claim_type']);
            message = message.replace('%text%', data[i]['text']);
            message = message.replace('%created%', data[i]['created']);
            messages += message;

            record = {recid: i+1, complainer: data[i]['complainer'], servant: data[i]['servant'], claim_type: data[i]['claim_type'],
                        text: data[i]['text'], created: data[i]['created']};
            records.push(record); 
        }

        w2ui.grid.records = records;

        template_button = template_button.replace('%org_id%', org_id);
        if (messages == "") {
            messages = 'No claims for this polygon';
            template_button=''};            
        $("#target").html(messages + template_button_grid + template_button);

        for (var i = places.length - 1; i >= 0; i--) {
            if (places[i].data === org_id){
                $('#org_id').val(places[i].value);
                return;
            }
        };
    });
}


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


$(document).ready(function () {
    $("#get_claims").click(function() {
        var org_id = $('#org_id').val();
        select_building(org_id);
    });

    $('#org_id').autocomplete({
        lookup: places,
        onSelect: function (suggestion) {
            select_building(suggestion.data);
        }
    });

    var pair;
    var hash_data = window.location.hash.replace("#", "").split("&");
    for (var i = hash_data.length - 1; i >= 0; i--) {
        pair = hash_data[i].split('=');
        if (pair[0] === 'organization') {
            select_building(pair[1]);
            $('#org_id').val(get_name_by_id(pair[1]));
            break;
        }
    }

});


