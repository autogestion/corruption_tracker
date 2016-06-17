import React from 'react';
import { FormControl, FormGroup, ControlLabel, Button} from 'react-bootstrap';
import { reduxForm } from 'redux-form';
const fields = ['organization', 'claim_type', 'servant', 'text', 'bribe'];


class AddClaimForm extends React.Component {
    render() {
        const {
            fields: { organization, claim_type, servant, text, bribe },
            handleSubmit,
            handleSubmitClaim
        } = this.props;
        const submitResult = (values) => {
            console.log(values);
            handleSubmitClaim(values);
        };
        return (
        <form onSubmit={handleSubmit(submitResult)}>
                <FormGroup controlId="formControlsText">
                    <FormControl type="text" placeholder="Type organization name and select" {...organization} />
                </FormGroup>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>Choose Violation type</ControlLabel>
                    <FormControl componentClass="select" placeholder="select" {...claim_type}>
                        <option value="1">Murder</option>
                        <option value="2">Money</option>
                        <option value="0">Prostitution</option>
                    </FormControl>
                </FormGroup>
                <FormGroup controlId="formControlsEmail">
                    <ControlLabel>Servant name</ControlLabel>
                    <FormControl type="text" {...servant}/>
                </FormGroup>
                <FormGroup controlId="formControlsTextarea">
                    <ControlLabel>Claim message</ControlLabel>
                    <FormControl componentClass="textarea" {...text}/>
                </FormGroup>
                <FormGroup controlId="formControlsPassword">
                    <ControlLabel>Brime amount</ControlLabel>
                    <FormControl type="text" {...bribe}/>
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