'use strict';

import React       from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';

import TodosPage from '../../components/todos/Todos.page.jsx';
import { addTodo, clearAll, completeTodo } from '../../actions/todos.actions.js';

class TodosPageContainer extends React.Component {
    static propTypes = {
        todos: React.PropTypes.array
    };
    
    componentDidMount() {
        // Use for pre-loading component data
    }

    render() {
        const {todos, handleAddTodo, handleClearAll, handleTodoComplete} = this.props;
        
        return (
            <TodosPage
                todos              = {todos}
                handleAddTodo      = {handleAddTodo}
                handleClearAll     = {handleClearAll}
                handleTodoComplete = {handleTodoComplete}
            />
        );
    }
}

function mapStateToProps(state) {
    return {
        todos: state.todos || []
    };
}

function mapDispatchToProps(dispatch) {
    return {
        handleAddTodo: bindActionCreators(addTodo, dispatch),
        handleClearAll: bindActionCreators(clearAll, dispatch),
        handleTodoComplete: bindActionCreators(completeTodo, dispatch)
    }
}

export default connect(mapStateToProps)(TodosPageContainer);

