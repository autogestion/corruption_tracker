function main_map_init (map, options) {
    $("#main > div.leaflet-control-container > div.leaflet-top.leaflet-right").addClass('layout_chooser');
    $('.layout_chooser').removeClass("leaflet-right");
    $('.layout_chooser').addClass("leaflet-left");


    // Add GeoJSON layer
    var marker, org_row, orgs_set, org_rows;
    // console.log(polygons)

    // Add building markers with popups to polygons.
    for (var i = polygons['features'].length - 1; i >= 0; i--) {

        orgs_set = polygons['features'][i]['properties']["organizations"]

        org_rows = []
        for (var ii = orgs_set.length - 1; ii >= 0; ii--) {
            org_row = document.createElement('a');
            org_row.href = '#' + polygons['features'][i]['properties']["ID"];
            org_row.id = orgs_set[ii]['id'];            
            org_row.innerHTML = orgs_set[ii]['name'] + ': <div class="counts">' + orgs_set[ii]['claims_count'] + '<div>';

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

        if (polygons['features'][i]["geometry"]) { 

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
        } else {
            marker = L.marker(
                [
                    polygons['features'][i]['properties']["centroid"][0],
                    polygons['features'][i]['properties']["centroid"][1],
                ]           
            )

            if (orgs_set.length==1){       
                marker.organization = orgs_set[0]['id']
            }

            marker.addTo(map).bindPopup(org_list);

            marker.on('click',function()  {
                if ($_selectedPolygon) {
                    $_selectedPolygon.setStyle({
                        weight: 2,
                        color: 'blue',
                        opacity: 0.3,
                        fillOpacity: 0.3
                });
                }; 
            
                if (this.organization) {
                    select_building(this.organization);
                }
                else {
                    $('#target').empty();            
                };
            });                        
        
        }
        
    }; 

    map.setView(polygons['config']['center'], polygons['config']['zoom']); 

    $_selectedPolygon = null;
	
	
	// reset selected polygon highlight to default
	map.on('click', function() {
		$_selectedPolygon.setStyle({
			weight: 2,
			color: 'blue',
			opacity: 0.3,
			fillOpacity: 0.3
		});
	});	

	
	// set map view in search polygon feature
	$('#organization_name').autocomplete({
		lookup: places,
		onSelect: function (suggestion) {
		$('#org_id').val(suggestion.data);
			update_dropdown(suggestion.org_type_id);
			AddPage.validate();
			
			map.setView([ suggestion.centroid[0], suggestion.centroid[1] ], 16);
		}
	});

	/* GPS enabled geolocation control set to follow the user's location */
	var locateControl = L.control.locate({
	  position: "topleft",
	  drawCircle: true,
	  follow: true,
	  setView: true,
	  keepCurrentZoomLevel: true,
	  markerStyle: {
		weight: 1,
		opacity: 0.8,
		fillOpacity: 0.8
	  },
	  circleStyle: {
		weight: 1,
		clickable: false
	  },
	  icon: "fa fa-location-arrow",
	  metric: false,
	  strings: {
		title: "My location",
		popup: "You are within {distance} {unit} from this point",
		outsideMapBoundsMsg: "You seem located outside the boundaries of the map"
	  },
	  locateOptions: {
		maxZoom: 18,
		watch: true,
		enableHighAccuracy: true,
		maximumAge: 10000,
		timeout: 10000
	  }
	}).addTo(map);


	
}