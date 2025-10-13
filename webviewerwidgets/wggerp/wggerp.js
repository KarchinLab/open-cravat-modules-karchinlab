widgetGenerators['gerp'] = {
	'variant': {
		'width': 280, 
		'height': 120, 
		'default_hidden': false,
		'function': function (div, row, tabName) {
			let rank_score = getWidgetData(tabName, 'gerp', row, 'gerp_rs_rank')
			if (rank_score === undefined) {
				return;
			}
			addInfoLine(div, row, 'Gerp Neutral Rate', 'gerp__gerp_nr', tabName);

			let neutral_rate = getWidgetData(tabName, 'gerp', row,' gerp_nr')
			let rs_score = getWidgetData(tabName, 'gerp', row, 'gerp_rs')
			var pathogenic = "Indeterminate";
			var bp4 = getWidgetData(tabName, 'gerp', row, 'bp4_benign');
			var pp3 = getWidgetData(tabName, 'gerp', row, 'pp3_pathogenicity');
			if (bp4) {
				pathogenic = "BP4 " + bp4;
			} else {
				pathogenic = "PP3 " + pp3;
			}
			var table = getWidgetTableFrame();
            var thead = getWidgetTableHead([
				'Neutral Rate', 
				'RS Score', 
				'RS Rank Score', 
				'ACMG/AMP Pathogenicity'
			]);
			var tr = getWidgetTableTr([neutral_rate, rs_score, rank_score, pathogenic]);
			const color = getCalibrationGradientColor(pathogenic);
			if (pathogenic) {
				$(tr).children().eq(3).css("background-color", color);
				$(tr).children().eq(3).css("color", pathogenic.includes("Strong") ? "white" : "black");
			}
			addEl(div, table);
			addEl(table, thead);
			addEl(table, tr);
		}
	}
}
