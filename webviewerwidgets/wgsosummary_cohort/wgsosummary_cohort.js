widgetGenerators['sosummary_cohort'] = {
    'cohort': {
        'name': 'Sequence Ontology by Cohort',
        'width': 880,
        'height': 280,
        'callserver': true,
        'variables': {},
        'init': function (data) {
            this['variables']['data'] = data;
        },
        'function': function (div, data) {
            var colorPalette = {
                'Frameshift insertion': '#2166AC',
                'Frameshift deletion': '#4393C3',
                'Stopgain': '#92C5DE',
                'Stoploss': '#D1E5F0',
                'Missense': '#B2182B',
                'Inframe insertion': '#FDDBC7',
                'Inframe deletion': '#F4A582',
                'Splice site': '#5AAE61',
                'frameshift_elongation': '#2138ac',
                'frameshift_truncation': '#2166AC',
                'stop_gained': '#4393C3',
                'stop_lost': '#92C5DE',
                'missense_variant': '#B2182B',
                'inframe_insertion': '#5AAE61',
                'inframe_deletion': '#ACD39E',
                'splice_site_variant': '#D1E5F0',
                'lof': '#92C5DE',
                'missense': '#B2182B',
                'indel': '#5AAE61'
            };

            div.style.overflow = "hidden"
            var chartDiv = getEl('canvas');
            chartDiv.style.width = '800px';
            chartDiv.style.height = '300px';
            addEl(div, chartDiv);

            const titles = { "so_percent": "Percentage of Variants", "so_counts": "Number of Variants" }

            function handleToggle(measure) {
                var newData = []
                if (document.getElementById("mySelect").value == "0") {
                    for (var j = 0; j < initDatasets.length; j++) {
                        if (initDatasets[j]['measure'] == measure) {
                            newData.push(initDatasets[j])
                        }
                    }
                } else {
                    for (var j = 0; j < nextDatasets.length; j++) {
                        if (nextDatasets[j]['group'] == document.getElementById("mySelect").value) {
                            if (nextDatasets[j]['measure'] == measure) {
                                newData.push(nextDatasets[j])
                            }
                        }
                    }
                }
                chart.options.scales.xAxes[0].scaleLabel.labelString = titles[measure]
                chart.data.datasets = newData
                chart.update()
            }

            $(document.getElementById("widgetcontentdiv_sosummary_cohort_cohort")).ready(function () {
                $(button).change(function () {
                    if (percRadio.checked) {
                        handleToggle(percRadio.value);
                    } else if (countRadio.checked) {
                        handleToggle(countRadio.value);
                    }

                });
            });
            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.marginRight = "106px"
            container.style.bottom = "45%"
            var radioDiv = getEl("div")
            radioDiv.className = "cohorts-radio"
            var button = document.createElement('select');
            button.id = "mySelect"
            button.style.marginBottom = "4px"
            var option = document.createElement('option')
            option.innerHTML = "Select Sequence Ontology "
            option.value = "0"
            var option1 = document.createElement('option')
            option1.innerHTML = "Missense"
            option1.value = "missense"
            var option2 = document.createElement('option')
            option2.innerHTML = "Loss of Function"
            option2.value = "lof"
            var option3 = document.createElement('option')
            option3.value = "indel"
            option3.innerHTML = "Indel"
            addEl(button, option)
            addEl(button, option1)
            addEl(button, option2)
            addEl(button, option3)
            var span = getEl("span")
            span.innerHTML = "View data by: "
            var percLabel = document.createElement('label')
            percLabel.innerHTML = "Percentage"
            percLabel.htmlFor = "so_percent"
            var countLabel = document.createElement('label')
            countLabel.innerHTML = "Count"
            var percRadio = document.createElement('input')
            percRadio.id = "so_percent"
            percRadio.type = "radio"
            percRadio.value = "so_percent"
            percRadio.checked = true
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "so_counts"
            countRadio.id = "so_counts"
            addEl(radioDiv, button)
            addEl(radioDiv, span)
            addEl(radioDiv, percRadio)
            addEl(radioDiv, percLabel)
            addEl(radioDiv, countRadio)
            addEl(radioDiv, countLabel)
            addEl(container, radioDiv)
            addEl(div, container)


            function handleClick() {
                if (this.value == "so_counts") {
                    document.getElementById("so_percent").checked = false
                } else if (this.value == "so_percent") {
                    document.getElementById("so_counts").checked = false
                }
                handleToggle(this.value)
            }
            document.getElementById("so_percent").addEventListener("click", handleClick);
            document.getElementById("so_counts").addEventListener("click", handleClick);

            var data = this['variables']['data'];
            var sos = ["lof", "missense", "indel"]
            var sos2 = data['sos']
            var selectedCohorts = getSelectedCohorts()
            var firstDatasets = [];
            var initDatasets = [];
            var nextDatasets = [];
            const labelDict = {
                'lof': "Loss of Function         ",
                "missense": "Missense",
                "indel": "Indels",
                "missense_variant": "Missense Variant         ",
                "frameshift_elongation": "Frame Shift Elongation",
                "frameshift_truncation": "Frame Shift Truncation",
                "stop_gained": "Stop Gained",
                "stop_lost": "Stop Lost",
                "splice_site_variant": "Splice Site Variant",
                "inframe_insertion": "Inframe Insertion        ",
                "inframe_deletion": "Inframe Deletion          "
            }
            var options = ['so_percent', 'so_counts']
            for (var set in data['socountdata']) {
                var row = data['socountdata'][set];
                for (var cohort in row) {
                    var soData = row[cohort]
                    if (Object.keys(soData).sort().join(',') === selectedCohorts.sort().join(',')) {
                        for (var i = 0; i < sos.length; i++) {
                            var so = sos[i]
                            for (opt in options) {
                                var measure = options[opt]
                                var initDatasetCounts = [];
                                var firstDatasetCounts = [];
                                for (var j in soData) {
                                    var summed = 0
                                    var firstSum = 0
                                    var allData = soData[j][0][so]
                                    for (var val in allData[measure]) {
                                        summed += allData[measure][val]
                                        if (measure == "so_percent") {
                                            firstSum += allData[measure][val]
                                        }
                                    }
                                    initDatasetCounts.push(summed)
                                    firstDatasetCounts.push(firstSum)
                                }
                                var backgroundColor = colorPalette[so]

                                initDatasets.push({
                                    'label': labelDict[so],
                                    'backgroundColor': backgroundColor,
                                    'data': initDatasetCounts,
                                    'labels': selectedCohorts,
                                    'measure': measure
                                });
                                if (measure == "so_percent") {
                                    firstDatasets.push({
                                        'label': labelDict[so],
                                        'backgroundColor': backgroundColor,
                                        'data': firstDatasetCounts,
                                        'labels': selectedCohorts,
                                    })
                                }
                            }
                        }
                        for (var key of Object.keys(sos2)) {
                            for (value in sos2[key]) {
                                var so = sos2[key][value];
                                for (opt in options) {
                                    var measure = options[opt]
                                    var nextDatasetCounts = [];
                                    for (var i in soData) {
                                        var breakdown = soData[i][0][key][measure][so]
                                        nextDatasetCounts.push(breakdown)
                                    }
                                    var backgroundColor = colorPalette[so]
                                    nextDatasets.push({
                                        'label': labelDict[so],
                                        'data': nextDatasetCounts,
                                        'labels': selectedCohorts,
                                        'backgroundColor': backgroundColor,
                                        'group': key,
                                        'measure': measure
                                    });
                                }
                            }
                        }
                    }
                }
            }
            var chart = new Chart(chartDiv, {
                type: 'horizontalBar',
                data: {
                    labels: selectedCohorts,
                    datasets: firstDatasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: true,
                        position: 'right',
                        align: 'center',
                        maxWidth: 100
                    },
                    tooltips: {
                        mode: 'index',
                        callbacks: {
                            label: function (tooltipItem, data) {

                                var percent = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
                                if (data.datasets[0]['measure'] == "so_counts") {
                                    return percent
                                } else {
                                    percent = percent.toFixed(2);
                                    return percent + "%"
                                }
                            }
                        }
                    },
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Percentage of Variants',
                            },
                            ticks: {
                                beginAtZero: true,
                            }
                        }],
                    },
                }
            })
        }
    }
}