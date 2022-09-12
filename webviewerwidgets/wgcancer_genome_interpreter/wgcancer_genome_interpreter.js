widgetGenerators['cancer_genome_interpreter'] = {
	'variant': {
		'width': 580, 
		'height': 220, 
		'function': function (div, row, tabName) {
			var allMappings = getWidgetData(tabName, 'cancer_genome_interpreter', row, 'all');
			if (allMappings != undefined && allMappings != null) {
                var results = JSON.parse(allMappings);
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Association','Biomarker', 'Drug', 'Evidence', 'Source', "Tumor Type"], ["15%"]);
				addEl(table, thead);
				var tbody = getEl('tbody');
                for (var i = 0; i < results.length; i++) {
					var row = results[i];
                    var assoc = row[0];
                    var biomarker = row[1]
					var drug = row[2];
                    var evidence = row[3];
                    var source = row[4]
                    var tumor = row[5]
					var tr = getWidgetTableTr([assoc, biomarker, drug, evidence, source, tumor]);
					addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			}
		}
	}
}