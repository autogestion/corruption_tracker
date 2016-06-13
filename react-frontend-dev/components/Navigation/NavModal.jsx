import React from 'react';
import { Modal, Button } from 'react-bootstrap';

export default React.createClass({
    render() {
        const { title_cont, body_cont, footer_cont } = this.props.content;
        return (
            <Modal show={this.props.show} onHide={this.props.close}>
                <Modal.Header closeButton>
                    <Modal.Title>{title_cont || null}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {body_cont || null}
                </Modal.Body>
                <Modal.Footer>
                    {footer_cont || null}
                    <Button onClick={this.props.close}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
        }
    });