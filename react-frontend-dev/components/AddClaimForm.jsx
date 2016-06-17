import React from 'react';
import { FormControl, FormGroup, ControlLabel, Button} from 'react-bootstrap';
import { reduxForm } from 'redux-form';
const fields = ['organizationType', 'violationType', 'servantName', 'claimMsg', 'bribeAmount'];


class AddClaimForm extends React.Component {
    render() {
        console.log(this.props);  
        const {
            fields: { organizationType, violationType, servantName, claimMsg, bribeAmount },
            handleSubmitClaim
        } = this.props;
        return (
            <form onSubmit={handleSubmitClaim} >
                <FormGroup controlId="formControlsText">
                    <FormControl type="text" placeholder="Type organization name and select" {...organizationType} />
                </FormGroup>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>Choose Violation type</ControlLabel>
                    <FormControl componentClass="select" placeholder="select" {...violationType}>
                        <option value="select">select</option>
                        <option value="select">variant</option>
                        <option value="other">...</option>
                    </FormControl>
                </FormGroup>
                <FormGroup controlId="formControlsEmail">
                    <ControlLabel>Servant name</ControlLabel>
                    <FormControl type="text" {...servantName}/>
                </FormGroup>
                <FormGroup controlId="formControlsTextarea">
                    <ControlLabel>Claim message</ControlLabel>
                    <FormControl componentClass="textarea" {...claimMsg}/>
                </FormGroup>
                <FormGroup controlId="formControlsPassword">
                    <ControlLabel>Brime amount</ControlLabel>
                    <FormControl type="text" {...bribeAmount}/>
                </FormGroup>

                <Button type="submit">
                    Send Claim
                </Button>
            </form>
        )
    }
}
AddClaimForm.propTypes = {
    handleSubmitClaim: React.PropTypes.func.isRequired
};

export default reduxForm({
    form: 'adClaimForm',
    fields
})(AddClaimForm);