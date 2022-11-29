widgetGenerators['aloft'] = {
	'variant': {
		'width': 700, 
		'height': 120, 
		'function': function (div, row, tabName) {
			var allMappings = getWidgetData(tabName, 'aloft', row, 'all');
			if (allMappings == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			if (allMappings != undefined && allMappings != null) {
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Transcript', 'Transcripts Affected', 'Tolerated Probability', 'Recessive Probability', 'Dominant Probability', 'Classification', 'Confidence'], ["16%"]);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var transcript = row[0];
					var affect = row[1];
					var tolerated = row[2];
                    var recessive = row[3];
                    var dominant = row[4];
                    var pred = row[5];
                    var conf = row[6];
					var tr = getWidgetTableTr([transcript, affect, tolerated, recessive, dominant, pred, conf]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}