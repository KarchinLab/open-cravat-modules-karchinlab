widgetGenerators['clinvar_cohort'] = {
    'cohort': {
        'width': 420,
        'height': 780,
        'callserver': true,
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

        'function': function (div, dummy) {
            var colorPalette = {
                '0': '#ACD39E',
                '1': '#5AAE61',
                '2': '#92C5DE',
                '3': '#D1E5F0',
                '4': '#F7F7F7',
                '5': '#FDDBC7',
                '6': '#F4A582',
                // '#D6604D',
                // '#B2182B',
                // '#762A83',
                // '#9970AB',
                // '#C2A5CF',
            }

            // Set up for % vs # toggling
            div.style.overflowX = "hidden"
            div.style.overflowY = "auto"
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
            percRadio.id = "clinvar_percent"
            percRadio.type = "radio"
            percRadio.value = "clinvar_percent"
            percRadio.checked = true
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "clinvar_counts"
            countRadio.id = "clinvar_counts"
            addEl(radioDiv, span)
            addEl(radioDiv, percRadio)
            addEl(radioDiv, percLabel)
            addEl(radioDiv, countRadio)
            addEl(radioDiv, countLabel)
            addEl(container, radioDiv)
            addEl(div, container)

            document.getElementById("clinvar_percent").addEventListener("click", handleClick);
            document.getElementById("clinvar_counts").addEventListener("click", handleClick);

            function handleClick() {
                if (this.value == "clinvar_counts") {
                    document.getElementById("clinvar_percent").checked = false
                } else if (this.value == "clinvar_percent") {
                    document.getElementById("clinvar_counts").checked = false
                }
                handleToggle(this.value)
            }
            // Mapping data
            var response = this['variables']['data']['response'];
            var sigs = this['variables']['data']['sig']
            var selectedCohorts = getSelectedCohorts()
            var colorIndex = []
            for (var color in selectedCohorts) {
                colorIndex.push(colorPalette[color])
            }
            var allDatasets = [];
            var initDatasets = [];
            var legendDiv = getEl("div")
            legendDiv.style.position = "sticky"
            legendDiv.style.top = "60px";
            legendDiv.style.height = "10px"
            addEl(div, legendDiv)
            let index = 0;
            var options = ['clinvar_percent', 'clinvar_counts']
            for (var set in response) {
                var row = response[set];
                for (var cohort in row) {
                    var data = row[cohort]
                    if (Object.keys(data).sort().join(',') === selectedCohorts.sort().join(',')) {
                        for (var i = 0; i < sigs.length; i++) {
                            index = index + 1
                            div.setAttribute("id", "clinvar_cohort")
                            var chartDiv = getEl('canvas');
                            chartDiv.setAttribute("id", "clinvar_cohort_" + i)
                            addEl(div, chartDiv);
                            addEl(div, getEl("br"))
                            var sig = sigs[i]
                            var initDatasets = [];
                            var firstDatasets = []
                            for (opt in options) {
                                var measure = options[opt]
                                var dataArray = []
                                for (var j in data) {
                                    var sigData = data[j][measure]
                                    var totalData = sigData[sig]
                                    dataArray.push(totalData)
                                }
                                initDatasets.push({
                                    'label': sig,
                                    'backgroundColor': colorIndex,
                                    'data': dataArray,
                                    'labels': selectedCohorts,
                                    'measure': measure
                                })
                                if (measure == "clinvar_percent") {
                                    firstDatasets.push({
                                        'label': sig,
                                        'backgroundColor': colorIndex,
                                        'data': dataArray,
                                        'labels': selectedCohorts,
                                        'measure': measure
                                    })
                                }
                            }
                            allDatasets.push(initDatasets)
                            // For the significance labels on each chart
                            Chart.pluginService.register({
                                beforeDraw: function (chart) {
                                    var width = chart.chart.width
                                    height = chart.chart.height
                                    ctx = chart.chart.ctx
                                    ctx.restore()
                                    var fontSize = (height / 150).toFixed(2);
                                    ctx.font = fontSize + "em sans-serif";
                                    ctx.textAlign = "left";
                                    ctx.textBaseline = "middle";
                                    var text = [];
                                    const label = chart.config.options.title.text
                                    text.push(Array.isArray(label) ? label.join('<br>') : label);
                                    text.push('</li>');
                                    var text = chart.config.options.title.text
                                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                                        textY = height / 2;
                                    var lines = text.split(' ');
                                    for (var i = 0; i < lines.length; i++) {
                                        ctx.fillText(lines[i], 4, 18 + (i * 20));
                                    }
                                    ctx.save();
                                }
                            });

                            var chart = new Chart(chartDiv, {
                                type: 'doughnut',
                                data: {
                                    labels: selectedCohorts,
                                    datasets: firstDatasets
                                },
                                options: {
                                    responsive: false,
                                    maintainAspectRatio: false,
                                    legend: {
                                        display: false,
                                    },
                                    title: {
                                        text: "  " + sig
                                    },
                                    tooltips: {
                                        mode: 'index',
                                        callbacks: {
                                            label: function (tooltipItem, data) {

                                                var percent = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]

                                                if (data.datasets[0]['measure'] == "clinvar_counts") {
                                                    return percent
                                                } else {
                                                    percent = percent.toFixed(2);
                                                    return percent + "%"
                                                }
                                            }
                                        }
                                    },
                                },
                            });
                        }
                    }
                }
                const titles = { "clinvar_percent": "Percentage of Samples", "clinvar_counts": "Number of Samples" }

                function handleToggle(measure) {
                    var count = 0
                    var newData = {}
                        for (var j = 0; j < allDatasets.length; j++) {
                            newData[j] = []
                            for (var k = 0; k < allDatasets[j].length; k++) {
                                if (allDatasets[j][k]['measure'] == measure) {
                                    newData[j].push(allDatasets[j][k])
                                }
                            }
                        }
                        document.querySelectorAll('canvas').forEach((chartItem, index) => {
                            var canvasID = Chart.instances[index].canvas.id
                            if (canvasID.includes("clinvar")) {
                                var newIndex = index - index + count
                                count = count + 1
                                var chart = Chart.instances[index]
                                chart.data.datasets = newData[newIndex]
                                chart.update()
                            }
                        })
                    }
                }

            // Custom legend
            var ul = getEl("ul")
            ul.innerHTML = chart.generateLegend();
            ul.style.position = "relative"
            ul.style.left = "220px"
            ul.style.top = "20px"
            addEl(legendDiv, ul)
            var legendDict = {}
            var legendItems = ul.getElementsByTagName('li')
            var uld = ul.getElementsByTagName("ul")[0]
            uld.style.listStyleType = "none";
            for (var i = 0; i < legendItems.length; i++) {
                legendItems[i].addEventListener("click", legendClickCallback.bind(this, i), false);
                legendDict[i] = false
                legendItems[i].style.display = "flex"
                legendItems[i].style.margin = "4px"
                var spans = legendItems[i].getElementsByTagName("span")[0]
                spans.style.display = "inline-flex";
                spans.style.width = "45px";
                spans.style.height = "13px";
                spans.style.border = "1px solid lightgray"
                spans.style.marginRight = "6px"
            }
            function legendClickCallback(legendItemIndex) {
                var count2 = 0
                if (legendDict[legendItemIndex] === false) {
                    legendDict[legendItemIndex] = true
                    legendItems[legendItemIndex].style.textDecoration = "line-through"
                }
                else if (legendDict[legendItemIndex] === true) {
                    legendDict[legendItemIndex] = false
                    legendItems[legendItemIndex].style.textDecoration = "none"
                }
                document.querySelectorAll('canvas').forEach((chartItem, index) => {
                    if (document.getElementById("clinvar_percent").checked === true) {
                        var measure = "clinvar_percent"
                    } else {
                        var measure = "clinvar_counts"
                    }
                    var canvasID = Chart.instances[index].canvas.id
                    if (canvasID.includes("clinvar_cohort")) {
                        var newIndex = index - index + count2
                        count2 = count2 + 1
                        var newData = []
                        var newLabels = []
                        var newBg = []
                        var chart = Chart.instances[index]
                        for (var i = 0; i < allDatasets[newIndex].length; i++) {
                            var m = allDatasets[newIndex][i]["measure"]
                            if (m === measure) {
                                var dataItem = allDatasets[newIndex][i]['data']
                            }
                            else {
                                continue;
                            }
                        }
                        var bg = colorIndex
                        for (var j in dataItem) {
                            if (legendDict[j] !== true) {
                                newData.push(dataItem[j])
                                newLabels.push(selectedCohorts[j])
                                newBg.push(bg[j])
                            }
                        }
                        chart.data.datasets[0].data = newData
                        chart.data.datasets[0].labels = newLabels
                        chart.data.datasets[0].backgroundColor = newBg
                        chart.tooltip._data.labels = newLabels
                        chart.update()
                    }
                })
            }
        }
    }
};