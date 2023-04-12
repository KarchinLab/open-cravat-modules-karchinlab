widgetGenerators['sosummary_cohort'] = {
    'cohort': {
        'name': 'Sequence Ontology by Cohort',
        'width': 880,
        'height': 380,
        'callserver': true,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'function': function(div, data) {
            var colorPalette = {
                'Frameshift insertion': '#2166AC',
                'Frameshift deletion': '#4393C3',
                'Stopgain': '#92C5DE',
                'Stoploss': '#D1E5F0',
                'Missense': '#E7D4E8',
                'Inframe insertion': '#FDDBC7',
                'Inframe deletion': '#F4A582',
                'Splice site': '#5AAE61',
                '2k upstream': '#D6604D',
                '2k downstream': '#B2182B',
                '3\' UTR': '#762A83',
                '5\' UTR': '#9970AB',
                'Complex substitution': '#C2A5CF',
                'Synonymous': '#E7D4E8',
                'Intron': '#D9F0D3',
                'Unknown': '#ACD39E',
                'Intergenic': '#ACD39E',
                'frameshift_elongation': '#2138ac',
                'frameshift_truncation': '#2166AC',
                'stop_gained': '#4393C3',
                'stop_lost': '#92C5DE',
                'missense_variant': '#C2A5CF',
                'inframe_insertion': '#5AAE61',
                'inframe_deletion': '#ACD39E',
                'splice_site_variant': '#D1E5F0',
                '2kb_upstream_variant': '#D6604D',
                '2kb_downstream_variant': '#B2182B',
                '3_prime_UTR_variant': '#762A83',
                '5_prime_UTR_variant': '#9970AB',
                'complex_substitution': '#C2A5CF',
                'synonymous_variant': '#E7D4E8',
                'intron_variant': '#D9F0D3',
                'Unknown': '#ACD39E',
                'lof': '#92C5DE',
                'missense': '#C2A5CF',
                'indel': '#5AAE61'
            };

            // div.style.width = 'calc(100% - 37px)';
            var chartDiv = getEl('canvas');
            chartDiv.style.width = '800px';
            chartDiv.style.height = '300px';
            addEl(div, chartDiv);

            const titles = {"percent": "Percentage of Variants", "counts": "Number of Variants"}

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
            var button = document.createElement('select');
            button.id = "mySelect"
            button.innerHTML = "Select Group";
            button.style.position = "relative"
            button.style.bottom = "200px"
            button.style.left = "690px"
            button.style.width = "150px"
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
            document.getElementById("widgetcontentdiv_sosummary_cohort_cohort").appendChild(button);
            $(document.getElementById("widgetcontentdiv_sosummary_cohort_cohort")).ready(function(){
                $(button).change(function(){
                    if (radio.checked){
                        leaveChange(radio.value);
                    }else if (radio2.checked){
                        leaveChange(radio2.value);
                    }
                    
                });
            });
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
            radio.style.left = "460px"
            radio.style.bottom = "19px"
            label.style.position = "relative"
            label.style.left = "530px"
            label.style.bottom = "22px"
            addEl(label, radio)
            var radio2 = document.createElement('input')
            radio2.type = "radio"
            radio2.value = "counts"
            radio2.id = "counts"
            radio2.style.position = "relative"
            radio2.style.left = "550px"
            radio2.style.bottom = "19px"
            label2.style.position = "relative"
            label2.style.left = "555px"
            label2.style.bottom = "22px"
            addEl(label2, radio2)
            

            function clicked (){
                if (this.value == "counts"){
                    document.getElementById("percent").checked = false
                }else if (this.value == "percent"){
                    document.getElementById("counts").checked = false
                }
                    leaveChange(this.value)
            }
            document.getElementById("widgetcontentdiv_sosummary_cohort_cohort").appendChild(label);
            document.getElementById("widgetcontentdiv_sosummary_cohort_cohort").appendChild(radio);
            document.getElementById("widgetcontentdiv_sosummary_cohort_cohort").appendChild(radio2);
            document.getElementById("percent").addEventListener("click", clicked);
            document.getElementById("counts").addEventListener("click", clicked);
            document.getElementById("widgetcontentdiv_sosummary_cohort_cohort").appendChild(label2);
 
            var data = this['variables']['data'];
            var sos = ["lof", "missense", "indel"]
            var sos2 = data['sos']
            var selectedCohorts = getSelectedCohorts()
            var firstDatasets = [];
            var initDatasets = [];
            var nextDatasets = [];
            const labelDict = {'lof': "Loss of Function         ",
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
            var scales = ['percent', 'counts']
            for (var set in data['socountdata']) {
                var row = data['socountdata'][set];
                for (var cohort in row) {
                    if (Object.keys(row[cohort]).sort().join(',') === selectedCohorts.sort().join(',')) {
                        for (var j = 0; j < sos.length; j++) {
                            
                            var so = sos[j]
                            for (s in scales){
                                var initDatasetCounts = [];
                                var firstDatasetCounts = [];
                            for (var i in row[cohort]) {
                                var summed = 0
                                var firstSum = 0
                                    for ( var c in row[cohort][i][0][so][scales[s]]){
                                        summed += row[cohort][i][0][so][scales[s]][c]
                                        if (scales[s] == "percent"){
                                            firstSum += row[cohort][i][0][so][scales[s]][c]
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
                                'scale': scales[s]
                            });
                            if (scales[s] == "percent"){
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
                            for (value in sos2[key]){
                                var so = sos2[key][value];
                            
                            for (s in scales){
                                var nextDatasetCounts = [];
                            for (var i in row[cohort]) {
                                nextDatasetCounts.push(row[cohort][i][0][key][scales[s]][so])
                            }
                            var backgroundColor = colorPalette[so]
                            nextDatasets.push({
                                'label': labelDict[so],
                                'data': nextDatasetCounts,
                                'labels': selectedCohorts,
                                'backgroundColor': backgroundColor,
                                'group': key,
                                'scale': scales[s]
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
                        // minWidth: 5,
                        maxWidth: 100
                    },
                    tooltips: {
                        mode: 'index',
                      callbacks: {
                        label: function(tooltipItem, data) {
                        
                          var percent = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
                          if (data.datasets[0]['scale']== "counts"){
                            return percent
                          }else{
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
                                // tickWidth: "25px",
                                // stepSize: 5,
                                // max: 100,
                                // color: "red"
                            }
                        }],
                    },
                }
            })
            console.log(chart)

        }
    }
}