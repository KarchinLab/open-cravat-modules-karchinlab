widgetGenerators['clinvar_cohort'] = {
    'cohort': {
        'width': 800,
        'height': 780,
        'top': 400,
        'left': 200,
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

        'function': function(div, dummy) {
            div.style.overflowX = "hidden"
            div.style.overflowY = "auto"
            div.style.display = "flex"
            div.style.flexDirection = "column"
            div.style.alignItems = "center"
            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.marginLeft = "474px"
            container.style.top = "676px"
            container.style.position = "sticky"
            container.style.height = "35px"
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
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "clinvar_counts"
            countRadio.id = "clinvar_counts"
            countRadio.checked = true
            addEl(radioDiv, span)
            addEl(radioDiv, percRadio)
            addEl(radioDiv, percLabel)
            addEl(radioDiv, countRadio)
            addEl(radioDiv, countLabel)
            addEl(container, radioDiv)
            addEl(div, container)

            document.getElementById("clinvar_percent").addEventListener("click", handleClick);
            document.getElementById("clinvar_counts").addEventListener("click", handleClick);

            let numberofdeleted = new Set();

            function handleClick() {
                if (this.value == "clinvar_counts") {
                    document.getElementById("clinvar_percent").checked = false
                } else if (this.value == "clinvar_percent") {
                    document.getElementById("clinvar_counts").checked = false
                }
                handleToggle(this.value)
            }

            const removeFromArray = function(array1, removed) {
                var filtered = array1.filter(function(value, index, array) {
                    return !removed.includes(index);
                });
                return filtered;
            }

            const keepFromArray = function(array1, removed) {
                var filtered = array1.filter(function(value, index, array) {
                    return removed.includes(index);
                });
                return filtered;
            }

            function handleToggle(measure) {
                var deletedArray = Array.from(numberofdeleted)
                var count = 0
                var newData = []
                all_filtered_data.map((elem, index) => {
                    var newElem = {
                        ...elem
                    }
                    delete newElem.data;
                    newElem.data = removeFromArray(measure === "clinvar_counts" ? newElem.count_data : newElem.perc_data, deletedArray)
                    newElem.labels = removeFromArray(newElem.labels, deletedArray)
                    newElem.backgroundColor = removeFromArray(newElem.backgroundColor, deletedArray)
                    newData.push(newElem)
                })
                document.querySelectorAll('canvas').forEach((chartItem, index) => {
                    var canvasID = Chart.instances[index].canvas.id
                    if (canvasID.includes("clinvar_cohort")) {
                        var chart = Chart.instances[index]
                        chart.data.datasets = [newData[count]]
                        chart.update()
                        count = count + 1
                    }
                })
            }

            // Mapping data
            var data = this['variables']['data'];
            var selectedCohorts = getSelectedCohorts()
            var cohortsColors = getCohortColors()
            var legendDiv = getEl("div")
            legendDiv.style.position = "sticky"
            legendDiv.style.top = "60px";
            legendDiv.style.height = "10px"
            addEl(div, legendDiv)
            var indexes = []
            var all_filtered_data = []
            var all_cohorts = data[0].labels
            for (var cohort in selectedCohorts) {
                indexes.push(all_cohorts.indexOf(selectedCohorts[cohort]))
            }
            for (var set in data) {
                const extraDiv = getEl("div")
                extraDiv.classList = "clinvar-cohort-chart"
                var measure = document.getElementById("clinvar_percent").checked
                var filtered_data = {
                    ...data[set]
                }
                filtered_data.backgroundColor = cohortsColors
                filtered_data.data = keepFromArray(measure ? data[set].perc_data : data[set].count_data, indexes)
                filtered_data.labels = keepFromArray(data[set].labels, indexes)
                filtered_data.count_data = keepFromArray(data[set].count_data, indexes)
                filtered_data.perc_data = keepFromArray(data[set].perc_data, indexes)
                filtered_data.backgroundColor = keepFromArray(cohortsColors, indexes)
                all_filtered_data.push(filtered_data)
                div.setAttribute("id", "clinvar_cohort")
                var chartDiv = getEl('canvas')
                chartDiv.setAttribute("id", "clinvar_cohort_" + set)
                var span = getEl("span")
                span.innerHTML = filtered_data.label
                addEl(extraDiv, span)
                addEl(extraDiv, chartDiv);
                addEl(div, extraDiv)
                addEl(div, getEl("br"))
                var chart = new Chart(chartDiv, {
                    type: 'doughnut',
                    data: {
                        labels: selectedCohorts,
                        datasets: [filtered_data],
                    },
                    options: {
                        responsive: false,
                        maintainAspectRatio: false,
                        legend: {
                            display: false,
                        },
                        title: {
                            text: filtered_data.label,
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
                    },
                });
            }

            // Custom legend
            var ul = getEl("ul")
            ul.innerHTML = chart.generateLegend();
            ul.style.position = "relative"
            ul.style.left = "240px"
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
                var my_new_data = []
                if (numberofdeleted.has(legendItemIndex)) {
                    numberofdeleted.delete(legendItemIndex)
                } else {
                    numberofdeleted.add(legendItemIndex)
                }

                var deletedArray = Array.from(numberofdeleted)
                all_filtered_data.map(elem => {
                    var newElem = {
                        ...elem
                    }
                    var measure = document.getElementById("clinvar_percent").checked
                    newElem.data = removeFromArray(measure ? newElem.perc_data : newElem.count_data, deletedArray)
                    newElem.perc_data = removeFromArray(newElem.perc_data, deletedArray)
                    newElem.count_data = removeFromArray(newElem.count_data, deletedArray)
                    newElem.labels = removeFromArray(newElem.labels, deletedArray)
                    newElem.backgroundColor = removeFromArray(newElem.backgroundColor, deletedArray)
                    my_new_data.push(newElem)
                })
                if (legendDict[legendItemIndex] === false) {
                    legendDict[legendItemIndex] = true
                    legendItems[legendItemIndex].style.textDecoration = "line-through"
                } else if (legendDict[legendItemIndex] === true) {
                    legendDict[legendItemIndex] = false
                    legendItems[legendItemIndex].style.textDecoration = "none"
                }
                document.querySelectorAll('canvas').forEach((chartItem, index) => {
                    var canvasID = Chart.instances[index].canvas.id
                    if (canvasID.includes("clinvar_cohort")) {
                        var chart = Chart.instances[index]
                        chart.data.datasets = [my_new_data[count2]]
                        chart.update()
                        count2 = count2 + 1
                    }
                })
            }
        }
    }
};