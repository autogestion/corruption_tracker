function main_map_init (map, options) {
    // Add GeoJSON layer   
    var marker, org_row, orgs_set, org_rows;

    // Add building markers with popups to buildings.
    for (var i = buildings['features'].length - 1; i >= 0; i--) {

        var myIcon = L.divIcon({
            className: 'icon_with_number',
            html: buildings['features'][i]['properties']["polygon_claims"]
        }); 

        marker = L.marker(
            [
                buildings['features'][i]['properties']["centroid"][0],
                buildings['features'][i]['properties']["centroid"][1],
            ],
            {icon: myIcon}
        )

        orgs_set = buildings['features'][i]['properties']["organizations"]
        var polygon = L.polygon(buildings['features'][i]["geometry"]["coordinates"]);
        polygon.setStyle({
            fillColor: 'grey' ,
            weight: 1,
            color: 'white'
        });

        org_rows = []
        for (var ii = orgs_set.length - 1; ii >= 0; ii--) {
            org_row = document.createElement('a');
            org_row.href = '#' + buildings['features'][i]['properties']["ID"];
            org_row.id = orgs_set[ii]['id'];            
            org_row.innerHTML = orgs_set[ii]['name'] + ': &nbsp;&nbsp;' + orgs_set[ii]['claims_count'];

            org_row.onclick = function(event) {
                select_building($(this).attr('id'));               
                var polygon_id = $(this).attr('href').replace('#','');
                var centroid_coordinates;
                for (var i = buildings['features'].length - 1; i >= 0; i--) {
                    if (buildings['features'][i]['properties']["ID"]==polygon_id){                        
                        centroid_coordinates = buildings['features'][i]['properties']["centroid"]
                    }
                }                
                map.setView(centroid_coordinates, buildings['config']['zoom'] + 1);
                event.preventDefault();
                };
            org_rows.push(org_row);
            }; 

            // Here have to be implemented callback for polygon with single org
            // if (orgs_set.length == 1){                
            //     polygon.onclick = function(event) {
            //         console.log('polygon clicked');
            //         select_building(org_row.id);
            //     }   
            // }

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
                    fillColor: 'grey' ,
                    weight: 1,
                    color: 'white'
            });
            };

            this.setStyle({
                fillColor: 'red' ,
                weight: 1,
                color: 'grey'
            });
            $_selectedPolygon = this;
        });
    };
    map.setView(buildings['config']['center'], buildings['config']['zoom']);  
    $_selectedPolygon = null;
}