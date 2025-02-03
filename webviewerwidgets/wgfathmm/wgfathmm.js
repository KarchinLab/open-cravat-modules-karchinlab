widgetGenerators['fathmm'] = {
	'variant': {
		'width': 480, 
		'height': 180, 
		'default_hidden': true,
		'function': function (div, row, tabName) {
			var value = getWidgetData(tabName, 'fathmm', row, 'fathmm_rscore');
			if (value == null) {
                var span = getEl('span');
                span.classList.add('nodata');
				addEl(div, addEl(span, getTn('No data')));
                return;
			}
			addInfoLine(div, 'FATHMM Converted Rank Score', getWidgetData(tabName, 'fathmm', row, 'fathmm_rscore'), tabName);
			var tid = getWidgetData(tabName, 'fathmm', row, 'ens_tid');
			var tidls = tid != null ? tid.split(';') : [];
			var pid = getWidgetData(tabName, 'fathmm', row, 'ens_pid');
			var pidls = pid != null ? pid.split(';') : [];
			var score = getWidgetData(tabName, 'fathmm', row, 'fathmm_score');
			var scorels = score != null ? score.split(';') : [];
			var pathogenic = getWidgetData(tabName, 'fathmm', row, 'pp3_pathogenic');
			var pathogenicls = pathogenic != null ? pathogenic.split(';') : [];
			var benign = getWidgetData(tabName, 'fathmm', row, 'bp4_benign');
			var benignls = benign != null ? benign.split(';') : [];
			for (var i=0;i<scorels.length;i++){
				if (scorels[i] == '.'){
					scorels[i] = null;
				}
			}
			var pred = getWidgetData(tabName, 'fathmm', row, 'fathmm_pred');
			var predls = pred != null ? pred.split(';') : [];
			for(var i=0;i<predls.length;i++){
				if(predls[i] == '.'){
					predls[i] = null;
				}
			}
			var table = getWidgetTableFrame();
			addEl(div, table);
			var thead = getWidgetTableHead(['Transcript', 'Protein', 'Score', 'Prediction', 'ACMG/AMP Benignity', 'ACMG/AMP Pathogenicity'],['25%','22%','10%','12%', '15%', '15%']);
			addEl(table, thead);
			var tbody = getEl('tbody');
			addEl(table, tbody);
			for (var i =0; i<tidls.length;i++){
				var tiditr = tidls[i];
				var piditr = pidls[i];
				var sitr = scorels[i];
				var pitr = predls[i];
				var bp4 = benignls[i]
				var pp3 = pathogenicls[i];
				if (bp4) {
					bp4 = "BP4 " + bp4;
				} else if (pp3) {
					pp3 = "PP3 " + pp3;
				} 
				var tr = getWidgetTableTr([tiditr, piditr, sitr, pitr, bp4, pp3]);
				const bp4Color = getCalibrationGradientColor(bp4);
				if (bp4) {
					$(tr).children().eq(4).css("background-color", bp4Color);
					$(tr).children().eq(4).css("color", bp4.includes("Strong") ? "white" : "black");
				}
				const pp3Color = getCalibrationGradientColor(pp3);
				if (pp3) {
					$(tr).children().eq(5).css("background-color", pp3Color);
					$(tr).children().eq(5).css("color", pp3.includes("Strong") ? "white" : "black");
				}
				addEl(tbody, tr);
			}
			addEl(div, addEl(table, tbody));
		}
	}
}
