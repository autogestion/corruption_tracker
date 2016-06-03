'use strict';

import React   from 'react';

class MainLayout extends React.Component {

    handleTabClick(type) {
        history.pushState(null, `/${type}`);
    }

    render() {
        return (
            <div>
                {this.props.children}
            </div>
        );
    }
}

export default MainLayout;
