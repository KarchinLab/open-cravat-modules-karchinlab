widgetGenerators['fathmm_mkl'] = {
    'variant': {
        'width': 400,
        'height': 120,
        'default_hidden': true,
        'function': function (div, row, tabName) {
            var rankscore = getWidgetData(tabName, 'fathmm_mkl', row, 'fathmm_mkl_coding_rankscore');
            if (rankscore == null) {
                var span = getEl('span');
                span.classList.add('nodata');
                addEl(div, addEl(span, getTn('No data')));
                return;
            }
            addInfoLine(div, 'FATHMM MKL Converted Rank Score', rankscore, tabName);
            var score = getWidgetData(tabName, 'fathmm_mkl', row, 'fathmm_mkl_coding_score');
            var pred = getWidgetData(tabName, 'fathmm_mkl', row, 'fathmm_mkl_coding_pred');
            var pp3 = getWidgetData(tabName, 'fathmm_mkl', row, 'pp3_pathogenic');
            var bp4 = getWidgetData(tabName, 'fathmm_mkl', row, 'bp4_benign');
            let acmg_pathogenicity = null;
            if (bp4) {
                acmg_pathogenicity = "BP4 " + bp4;
            } else if (pp3) {
                acmg_pathogenicity = "PP3 " + pp3;
            } else {
                acmg_pathogenicity = "Indeterminate";
            }
            var table = getWidgetTableFrame();
            addEl(div, table);
            var thead = getWidgetTableHead(['Score', 'Rank Score', 'Prediction', 'ACMG/AMP Pathogenicity'],['25%','22%','10%','12%', '30%']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([score, rankscore, pred, acmg_pathogenicity]);
            const color = getCalibrationGradientColor(acmg_pathogenicity);
            if (acmg_pathogenicity) {
                $(tr).children().eq(3).css("background-color", color);
                $(tr).children().eq(3).css("color", acmg_pathogenicity.includes("Strong") ? "white" : "black");
            }
            addEl(tbody, tr);
            addEl(div, addEl(table, tbody));
        }
    }
}
