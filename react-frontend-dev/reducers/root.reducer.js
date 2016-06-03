'use strict';

import { combineReducers } from 'redux';

/**
 * Reducers
 */
import todos from './todos.reducer';


const rootReducer = combineReducers({
    todos
});

export default rootReducer;
