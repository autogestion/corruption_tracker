'use strict';

import { jsdom } from 'jsdom';


/**
 * Setup the simplest DOM mock up
 */
const document = jsdom('<!doctype html><html><body></body></html>');
/**
 * Set globals for mocha that make access to document
 */
global.document = document;


/**
 * Setup the window object out of the document
 * @type {DocumentView}
 */
const window = document.defaultView;
/**
 * Set globals for mocha that make access to window
 */
global.window = window;
