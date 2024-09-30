widgetGenerators['gerp'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
			getGradientColor = function(pathogenicity) {
                let color = ""
                if (pathogenicity === "Indeterminate") {
                    color = "#fffff"
                } else if (pathogenicity === "Moderate") {
                    color = "#48cae4"
                } else if (pathogenicity === "Supporting") {
                    color = "#ade8f4"
                }
                return color
            }
			addInfoLine(div, row, 'Neutral Rate', 'gerp__gerp_nr', tabName);
			addInfoLine(div, row, 'RS Score', 'gerp__gerp_rs', tabName);
			addInfoLine(div, row, 'RS Ranked Score', 'gerp__gerp_rs_rank', tabName);
			var pathogenicity = getWidgetData(tabName, 'gerp', row, 'gerp_benign');
			var score = getWidgetData(tabName, 'gerp', row, 'gerp_rs');
			if (pathogenicity === null && score != undefined) {
				addInfoLineText(div, 'BP4 Pathogenicity', 'Indeterminate')
			} else {
				addInfoLine(div, row, 'BP4 Pathogenicity', 'gerp__gerp_benign', tabName);
			}
			const color = getGradientColor(pathogenicity)
			
		}
	}
}
