widgetGenerators['cadd_exome'] = {
	'variant': {
		'width': 380, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
			var phred = getWidgetData(tabName, 'cadd_exome', row, 'phred');
			if (phred == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			getGradientColor = function(pathogenicity) {
                let color = ""
                if (pathogenicity === "Indeterminate") {
                    color = "#fffff"
                } else if (pathogenicity === "BP4 Strong") {
					color = "#023e8a"
				} else if (pathogenicity === "BP4 Moderate") {
                    color = "#48cae4"
                } else if (pathogenicity === "BP4 Supporting") {
                    color = "#ade8f4"
                } else if (pathogenicity === "PP3 Supporting") {
                    color = "#ffcbd1"
                } else if (pathogenicity === "PP3 Moderate") {
                    color = "#f94449"
                }
                return color
            }
			if (phred != undefined && phred != null) {
                var table = getWidgetTableFrame();
                var thead = getWidgetTableHead(['Phred','Pathogenicity']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var bp4 = getWidgetData(tabName, 'cadd_exome', row, 'benign');
                var pp3 = getWidgetData(tabName, 'cadd_exome', row, 'pathogenic');
                let pathogenicity 
                if (bp4 !== null) {
                    pathogenicity = "BP4 " + bp4
                } else if (pp3 !== null) {
                    pathogenicity = "PP3 " + pp3
                } else if (pp3 === null && bp4 === null) {
                    pathogenicity = "Indeterminate"
                }
                var tr = getWidgetTableTr([phred, pathogenicity]);
                const color = getGradientColor(pathogenicity)
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
