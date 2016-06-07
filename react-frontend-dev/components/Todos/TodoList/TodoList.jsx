'use strict';

import React    from 'react';
import ReactDOM from 'react-dom';

import Todo from './Todo.jsx';

class TodoList extends React.Component {
    static propTypes = {
        todos              : React.PropTypes.array,
        handleTodoComplete : React.PropTypes.func
    };

    static defaultProps = {
        todos: []
    };

    render() {
        const { todos, handleTodoComplete } = this.props;

        const rows = todos.map((todo, idx) => {
            return (
                <Todo
                    key  = {idx}
                    todo = {todo}
                    handleTodoComplete = {handleTodoComplete}
                />
            );
        });

        return (
            <div className='TodoList'>
                <table>
                    <thead>
                        <tr>
                            <th><b>Check</b></th>
                            <th><b>Todo</b></th>
                            <th><b>Date</b></th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default TodoList;


