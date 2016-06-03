'use strict';

import api from '../config/apiSingleton';

import {
    ADD_TODO,
    CLEAR_ALL,
    COMPLETE_TODO
} from './types/todos.types.js';

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



