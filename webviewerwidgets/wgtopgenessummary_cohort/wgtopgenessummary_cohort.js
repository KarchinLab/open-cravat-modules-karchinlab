widgetGenerators['topgenessummary_cohort'] = {
    'cohort': {
        'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
        'width': 580,
        'height': 580,
        'callserver': true,
        'default_hidden': true,
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
            div.style.overflow = "hidden"
            var chartDiv = getEl('canvas');
            chartDiv.style.width = '800px';
            chartDiv.style.height = '500px';
            addEl(div, chartDiv);
            var data = this['variables']['data']['counts'];
            var selectedCohorts = getSelectedCohorts()
            var cohortColors = getCohortColors()
            var data_filtered = []
            data.map((elem, index) => {
                elem.backgroundColor = cohortColors[index]
                if (selectedCohorts.includes(elem.label)) {
                    data_filtered.push(elem)
                }
            })
            var extracted_hugos = this['variables']['data']['hugos']

            const titles = {
                "topgene_percent": "Percentage of Samples",
                "topgene_counts": "Number of Samples"
            }

            function handleToggle(measure) {
                var newData = []
                if (measure === "topgene_counts") {
                    data_filtered.map(elem => {
                        delete elem.data;
                        elem.data = elem.count_data;
                        newData.push(elem)
                    })
                } else {
                    data_filtered.map(elem => {
                        delete elem.data;
                        elem.data = elem.perc_data;
                        newData.push(elem)
                    })
                }
                chart.data.datasets = newData
                chart.options.scales.xAxes[0].scaleLabel.labelString = titles[measure]
                chart.update()
            }

            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.left = "239px"
            container.style.justifyContent = "center"
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
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "topgene_counts"
            countRadio.id = "topgene_counts"
            countRadio.checked = true
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

            var chart = new Chart(chartDiv, {
                type: 'horizontalBar',
                data: {
                    labels: extracted_hugos,
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
                                labelString: 'Number of Samples',
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