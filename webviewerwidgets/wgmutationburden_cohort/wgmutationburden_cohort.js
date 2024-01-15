$.getScript('/result/widgetfile/wgmutationburden_cohort/plotly-2.16.1.min.js', function() {});
widgetGenerators['mutationburden_cohort'] = {
    'cohort': {
        'name': 'Mutation Burden',
        'width': 800,
        'height': 480,
        'callserver': true,
        'default_hidden': true,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'function': function(div, data) {
            var selectedCohorts = getSelectedCohorts()
            var cohortColors = getCohortColors()
            selectedCohorts.sort()
            div.style.overflow = "hidden"
            var wrapperDiv = document.createElement('div');
            var chartDiv = document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort");
            const titles = {
                "mutation_percent": "Percentage of Non-Silent Mutations",
                "mutation_counts": "Count of Non-Silent Mutations"
            }

            function handleClick() {
                if (this.value == "mutation_counts") {
                    document.getElementById("mutation_percent").checked = false
                } else if (this.value == "mutation_percent") {
                    document.getElementById("mutation_counts").checked = false
                }
                handleToggle(this.value)
            }
            var gene_data = this['variables']['data']['countData'];
            var hugos = this['variables']['data']['hugos'];
            var all_data = []
            gene_data.map((elem, index) => {
                elem.backgroundColor = cohortColors[index]
                all_data.push(elem.data)
            })

            function handleToggle(measure) {
                var new_data = []
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
                }

                if (measure === "mutation_percent") {
                    gene_data.map(elem => {
                        new_data.push(elem.perc_data)
                    })
                } else {
                    gene_data.map(elem => {
                        new_data.push(elem.count_data)
                    })
                }
                var data = [{
                    z: new_data,
                    x: hugos,
                    y: selectedCohorts,
                    type: 'heatmap',
                    hoverongaps: false,
                    text: text,
                    hoverinfo: 'text',
                }];
                Plotly.newPlot(wrapperDiv, data, layout);
            }

            var text = all_data.map((row, i) => row.map((item, j) => {
                return item
            }))
            var data = [{
                z: all_data,
                x: hugos,
                y: selectedCohorts,
                type: 'heatmap',
                measure: "percent",
                colorscale: 'RdBu',
                text: text,
                hoverinfo: 'text',
            }, ];
            var layout = {
                width: 700,
                annotations: [],
                title: "Number of Non-Silent Mutations",
                xaxis: {
                    ticks: '',
                    side: 'bottom',
                    autosize: false

                },
                yaxis: {
                    ticks: '',
                    ticksuffix: ' ',
                    autosize: false,
                    automargin: true
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
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "mutation_counts"
            countRadio.id = "mutation_counts"
            countRadio.checked = true
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