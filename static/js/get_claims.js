function get_name_by_id (org_id) {
        for (var i = places.length - 1; i >= 0; i--) {
            if (places[i].data === parseInt(org_id)){
                return places[i].value;
            }
        }
        return '{% trans "Name not found" %}'
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

    function select_building (org_id) {
        window.location.hash = "organization=" + org_id;  

        $.get("/get_claims/"  + org_id + "/", function(data) {
            var messages = "";
            var template,
                message,
                template_button;

            template = document.getElementById('claim_template_global').innerHTML;
            template_button = document.getElementById('show_all_button_template').innerHTML;

            for (var i = data.length - 1; i >= 0; i--) {
                message = template.replace('%complainer%', data[i]['complainer']);
                message = message.replace('%servant%', data[i]['servant']);
                message = message.replace('%claim_type%', data[i]['claim_type']);
                message = message.replace('%text%', data[i]['text']);
                messages += message;
            }
            template_button = template_button.replace('%org_id%', org_id);
            if (messages == "") {
                messages = 'No claims for this polygon';
                template_button=''};            
            $("#target").html(messages + template_button);

            for (var i = places.length - 1; i >= 0; i--) {
                if (places[i].data === org_id){
                    $('#org_id').val(places[i].value);
                    return;
                }
            };
        });
    }

