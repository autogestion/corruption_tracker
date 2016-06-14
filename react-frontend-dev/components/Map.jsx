import React from 'react';
import { render } from 'react-dom';
import { Map, Marker, Popup, TileLayer } from 'react-leaflet';

class MyMap extends React.Component {
    render (){
        const { position, zoom } = this.props;
     return (
         <Map center={position} zoom={zoom}>
             <TileLayer
                 url='http://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png'
                 attribution={'Tiles courtesy of' +
                 '<a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a>' +
                 ' &mdash; Map data &copy; ' +
                 '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'}
             />
         </Map>
     )
    }
};

export default MyMap;