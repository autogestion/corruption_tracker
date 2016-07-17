function main_map_init (map, options) {

    // var reselect_selected = false;

    // reset selected polygon highlight to default
    function deselect_selected(){
        if ($_selectedPolygon) {
            $_selectedPolygon.setStyle({
                weight: 2, color: 'blue',
                opacity: 0.3, fillOpacity: 0.3
          });
        };      
    }
  
    var dataBounds, zoom, dataUrl, dataType;
    function updateMapLayer() {
        console.time("updateMapLayer executed in");

        // W, S, E, N
        dataBounds = map.getBounds().getWest().toFixed(5) + ',' +
        map.getBounds().getSouth().toFixed(5) + ',' +
        map.getBounds().getEast().toFixed(5) + ',' + 
        map.getBounds().getNorth().toFixed(5);
        
        zoom = map.getZoom();
               if ( zoom <=8 )   { dataType = 1; // region = 1     <=8
        } else if ( zoom <= 10 ) { dataType = 2; // area = 2       <=10
        } else if ( zoom <= 14 ) { dataType = 3; // district = 3   <=12
        } else                   { dataType = 4; // building = 4   >=13
        };

        dataUrl = api_url + 'polygon/fit_bounds/' + dataType + '/' + dataBounds + '/';      
        map.removeLayer(districtLayer);
        districtLayer.clearLayers()

        $.getJSON(dataUrl, function (data, textStatus, request) {
            var polygons = data;

            console.log('django executed in: '+ request.getResponseHeader('executed'))
            console.log('rendered ' + polygons.length + ' polygons of level ' + dataType)
            
            districtLayer.clearLayers();

            if (polygons) {
                var marker, object_centroid, org_row, orgs_set, org_rows;
                places = []
                
                // Create geo-objects from fetched data.
                for (var i = polygons.length - 1; i >= 0; i--) {
                    orgs_set = polygons[i]['properties']["organizations"]
                    object_centroid = polygons[i]['properties']["centroid"]

                    // console.log(orgs_set, 'orgs_set');
                    // if geo-object is building, process its orgs
                    if (orgs_set){                        
                        org_rows = [];                
                        for (var ii = orgs_set.length - 1; ii >= 0; ii--) {                    
                            org_row = document.createElement('a');
                            org_row.href = '#' + polygons[i]['properties']["ID"];
                            org_row.id = orgs_set[ii]['id'];
                            org_row.innerHTML = orgs_set[ii]['name'] + ': <div class="counts">' + orgs_set[ii]['claims'] + '<div>';

                            org_row.onclick = function(event) {
                                select_building($(this).attr('id'), $(this).text().split(":")[0], object_centroid);
                                event.preventDefault();
                            };
                            org_rows.push(org_row);
                            places.push({data: orgs_set[ii]['id'],
                                       value: orgs_set[ii]['name'],
                                       centroid: object_centroid,
                                       org_type_id: orgs_set[ii]['org_type']});
                        };
              
                        org_list = document.createElement("ul");
                        $.each(org_rows, function(i){
                            var li = $('<li/>')
                                .addClass('ui-menu-item')
                                .attr('role', 'menuitem')
                                .appendTo(org_list);        
                            li.html(org_rows[i]);
                        });

                    // if geo-object is district or higher
                    } else {
                        org_list = polygons[i]['properties']['address']
                    };

                    // create polygon with marker if geo-object have shape
                    if (polygons[i]["geometry"]) {

                        var myIcon = L.divIcon({
                            className: 'icon_with_number',
                            html: polygons[i]['properties']["polygon_claims"]
                        }); 
                        marker = L.marker(object_centroid, {icon: myIcon})                      

                        var polygon = L.polygon(polygons[i]["geometry"]["coordinates"]);

                        if (orgs_set){       
                            polygon.organization = orgs_set[0]['id']
                            polygon.org_name = orgs_set[0]['name']
                        }

                        polygon.setStyle({
                            fillColor: polygons[i]['properties']['color'],
                            weight: 2, color: 'blue',
                            opacity: 0.3, fillOpacity: 0.3
                        });
                        
                        marker.addTo(districtLayer);              
                        polygon.addTo(districtLayer).bindPopup(org_list);

                        // polygon select callback
                        polygon.on('click',function() {                      
                            deselect_selected();
                            // map.setView(this.centroid);

                            this.setStyle({
                                weight: 6, color: 'green',
                                opacity: 1, fillOpacity: 0.8
                            });
                            $_selectedPolygon = this;

                            if (this.organization) {
                                select_building(this.organization, this.org_name, object_centroid);
                            }
                            else {
                                $('#claims_list').empty();            
                            };
                        });  
               
                    // create only marker if no shape
                    } else {
                        marker = L.marker(object_centroid)

                        if (orgs_set.length==1){       
                            marker.organization = orgs_set[0]['id']
                            marker.org_name = orgs_set[0]['name']
                        }

                        marker.addTo(districtLayer).bindPopup(org_list);                  

                        marker.on('click',function()  {
                            deselect_selected();
                            // $_selectedPolygon = null;                        
                            if (this.organization) {
                                select_building(this.organization, this.org_name, object_centroid);
                            }
                            else {
                                $('#claims_list').empty();            
                            };
                        });                        
                    };
                  
                }; // end of loop over polygons
              // console.log(places)
                $('#organization_name').autocomplete({
                    lookup: places,
                    onSelect: function (suggestion) {
                        $('#organization').val(suggestion.data);
                        update_dropdown(suggestion.org_type_id);
                        var org_id = $('#organization').val();
                        select_building(org_id);
                        // AddPage.validate();
                    }
                });          
            }; // if polygons 

        }); // get json
        
        console.time("districtLayer.addTo(map) executed in");
        districtLayer.addTo(map);
        console.timeEnd("districtLayer.addTo(map) executed in");   
        console.timeEnd("updateMapLayer executed in");
    }; // end of updateMapLayer


    //  Page onload logic
    var districtLayer = L.geoJson(null,{});
    $_selectedPolygon = null;
    
    if (window.location.hash) {        
        try {
            var hash_data = window.location.hash.replace("#", "").split("&");

            if (hash_data[0].split('=')[0]=='cityzoom'){
                var hashed_coordinates = hash_data[0].split('=')[1].split(',');
                map.setView(hashed_coordinates, 12);
                updateMapLayer(); 

            } else {
                var hashed_org_id = hash_data[0].split('=')[1];
                var hashed_coordinates = hash_data[1].split('=')[1].split(','); 
                map.setView(hashed_coordinates, 16);
                updateMapLayer();     
                select_building(hashed_org_id, 'organization', hashed_coordinates );  
            }
        } catch(err) {
            console.log(err)
            map.setView(zoom_to, 12);
            updateMapLayer();    
        };
    } else {
        map.setView(zoom_to, 12);
        updateMapLayer();    
    }

    
    map.on('moveend', function() { 
        updateMapLayer();
    });
    
    map.on('click', function() {
        $("#claims_list").empty();
        clear_claim_form();
        deselect_selected();
    });
  
  /* GPS enabled geolocation control set to follow the user's location */
    var locateControl = L.control.locate({
        position: "topleft", drawCircle: true, follow: true,
        setView: true, keepCurrentZoomLevel: true,
        markerStyle: { weight: 1, opacity: 0.8, fillOpacity: 0.8 },
        circleStyle: { weight: 1, clickable: false },
        icon: "fa fa-location-arrow",
        metric: false,
        strings: { title: "My location", popup: "You are within {distance} {unit} from this point",
            outsideMapBoundsMsg: "You seem located outside the boundaries of the map"},
        locateOptions: { maxZoom: 18, watch: true, enableHighAccuracy: true,
            maximumAge: 10000, timeout: 10000 }
    }).addTo(map);
  
}


