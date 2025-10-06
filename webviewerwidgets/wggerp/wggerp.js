widgetGenerators['gerp'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'default_hidden': false,
		'function': function (div, row, tabName) {
			addInfoLine(div, row, 'Neutral Rate', 'gerp__gerp_nr', tabName);
			addInfoLine(div, row, 'RS Score', 'gerp__gerp_rs', tabName);
			addInfoLine(div, row, 'RS Ranked Score', 'gerp__gerp_rs_rank', tabName);
			if (score != undefined) {
				var pathogenicity = "Indeterminate";
				var bp4 = getWidgetData(tabName, 'gerp', row, 'bp4_benign');
				var pp3 = getWidgetData(tabName, 'gerp', row, 'pp3_pathogenicity');
				if (bp4) {
					pathogenic = "BP4 " + bp4;
				} else {
					pathogenic = "PP3 " + pp3;
				}
				addInfoLineText(div, 'ACMG/AMP Pathogenicity', pathogenic)
			} 
		}
	}
}
