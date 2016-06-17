/**
 * Created by aul on 6/10/2016.
 */
'use strict';

import { TOGGLE_MODAL, SEND_CLAIM, NETWORK_ERROR, SUCCESSFUL_REQUEST} from '../actions/types/types.js';

function uibehavior(state = [], action) {
    console.log('---> ACTION', action);
    switch (action.type) {
        case TOGGLE_MODAL: {
            return {
                ...state,
                showNavModal: action.showNavModal,
                navModalcontent: action.navModalcontent
            };
        } break;
        case NETWORK_ERROR: {
            return { ...state,
                showNavModal: true,
                navModalcontent: {
                    title_cont: `Network Error! Status ${action.status}.`
                }
            };

        } break;
        case SUCCESSFUL_REQUEST: {
            return { ...state,
                showNavModal: true,
                navModalcontent: {
                    title_cont: 'Successfuly updated!'
                }
            };

        } break;

        default:
            return state;
    }

}

export default uibehavior;
