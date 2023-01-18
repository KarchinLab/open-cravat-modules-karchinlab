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
            var selectedCohorts = getSelectedCohorts()
            for (var set in data) {
                var row = data[set][0];
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
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
                        });
                    }
                }
            }

            var chart = new Chart(chartDiv, {
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
            });
        }
    }
};