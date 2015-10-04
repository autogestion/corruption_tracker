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
                buildings['features'][i]['properties']["centroid"][1],
                buildings['features'][i]['properties']["centroid"][0],
            ],
            {icon: myIcon}
        )

        orgs_set = buildings['features'][i]['properties']["organizations"]
        org_rows = []
        for (var ii = orgs_set.length - 1; ii >= 0; ii--) {
            org_row = document.createElement('a');
            org_row.href = "#";
            org_row.id = orgs_set[ii]['id'];
            org_row.innerHTML = orgs_set[ii]['name'] + ': &nbsp;&nbsp;' + orgs_set[ii]['claims_count'];

            org_row.onclick = function(event) {
                select_building($(this).attr('id'));
                event.preventDefault();   
                }        
            org_rows.push(org_row);
            };   
      
        org_list = document.createElement("ul");
        $.each(org_rows, function(i)
        {
            var li = $('<li/>')
                .addClass('ui-menu-item')
                .attr('role', 'menuitem')
                .appendTo(org_list);        
            li.html(org_rows[i]);  
        });
        marker.addTo(map).bindPopup(org_list);        
    };
    L.geoJson(buildings).addTo(map);                    
}