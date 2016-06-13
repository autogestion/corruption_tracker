'use strict';

import api from '../config/apiSingleton';

import {
    ADD_TODO,
    CLEAR_ALL,
    COMPLETE_TODO,
    TOGGLE_MODAL
} from './types/types.js';

export function toggleModal(showNavModal = false) {
    console.log(showNavModal);
   return {
       type: TOGGLE_MODAL,
       showNavModal
   } 
}
export function addTodo(params = {}, query = {}) {
    return {
        type: ADD_TODO,
        todo: params.todo
    };
}

export function clearAll(params = {}, query = {}) {
    return {
        type: CLEAR_ALL
    };
}

export function completeTodo(params = {}, query = {}) {
    return (dispatch) => {
        const search = query.search || '';

        dispatch({
            type   : COMPLETE_TODO,
            todoId : params.todoId
        });
    };
}



