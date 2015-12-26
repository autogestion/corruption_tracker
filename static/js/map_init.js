function main_map_init (map, options) {
    $("#main > div.leaflet-control-container > div.leaflet-top.leaflet-right").addClass('layout_chooser');
    $('.layout_chooser').removeClass("leaflet-right");
    $('.layout_chooser').addClass("leaflet-left");

    // $('.layout_chooser').removeClass("leaflet-top");
    // $('.layout_chooser').addClass("leaflet-bottom");
    // Add GeoJSON layer
    var marker, org_row, orgs_set, org_rows;
    console.log(polygons)

    // Add building markers with popups to polygons.
    for (var i = polygons['features'].length - 1; i >= 0; i--) {

        var myIcon = L.divIcon({
            className: 'icon_with_number',
            html: polygons['features'][i]['properties']["polygon_claims"]
        }); 

        marker = L.marker(
            [
                polygons['features'][i]['properties']["centroid"][0],
                polygons['features'][i]['properties']["centroid"][1],
            ],
            {icon: myIcon}
        )

        orgs_set = polygons['features'][i]['properties']["organizations"]

        var polygon = L.polygon(polygons['features'][i]["geometry"]["coordinates"]);
        polygon.centroid = polygons['features'][i]['properties']["centroid"]

        if (orgs_set.length==1){       
            polygon.organization = orgs_set[0]['id']
        }

        polygon.setStyle({
            fillColor: polygons['features'][i]['properties']['color'],
            weight: 2,
            color: 'blue',
            opacity: 0.3,
            fillOpacity: 0.3
        });

        org_rows = []
        for (var ii = orgs_set.length - 1; ii >= 0; ii--) {
            org_row = document.createElement('a');
            org_row.href = '#' + polygons['features'][i]['properties']["ID"];
            org_row.id = orgs_set[ii]['id'];            
            org_row.innerHTML = orgs_set[ii]['name'] + ': &nbsp;&nbsp;' + orgs_set[ii]['claims_count'];

            org_row.onclick = function(event) {
                select_building($(this).attr('id'));
                event.preventDefault();
            };
            org_rows.push(org_row);
        };

        org_list = document.createElement("ul");
        $.each(org_rows, function(i){
            var li = $('<li/>')
                .addClass('ui-menu-item')
                .attr('role', 'menuitem')
                .appendTo(org_list);        
            li.html(org_rows[i]);  
        });
        marker.addTo(map);
        polygon.addTo(map).bindPopup(org_list);



        polygon.on('click',function()  {
            if ($_selectedPolygon) {
                $_selectedPolygon.setStyle({
                    weight: 2,
                    color: 'blue',
                    opacity: 0.3,
                    fillOpacity: 0.3
            });
            };
            map.setView(this.centroid, polygons['config']['zoom'] + 1);
            this.setStyle({
                weight: 6,
                color: 'green',
                opacity: 1,
                fillOpacity: 0.8
            });
            $_selectedPolygon = this;
            if (this.organization) {
                select_building(this.organization);
            }
            else {
                $('#target').empty();            
            };
        });  
    };
    map.setView(polygons['config']['center'], polygons['config']['zoom']);  
    $_selectedPolygon = null;
}