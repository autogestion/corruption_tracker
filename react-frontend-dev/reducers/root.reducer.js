'use strict';

import { combineReducers } from 'redux';

/**
 * Reducers
 */
import todos from './todos.reducer';
import uibehavior from './uibehavior.reducer';


const rootReducer = combineReducers({
    todos,
    uibehavior
});

export default rootReducer;
