require("bootstrap-webpack")

require("./csrftoken");

var amyshit = require("./ajaxmyshit.js");

var Chart = require('chart.js/src/chart.js');

$(document).ready(function() {
    "use strict";

    var bchartelem = $("#balanceChart");

    var data = {
        labels: [
            "Negative",
            "Positive"
        ],
        datasets: [
            {
                data: [
                    bchartelem.data("negative"),
                    bchartelem.data("positive")
                ],
                backgroundColor: [
                    "red",
                    "green"
                ]
            }]
    };

    var balanceChart = new Chart(bchartelem, {
        type: "doughnut",
        data: data
    });


});
