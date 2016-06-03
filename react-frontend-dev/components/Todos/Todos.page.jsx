'use strict';

import React from 'react';

import AddTodo  from './AddTodo.jsx';
import TodoList from './TodoList/TodoList.jsx';

import './TodosPage.less';
import './sass-test.scss';


class TodosPage extends React.Component {
    static propTypes = {
        todos              : React.PropTypes.array,
        handleAddTodo      : React.PropTypes.func,
        handleTodoComplete : React.PropTypes.func
    };

    render() {
        const { todos, handleAddTodo, handleClearAll, handleTodoComplete } = this.props;

        return (
            <div className='TodosPage'>
                <AddTodo
                    handleAddTodo   = {handleAddTodo}
                    handleClearAll  = {handleClearAll}
                    isClearDisabled = {!todos.length}
                />
                <TodoList
                    todos              = {todos}
                    handleTodoComplete = {handleTodoComplete}
                />
            </div>
        );
    }
}

export default TodosPage;


