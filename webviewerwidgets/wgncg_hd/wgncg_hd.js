widgetGenerators['ncg_hd'] = {
	'gene': {
		'width': 600,
		'height': 120,
		'function': function (div, row, tabName) {

			let organSystem = getWidgetData(tabName, 'ncg', row, 'organ_system');
			if (organSystem == null) {
				let span = getEl('span');
				span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
				return;
			}
			if (organSystem != undefined && organSystem != null) {
				let organSystem = getWidgetData(tabName, 'ncg_hd', row, 'organ_system').split(',');
				let organSite = getWidgetData(tabName, 'ncg_hd', row, 'organ_site').split(',');
				let tissueType = getWidgetData(tabName, 'ncg_hd', row, 'tissue_type').split(',');
				const table = getWidgetTableFrame();
				addEl(div, table);
				const thead = getWidgetTableHead(
					['Organ System', 'Organ Site', 'Tissue Type'],
					[200,200,200]
				);
				addEl(table, thead);
				const tbody = getEl('tbody');
				addEl(table, tbody);
				const osLength = organSystem?.length || 0;
				const oSiteLength = organSite?.length || 0;
				const ttLength = tissueType?.length || 0;
				let maxLength = Math.max(osLength, oSiteLength, ttLength)
				for (let i = 0; i < maxLength; i++) {
					const tr = getWidgetTableTr(
						[
							i < osLength ? organSystem[i] : null,
							i < oSiteLength ? organSite[i] : null,
							i < ttLength ? tissueType[i] : null
						]);
					addEl(tbody, tr);
				}
			}
		}
	}
}
