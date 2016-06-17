'use strict';

import api from '../config/apiSingleton';

import {
    TOGGLE_MODAL,
    FETCH_TEST,
    SEND_CLAIM,
    NETWORK_ERROR,
    SUCCESSFUL_REQUEST
} from './types/types.js';

export function toggleModal(params = {showNavModal: false}) {
   return {
       type: TOGGLE_MODAL,
       showNavModal: params.showNavModal,
       navModalcontent: params.navModalcontent
   } 
}

export function submitClaim(params) {
    return (dispatch) => {
        console.log(params);
        api.claim.sendClaim(params)
            .then((resp) => {
                dispatch({
                    type: SUCCESSFUL_REQUEST,
                    results: resp
                })
            })
            .catch((resp) => {
                dispatch({
                    type: NETWORK_ERROR,
                    status: resp.status
                })
            })
        ;
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

