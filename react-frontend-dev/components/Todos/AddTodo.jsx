'use strict';

import React    from 'react';
import ReactDOM from 'react-dom';

import './TodosPage.less';


class AddTodo extends React.Component {
    constructor() {
        super();
        this.state = { isDisabled: true };
    }

    static propTypes = {
        isClearDisabled : React.PropTypes.bool,
        handleClearAll  : React.PropTypes.func,
        handleAddTodo   : React.PropTypes.func
    };

    handleChange(event) {
        if (event.keyCode === 13) {
            this.handleAdTodo();
        }
        console.log(this.refs);

        const isTodoEmpty = !this.refs.todoNode.value.length;
        this.setState({ isDisabled: isTodoEmpty });
    }

    handleAdTodo() {
        const addTodo = this.refs.todoNode;

        if (!addTodo.value.length) return false;

        this.props.handleAddTodo({todo: addTodo.value});

        addTodo.value = '';
    }

    render() {
        const textFieldStyle = {
            margin: '0 20px 0 0'
        };

        const { isClearDisabled, handleClearAll } = this.props;

        return (
            <div className='AddTodo'>
                <input
                    ref = 'todoNode'
                    placeholder = 'Enter todo'
                    style     = {textFieldStyle}
                    onChange  = {this.handleChange.bind(this)}
                    onKeyDown = {this.handleChange.bind(this)}
                />
                <button
                    onClick  = {this.handleAdTodo.bind(this)}
                    disabled = {this.state.isDisabled}
                >
                    Add</button>
                <button
                    onClick   = {handleClearAll}
                    disabled  = {isClearDisabled}>
                    clear all</button>
            </div>
        );
    }
}

export default AddTodo;


