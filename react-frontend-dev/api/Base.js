'use strict';

class Base {
    constructor({apiClient}) {
        if (!apiClient) throw '[apiClient] is required';

        this.apiClient = apiClient;
    }
}

export default Base;

