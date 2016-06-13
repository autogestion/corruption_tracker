import React from 'react';
import { FormControl, FormGroup, ControlLabel, Button} from 'react-bootstrap';

class AddOrganizationForm extends React.Component {
    static propTypes = {

    };

    render() {
        //const { content, modalstate, handleToggleModal } = this.props;
        return (
            <form>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>Choose Organization type</ControlLabel>
                    <FormControl componentClass="select" placeholder="select">
                        <option value="select">select</option>
                        <option value="other">...</option>
                    </FormControl>
                </FormGroup>
                <FormGroup controlId="formControlsEmail">
                    <ControlLabel>Centroid</ControlLabel>
                    <FormControl type="text"/>
                </FormGroup>
                <FormGroup controlId="formControlsEmail">
                    <ControlLabel>Adress</ControlLabel>
                    <FormControl type="text"/>
                </FormGroup>
                <FormGroup controlId="formControlsPassword">
                    <ControlLabel>Organization Name</ControlLabel>
                    <FormControl type="text" />
                </FormGroup>

                <Button type="submit">
                    Send Organization
                </Button>
            </form>
        )
    }
};

export default AddOrganizationForm;