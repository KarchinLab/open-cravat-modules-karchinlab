widgetGenerators['clinvar_cohort'] = {
    'cohort': {
        'width': 420,
        'height': 780,
        'callserver': true,
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
            var colorPalette = {
                '0':'#ACD39E',
				'1':'#5AAE61',
				'2':'#92C5DE',
				'3':'#D1E5F0',
				'4':'#F7F7F7',
				'5':'#FDDBC7',
				'6':'#F4A582',
				// '#D6604D',
				// '#B2182B',
				// '#762A83',
				// '#9970AB',
				// '#C2A5CF',
            }
            var data = this['variables']['data'];
            var sigs = data['sig']
            var selectedCohorts = getSelectedCohorts()
            var colorIndex = []
            for (var color in selectedCohorts){
                colorIndex.push(colorPalette[color])
            }
            var allDatasets = [];
            var initDatasets = [];
            var backgroundColors = [];
            var legendDiv = getEl("div")
            legendDiv.style.position = "sticky"
            legendDiv.style.top = 0;
            legendDiv.style.height = "10px"
            addEl(div, legendDiv)
            for (var set in data['response']) {
                var row = data['response'][set];
                for (var cohort in row) {
                    if (Object.keys(row[cohort]).sort().join(',') === selectedCohorts.sort().join(',')) {
                        for (var i = 0; i < sigs.length; i++){
                            div.setAttribute("id", "clinvar_cohort")
                            var chartDiv = getEl('canvas');
                            chartDiv.style.width = 'calc(100% - 140px)';
                            chartDiv.style.height = 'calc(100% -140px)';
                            chartDiv.setAttribute("id", "clinvar_cohort_" + i)
                            
                            addEl(div, chartDiv);
                            addEl(div, getEl("br"))
                            var sig = sigs[i]
                            var initDatasets = [];
                            var initDatasetCounts = [];
                            for (var j in row[cohort]) {
                                initDatasetCounts.push(row[cohort][j][0][sig])
                            }
                            allDatasets.push(initDatasetCounts)
                            initDatasets.push({
                                'label': sig,
                                'backgroundColor': colorIndex,
                                'data': initDatasetCounts,
                                'labels': selectedCohorts,
                            });
                            Chart.pluginService.register({
                                beforeDraw: function (chart) {
                                    var width = chart.chart.width,
                                        height = chart.chart.height,
                                        ctx = chart.chart.ctx;
                                    ctx.restore();
                                    var fontSize = (height / 170).toFixed(2);
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
                                    for (var i = 0; i<lines.length; i++){
                                        ctx.fillText(lines[i], 18, 20 + (i*15));
                                    }
                                    ctx.save();
                                }
                            });
                            
                            var chart = new Chart(chartDiv, {
                                type: 'doughnut',
                                data: {
                                    labels: selectedCohorts,
                                    datasets: initDatasets
                                },
                                options: {
                                    responsive: false,
                                    maintainAspectRatio: false,
                                    legend: {
                                        display: false,
                                    },
                                    title: {
                                        text: "  " +  sig//set as you wish
                                    }
                                },
                            });
                        }
                    }
                }
            }
            var x = getEl("ul")
            x.innerHTML = chart.generateLegend();
            x.style.position = "relative"
            x.style.left = "220px"
            x.style.top = "20px"
            
            addEl(legendDiv, x)
            var legendDict = {}
            var legendItems = x.getElementsByTagName('li')
            var ul = x.getElementsByTagName("ul")[0]
            ul.style.listStyleType = "none";
            for (var i = 0; i < legendItems.length; i++) {
              legendItems[i].addEventListener("click", legendClickCallback.bind(this,i), false);
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
            function legendClickCallback(legendItemIndex){
                var count = 0
                document.querySelectorAll('canvas').forEach((chartItem,index)=>{
                var canvasID = Chart.instances[index].canvas.id
                if (canvasID.includes("clinvar")){
                    var newIndex = index - index + count 
                    count = count + 1
                    var newData = []
                    var newLabels = []
                    var newBg = []
                    var chart = Chart.instances[index]
                    var dataItem = allDatasets[newIndex]
                    // console.log(dataItem)
                    // for (var z in legendDict){
                    //     if (legendDict[z] == true){
                    //         var dataItem = allDatasets[newIndex]
                            
                    //     }
                    // }
                    var bg = colorIndex
                    for (var j in dataItem){
                        if (legendDict[j] == true){
                            console.log(dataItem[j])
                        }
                        if (legendDict[legendItemIndex] == true){
                            newData.push(dataItem[j])
                            newLabels.push(selectedCohorts[j])
                            newBg.push(bg[j])
                        }else{
                            if (j != legendItemIndex){
                                newData.push(dataItem[j])
                                newLabels.push(selectedCohorts[j])
                                newBg.push(bg[j])
                            }
                        }
                    }
                    console.log(newData)
                    chart.data.datasets[0].data = newData
                    chart.data.datasets[0].labels = newLabels
                    chart.data.datasets[0].backgroundColor = newBg
                    chart.tooltip._data.labels = newLabels
                    console.log(chart)
                    chart.update()
                }
              })
              if (legendDict[legendItemIndex] == false){
                legendDict[legendItemIndex] = true
                legendItems[legendItemIndex].style.textDecoration = "line-through"
              }else{
                legendDict[legendItemIndex] = false
                legendItems[legendItemIndex].style.textDecoration = "none"
              }
            }
        }
    }
};