'use strict';

import React from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import { toggleModal } from '../actions/map.actions.js';

import NavbarWrapper from '../components/Navigation/Navbar.jsx';
import FormTabs from '../components/FormTabs.jsx';
import Map from '../components/Map.jsx';
import '../Styles/mainstyles.scss';

class MapPageContainer extends React.Component {
    static propTypes = {
        modalstate: React.PropTypes.bool
    };

    render() {
        const {modalstate, handleToggleModal} = this.props;
        const content = {
            title_cont: 'Break corruption',
            body_cont: (<p>Test body cont</p>)
        };
        return (
            <div>
                <div id="full-screen-mapwrapper">
                    <Map position={[50, 36.25]} zoom={13}/>
                </div>
                <NavbarWrapper
                    modalstate = {modalstate}
                    handleToggleModal = {handleToggleModal}
                    content = {content}
                />
                <FormTabs text={'I\'m form'}/>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        modalstate: state.uibehavior.showNavModal || false
    };
}

function mapDispatchToProps(dispatch) {
    return {
        handleToggleModal: bindActionCreators(toggleModal, dispatch)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(MapPageContainer);

