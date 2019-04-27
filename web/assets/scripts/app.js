// Dependencies
import 'jquery'
import 'popper.js'

// Bootstrap
import 'bootstrap';

// FontAwesome
import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'

// Bootstrap table
import 'bootstrap-table'

// Select2
import 'select2';
import 'select2/dist/css/select2.css'
import 'select2-bootstrap4-theme/dist/select2-bootstrap4.css'

// Moment.js
import 'moment'

// Chart.js
import 'chart.js'

// Project
import '../sass/app.scss'
import './forms'
import * as Charts from './charts';
import * as Utils from './utils';

window.App = {
	Charts,
	Utils
};
