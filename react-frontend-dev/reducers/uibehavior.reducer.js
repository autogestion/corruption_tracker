/**
 * Created by aul on 6/10/2016.
 */
'use strict';

import { TOGGLE_MODAL } from '../actions/types/types.js';

function uibehavior(state = [], action) {
    // console.log('---> ACTION', action);
    switch (action.type) {
        case TOGGLE_MODAL: {
            return { ...state,
                showNavModal: action.showNavModal };

        } break;

        default:
            return state;
    }
}

export default uibehavior;
