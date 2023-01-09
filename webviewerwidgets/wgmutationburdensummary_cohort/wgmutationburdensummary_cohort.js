widgetGenerators['mutationburdensummary_cohort'] = {
    'cohort': {
        'width': 720,
        'height': 670,
        'callserver': true,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },

        'function': function(div, dummy) {
            if (div != null) {
                emptyElement(div);
            }

            function createButton(range) {
                if (range.length < 2) {
                    return null;
                } else {
                    for (var i = 0; i < range.length; i++) {
                        var button = document.createElement('button');
                        button.id = range[i] + "_burden";
                        button.innerHTML = "Group" + range[i];
                        button.classList.add("butn");
                        button.style.position = "relative"
                        button.style.bottom = "25px"
                        document.getElementById("widgetcontentdiv_mutationburdensummary_cohort_cohort").appendChild(button);
                    }
                }
            }

            function plotData(range, id) {
                var forecast_chart = new Chart(chartDiv, chart);
                forecast_chart.width = "700px"
                var chartdata = forecast_chart.chart.data;
                var data = initDatasets
                for (var i = 0; i < range.length; i++) {
                    var newdata = []
                    for (var j in data) {
                        if (data[j].group.toString() + "_burden" == id) {
                            newdata.push(data[j])
                        } else if (id == "start") {
                            if (data[j].group.toString() == "1") {
                                newdata.push(data[j])
                            }
                        }

                    }
                    chartdata.datasets = newdata
                    forecast_chart.update();
                }
                var elem = document.getElementById('widgetcontentdiv_mutationburdensummary_cohort_cohort').getElementsByTagName("button")
                for (var i = 0; i < elem.length; i++) {
                    elem[i].onclick = function() {
                        plotData(range, this.id)
                    };
                }
            }

            var colorPalette = {
                '1': '#2166AC',
                '2': '#4393C3',
                '3': '#92C5DE',
                '4': '#D1E5F0',
                '5': '#1B7837',
                '6': '#FDDBC7',
                '7': '#F4A582',
                '8': '#5AAE61',
                '9': '#D6604D',
                '10': '#B2182B',
            }
            div.style.width = 'calc(100% - 37px)';
            var chartDiv = getEl('canvas');
            chartDiv.style.width = 'calc(100% - 20px)';
            chartDiv.style.height = 'calc(100% - 20px)';
            addEl(div, chartDiv);
            var initDatasets = [];
            var data = this['variables']['data'];
            let index = 0;
            var numGroups = []
            for (var set in data) {
                numGroups.push(Number(set))
                var row = data[set][0];
                for (var cohort in row) {
                    var initSamples = [];
                    var initDatasetCounts = [];
                    index = index + 1
                    for (var i in row[cohort]) {
                        initDatasetCounts.push(row[cohort][i][1]);
                        if (!(row[cohort][i][0] in initSamples)) {
                            initSamples.push(row[cohort][i][0])
                        } else {
                            continue
                        }
                    }
                    var backgroundColor = colorPalette[index];
                    initDatasets.push({
                        'label': cohort,
                        'backgroundColor': backgroundColor,
                        'data': initDatasetCounts,
                        'group': set
                    });
                }
            }

            createButton(numGroups)
            var chart = {
                type: 'horizontalBar',
                data: {
                    labels: initSamples,
                    datasets: initDatasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Number of Variants',
                            },
                            ticks: {
                                beginAtZero: true,
                            }
                        }],
                    },
                }
            };
            plotData(numGroups, 'start')
        }
    }
};