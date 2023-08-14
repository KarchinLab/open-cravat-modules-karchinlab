widgetGenerators['phylop'] = {
	'variant': {
		'width': 280, 
		'height': 160, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			addInfoLine(div, 'Vertebrate Score', getWidgetData(tabName, 'phylop', row, 'phylop100_vert'), tabName);
			addInfoLine(div, 'Vertebrate Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop100_vert_r'), tabName);
			addInfoLine(div, 'Mammalian Score', getWidgetData(tabName, 'phylop', row, 'phylop30_mamm'), tabName);
			addInfoLine(div, 'Mammalian Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop30_mamm_r'), tabName);
			addInfoLine(div, 'Primate Score', getWidgetData(tabName, 'phylop', row, 'phylop17_primate'), tabName);
			addInfoLine(div, 'Primate Ranked Score', getWidgetData(tabName, 'phylop', row, 'phylop17_primate_r'), tabName);
		}
	}
}
