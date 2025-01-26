widgetGenerators['bayesdel'] = {
	'variant': {
		'width': 380, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
            var noAfScore = getWidgetData(tabName, 'bayesdel', row, 'bayesdel_noAF_score');
            if (noAfScore == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			var table = getWidgetTableFrame();
            var thead = getWidgetTableHead(['Score (no AF)', 'ACMG/AMP Pathogenicity']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            var bp4 = getWidgetData(tabName, 'bayesdel', row, 'bp4_benign');
            var pp3 = getWidgetData(tabName, 'bayesdel', row, 'pp3_pathogenic');
            let pathogenicity 
            if (bp4 !== null) {
                pathogenicity = "BP4 " + bp4
            } else if (pp3 !== null) {
                pathogenicity = "PP3 " + pp3
            } else if (pp3 === null && bp4 === null) {
                pathogenicity = "Indeterminate"
            }
            var tr = getWidgetTableTr([noAfScore, pathogenicity]);
            const color = getCalibrationGradientColor(pathogenicity)
            if (pathogenicity !== "") {
                $(tr).children().eq(1).css("background-color", color);
                $(tr).children().eq(1).css("color", pathogenicity.includes("Strong") ? "white" : "black");
            }
            addEl(tbody, tr);
            addEl(div, addEl(table, tbody));
			}
		}
	}
