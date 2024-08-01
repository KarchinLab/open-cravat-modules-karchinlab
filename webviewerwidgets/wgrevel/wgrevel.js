widgetGenerators['revel'] = {
	'variant': {
		'width': 480, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
			var allMappings = getWidgetData(tabName, 'revel', row, 'all');
			if (allMappings == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			getGradientColor = function(pathogenicity) {
                let color = ""
                if (pathogenicity === "Indeterminate") {
                    color = "#fffff"
                } else if (pathogenicity === "BP4 Very Strong") {
					color = "#03045e"
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
                } else if (pathogenicity === "PP3 Strong") {
                    color = "#c30010"
                }
                return color
            }
			if (allMappings != undefined && allMappings != null) {
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Transcript', 'Score', 'Rank score', 'Pathogenicity']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var transcript = row[0];
					var score = row[1];
					var rankscore = row[2];
					var bp4 = row[3]
					var pp3 = row[4]
					let pathogenicity 
					if (bp4 !== "") {
						pathogenicity = "BP4 " + bp4
					} else if (pp3 !== "") {
						pathogenicity = "PP3 " + pp3
					} else if (pp3 === "" && bp4 === "") {
						pathogenicity = "Indeterminate"
					}
					var tr = getWidgetTableTr([transcript, score, rankscore, pathogenicity]);
					const color = getGradientColor(pathogenicity)
                    if (pathogenicity !== "") {
                        $(tr).children().eq(3).css("background-color", color);
						$(tr).children().eq(3).css("color", pathogenicity.includes("Strong") ? "white" : "black");
                    }
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}
