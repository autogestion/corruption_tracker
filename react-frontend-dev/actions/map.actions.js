'use strict';

import api from '../config/apiSingleton';

import {
    TOGGLE_MODAL
} from './types/types.js';

export function toggleModal(showNavModal = false) {
   return {
       type: TOGGLE_MODAL,
       showNavModal
   } 
}




