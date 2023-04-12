widgetGenerators['topgenessummary_cohort'] = {
    'cohort': {
        'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
        'width': 580,
        'height': 580,
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

            const titles = {"percent": "Percentage of Samples", "counts": "Number of Samples"}

            function leaveChange(scale) {
                var newData = []
                if (document.getElementById("mySelect").value == "0"){
                    for (var j = 0; j < initDatasets.length; j++) {
                        if (initDatasets[j]['scale'] == scale){
                            newData.push(initDatasets[j])
                        }
                    }
                }else{
                    for (var j = 0; j < nextDatasets.length; j++) {
                        if (nextDatasets[j]['group'] == document.getElementById("mySelect").value){
                            if (nextDatasets[j]['scale'] == scale){
                                newData.push(nextDatasets[j])
                            }
                        }
                    }
                }
                chart.options.scales.xAxes[0].scaleLabel.labelString = titles[scale]
                chart.data.datasets = newData
                chart.update()
            }
            var span = getEl("span")
            span.innerHTML = "View data by: "
            span.style.position = "relative"
            span.style.bottom = "400px"
            span.style.left = "430px"
            var label = document.createElement('label')
            label.innerHTML = "Percentage"
            var label2 = document.createElement('label')
            label2.innerHTML = "Count"
            var radio = document.createElement('input')
            radio.id = "percent"
            radio.type = "radio"
            radio.value = "percent"
            radio.checked = true
            radio.style.position = "relative"
            radio.style.left = "310px"
            radio.style.bottom = "378px"
            label.style.position = "relative"
            label.style.left = "380px"
            label.style.bottom = "380px"
            addEl(label, radio)
            var radio2 = document.createElement('input')
            radio2.type = "radio"
            radio2.value = "counts"
            radio2.id = "counts"
            radio2.style.position = "relative"
            radio2.style.left = "297px"
            radio2.style.bottom = "358px"
            label2.style.position = "relative"
            label2.style.left = "300px"
            label2.style.bottom = "360px"
            addEl(label2, radio2)
            

            function clicked (){
                if (this.value == "counts"){
                    document.getElementById("percent").checked = false
                }else if (this.value == "percent"){
                    document.getElementById("counts").checked = false
                }
                    leaveChange(this.value)
            }
            document.getElementById("widgetcontentdiv_topgenessummary_cohort_cohort").appendChild(span);
            document.getElementById("widgetcontentdiv_topgenessummary_cohort_cohort").appendChild(label);
            document.getElementById("widgetcontentdiv_topgenessummary_cohort_cohort").appendChild(radio);
            document.getElementById("widgetcontentdiv_topgenessummary_cohort_cohort").appendChild(radio2);
            document.getElementById("percent").addEventListener("click", clicked);
            document.getElementById("counts").addEventListener("click", clicked);
            document.getElementById("widgetcontentdiv_topgenessummary_cohort_cohort").appendChild(label2);


            var initDatasets = [];
            var data = this['variables']['data']['counts'];
            var initDatasets = [];
            var firstDatasets = [];
            var labels = [];
            let index = 0;
            var selectedCohorts = getSelectedCohorts()
            var scales = ['percent', 'counts']
            for (var set in data) {
                var row = data[set][0];
                
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
                    for (var cohort in row) {
                        var initSamples = [];
                        index = index + 1
                        for (var s in scales){
                            var scale = scales[s]
                            var initDatasetCounts = [];
                            var firstDatasetCounts = [];
                            var labels = []
                            var totalData = row[cohort][scale]
                            for (var values in totalData){
                               labels.push(this['variables']['data']['hugos'][values])
                            }
                            var backgroundColor = colorPalette[index]
                            initDatasets.push({
                                'label': cohort,
                                'backgroundColor': backgroundColor,
                                'data': totalData,
                                'labels': labels,
                                'scale': scale
                            })
                            if (scale == "percent"){
                                firstDatasets.push({
                                    'label': cohort,
                                    'backgroundColor': backgroundColor,
                                    'data': totalData,
                                    'labels': labels,
                                    'scale': scale
                                })

                            }
                        }
                        
                    //     for (var i in row[cohort]) {
                    //         console.log(row[cohort][i])
                    //         // initDatasetCounts.push(row[cohort][i][1].toFixed(2));
                    //         if (!(row[cohort][i][0] in initSamples)) {
                    //             initSamples.push(row[cohort][i][0])
                    //         } else {
                    //             continue
                    //         }
                    //     }
                    // }
                        // var backgroundColor = colorPalette[index];
                        // initDatasets.push({
                        //     'label': cohort,
                        //     'backgroundColor': backgroundColor,
                        //     'data': initDatasetCounts,
                        // });
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