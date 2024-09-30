widgetGenerators['sift'] = {
	'variant': {
		'width': 680, 
		'height': 180, 
		'function': function (div, row, tabName) {
			var allMappings = getWidgetData(tabName, 'sift', row, 'all');
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
				var thead = getWidgetTableHead(['Transcript', 'Prediction', 'Confidence', 'Score', 'Rank Score', 'Median Info', 'Seqs at Position', 'Pathogenicity'],['15%']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var trans = row[0];
					var score = row[1];
					var pred = row[2];
					var rank = row[3];
					rank = rank.toFixed(3);
					var med = row[4];
					var conf = row[5];
					var seqs = row[6];
					var bp4 = row[7]
					var pp3 = row[8]
					let pathogenicity 
					if (bp4 !== "") {
						pathogenicity = "BP4 " + bp4
					} else if (pp3 !== "") {
						pathogenicity = "PP3 " + pp3
					} else if (pp3 === "" && bp4 === "") {
						pathogenicity = "Indeterminate"
					}
					var tr = getWidgetTableTr([trans, pred,conf,score, rank, med, seqs, pathogenicity]);
					const color = getGradientColor(pathogenicity)
                    if (pathogenicity !== "") {
                        $(tr).children().eq(7).css("background-color", color);
						$(tr).children().eq(7).css("color", pathogenicity.includes("Strong") ? "white" : "black");
                    }
					
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}