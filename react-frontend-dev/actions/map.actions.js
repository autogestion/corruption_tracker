'use strict';

import api from '../config/apiSingleton';

import {
    TOGGLE_MODAL,
    FETCH_TEST,
    SEND_CLAIM
} from './types/types.js';

export function toggleModal(showNavModal = false) {
   return {
       type: TOGGLE_MODAL,
       showNavModal
   } 
}

export function submitClaim(params) {
    return (dispatch) => {
        api.claim.sendClaim(params)
            .then((resp) => {
                debugger;
                dispatch({
                    type: SEND_CLAIM,
                    results: resp.results
                })
            });
    };
    // console.log();

}
export function fitBounds() {
    return (dispatch) => {
        api.polygon.fitBounds({layer: 3, coord: [30.23060, 50.31828, 30.80326, 50.54813]})
            .then((resp) => {
                console.log(resp);
                dispatch({
                    type: FETCH_TEST,
                    results: resp.results
                })
            });
    };
}

