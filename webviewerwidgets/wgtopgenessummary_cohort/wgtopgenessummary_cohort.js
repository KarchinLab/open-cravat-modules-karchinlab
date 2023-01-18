widgetGenerators['topgenessummary_cohort'] = {
    'cohort': {
        'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
        'width': 780,
        'height': 780,
        'callserver': true,
        'default_hidden': false,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'shoulddraw': function() {
            if (this['variables']['data'].length == 0 || this['variables']['data'] == null || infomgr.datas.variant.length > 3000) {
                return false;
            } else {
                return true;
            }
        },
        'function': function(div, data) {
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
                            initDatasetCounts.push(row[cohort][i][1].toFixed(2));
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
                                labelString: 'Percentage of Samples',
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
}