widgetGenerators['oncokb'] = {
    'variant': {
        'width': 780,
        'height': 280,
        'function': function(div, row, tabName) {
            let all = getWidgetData(tabName, 'oncokb', row, 'all')
            let oncogenic = getWidgetData(tabName, 'oncokb', row, 'oncogenic')
            let knowneffect = getWidgetData(tabName, 'oncokb', row, 'knownEffect')
            let hotspot = getWidgetData(tabName, 'oncokb', row, 'hotspot')
            let pmid = getWidgetData(tabName, 'oncokb', row, 'pmids')
            let geneSummary = getWidgetData(tabName, 'oncokb', row, 'geneSummary')
            var variantSummary = getWidgetData(tabName, 'oncokb', row, 'variantSummary')
            if (knowneffect == null || knowneffect == undefined) {
                var span = getEl('span');
                span.classList.add('nodata');
                addEl(div, getEl("br"))
                addEl(div, addEl(span, getTn('No data')));
                return;
            }
            if (knowneffect != null || knowneffect != undefined) {
                var table = getWidgetTableFrame();
                table.id = "table"
                var buttons = ["general", "therapeutic", "diagnostic",  "prognostic"]
                for (var i = 0; i < buttons.length; i++) {
                    var button = getEl("button")
                    button.id = buttons[i]
                    button.style.border = 'none'
                    if (button.id == "general") {
                        var color = "#98d9e9"
                    } else {
                        var color = "lightgray"
                    }
                    button.style.backgroundColor = color
                    button.style.padding = '10px'
                    button.style.margin = '2px'
                    button.innerHTML = buttons[i].charAt(0).toUpperCase() + buttons[i].slice(1);
                    document.getElementById("widgetcontentdiv_oncokb_variant").appendChild(button);
                }
                var tbody = getEl('tbody');
                pmids = pmid !== null ? pmid.split('; ') : [];
                var thead = getWidgetTableHead(['Oncogenic', 'Known Effect', 'Hotspot', 'Gene Summary', 'Variant Summary', 'Pubmed'], ['10%', '10%', '10%', '25%', '25%', '10%']);
                addEl(table, thead);
                if (pmids.length > 0) {
                    var link = 'https://pubmed.ncbi.nlm.nih.gov/?term='
                    for (var p = 0; p < pmids.length; p++) {
                        var pubmed = pmids[p]
                        link = link + '(' + pubmed + '[pmid])+OR+'
                        if (p + 1 == pmids.length) {
                            link = link + '(' + pubmed + '[pmid])'
                        }
                    }
                    var tr = getWidgetTableTr([oncogenic, knowneffect, hotspot, geneSummary, variantSummary, link], [pmids]);
                    addEl(tbody, tr);
                } else {
                    var pubmed = ""
                    var link = ""
                    var tr = getWidgetTableTr([oncogenic, knowneffect, hotspot, geneSummary, variantSummary, link], [pubmed]);
                    addEl(tbody, tr);
                }
                var populateTab = function(thead, data) {
                    document.querySelector('#table').innerHTML = ""
                    var span = document.getElementsByClassName("nodata")
                    if (span[0] != undefined) {
                        span[0].parentNode.removeChild(span[0]);
                    }
                    if (data != undefined) {
                        if (data.length > 0) {
                            addEl(table, thead)
                            return data;
                        } else {
                            var span = getEl('span');
                            span.classList.add('nodata');
                            addEl(div, addEl(span, getTn('No data')));
                            return;
                        }
                    } else {
                        var span = getEl('span');
                        span.classList.add('nodata');
                        addEl(div, addEl(span, getTn('No data')));
                        return;
                    }

                }
                addEl(div, addEl(table, tbody));
                document.querySelector('#general').addEventListener('click', async e => {
                    var thead = getWidgetTableHead(['Oncogenic', 'Known Effect', 'Hotspot', 'Gene Summary', 'Variant Summary', 'Pubmed'], ['10%', '10%', '10%', '25%', '25%', '10%']);
                    document.querySelector("#general").style.backgroundColor = '#98d9e9'
                    var tbody = getEl('tbody');
                    document.querySelector("#therapeutic").style.backgroundColor = 'lightgray'
                    document.querySelector("#diagnostic").style.backgroundColor = 'lightgray'
                    document.querySelector("#prognostic").style.backgroundColor = 'lightgray'
                    row = populateTab(thead, knowneffect)
                    var links = []
                    var pubmeds = []
                    var link = 'https://pubmed.ncbi.nlm.nih.gov/?term='
                    if (pmids.length > 0) {
                        for (var p = 0; p < pmids.length; p++) {
                            var pubmed = pmids[p]
                            link = link + '(' + pubmed + '[pmid])+OR+'
                            if (p + 1 == pmids.length) {
                                link = link + '(' + pubmed + '[pmid])'
                            }
                        }
                        var tr = getWidgetTableTr([oncogenic, knowneffect, hotspot, geneSummary, variantSummary, link], [pmids]);
                        addEl(tbody, tr);

                    } else {
                        if (pubmed == undefined) {
                            var pubmed = ""
                            var link = ""
                            var tr = getWidgetTableTr([oncogenic, knowneffect, hotspot, geneSummary, variantSummary, link], [pubmed]);
                            addEl(tbody, tr);
                        }
                    }

                    addEl(div, addEl(table, tbody));
                })
                if (all != null || all != undefined) {
                    var results = JSON.parse(all);
                    var diagnostics = []
                    var therapeutics = []
                    var prognostics = []
                    for (var i = 0; i < results.length; i++) {
                        for (var j = 0; j < results[i].length; j++) {
                            var diagnostic = results[i][j]["diagnostic_data"];
                            if (diagnostic != undefined) {
                                diagnostics.push(diagnostic)
                            }
                            var therapeutic = results[i][j]["treatment_data"]
                            if (therapeutic != undefined) {
                                therapeutics.push(therapeutic)
                            }
                            var prognostic = results[i][j]["prognostic_data"]
                            if (prognostic != undefined) {
                                prognostics.push(prognostic)
                            }
                        }
                    }
                }
                document.querySelector('#therapeutic').addEventListener('click', async e => {
                    var thead = getWidgetTableHead(['NCIT Code', 'Drug Name', 'Pubmed', 'Level', 'Cancer Name', 'Tissue', 'Tumor Form'], ["10%", "20%","10%", "10%", "20%", "15%", "15%"]);
                    var tbody = getEl('tbody');
                    document.querySelector("#therapeutic").style.backgroundColor = '#98d9e9'
                    document.querySelector("#general").style.backgroundColor = 'lightgray'
                    document.querySelector("#diagnostic").style.backgroundColor = 'lightgray'
                    document.querySelector("#prognostic").style.backgroundColor = 'lightgray'
                    row = populateTab(thead, therapeutics)
                    if (row != undefined) {
                        for (var r = 0; r < row.length; r++) {
                            rows = row[r]
                            var link = "https://pubmed.ncbi.nlm.nih.gov/?term="
                            for (var i = 0; i < rows[3].length; i++) {
                                var pubmed = rows[3][i]
                                link = link + '(' + pubmed + '[pmid])+OR+'
                                if (i + 1 == rows[3].length) {
                                    link = link + '(' + pubmed + '[pmid])'
                                }
                            }
                            for (var j = 0; j < rows[0].length; j++) {
                                let link2 = `https://ncithesaurus.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&code=${rows[0][j]}`;
                                var tr = getWidgetTableTr([link2, rows[1][j], link, rows[3], rows[4], rows[5], rows[6]], [rows[0][j], rows[2]]);
                                addEl(tbody, tr);
                            }
                        }
                    }
                    addEl(div, addEl(table, tbody));
                })
                document.querySelector('#diagnostic').addEventListener('click', async e => {
                    var thead = getWidgetTableHead(['Dx Level', 'Tumor Type', 'Tumor Form', 'Pubmed'], ["10%", "40%", "25%", "25%"]);
                    row = populateTab(thead, diagnostics)
                    var tbody = getEl('tbody');
                    document.querySelector("#therapeutic").style.backgroundColor = 'lightgray'
                    document.querySelector("#general").style.backgroundColor = 'lightgray'
                    document.querySelector("#diagnostic").style.backgroundColor = '#98d9e9'
                    document.querySelector("#prognostic").style.backgroundColor = 'lightgray'
                    if (row != undefined) {
                        for (var r = 0; r < row.length; r++) {
                            rows = row[r]
                            var link = "https://pubmed.ncbi.nlm.nih.gov/?term="
                            for (var i = 0; i < rows[3].length; i++) {
                                var pubmed = rows[3][i]
                                link = link + '(' + pubmed + '[pmid])+OR+'
                                if (i + 1 == rows[3].length) {
                                    link = link + '(' + pubmed + '[pmid])'
                                }
                            }
                            var tr = getWidgetTableTr([rows[0], rows[1], rows[2], link], [rows[3]]);
                            addEl(tbody, tr);
                        }

                    }
                    addEl(div, addEl(table, tbody));
                })
                document.querySelector('#prognostic').addEventListener('click', async e => {
                    var thead = getWidgetTableHead(['Px Level', 'Tumor Type', 'Tumor Form', 'Tissue', 'Pubmed'], ["10%", "30%", "20%", "20%", "20%"]);
                    row = populateTab(thead, prognostics)
                    var tbody = getEl('tbody');
                    document.querySelector("#therapeutic").style.backgroundColor = 'lightgray'
                    document.querySelector("#general").style.backgroundColor = 'lightgray'
                    document.querySelector("#diagnostic").style.backgroundColor = 'lightgray'
                    document.querySelector("#prognostic").style.backgroundColor = '#98d9e9'
                    if (row != undefined) {
                        for (var r = 0; r < row.length; r++) {
                            rows = row[r]
                            var link = "https://pubmed.ncbi.nlm.nih.gov/?term="
                            for (var i = 0; i < rows[4].length; i++) {
                                var pubmed = rows[4][i]
                                link = link + '(' + pubmed + '[pmid])+OR+'
                                if (i + 1 == rows[4].length) {
                                    link = link + '(' + pubmed + '[pmid])'
                                }
                            }
                            var tr = getWidgetTableTr([rows[0], rows[1], rows[2], rows[3], link], [rows[4]]);
                            addEl(tbody, tr);
                        }
                    }
                    addEl(div, addEl(table, tbody));
                })
                addEl(div, addEl(table, tbody));

            }
        }
    }
}