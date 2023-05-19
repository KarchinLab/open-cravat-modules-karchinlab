widgetGenerators['topgenessummary_cohort'] = {
    'cohort': {
        'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
        'width': 580,
        'height': 580,
        'callserver': true,
        'default_hidden': false,
        'variables': {},
        'init': function (data) {
            this['variables']['data'] = data;
        },
        'shoulddraw': function () {
            if (this['variables']['data'].length == 0 || this['variables']['data'] == null || infomgr.datas.variant.length > 3000) {
                return false;
            } else {
                return true;
            }
        },
        'function': function (div, data) {
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

            const titles = { "topgene_percent": "Percentage of Samples", "topgene_counts": "Number of Samples" }

            function handleToggle(measure) {
                var newData = []
                for (var j = 0; j < initDatasets.length; j++) {
                    if (initDatasets[j]['measure'] == measure) {
                        newData.push(initDatasets[j])
                    }
                }
                chart.options.scales.xAxes[0].scaleLabel.labelString = titles[measure]
                chart.data.datasets = newData
                chart.update()
            }
            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.marginRight = "32px"
            container.style.top = "14px"
            container.style.position = "sticky"
            var radioDiv = getEl("div")
            radioDiv.className = "cohorts-radio"
            var span = getEl("span")
            span.innerHTML = "View data by: "
            var percLabel = document.createElement('label')
            percLabel.innerHTML = "Percentage"
            var countLabel = document.createElement('label')
            countLabel.innerHTML = "Count"
            var percRadio = document.createElement('input')
            percRadio.id = "topgene_percent"
            percRadio.type = "radio"
            percRadio.value = "topgene_percent"
            percRadio.checked = true
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "topgene_counts"
            countRadio.id = "topgene_counts"
            addEl(radioDiv, span)
            addEl(radioDiv, percRadio)
            addEl(radioDiv, percLabel)
            addEl(radioDiv, countRadio)
            addEl(radioDiv, countLabel)
            addEl(container, radioDiv)
            addEl(div, container)


            function handleClick() {
                if (this.value == "topgene_counts") {
                    document.getElementById("topgene_percent").checked = false
                } else if (this.value == "topgene_percent") {
                    document.getElementById("topgene_counts").checked = false
                }
                handleToggle(this.value)
            }

            document.getElementById("topgene_percent").addEventListener("click", handleClick);
            document.getElementById("topgene_counts").addEventListener("click", handleClick);

            var initDatasets = [];
            var data = this['variables']['data']['counts'];
            var initDatasets = [];
            var firstDatasets = [];
            var labels = [];
            let index = 0;
            var selectedCohorts = getSelectedCohorts()
            var options = ['topgene_percent', 'topgene_counts']
            for (var set in data) {
                var row = data[set][0]
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
                    for (var cohort in row) {
                        var counts = row[cohort]
                        index = index + 1
                        for (var opt in options) {
                            var measure = options[opt]
                            var labels = []
                            var totalData = counts[measure]
                            for (var values in totalData) {
                                labels.push(this['variables']['data']['hugos'][values])
                            }
                            var backgroundColor = colorPalette[index]
                            initDatasets.push({
                                'label': cohort,
                                'backgroundColor': backgroundColor,
                                'data': totalData,
                                'labels': labels,
                                'measure': measure
                            })
                            if (measure == "topgene_percent") {
                                firstDatasets.push({
                                    'label': cohort,
                                    'backgroundColor': backgroundColor,
                                    'data': totalData,
                                    'labels': labels,
                                    'measure': measure
                                })
                            }
                        }
                    }
                }
            }
            var chart = new Chart(chartDiv, {
                type: 'horizontalBar',
                data: {
                    labels: labels,
                    datasets: firstDatasets
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