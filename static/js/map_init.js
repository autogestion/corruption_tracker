function main_map_init (map, options) {
    $("#main > div.leaflet-control-container > div.leaflet-top.leaflet-right").addClass('layout_chooser');
    $('.layout_chooser').removeClass("leaflet-right");
    $('.layout_chooser').addClass("leaflet-left");

  var reselect_selected = false;

  map.on('moveend', function() { 
      updateMapLayer();
  });
  
  var dataBounds, zoom, dataUrl, dataType;
  function updateMapLayer() {
      // W, S, E, N
      dataBounds = map.getBounds().getWest().toFixed(5) + ',' +
      map.getBounds().getSouth().toFixed(5) + ',' +
      map.getBounds().getEast().toFixed(5) + ',' + 
      map.getBounds().getNorth().toFixed(5);
      
      zoom = map.getZoom();  

      if( zoom <=8 ) {
          dataType = 1; // region = 1     <=8
      } else if ( zoom <= 10 ) {
          dataType = 2; // area = 2       <=10
      } else if ( zoom <= 12 ) {
          dataType = 3; // district = 3   <=12
      } else { // 
          dataType = 4; // building = 4   >=13
      };

      dataUrl = api_url + 'polygon/fit_bounds/' + dataType + '/' + dataBounds + '/';      
      map.removeLayer(districtLayer);
      districtLayer.clearLayers()
      
      
      $.getJSON(dataUrl, function (data) {
        var polygons = data;
        districtLayer.clearLayers();        
             
        // Add GeoJSON layer
        var marker, org_row, orgs_set, org_rows;
        // console.log(polygons)

        if (polygons) {
        // Add building markers with popups to polygons.
          for (var i = polygons.length - 1; i >= 0; i--) {


              orgs_set = polygons[i]['properties']["organizations"]
              if (orgs_set){
                org_rows = []
                for (var ii = orgs_set.length - 1; ii >= 0; ii--) {
                    org_row = document.createElement('a');
                    org_row.href = '#' + polygons[i]['properties']["ID"];
                    org_row.id = orgs_set[ii]['id'];            
                    org_row.innerHTML = orgs_set[ii]['name'] + ': <div class="counts">' + orgs_set[ii]['claims'] + '<div>';

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
              } else {
                org_list = polygons[i]['properties']['address']
              };      

              if (polygons[i]["geometry"]) { 

                  var myIcon = L.divIcon({
                      className: 'icon_with_number',
                      html: polygons[i]['properties']["polygon_claims"]
                  }); 

                  marker = L.marker(
                      [
                          polygons[i]['properties']["centroid"][0],
                          polygons[i]['properties']["centroid"][1],
                      ],
                      {icon: myIcon}
                  )
                
                  var polygon = L.polygon(polygons[i]["geometry"]["coordinates"]);
                  polygon.centroid = polygons[i]['properties']["centroid"]

                  if (orgs_set && orgs_set.length==1){       
                      polygon.organization = orgs_set[0]['id']
                  }

                  polygon.setStyle({
                      fillColor: polygons[i]['properties']['color'],
                      weight: 2,
                      color: 'blue',
                      opacity: 0.3,
                      fillOpacity: 0.3
                  });
                  
                  // console.log(polygon)                  
                  marker.addTo(districtLayer);              
                  polygon.addTo(districtLayer).bindPopup(org_list);
                 

                  polygon.on('click',function()  {
                      if ($_selectedPolygon) {
                          $_selectedPolygon.setStyle({
                              weight: 2,
                              color: 'blue',
                              opacity: 0.3,
                              fillOpacity: 0.3
                        });
                      };
                      // map.setView(this.centroid);

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
                          polygons[i]['properties']["centroid"][0],
                          polygons[i]['properties']["centroid"][1],
                      ]           
                  )

                  if (orgs_set.length==1){       
                      marker.organization = orgs_set[0]['id']
                  }

                  marker.addTo(districtLayer).bindPopup(org_list); 
                  // marker.addTo(map).bindPopup(org_list);

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
              };
            
          }; 
        };
      });
      
      districtLayer.addTo(map);
  };    

  var districtLayer = L.geoJson(null,{});
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
        $("#claims_list").empty()
  }); 
  
  // set map view in search polygon feature
  $('#organization_name').autocomplete({
    lookup: places,
    onSelect: function (suggestion) {
    $('#organization').val(suggestion.data);
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


