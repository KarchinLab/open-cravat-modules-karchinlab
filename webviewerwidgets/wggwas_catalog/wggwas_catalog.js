widgetGenerators['gwas_catalog'] = {
	'variant': {
		'width': 580,
		'height': 180,
		'function': function (div, row, tabName) {
			let all_annot_data = getWidgetData(tabName, 'gwas_catalog', row, 'all_annots');
			let disease = getWidgetData(tabName, 'gwas_catalog', row, 'disease');
			if (!all_annot_data && !disease) {
				const span = getEl('span');
				span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
				return;
			}
			// build table
			const table = getWidgetTableFrame();
			addEl(div, table);
			table.style.tableLayout = 'auto';
			table.style.width = '100%';
			const thead = getWidgetTableHead(
				['Disease/Trait', 'Risk Allele', 'OR/Beta', 'P-Val', 'CI', 'PubMed'],
				['40%', '10%', '10%', '10%', '10%', '10%']
			);
			addEl(table, thead);
			const tbody = getEl('tbody');
			addEl(table, tbody);
			if (all_annot_data != undefined && all_annot_data != null) {
				let all_data = JSON.parse(all_annot_data);
				for (let data of all_data) {
					let pmLink = getEl('a');
					pmLink.href = `https://pubmed.ncbi.nlm.nih.gov/${data['pmid']}`;
					pmLink.innerText = data['pmid'];
					pmLink.target = '_blank';
					let riskDiv = getEl('div')
					riskDiv.innerText = data['risk_allele'];
					riskDiv.style.width = '100%';
					riskDiv.style.textAlign = 'center';
					if (data['risk_allele_match']) {
						riskDiv.style.backgroundColor = 'rgb(255, 203, 209)';
					}
					const tr = elementsToWidgetTr([data['disease'], riskDiv, data['or_beta'], data['pval'], data['ci'], pmLink]);
					addEl(tbody, tr);
				}
			} else {
				// legacy gwas data - use single row
				const disease = getWidgetData(tabName, 'gwas_catalog', row, 'disease');
				const risk_allele = getWidgetData(tabName, 'gwas_catalog', row, 'risk_allele');
				const or_beta = getWidgetData(tabName, 'gwas_catalog', row, 'or_beta');
				const pval = getWidgetData(tabName, 'gwas_catalog', row, 'pval');
				const ci = getWidgetData(tabName, 'gwas_catalog', row, 'ci');
				const pmid = getWidgetData(tabName, 'gwas_catalog', row, 'pmid');
				const altBase = getWidgetData(tabName, 'base', row, 'alt_base');
				const refBase = getWidgetData(tabName, 'base', row, 'ref_base');
				const risk_allele_match = risk_allele === altBase || risk_allele === refBase;
				let pmLink = getEl('a');
				pmLink.href = `https://pubmed.ncbi.nlm.nih.gov/${pmid}`;
				pmLink.innerText = pmid;
				pmLink.target = '_blank';
				let riskDiv = getEl('div')
				riskDiv.innerText = risk_allele;
				riskDiv.style.width = '100%';
				riskDiv.style.textAlign = 'center';
				if (risk_allele_match) {
					riskDiv.style.backgroundColor = 'rgb(255, 203, 209)';
				}

				const tr = elementsToWidgetTr([disease, riskDiv, or_beta, pval, ci, pmLink]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}
