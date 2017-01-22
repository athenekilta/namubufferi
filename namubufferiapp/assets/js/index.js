var bootstrap = require("bootstrap-webpack");
bootstrap.$ = bootstrap.jQuery = jQuery;

require("../css/style.css");

require("./namubufferihome.js");
require("./csrftoken.js");
require("./ajaxmyshit.js");
require("./ux.js");
require("./usertags.js");
require("./namubufferiadmin.js");

require("jQuery-Scanner-Detection/jquery.scannerdetection");

$(document).ready(function() {
    "use strict";

    $(document).scannerDetection();
});
