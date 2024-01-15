widgetGenerators['sosummary_cohort'] = {
    'cohort': {
        'name': 'Sequence Ontology by Cohort',
        'width': 800,
        'height': 280,
        'callserver': true,
        'variables': {},
        'default_hidden': true,
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'function': function(div, data) {

            var data = this['variables']['data'];
            var initData = (data['base_data'])
            const hasData = isAllZero()
            if (hasData) {
                var span = getEl('span');
                span.classList.add('cohorts-nodata');
                addEl(div, addEl(span, getTn('No data')));
                return;
            }
            div.style.overflow = "hidden"
            var chartDiv = getEl('canvas');
            chartDiv.style.width = '800px';
            chartDiv.style.height = '450px';
            addEl(div, chartDiv);

            const titles = {
                "so_percent": "Percentage of Variants",
                "so_counts": "Number of Variants"
            }

            var sos_groups = {
                'Loss of Function': ["Frame Shift Elongation", "Frame Shift Truncation", "Stop Gained", "Stop Lost", "Splice Site Variant"],
                'Missense': ["Missense Variant"],
                'Insertion / Deletions': ["Inframe Insertion", "Inframe Deletion"]
            }

            const labelDict = {
                "MIS": "Missense Variant",
                "FSI": "Frame Shift Elongation",
                "FSD": "Frame Shift Truncation",
                "STG": "Stop Gained",
                "STL": "Stop Lost",
                "SPL": "Splice Site Variant",
                "INI": "Inframe Insertion",
                "IND": "Inframe Deletion"
            }

            function handleToggle(measure) {
                let newData = []
                if (document.getElementById("mySelect").value == "0") {

                    for (var j = 0; j < initData.length; j++) {
                        if (measure === "so_counts") {
                            newData = initData
                            newData[j]['data'] = initData[j]['count_data']
                        } else {
                            newData = initData
                            newData[j]['data'] = initData[j]['perc_data']
                        }
                    }
                } else {
                    var selectedVal = document.getElementById("mySelect").value
                    if (measure === "so_counts") {
                        fullData.map(elem => {
                            let label = labelDict[elem.label]
                            if (label === undefined) {
                                label = elem.label
                            }
                            if (sos_groups[selectedVal].includes(label)) {
                                elem.label = label
                                delete elem.data;
                                elem.data = elem.count_data;
                                if (elem.data.every(item => item === 0)) {
                                    var span = getEl('span');
                                    span.classList.add('cohorts-nodata');
                                    addEl(div, addEl(span, getTn('No data')));
                                    return;
                                }
                                newData.push(elem)
                            }
                        })
                    } else {
                        fullData.map(elem => {
                            let label = labelDict[elem.label]
                            if (label === undefined) {
                                label = elem.label
                            }
                            if (sos_groups[selectedVal].includes(label)) {
                                elem.label = label
                                delete elem.data;
                                elem.data = elem.perc_data;
                                if (elem.data.every(item => item === 0)) {
                                    var span = getEl('span');
                                    span.classList.add('cohorts-nodata');
                                    addEl(div, addEl(span, getTn('No data')));
                                    return;
                                }
                                newData.push(elem)
                            }
                        })
                    }
                }
                chart.options.scales.xAxes[0].scaleLabel.labelString = titles[measure]
                chart.data.datasets = newData
                chart.update()
            }

            $(document.getElementById("widgetcontentdiv_sosummary_cohort_cohort")).ready(function() {
                $(button).change(function() {
                    if (percRadio.checked) {
                        handleToggle(percRadio.value);
                    } else if (countRadio.checked) {
                        handleToggle(countRadio.value);
                    }
                })
            })
            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.marginRight = "92px"
            container.style.bottom = "45%"
            var radioDiv = getEl("div")
            radioDiv.className = "cohorts-radio"
            var button = document.createElement('select');
            button.id = "mySelect"
            button.style.marginBottom = "4px"
            var option = document.createElement('option')
            option.innerHTML = "Select"
            option.value = "0"
            var option1 = document.createElement('option')
            option1.innerHTML = "Missense"
            option1.value = "Missense"
            var option2 = document.createElement('option')
            option2.innerHTML = "Loss of Function"
            option2.value = "Loss of Function"
            var option3 = document.createElement('option')
            option3.value = "Insertion / Deletions"
            option3.innerHTML = "Insertion / Deletions"
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
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "so_counts"
            countRadio.id = "so_counts"
            countRadio.checked = true
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

            function isAllZero() {
                let isAllZero = true
                initData.map((elem) => {
                    if (isAllZero) {
                        isAllZero = elem.data.every(item => item === 0)
                    } else {
                        isAllZero = false
                    }
                })
                return isAllZero
            }
            var fullData = data['complete_data']
            var selectedCohorts = getSelectedCohorts()
            var chart = new Chart(chartDiv, {
                type: 'horizontalBar',
                data: {
                    labels: selectedCohorts,
                    datasets: initData
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
                            label: function(tooltipItem, data) {
                                var percent = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
                                if (countRadio.checked) {
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
                                labelString: 'Number of Variants',
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