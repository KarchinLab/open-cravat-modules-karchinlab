widgetGenerators['gtex'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'function': function (div, row, tabName) {
			var genes = getWidgetData(tabName, 'gtex', row, 'gtex_gene');
			if (genes == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			var genels = genes != null ? genes.split('|') : [];
			var tissues = getWidgetData(tabName, 'gtex', row, 'gtex_tissue');
			var tissuels = tissues != null ? tissues.split('|') : [];
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Target Gene', 'Tissue Type']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var i =0; i<genels.length;i++){
				var geneitr = genels[i];
				var tissueitr = tissuels[i];
				tissueitr = tissueitr.replace("_", " ")
				var gtexLink = 'https://www.gtexportal.org/home/gene/'+geneitr;
				var tr = getWidgetTableTr([gtexLink, tissueitr],[geneitr]);
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}
