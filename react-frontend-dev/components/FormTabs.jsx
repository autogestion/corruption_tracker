import React from 'react';
import Tabs from 'react-bootstrap/lib/Tabs';
import Tab from 'react-bootstrap/lib/Tab';
import AddClaimForm from './AddClaimForm.jsx';
import AddOrganizationForm from './AddOrganizationForm.jsx';

//class ClaimForm extends React.Component {
const FormTabs = props => {
        const { handleSubmitClaim } = props;
        return (
            <div className="claim-form">
                <Tabs defaultActiveKey={2} id="float_block">
                    <Tab eventKey={1} title="Add Claim">
                        <AddClaimForm handleSubmitClaim={handleSubmitClaim}/>
                    </Tab>
                    <Tab eventKey={2} title="Add organization">
                        <AddOrganizationForm/>
                    </Tab>
                </Tabs>
            </div>
        )

};

export default FormTabs;