'use strict';

import ApiClient from './ApiClient';
import { SignUpAPI, ClaimAPI, OrganizationAPI, PolygonAPI, UpdateAPI }  from './allEndpointsAPI';

export default function({apiPrefix} = {}) {
    if (!apiPrefix) throw '[apiPrefix] is required';

    const api = new ApiClient({ prefix: apiPrefix });

    return {
        signup: new SignUpAPI({ apiClient: api }),
        claim: new ClaimAPI({ apiClient: api }),
        organization: new OrganizationAPI({ apiClient: api }),
        polygon: new PolygonAPI({ apiClient: api }),
        update: new UpdateAPI({ apiClient: api })
    };
}
