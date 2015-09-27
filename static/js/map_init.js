function main_map_init (map, options) {
    // Add GeoJSON layer   
    var marker, org_id;

    // Add building markers with popups to buildings.
    for (var i = buildings['features'].length - 1; i >= 0; i--) {        

        for (var ii = buildings['features'][i]['properties']["ORGANIZATIONS"].length - 1; ii >= 0; ii--) {
            org_id = buildings['features'][i]['properties']["ORGANIZATIONS"][ii]['id'];

            var myIcon = L.divIcon({
                className: 'icon_with_number',
                html: buildings['features'][i]['properties']["ORGANIZATIONS"][ii]['claims_count']
            });

            marker = L.marker(
                [
                    buildings['features'][i]['geometry']['coordinates'][0][ii][1],
                    buildings['features'][i]['geometry']['coordinates'][0][ii][0]
                ],
                {icon: myIcon}
            )

            function select_building_callback(org_id){
                return function(){
                    select_building(org_id);
                }
            }

            marker.on('click', select_building_callback(org_id));
            marker.addTo(map).bindPopup(buildings['features'][i]['properties']["ORGANIZATIONS"][ii]['name']);
        };
    };

    L.geoJson(buildings).addTo(map);
                    
}