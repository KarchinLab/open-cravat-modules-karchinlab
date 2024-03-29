widgetGenerators['cosmic'] = {
	'variant': {
		'width': 280, 
		'height': 220, 
		'word-break': 'normal',
		'function': function (div, row, tabName) {
			addInfoLine(div, 'ID', getWidgetData(tabName, 'cosmic', row, 'cosmic_id'), tabName, 4);
			addInfoLine(div, 'Variant Count', getWidgetData(tabName, 'cosmic', row, 'variant_count'), tabName);
			addInfoLine(div, 'Transcript', getWidgetData(tabName, 'cosmic', row, 'transcript'), tabName);
			addInfoLine(div, 'Protein Change', getWidgetData(tabName, 'cosmic', row, 'protein_change'), tabName);
			var vcTissue = getWidgetData(tabName, 'cosmic', row, 'variant_count_tissue');
			if (vcTissue != undefined && vcTissue !== null && typeof(vcTissue) == 'object') {
                var results = vcTissue;
				var table = getWidgetTableFrame();
				var thead = getWidgetTableHead(['Tissue', 'Count'],['85%','15%']);
				addEl(table, thead);
				var tbody = getEl('tbody');
				for (var i = 0; i < results.length; i++) {
                    var tr = getWidgetTableTr(results[i]);
                    addEl(tbody, tr);
				}
				addEl(div, addEl(table, tbody));
			} else {
                var vcTissue = getWidgetData(tabName, 'cosmic', row, 'variant_count_tissue');
                if (vcTissue != undefined && vcTissue !== null) {
                    hits = JSON.parse(vcTissue);
                    var table = getWidgetTableFrame();
                    var thead = getWidgetTableHead(['Tissue', 'Count'],['85%','15%']);
                    addEl(table, thead);
                    var tbody = getEl('tbody');
                    for (var i = 0; i < hits.length; i++) {
                        var tok = hits[i];
                        var tissue = tok[0]
                        var count = tok[1]
                        var tr = getWidgetTableTr([tissue, count]);
                        addEl(tbody, tr);
                    }
                    addEl(div, addEl(table, tbody));
                }
            }
		}
	}
}
