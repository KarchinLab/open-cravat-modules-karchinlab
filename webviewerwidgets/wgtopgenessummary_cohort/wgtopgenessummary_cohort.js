widgetGenerators['topgenessummary_cohort'] = {
	'cohort': {
		'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
		'width': 380, 
		'height': 380, 
		'callserver': true,
        'default_hidden': false,
        'variables': {},
        'init': function (data) {
            this['variables']['data'] = data;
        },
        'shoulddraw': function () {
            if (this['variables']['data'].length == 0 || this['variables']['data'] == null || infomgr.datas.variant.length > 1000){
                return false;
            } else {
                return true;
            }
		},
		'function': function (div, dummy) {
			if (div != null) {
				emptyElement(div);
			}
			var colorPalette = {
				'1':'#2166AC',
				'2':'#4393C3',
				'3':'#92C5DE',
				'4':'#D1E5F0',
				'5':'#1B7837',
				'6':'#FDDBC7',
				'7':'#F4A582',
				'8':'#5AAE61',
				'9':'#D6604D',
				'10':'#B2182B',
			}
			div.style.width = 'calc(100% - 37px)';
			var chartDiv = getEl('canvas');
			chartDiv.style.width = 'calc(100% - 20px)';
			chartDiv.style.height = 'calc(100% - 20px)';
			addEl(div, chartDiv);
			var x = [];
			var y = [];
			var initDatasets = [];
			var data = this['variables']['data'];
			let index = 0;
                        console.log(data)
			for (var i in data) {
				var row = data[i][0];
				for (var j in row) {
                    var initSamples = [];
					var initDatasetCounts = [];
					index = index + 1
					for (var m in row[j]){
						initDatasetCounts.push(row[j][m][1]);
						if (!(row[j][m][0] in initSamples)){
							initSamples.push(row[j][m][0])
						}else{
							continue
						}
					}
					var backgroundColor = colorPalette[index];
					initDatasets.push({'label': j, 'backgroundColor': backgroundColor, 'data': initDatasetCounts});
				}
			}
			var chart = new Chart(chartDiv, {
				type: 'horizontalBar',
				data: {
					labels: initSamples,
					datasets: initDatasets
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					legend: {display: true},
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
					tooltips: {
                            mode: 'index',
                          callbacks: {
                              afterLabel: function(tooltipItem, data) {
                                var sum = data.datasets.reduce((sum, dataset) => {
                                  return sum + dataset.data[tooltipItem.index];
                              }, 0);
                              var percent = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] / sum * 100;
                              percent = percent.toFixed(2);
                              return data.datasets[tooltipItem.datasetIndex].label + ': ' + percent + '%';
                            }
                          }
                        }
				}
			});
		}
	}
};
