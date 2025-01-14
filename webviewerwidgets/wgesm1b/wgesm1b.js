widgetGenerators['esm1b'] = {
	'variant': {
		'width': 480, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
			var allMappings = getWidgetData(tabName, 'esm1b', row, 'all');
			if (allMappings == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			if (allMappings != undefined && allMappings != null) {
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				// TODO: cvaske should check with kylem about how these are ordered... most likely by YML?
				var thead = getWidgetTableHead(['Transcript', 'Score', 'Pathogenicity', 'Rank score', 'Prediction']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var transcript = row[0];
					var score = row[1];
					var pathogenicity = row[2];
					var rankscore = row[3];
                    var pred = row[4]
					var tr = getWidgetTableTr([transcript, score, pathogenicity, rankscore, pred]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}
