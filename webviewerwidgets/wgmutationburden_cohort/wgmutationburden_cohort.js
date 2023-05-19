$.getScript('/result/widgetfile/wgmutationburden_cohort/plotly-2.16.1.min.js', function () { });
widgetGenerators['mutationburden_cohort'] = {
    'cohort': {
        'name': 'Mutation Burden',
        'width': 780,
        'height': 480,
        'callserver': true,
        'default_hidden': false,
        'variables': {},
        'init': function (data) {
            this['variables']['data'] = data;
        },
        'function': function (div, data) {
            var selectedCohorts = getSelectedCohorts()
            selectedCohorts.sort()
            div.style.overflow = "hidden"
            var wrapperDiv = document.createElement('div');
            var chartDiv = document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort");
            const titles = { "mutation_percent": "Percentage of Non-Silent Mutations", "mutation_counts": "Count of Non-Silent Mutations" }
            function handleToggle(measure) {
                var newData = []
                var layout = {
                    title: titles[measure],
                    annotations: [],
                    width: 700,
                    xaxis: {
                        ticks: '',
                        side: 'bottom',
                        autosize: true
                    },
                    yaxis: {
                        ticks: '',
                        ticksuffix: ' ',
                        autosize: true
                    }
                };
                for (var j in allData) {
                    if (allData[j].includes(measure)) {
                        newData.push(allData[j])
                    }
                }
                if (measure == "mutation_percent") {
                    var data = [
                        {
                            z: newData,
                            x: hugos,
                            y: selectedCohorts,
                            type: 'heatmap',
                            hoverongaps: false,
                            text: text,
                            hoverinfo: 'text',
                        }
                    ];
                } else {
                    var data = [
                        {
                            z: newData,
                            x: hugos,
                            y: selectedCohorts,
                            type: 'heatmap',
                            hoverongaps: false,
                        }
                    ];
                }
                var config = { responsive: true }
                Plotly.newPlot(div, data, layout, config);
            }
            function handleClick() {
                if (this.value == "mutation_counts") {
                    document.getElementById("mutation_percent").checked = false
                } else if (this.value == "mutation_percent") {
                    document.getElementById("mutation_counts").checked = false
                }
                handleToggle(this.value)
            }
            var data = this['variables']['data']['countData'];
            var cohorts = this['variables']['data']['cohorts']
            let hugos;
            for (const [key, value] of Object.entries(cohorts)) {
                var selected = value.sort()
                if (JSON.stringify(selected) === JSON.stringify(selectedCohorts)) {
                    hugos = this['variables']['data']['hugos'][key]
                }
            }
            var allData = []
            var firstData = []
            for (var set in data) {
                var row = data[set][0];
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
                    for (var cohort in row) {
                        for (var i in row[cohort]) {
                            var measure = "mutation_" + i
                            var counts = []
                            for (var hugo in hugos) {
                                var count = row[cohort][i][hugos[hugo]]
                                counts.push(count)
                            }
                            counts.push(measure)
                            allData.push(counts);
                            if (i == "percent") {
                                firstData.push(counts)
                            }
                        }
                    }
                }
            }
            var text = firstData.map((row, i) => row.map((item, j) => {
                return `${item + "%"}`
            }))
            var data = [

                {
                    z: firstData,
                    x: hugos,
                    y: selectedCohorts,
                    type: 'heatmap',
                    measure: "percent",
                    colorscale: 'RdBu',
                    text: text,
                    hoverinfo: 'text',
                    

                },

            ];
            var layout = {
                width: 700,
                annotations: [],
                title: "Percentage of Non-Silent Mutations",
                xaxis: {
                    ticks: '',
                    side: 'bottom',
                    autosize: false

                },
                yaxis: {
                    ticks: '',
                    ticksuffix: ' ',
                    autosize: false
                }
            };

            Plotly.newPlot(wrapperDiv, data, layout);
            addEl(chartDiv, wrapperDiv)
            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.width = "767px"
            container.style.marginRight = "auto"
            container.style.bottom = "138px"
            var measureDiv = getEl("div")
            measureDiv.className = "cohorts-radio"
            var span = getEl("span")
            span.innerHTML = "View data by: "
            var label = document.createElement('label')
            label.innerHTML = "Percentage"
            var label2 = document.createElement('label')
            label2.innerHTML = "Count"
            var percRadio = document.createElement('input')
            percRadio.id = "mutation_percent"
            percRadio.type = "radio"
            percRadio.value = "mutation_percent"
            percRadio.checked = true
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "mutation_counts"
            countRadio.id = "mutation_counts"
            addEl(measureDiv, span)
            addEl(measureDiv, percRadio)
            addEl(measureDiv, label)
            addEl(measureDiv, countRadio)
            addEl(measureDiv, label2)
            addEl(container, measureDiv)
            addEl(div, container)
            document.getElementById("mutation_percent").addEventListener("click", handleClick);
            document.getElementById("mutation_counts").addEventListener("click", handleClick);
        }
    }
}