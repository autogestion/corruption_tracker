'use strict';

import React from 'react';
import { Route, IndexRoute } from 'react-router';

import App                from './../containers/App.jsx';
import MainLayout         from '../containers/layouts/MainLayout.container.jsx';
import TodosPageContainer from '../containers/todos/Todos.container.jsx';

export default (
    <Route path="/" component={App} >
        <IndexRoute component={TodosPageContainer}/>
    </Route>
);
