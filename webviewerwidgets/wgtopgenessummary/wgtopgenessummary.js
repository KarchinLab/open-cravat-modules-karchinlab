widgetGenerators['topgenessummary'] = {
	'info': {
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
            if (this['variables']['data'].length == 0 || this['variables']['data'] == null || infomgr.datas.variant.length > 500){
                return false;
            } else {
                return true;
            }
        },
		'function': function (div, dummy) {
			if (div != null) {
				emptyElement(div);
			}
			div.style.width = 'calc(100% - 37px)';
			var chartDiv = getEl('canvas');
			chartDiv.style.width = 'calc(100% - 20px)';
			chartDiv.style.height = 'calc(100% - 20px)';
			addEl(div, chartDiv);
			var x = [];
			var y = [];
			var data = this['variables']['data'];
			for (var i = 0; i < data.length; i++) {
				var row = data[i];
				x.push(row[0]);
				y.push(row[1]);
			}
			var chart = new Chart(chartDiv, {
				type: 'horizontalBar',
				data: {
					labels: x,
					datasets: [
						{
							data: y,
							borderColor: '#000000',
							borderWidth: 0.7,
							hoverBorderColor: '#aaaaaa',
							backgroundColor: '#D6604D'
						}
					]
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					legend: {display: false},
					scales: {
						xAxes: [{
							scaleLabel: {
								display: true,
								labelString: 'Number of Samples',
							},
							ticks: {
								beginAtZero: true,
								stepSize: 1,
							}
						}],
					},
					tooltips: {
						backgroundColor: '#ffffff',
						displayColors: false,
						titleFontColor: '#000000',
						titleFontStyle: 'normal',
						bodyFontColor: '#000000',
						borderColor: '#333333',
						borderWidth: 1,
					}
				}
			});
		}
	}
};
