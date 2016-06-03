'use strict';

import React from 'react';
import classNames from 'classnames';

import '../TodosPage.less';

class Todo extends React.Component {
    static propTypes = {
        todo               : React.PropTypes.object,
        handleTodoComplete : React.PropTypes.func
    };

    render() {
        const { key,  todo, handleTodoComplete } = this.props;
        const tableRow = classNames({'completed': todo.completed});

        return (
            <tr key={key} className={tableRow}>
                <td>
                    <input
                        type     = "checkbox"
                        onChange = {handleTodoComplete.bind(this, {todoId: todo.id})}
                    />
                </td>
                <td>{todo.value}</td>
                <td>{todo.date}</td>
            </tr>
        );
    }
}

export default Todo;


