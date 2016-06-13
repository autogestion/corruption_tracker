import React from 'react';
import { FormControl, FormGroup, ControlLabel, Button} from 'react-bootstrap';


class AddClaimForm extends React.Component {
    static propTypes = {

    };

    render() {
        //const { content, modalstate, handleToggleModal } = this.props;
        return (
            <form>
                <FormGroup controlId="formControlsText">
                    <FormControl type="text" placeholder="Type organization name and select" />
                </FormGroup>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>Choose Violation type</ControlLabel>
                    <FormControl componentClass="select" placeholder="select">
                        <option value="select">select</option>
                        <option value="other">...</option>
                    </FormControl>
                </FormGroup>
                <FormGroup controlId="formControlsEmail">
                    <ControlLabel>Servant name</ControlLabel>
                    <FormControl type="text"/>
                </FormGroup>
                <FormGroup controlId="formControlsTextarea">
                    <ControlLabel>Claim message</ControlLabel>
                    <FormControl componentClass="textarea"/>
                </FormGroup>
                <FormGroup controlId="formControlsPassword">
                    <ControlLabel>Brime amount</ControlLabel>
                    <FormControl type="text" />
                </FormGroup>

                <Button type="submit">
                    Send Claim
                </Button>
            </form>
        )
    }
};

export default AddClaimForm;