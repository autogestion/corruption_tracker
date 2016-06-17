'use strict';

import Base from './Base';

export class SignUpAPI extends Base {
    // googleTypeahead(params) {
    //     const url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%D0%A2&sensor=false'
    //     const payload = {a:'er'};
    //     return this.apiClient.get(url, payload);
    // }
}

export class ClaimAPI extends Base {
    sendClaim(params) {
        const url = '/claim/';
        const payload = params;
        return this.apiClient.post(url, payload);
    }
    getUserClaim(params) {
        const url = '/claim/';
        return this.apiClient.get(url, {}, params);
    }
    getOrganizationClaim(params) {
        const url = '/claim/';
        return this.apiClient.get(url, {}, params);
    }
}

export class OrganizationAPI extends Base {
    getOrganizationClaim(params) {
        const url = '/claim/';
        return this.apiClient.get(url, {}, params);
    }
}

export class PolygonAPI extends Base {
    search(param) {
        const url = '/polygon/';
        const queryParams = {search: param};
        return this.apiClient.get(url, {}, queryParams);
    }
    fitBounds(params) {
        const url = `/polygon/fit_bounds/${params.layer}/${params.coord}/`;
        return this.apiClient.get(url);
    }
}

export class UpdateAPI extends Base {
    // googleTypeahead(params) {
    //     const url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%D0%A2&sensor=false'
    //     const payload = {a:'er'};
    //     return this.apiClient.get(url, payload);
    // }
}