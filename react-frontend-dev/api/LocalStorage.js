'use strict';

export default {
    set(property, value) {
        window.localStorage.setItem(property, JSON.stringify(value));
    },

    get(property) {
        return JSON.parse(localStorage.getItem(property)) || null;
    },

    remove(property) {
        window.localStorage.removeItem(property);
    }
}
