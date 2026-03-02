widgetGenerators['dann_coding'] = {
    'variant': {
    'width': 400,
    'height': 120,
    'default_hidden': true,
    'function': function(div, row, tabName) {
            var score = getWidgetData(tabName, 'dann_coding', row, 'dann_coding_score');
            var rscore = getWidgetData(tabName, 'dann_coding', row, 'dann_coding_rscore');
            if (score == null) {
                var span = getEl('span');
                span.classList.add('nodata');
                addEl(div, addEl(span, getTn('No data')));
                return;
            }
            var pp3 = getWidgetData(tabName, 'dann_coding', row, 'pp3_pathogenic');
            var bp4 = getWidgetData(tabName, 'dann_coding', row, 'bp4_benign');
            let acmg_pathogenicity = "Indeterminate";
            if (bp4) {
                acmg_pathogenicity = "BP4 " + bp4;
            } else if (pp3) {
                acmg_pathogenicity = "PP3 " + pp3;
            }
            var table = getWidgetTableFrame();
            addEl(div, table);
            var thead = getWidgetTableHead(['Score', 'Rank Score', 'ACMG/AMP Pathogenicity']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([score, rscore, acmg_pathogenicity]);
            const color = getCalibrationGradientColor(acmg_pathogenicity);
            if (acmg_pathogenicity) {
                $(tr).children().eq(2).css("background-color", color);
                $(tr).children().eq(2).css("color", acmg_pathogenicity.includes("Strong") ? "white" : "black");
            }
            addEl(tbody, tr);
            addEl(div, addEl(table, tbody));
       }
    }
}
