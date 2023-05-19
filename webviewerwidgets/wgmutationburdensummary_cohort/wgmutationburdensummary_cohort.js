widgetGenerators['mutationburdensummary_cohort'] = {
    'cohort': {
        'width': 580,
        'height': 580,
        'callserver': true,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },

        'function': function(div, dummy) {
            var colorPalette = {
                '10': '#2166AC',
                '9': '#4393C3',
                '8': '#92C5DE',
                '7': '#D1E5F0',
                '6': '#1B7837',
                '4': '#FDDBC7',
                '3': '#F4A582',
                '5': '#5AAE61',
                '2': '#D6604D',
                '1': '#B2182B',
            }
            div.style.width = 'calc(100% - 37px)';
            var chartDiv = getEl('canvas');
            chartDiv.style.width = 'calc(100% - 20px)';
            chartDiv.style.height = 'calc(100% - 20px)';
            addEl(div, chartDiv);
            var initDatasets = [];
            var data = this['variables']['data']['counts'];
            var hugos = this['variables']['data']['hugos']
            let index = 0;
            var selectedCohorts = getSelectedCohorts()
            for (var set in data) {
                var row = data[set][0];
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
                    for (var cohort in row) {
                        var counts = row[cohort]
                        var initDatasetCounts = [];
                        index = index + 1
                        for (var i in counts) {
                            for (var val in counts[i]){
                            initDatasetCounts.push(counts[i][val]);
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
                    labels: hugos,
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