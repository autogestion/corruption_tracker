'use strict';

import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import { toggleModal, submitClaim } from '../actions/map.actions.js';

import NavbarWrapper from '../components/Navigation/Navbar.jsx';
import FormTabs from '../components/FormTabs.jsx';
import Map from '../components/Map.jsx';
import '../Styles/mainstyles.scss';

class MapPageContainer extends React.Component {
    static propTypes = {
        modalstate: React.PropTypes.bool
    };

    render() {
        const {modalstate, handleToggleModal, handleSubmitClaim, navModalcontent} = this.props;
        return (
            <div>
                <div id="full-screen-mapwrapper">
                    <Map position={[50, 36.25]} zoom={13}/>
                </div>
                <NavbarWrapper
                    modalstate = {modalstate}
                    handleToggleModal = {handleToggleModal}
                    content = {navModalcontent}
                />
                <FormTabs handleSubmitClaim={handleSubmitClaim} />
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        modalstate: state.uibehavior.showNavModal || false,
        navModalcontent: state.uibehavior.navModalcontent
    };
}

function mapDispatchToProps(dispatch) {
    return {
        handleToggleModal: bindActionCreators(toggleModal, dispatch),
        handleSubmitClaim: bindActionCreators(submitClaim, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapPageContainer);

