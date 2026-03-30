widgetGenerators['ncg'] = {
	'gene': {
		'width': 600,
		'height': 120,
		'function': function (div, row, tabName) {

			let organSystem = getWidgetData(tabName, 'ncg', row, 'organ_system').split(';');
			if (organSystem == null) {
				let span = getEl('span');
				span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
				return;
			}
			if (organSystem != undefined && organSystem != null) {
				let organSystem = getWidgetData(tabName, 'ncg', row, 'organ_system').split(',');
				let primarySite = getWidgetData(tabName, 'ncg', row, 'primary_site').split(',');
				let cancerType = getWidgetData(tabName, 'ncg', row, 'cancer_type').split(',');
				const table = getWidgetTableFrame();
				addEl(div, table);
				const thead = getWidgetTableHead(
					['Organ System', 'Primary Site', 'Cancer Type'],
					[200,200,200]
				);
				addEl(table, thead);
				const tbody = getEl('tbody');
				addEl(table, tbody);
				const osLength = organSystem?.length || 0;
				const psLength = primarySite?.length || 0;
				const ctLength = cancerType?.length || 0;
				let maxLength = Math.max(osLength, psLength, ctLength)
				for (let i = 0; i < maxLength; i++) {
					const tr = getWidgetTableTr(
						[
							i < osLength ? organSystem[i] : null,
							i < psLength ? primarySite[i] : null,
							i < ctLength ? cancerType[i] : null
						]);
					addEl(tbody, tr);
				}
			}
		}
	}
}
