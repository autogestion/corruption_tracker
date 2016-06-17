'use strict';

import { combineReducers } from 'redux';

/**
 * Reducers
 */
import todos from './todos.reducer';
import uibehavior from './uibehavior.reducer';
import {reducer as formReducer} from 'redux-form';

const rootReducer = combineReducers({
    todos,
    uibehavior,
    form: formReducer
});

export default rootReducer;
