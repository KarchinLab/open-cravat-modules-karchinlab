widgetGenerators['interpro'] = {
	'variant': {
		'width': 520, 
		'height': 140, 
		'word-break': 'normal',
		'function': function (div, row, tabName) {
            var allMappings = getWidgetData(tabName, 'interpro', row, 'all');
			if (allMappings == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			if (allMappings != undefined && allMappings != null) {
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Domain', 'UniProt', 'Ensembl', 'Sources'],['55%','15%','20%','10%']);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
					var domain = row[0];
					var uniprot = row[1];
                    var ensembl = row[2];
                    var count = row[3]
					var link = "https://www.ebi.ac.uk/interpro/protein/UniProt/" + uniprot
                    var tr = getWidgetTableTr([domain, link, ensembl, count],[uniprot]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}
