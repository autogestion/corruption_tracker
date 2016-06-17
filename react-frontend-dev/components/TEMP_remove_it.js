/**
 * Created by aul on 6/17/2016.
 */
[6/16/2016 17:57:28] Kobernik Yura: import {reduxForm} from 'redux-form';

import Filter from '../../controls/filter/Filter.jsx';
import Logo from '../../../components/controls/logo/Logo.jsx';
import Button from '../../../components/controls/button/Button.jsx';

import {
    createValidator,
    required,
    minLength,
    maxLength
} from '../../../utils/form.validator';
import './EditGroupPage.less';
import dataConstants, {getGroupTypeInfo} from '../../../constant/data.constant';
import validationConstants from '../../../constant/validation.constant';
import {isEmptyGroup} from '../../../utils/mappers/groupAPI.mapper';
import classNames from 'classnames';


class EditGroupPage extends React.Component {

    state = {
        groupType: dataConstants.group.type.PUBLIC_TYPE,
    };

    static propTypes = {
        isLoading: React.PropTypes.bool,
        group: React.PropTypes.object,
        handleGoBack: React.PropTypes.func,
        handleOnSubmit: React.PropTypes.func
    };

    handleOnFilterChange = (groupType) => {
        this.setState({
            groupType: (groupType ? dataConstants.group.type.PUBLIC_TYPE : dataConstants.group.type.PRIVATE_TYPE)
        });
    };

    renderHeader() {
        const { handleGoBack, group } = this.props;
        const text = isEmptyGroup(group) ? 'Create new group' : 'Edit group info';
        return (
            <header className="header-modal">

                <a href="#" className="close-modal"></a>
                {text}

                <div className="hide">
                    <Logo
                        text={text}
                        rightHandleControl={handleGoBack}
                        rightIconClass={'glyphicon-remove'}
                    />
                </div>
            </header>
        );
    }

    renderContent() {
        const {
            group,
            fields: {
                title,
                description
            }
        } = this.props;

        const { groupType } = this.state;

        const titleObjClasses = {
            'field-line': true,
            'show-error': title.touched && title.error ? true : false
        };
        const titleClasses = classNames(titleObjClasses);

        const descriptionObjClasses = {
            'field-description': true,
            'show-error': description.error ? true : false
        };
        const descriptionClasses = classNames(descriptionObjClasses);
        const activeTabIndex = groupType === dataConstants.group.type.PUBLIC_TYPE ? 0 : 1;

        return (
            <div className="form-create-group form-grid">

                <div className="item-row">
                    <label className="label-row">Group title (40 characters max.)</label>
                    <input
                        className="field-line"
                        type='text'
                        {...title}
                        className="field-line {titleClasses}"
                    />
                </div>

                <div className="item-row">
                    <label className="label-row">Group type</label>
                    <Filter
                        ref="FilterTabs"
                        left={(groupType === dataConstants.group.type.PUBLIC_TYPE)}
                        filterInfo={getGroupTypeInfo()}
                        filterChanged={this.handleOnFilterChange}
                    />
                    <p className="sun-info">

                        Everyvone will see the group and content in it

                        {
                            group && group.type === dataConstants.group.type.PUBLIC_TYPE && groupType === dataConstants.group.type.PRIVATE_TYPE ?
                                (<span className="changeGroupWarning">If you change public group to private, shared posts from it will no longer be available to non-members of this group.</span>)
                                : null
                        }
                    </p>
                </div>
                <textarea
                    placeholder={'Description, max. 160 characters'}
                    {...description}
                    text={description.value}

                    className="field-description"
                />
            </div>
        );
    }

    renderFooter() {
        const { groupType } = this.state;
        const {
            handleSubmit,
            group,
            handleOnSubmit,
            invalid
        } = this.props;
        const text = group ? 'Save changes' : 'Create';

        const submitResult = (values) => {
            handleOnSubmit({
                ...group,
                ...values,
                type: groupType
            });
        };

        return (
            <div className="footer__create-group">
                <Button
                    className="button-primary"
                    text={text}
                    onClick={handleSubmit(submitResult)}
                    disabled={invalid}
                />
            </div>
        );
    }

    render() {
        return (
            <div className="modal">
                <div className="content-modal create-group__modal">
                    {this.renderHeader()}
                    {this.renderContent()}
                    {this.renderFooter()}
                </div>
            </div>
        );
    }
}


const mapStateToProps = (state, props) => {
    return {
        initialValues: props.group
    };
};

const mapDispatchToProps = () => {
    return {};
};

const config = {
    form: 'EditGroup',
    fields: [
        'title',
        'type',
        'description'
    ],
    validate: createValidator({
        title: [
            required,
            maxLength(validationConstants.group.maxTitleLength),
            minLength(validationConstants.group.minTitleLength)
        ],
        description: [
            maxLength(validationConstants.group.maxDescriptionLength)
        ]
    })
};


export default reduxForm(config, mapStateToProps, mapDispatchToProps)(EditGroupPage);


//--------------------------------------------------------
'use strict';

import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';

import appHistory from '../../config/appHistory';
import EditGroupPage from '../../components/pages/groups/EditGroup.page.jsx';
import {
    getGroup,
    clearGroupState,
    addGroup,
    editGroup,
} from '../../actions/group.actions';
import {isEmpty} from '../../utils/helpers';


class EditGroupContainer extends React.Component {

    componentDidMount() {
        const { params, handleGetGroup } = this.props;
        const { groupId } = params;
        if (groupId) {
            handleGetGroup({ groupId });
        }
    }

    componentWillUnmount() {
        this._clearState();
    }

    _clearState = () => {
        const { handleClearGroupState } = this.props;
        handleClearGroupState();
    };

    handleOnSubmit = (values) => {
        const { group, handleAddGroup, handleEditGroup } = this.props;
        if (!isEmpty(group) && group.id) {
            handleEditGroup(values);
        } else {
            handleAddGroup(values);
        }
    };

    handleGoBack = () => {
        this._clearState();
        appHistory.goBack();
    };

    render() {
        const { group } = this.props;

        return (
            <EditGroupPage
                group={group}
                handleOnSubmit={::this.handleOnSubmit}
                handleGoBack={::this.handleGoBack}
            />
        );
    }
}

const mapStateToProps = (state) => {
    return {
        group: state.group.group,
        editData: state.form.EditGroup
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        handleGetGroup: bindActionCreators(getGroup, dispatch),
        handleAddGroup: bindActionCreators(addGroup, dispatch),
        handleEditGroup: bindActionCreators(editGroup, dispatch),
        handleClearGroupState: bindActionCreators(clearGroupState, dispatch)
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(EditGroupContainer);