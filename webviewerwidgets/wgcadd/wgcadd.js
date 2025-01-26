widgetGenerators['cadd'] = {
	'variant': {
		'width': 380, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
			var phred = getWidgetData(tabName, 'cadd', row, 'phred');
			if (phred == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			if (phred != undefined && phred != null) {
                var table = getWidgetTableFrame();
                var thead = getWidgetTableHead(['Phred','ACMG/AMP Pathogenicity']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var bp4 = getWidgetData(tabName, 'cadd', row, 'bp4_benign');
                var pp3 = getWidgetData(tabName, 'cadd', row, 'pp3_pathogenic');
                let pathogenicity 
                if (bp4 !== null) {
                    pathogenicity = "BP4 " + bp4
                } else if (pp3 !== null) {
                    pathogenicity = "PP3 " + pp3
                } else if (pp3 === null && bp4 === null) {
                    pathogenicity = "Indeterminate"
                }
                var tr = getWidgetTableTr([phred, pathogenicity]);
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
}
