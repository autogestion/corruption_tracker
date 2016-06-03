'use strict';

import React    from 'react';
import ReactDOM from 'react-dom';

import Table             from 'material-ui/lib/table/table';
import TableBody         from 'material-ui/lib/table/table-body';
import TableHeader       from 'material-ui/lib/table/table-header';
import TableRow          from 'material-ui/lib/table/table-row';
import TableHeaderColumn from 'material-ui/lib/table/table-header-column';
import TableRowColumn from 'material-ui/lib/table/table-row-column';

import Todo from './Todo.jsx';

import '../TodosPage.less';


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
                <Table
                    fixedHeader = {true}
                >
                    <TableHeader
                        displaySelectAll  = {false}
                        adjustForCheckbox = {false}
                    >
                        <TableRow>
                            <TableHeaderColumn><b>Check</b></TableHeaderColumn>
                            <TableHeaderColumn><b>Todo</b></TableHeaderColumn>
                            <TableHeaderColumn><b>Date</b></TableHeaderColumn>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {rows}
                    </TableBody>
                </Table>
            </div>
        );
    }
}

export default TodoList;


