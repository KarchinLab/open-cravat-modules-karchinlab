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
            div.style.overflow = "hidden"
            var chartDiv = getEl('canvas');
            chartDiv.style.width = '800px';
            chartDiv.style.height = '500px';
            addEl(div, chartDiv);
            var data = this['variables']['data']['counts']
            var hugos = this['variables']['data']['hugos']
            var selectedCohorts = getSelectedCohorts()
            var cohortsColors = getCohortColors()
            var data_filtered = []
            data.map((elem, index) => {
                if (selectedCohorts.includes(elem.label)) {
                    elem.backgroundColor = cohortsColors[index]
                    data_filtered.push(elem)
                }
            })
            var chart = new Chart(chartDiv, {
                type: 'horizontalBar',
                data: {
                    labels: hugos,
                    datasets: data_filtered
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