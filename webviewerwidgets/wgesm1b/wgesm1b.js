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
				var thead = getWidgetTableHead(['Transcript', 'Score', 'Rank score', 'Prediction', 'Pathogenicity']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var transcript = row[0];
					var score = row[1];
					var rankscore = row[2];
                    var pred = row[3]
					var bp4 = row[4];
					var pp3 = row[5];
					var pathogenicity = "Indeterminate";
					if (bp4) {
						pathogenicity = "BP4 " + bp4;
					} else if(pp3) {
						pathogenicity = "PP3 " + pp3;
					}
					var tr = getWidgetTableTr([transcript, score, rankscore, pred, pathogenicity]);
					const color = getCalibrationGradientColor(pathogenicity)
					$(tr).children().eq(4).css("background-color", color);
					$(tr).children().eq(4).css("color", pathogenicity.includes("Strong") ? "white" : "black");

					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}
