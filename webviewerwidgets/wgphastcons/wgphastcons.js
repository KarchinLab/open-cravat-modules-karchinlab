widgetGenerators['phastcons'] = {
	'variant': {
		'width': 280, 
		'height': 160, 
        'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Vertebrate Score', getWidgetData(tabName, 'phastcons', row, 'phastcons100_vert'), tabName);
			addInfoLine(div, 'Vertebrate Ranked Score', getWidgetData(tabName, 'phastcons', row, 'phastcons100_vert_r'), tabName);
			addInfoLine(div, 'Mammalian Score', getWidgetData(tabName, 'phastcons', row, 'phastcons30_mamm'), tabName);
			addInfoLine(div, 'Mammalian Ranked Score', getWidgetData(tabName, 'phastcons', row, 'phastcons30_mamm_r'), tabName);
			addInfoLine(div, 'Primate Score', getWidgetData(tabName, 'phastcons', row, 'phastcons17way_primate'), tabName);
			addInfoLine(div, 'Primate Ranked Score', getWidgetData(tabName, 'phastcons', row, 'phastcons17way_primate_r'), tabName);
		}
	}
}
