widgetGenerators['phylop'] = {
	'variant': {
		'width': 280, 
		'height': 160, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			var vert_score = getWidgetData(tabName, 'phylop', row, 'phylop100_vert')
			addInfoLine(div, 'Vertebrate Score', vert_score , tabName);
			addInfoLine(div, 'Vertebrate Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop100_vert_r'), tabName);
			addInfoLine(div, 'Mammalian Score', getWidgetData(tabName, 'phylop', row, 'phylop470_mamm'), tabName);
			addInfoLine(div, 'Mammalian Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop470_mamm_r'), tabName);
			addInfoLine(div, 'Primate Score', getWidgetData(tabName, 'phylop', row, 'phylop17_primate'), tabName);
			addInfoLine(div, 'Primate Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop17_primate_r'), tabName);
			var bp4 = getWidgetData(tabName, 'phylop', row, 'benign')
			var pp3 = getWidgetData(tabName, 'phylop', row, 'pathogenic')
			let pathogenicity = null
			if (bp4 !== null) {
				pathogenicity = "BP4 " + bp4
			} else if (pp3 !== null) {
				pathogenicity = "PP3 " + pp3
			} else if (pp3 === null && bp4 === null && vert_score !== null) {
				pathogenicity = "Indeterminate"
			}
			addInfoLine(div, 'Primate Ranked Score', pathogenicity);
		}
	}
}
