widgetGenerators['fathmm_xf_coding'] = {
    'variant': {
        'width': 480,
        'height': 180,
        'default_hidden': true,
        'function': function (div, row, tabName) {
            var rscore = getWidgetData(tabName, 'fathmm_xf_coding', row, 'fathmm_xf_coding_rankscore');
            if (rscore == null) {
                var span = getEl('span');
                span.classList.add('nodata');
                addEl(div, addEl(span, getTn('No data for FATHMM XF Coding')));
                return;
            }
            addInfoLine(div, 'FATHMM XF Coding Rank Score', rscore, tabName);
            var table = getWidgetTableFrame();
            addEl(div, table);
            var thead = getWidgetTableHead(['Score', 'Rank Score', 'Prediction', 'ACMG/AMP Pathogenicity']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var score = getWidgetData(tabName, 'fathmm_xf_coding', row, 'fathmm_xf_coding_score');
            var pred = getWidgetData(tabName, 'fathmm_xf_coding', row, 'fathmm_xf_coding_pred');
            var pathogenic = getWidgetData(tabName, 'fathmm_xf_coding', row, 'pp3_pathogenic');
            var benign = getWidgetData(tabName, 'fathmm_xf_coding', row, 'bp4_benign');
            var pathogenicity = "Indeterminate";
            if (benign) {
                pathogenicity = "BP4 " + benign;
            } else if (pathogenic) {
                pathogenicity = "PP3 " + pathogenic;
            }
            var tr = getWidgetTableTr([score, rscore, pred, pathogenicity]);
            const color = getCalibrationGradientColor(pathogenicity);
            if (pathogenicity) {
                $(tr).children().eq(3).css("background-color", color);
                $(tr).children().eq(3).css("color", pathogenicity.includes("Strong") ? "white" : "black");
            }
            addEl(tbody, tr);
            addEl(div, addEl(table, tbody));
        }
    }
}
