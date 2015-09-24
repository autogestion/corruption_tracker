function main_map_init (map, options) {
    // Add GeoJSON layer
    var marker, polygon_id;

    // Add building markers with popups to buildings.
    for (var i = buildings['features'].length - 1; i >= 0; i--) {
        polygon_id = buildings['features'][i]['properties']['ID'];

        var myIcon = L.divIcon({
            className: 'icon_with_number',
            html: buildings['features'][i]['properties']['CLAIM_COUNT']
        });

        marker = L.marker(
            [
                buildings['features'][i]['geometry']['coordinates'][0][0][1],
                buildings['features'][i]['geometry']['coordinates'][0][0][0]
            ],
            {icon: myIcon}
        )

        function select_building_callback(polygon_id){
            return function(){
                select_building(polygon_id);
            }
        }

        marker.on('click', select_building_callback(polygon_id));
        marker.addTo(map).bindPopup(buildings['features'][i]['properties']['NAME']);
    };

    L.geoJson(buildings).addTo(map);

    // // create location control and add to map
    // lc = L.control.locate({
    //         follow: true,
    //         strings: {
    //             title: "подпись"
    //         }
    //     }).addTo(map);
    //  // request location update and set location
    // lc.locate();                       
}