function main_map_init (map, options) {
    // Add GeoJSON layer   
    var marker, org_id, org_row, orgs_set, org_rows;

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
        org_rows = []
        for (var ii = orgs_set.length - 1; ii >= 0; ii--) {

            org_id = orgs_set[ii]['id'];
            org_row = document.createElement('a');
            org_row.href = "#";
            org_row.innerHTML = orgs_set[ii]['name'] + ': ' + orgs_set[ii]['claims_count'];

            org_row.onclick = function(event) {  
                event.preventDefault();              
                return function(){
                        select_building(org_id);
                }

            }        
            org_rows.push(org_row);        

            // function select_building_callback(org_id){
            //     return function(){
            //         select_building(org_id);
            //     }
            // }
            // marker.on('click', select_building_callback(org_id));


            };
        // console.log(org_rows)
      
        org_list = document.createElement("ul");
        $.each(org_rows, function(i)
        {
            var li = $('<li/>')
                .addClass('ui-menu-item')
                .attr('role', 'menuitem')
                .appendTo(org_list);  
            console.log(org_rows[i]) ;        
            // org_rows[i].appendTo(li);
            li.add(org_rows[i])
         
            console.log(li); 
        });

        console.log(org_list); 
        marker.addTo(map).bindPopup(org_list);

        
    };

    L.geoJson(buildings).addTo(map);
                    
}