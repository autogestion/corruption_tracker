'use strict';

import React    from 'react';
import ReactDOM from 'react-dom';

import TextField    from 'material-ui/lib/text-field';
import FlatButton   from 'material-ui/lib/flat-button';
import FontIcon     from 'material-ui/lib/font-icon';

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

        const isTodoEmpty = !this.refs.todoNode.getValue().length;
        this.setState({ isDisabled: isTodoEmpty });
    }

    handleAdTodo() {
        const addTodo = this.refs.todoNode;

        if (!addTodo.getValue().length) return false;

        this.props.handleAddTodo({todo: addTodo.getValue()});

        addTodo.setValue('');
    }

    render() {
        const textFieldStyle = {
            margin: '0 20px 0 0'
        };

        const { isClearDisabled, handleClearAll } = this.props;

        return (
            <div className='AddTodo'>
                <TextField
                    ref       = 'todoNode'
                    hintText  = 'Enter todo'
                    style     = {textFieldStyle}
                    onChange  = {this.handleChange.bind(this)}
                    onKeyDown = {this.handleChange.bind(this)}
                />
                <FlatButton
                    label    = 'Add'
                    secondary= {true}
                    onClick  = {this.handleAdTodo.bind(this)}
                    disabled = {this.state.isDisabled}
                />
                <FlatButton
                    label     = 'clear all'
                    secondary = {true}
                    onClick   = {handleClearAll}
                    disabled  = {isClearDisabled}
                />
            </div>
        );
    }
}

export default AddTodo;


