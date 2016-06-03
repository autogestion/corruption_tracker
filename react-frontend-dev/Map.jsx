'use strict';

import React from 'react';
// import { render } from 'react-dom';
import { Map, Marker, Popup, TileLayer } from 'react-leaflet';

const position = [51.505, -0.09];
const map = (
    <Map center={position} zoom={13}>
        <TileLayer
            url='http://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png'
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
        <Marker position={position}>
            <Popup>
                <span>A pretty CSS3 popup.<br/>Easily customizable.</span>
            </Popup>
        </Marker>
    </Map>
);

export default map;//renderMap() {
    // render(map,map document.getElementById('map-container'));
// }
