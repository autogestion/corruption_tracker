'use strict';

import { expect }   from 'chai';
import types        from '../../develop/actions/types/todos.types.js';
import * as actions from '../../develop/actions/todos.actions.js';

import configureStore from 'redux-mock-store';

/**
 * Add your middlewares like `redux-thunk`
 * @type {Array}
 */
const middlewares = [];
const mockStore   = configureStore(middlewares);


describe('Actions:sync', () => {
    it('addTodo: should create an action to add a todo', () => {
        const todo = 'mochaTest';
        const expectedAction = {
            type: types.ADD_TODO,
            todo
        };

        expect(actions.addTodo({todo})).to.deep.equal(expectedAction);
    });

    it('clearAll: should create an action to delete all todos', () => {
        const expectedAction = {
            type: types.CLEAR_ALL
        };

        expect(actions.clearAll()).to.deep.equal(expectedAction);
    });

    it('addTodo: should create an action to complete a todo', (done) => {
        const todoId = 200913;

        /**
         * Init state
         * @type {{}}
         */
        const getState = {};
        const action   = {
            type: types.COMPLETE_TODO,
            todoId
        };
        const expectedActions = [action];

        const store = mockStore(getState, expectedActions, done);

        store.dispatch(action);

        //expect(actions.completeTodo({todoId})()).to.deep.equal(expectedAction);
    });
});
