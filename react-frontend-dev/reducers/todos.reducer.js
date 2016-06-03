'use strict';

import apiResponseFormatter from '../utils/apiResponseFormatter';
import {
    ADD_TODO,
    CLEAR_ALL,
    COMPLETE_TODO
} from '../actions/types/todos.types.js';

function todos(state = [], action) {
    switch (action.type) {
        case ADD_TODO: {
            return [
                ...state,
                simpleTodo(undefined, action)
            ];
        } break;

        case CLEAR_ALL: {
            return [];
        } break;

        case COMPLETE_TODO: {
            return state.map((todo) => simpleTodo(todo, action));
        } break;

        default:
            return state;
    }
}


function simpleTodo(state, action) {
    switch (action.type) {
        case ADD_TODO: {
            return {
                id    : Date.now(),
                value : action.todo,
                date  : (new Date).toLocaleDateString('en-US', {hour: '2-digit', minute:'2-digit'}),
                completed : false
            };
        } break;

        case COMPLETE_TODO: {
            if (state.id !== action.todoId) return state;

            return {
                ...state,
                completed: !state.completed
            };
        } break;

        default:
            return state;
    }
}

export default todos;

