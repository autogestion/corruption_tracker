'use strict';

// import '../node_modules/babel-core/polyfill';

import React        from 'react';
import ReactDOM     from 'react-dom';
import { Provider } from 'react-redux';

import { Router } from 'react-router';

import routes         from './config/appRoutes.jsx';
import configureStore from './store/root.store';
import appHistory     from './config/appHistory';


const initialState = {
    uibehavior: {
        showNavModal: false
    }
};
const store = configureStore(initialState);

ReactDOM.render(
    <Provider store={store}>
        <Router children={routes} history={appHistory} />        
    </Provider>,
    document.getElementById('react-view')
);
