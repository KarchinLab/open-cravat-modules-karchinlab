widgetGenerators['ncg'] = {
	'gene': {
		'width': 1100,
		'height': 120,
		'function': function (div, row, tabName) {

			let pubmedId = getWidgetData(tabName, 'ncg', row, 'pubmed_id').split(';');
			if (pubmedId == null) {
				let span = getEl('span');
				span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
				return;
			}
			if (pubmedId != undefined && pubmedId != null) {
				let type = getWidgetData(tabName, 'ncg', row, 'type').split(';');
				let organSystem = getWidgetData(tabName, 'ncg', row, 'organ_system').split(';');
				let primarySite = getWidgetData(tabName, 'ncg', row, 'primary_site').split(';');
				let cancerType = getWidgetData(tabName, 'ncg', row, 'cancer_type').split(';');
				let method = getWidgetData(tabName, 'ncg', row, 'method').split(';');
				let codingStatus = getWidgetData(tabName, 'ncg', row, 'coding_status').split(';');
				let cgcAnno = getWidgetData(tabName, 'ncg', row, 'cgc_annotation').split(';');
				let vogelsteinAnno = getWidgetData(tabName, 'ncg', row, 'vogelstein_annotation').split(';');
				let saitoAnno = getWidgetData(tabName, 'ncg', row, 'saito_annotation').split(';');
				let oncogene = getWidgetData(tabName, 'ncg', row, 'NCG_oncogene').split(';');
				let tsg = getWidgetData(tabName, 'ncg', row, 'NCG_tsg').split(';');
				const table = getWidgetTableFrame();
				addEl(div, table);
				const thead = getWidgetTableHead(
					['Pubmed','Type','Organ System', 'Primary Site', 'Cancer Type', 'Method', 'Coding', 'CGC', 'Vogelstein', 'Saito', 'Oncogene', 'TSG'],
					[80,80,80,80,120,120,80,80,80,80,80,80]
				);
				addEl(table, thead);
				const tbody = getEl('tbody');
				addEl(table, tbody);
				for (let i = 0; i < pubmedId.length; i++) {
					const pubmedLink = `https://pubmed.ncbi.nlm.nih.gov/${pubmedId[i]}`
					// linkNames is an array with a label for each link in the dataset...
					const linkNames = [pubmedId[i]];
					const tr = getWidgetTableTr(
						[pubmedLink, type[i], organSystem[i], primarySite[i], cancerType[i], method[i], codingStatus[i], cgcAnno[i], vogelsteinAnno[i], saitoAnno[i], oncogene[i], tsg[i]],
						linkNames
					);
					addEl(tbody, tr);
				}
			}
		}
	}
}
