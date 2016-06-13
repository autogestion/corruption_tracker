'use strict';

import React from 'react';
import { Route, IndexRoute } from 'react-router';

import App                from './../containers/App.jsx';
import MainLayout         from '../containers/layouts/MainLayout.container.jsx';
import MapPageContainer from '../containers/MapPageContainer.jsx';

export default (
    <div>
        <Route path="/" component={App} >
            <IndexRoute component={MapPageContainer}/>
        </Route>
    </div>
);
