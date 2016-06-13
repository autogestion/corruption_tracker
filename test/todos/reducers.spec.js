'use strict';

import { expect }  from 'chai';
import types       from '../../develop/actions/types/types.js';
import todoReducer     from '../../develop/reducers/todos.reducer';
import rootReducer from '../../develop/reducers/root.reducer';

const should = require('chai').should();


describe('Root reducer', () => {
    it('init action: should return the initial state', () => {
        expect(
            rootReducer(undefined, {})
        ).to.deep.equal({
            todos: []
        });
    });
});

describe('Reducers:todos', () => {
    it('init action: should return the initial state', () => {
        const expectedTodos = todoReducer(undefined, {});

        expect(expectedTodos).to.deep.equal([]);
    });

    it('ADD_TODO', () => {
        const expectedTodos = todoReducer([], {
            type: types.ADD_TODO,
            todo: 'mochaTest'
        });

        expectedTodos.should.have.length(1);


        const expectedTodo = expectedTodos[0];

        expectedTodo.should.have.property('id').be.a('number');
        expectedTodo.should.have.property('date').be.a('string');
        expect(expectedTodo.value).to.equal('mochaTest');
        expect(expectedTodo.completed).to.equal(false);
    });

    it('CLEAR_ALL', () => {
        const expectedTodos = todoReducer([
            {
                id       : 1,
                value    : 'add more one',
                date     : '23/10/1993',
                completed: true
            }
        ], {
            type: types.CLEAR_ALL
        });

        expectedTodos.should.have.length(0);
    });

    it('COMPLETE_TODO', () => {
        const expectedTodos = todoReducer([
            {
                id       : 1,
                value    : 'add more one',
                date     : '23/10/1993',
                completed: true
            }
        ], {
            type  : types.COMPLETE_TODO,
            todoId: 1
        });

        expectedTodos.should.have.length(1);


        const expectedTodo = expectedTodos[0];

        expect(expectedTodo.id).to.equal(1);
        expect(expectedTodo.date).to.equal('23/10/1993');
        expect(expectedTodo.value).to.equal('add more one');
        expect(expectedTodo.completed).to.equal(false);
    });
});
