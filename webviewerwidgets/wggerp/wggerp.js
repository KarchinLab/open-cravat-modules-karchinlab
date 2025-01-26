widgetGenerators['gerp'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
        'default_hidden': false,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Neutral Rate', 'gerp__gerp_nr', tabName);
			addInfoLine(div, row, 'RS Score', 'gerp__gerp_rs', tabName);
			addInfoLine(div, row, 'RS Ranked Score', 'gerp__gerp_rs_rank', tabName);
			var pathogenicity = getWidgetData(tabName, 'gerp', row, 'bp4_benign');
			var score = getWidgetData(tabName, 'gerp', row, 'gerp_rs');
			if (pathogenicity === null && score != undefined) {
				addInfoLineText(div, 'ACMG/AMP Pathogenicity', 'Indeterminate')
			} else {
				addInfoLine(div, row, 'ACMG/AMP Pathogenicity', 'gerp__bp4_benign', tabName);
			}
		}
	}
}
