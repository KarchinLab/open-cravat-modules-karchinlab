widgetGenerators['vest'] = {
	'variant': {
		'width': 480, 
		'height': 180, 
		'default_hidden': false,
		'function': function (div, row, tabName) {
			var allMappings = getWidgetData(tabName, 'vest', row, 'all');
			if (allMappings != undefined && allMappings != null) {
                if(typeof addGradientBarComponent == 'function'){
                    addGradientBarComponent(div, row, 'VEST p-value', 'vest__pval', tabName, colors={'0.0':[255,0,0],'0.05':[255,230,230],'1.0':[255,255,255]});
                }
                else{
                    addBarComponent(div, row, 'VEST p-value', 'vest__pval', tabName);
                }
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Transcript', 'Score', 'Pathogenicity']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var transcript = row[0];
					var score = row[1].toFixed(3);
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
					var tr = getWidgetTableTr([transcript, score, pathogenicity]);
                    const color = getCalibrationGradientColor(pathogenicity)
                    if (pathogenicity !== "") {
                        $(tr).children().eq(2).css("background-color", color);
                        $(tr).children().eq(2).css("color", pathogenicity.includes("Strong") ? "white" : "black");
                    }
                    
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			} else {
                var allMappings = getWidgetData(tabName, 'vest', row, 'all_results');
                if (allMappings != undefined && allMappings != null) {
                    if(typeof addGradientBarComponent == 'function'){
                        addGradientBarComponent(div, row, 'VEST p-value', 'vest__pval', tabName, colors={'0.0':[255,0,0],'0.05':[255,230,230],'1.0':[255,255,255]});
                    }
                    else{
                        addBarComponent(div, row, 'VEST p-value', 'vest__pval', tabName);
                    }
                    allMappings = allMappings.split(',');
                    var table = getWidgetTableFrame();
                    var thead = getWidgetTableHead(['Transcript', 'Score', 'P-value']);
                    addEl(table, thead);
                    var tbody = getEl('tbody');
                    for (var i = 0; i < allMappings.length; i++) {
                        var mapping = allMappings[i];
                        var toks = mapping.split('(');
                        var transcript = toks[0];
                        var toks2 = toks[1].split(':');
                        var score = parseFloat(toks2[0]).toFixed(3);
                        var pvalue = parseFloat(toks2[1].split(')')[0]).toFixed(4);
                        var tr = getWidgetTableTr([transcript, score, pvalue]);
                        addEl(tbody, tr);
                    }
                    addEl(div, addEl(table, tbody));
                } else {
                    var span = getEl('span');
                    span.classList.add('nodata');
                    addEl(div, addEl(span, getTn('No data')));
                }
            }
		}
	},
	'gene': {
		'width': 280, 
		'height': 80, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Max score', 'vest__max_score', tabName);
			addInfoLine(div, row, 'Mean score', 'vest__mean_score', tabName);
			addInfoLine(div, row, 'Gene p-value', 'vest__gene_pval', tabName);
		}
	}
}
