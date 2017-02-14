require("bootstrap-webpack")

require("./csrftoken");

var amyshit = require("./ajaxmyshit.js");

var Chart = require('chart.js/src/chart.js');

$(document).ready(function() {
    "use strict";


    // Doghnut chart for showing what's
    // the ratio between positive and
    // negative balances
    var balancegraph_elem = $("#balanceChart");

    var data = {
        labels: [
            "Negative",
            "Positive"
        ],
        datasets: [
            {
                data: [
                    balancegraph_elem.data("negative"),
                    balancegraph_elem.data("positive")
                ],
                backgroundColor: [
                    "red",
                    "green"
                ]
            }]
    };

    var balanceChart = new Chart(balancegraph_elem, {
        type: "doughnut",
        data: data
    });


});
