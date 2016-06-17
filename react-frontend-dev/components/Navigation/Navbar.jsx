import React from 'react';
import { Navbar, Nav, NavItem, MenuItem, DropdownButton, NavDropdown } from 'react-bootstrap';
import NavModal from './NavModal.jsx';

class NavbarWrapper extends React.Component {
    static propTypes = {
        modalstate: React.PropTypes.bool,
        content: React.PropTypes.object,
        handleToggleModal: React.PropTypes.func
    };

    render() {
        const { content, modalstate, handleToggleModal } = this.props;
        const whoisModalAction = {
            showNavModal: true,
            navModalcontent: {
                title_cont: "Test title",
                body_cont: "Test body",
                footer_cont: "Test footer"
            }
        };
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#">PDRK</a>  
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav>
                    <NavItem onClick={()=>{handleToggleModal(whoisModalAction)}} eventKey={1} href="#">Who is here?</NavItem>
                    <NavDropdown eventKey={3} title="Dropdown" id="basic-nav-dropdown">
                        <MenuItem eventKey={3.1}>API Docs</MenuItem>
                        <MenuItem eventKey={3.2}>Login</MenuItem>
                        <MenuItem eventKey={3.3}>Register</MenuItem>
                        <MenuItem divider />
                        <DropdownButton title='Language' key={3.4} id='dropdown-basic-language'>
                            <MenuItem eventKey={3.5}>UA</MenuItem>
                            <MenuItem eventKey={3.6}>ENG</MenuItem>
                        </DropdownButton>
                    </NavDropdown>
                </Nav>
                <NavModal show={modalstate} close={()=>handleToggleModal(false)} content = {content}/>
            </Navbar>
        )
    }
};

export default NavbarWrapper;