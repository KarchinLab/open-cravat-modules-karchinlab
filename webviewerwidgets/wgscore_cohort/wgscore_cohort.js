$.getScript('/result/widgetfile/wgscore_cohort/plotly-2.16.1.min.js', function() {});
widgetGenerators['score_cohort'] = {
    'cohort': {
        'name': 'Most Frequently Mutated Genes (normalized by gene length and sorted by % samples mutated)',
        'width': 600,
        'height': 780,
        'callserver': true,
        'default_hidden': false,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'function': function(div, dummy) {
            function createButton(range) {
                if (range.length < 2) {
                    return null;
                } else {
                    for (var i = 0; i < range.length; i++) {
                        var button = document.createElement('button');
                        button.id = range[i] + '_score';
                        button.innerHTML = "Group" + range[i];
                        button.classList.add("butn");
                        button.style.position = "relative"
                        document.getElementById("widgetcontentdiv_score_cohort_info").appendChild(button);
                    }
                }
            }

            function plotData(modules, id) {
                var chartDiv = document.getElementById("widgetcontentdiv_score_cohort_info");
                var containerDiv = getEl('div')
                containerDiv.setAttribute("id", "plot")
                containerDiv.style.display = "Flex";
                containerDiv.style.flexWrap = "wrap";
                modules = Array.from(modules);
                var toAdd = document.createDocumentFragment();
                for (var m in modules) {
                    var module = modules[m]
                    var layout = {
                        title: {
                            text: modTitle[module],
                        },
                        width: 250,
                        height: 250,
                        margin: {
                            l: 50,
                            r: 50,
                            b: 50,
                            t: 50,
                            pad: 4
                        },

                    };
                    var newDatasets = []
                    var newDiv = document.createElement('div');
                    newDiv.id = module
                    toAdd.appendChild(newDiv);
                    document.getElementById('widgetcontentdiv_score_cohort_info').appendChild(toAdd);

                    for (var j in initDatasets) {
                        var adiv = document.getElementById(module)
                        if (initDatasets[j]['module'] == module) {
                            if (initDatasets[j]['group'] + '_score' == id) {
                                newDatasets.push({
                                    'y': initDatasets[j]['y'],
                                    'type': 'box',
                                    'name': initDatasets[j]['name']
                                });
                            } else if (id == "start") {
                                if (initDatasets[j]['group'] + 'score' == '1score') {
                                    newDatasets.push({
                                        'y': initDatasets[j]['y'],
                                        'type': 'box',
                                        'name': initDatasets[j]['name']
                                    });
                                }
                            }
                        }
                    }
                    Plotly.newPlot(adiv, newDatasets, layout);
                    addEl(chartDiv, containerDiv)
                    addEl(containerDiv, adiv)
                }
                var elem = document.getElementById('widgetcontentdiv_score_cohort_info').getElementsByTagName("button")
                for (var i = 0; i < elem.length; i++) {
                    elem[i].onclick = function() {
                        $("#plot").remove();
                        plotData(modules, this.id)
                    };
                }
            }
            var data = this['variables']['data'];
            var modTitle = {}
            for (var i = 0; i < infomgr.colModels.variant.length; i++) {
                var name = infomgr.colModels.variant[i].name;
                var title = infomgr.colModels.variant[i].title;
                modTitle[name] = title;
            }
            var numGroups = []
            var initDatasets = [];
            const modules = new Set();
            for (var set in data) {
                numGroups.push(Number(set))
                var row = data[set][0];
                for (var cohort in row) {
                    var scores = row[cohort];
                    for (var module in scores[0]) {
                        modules.add(module)
                        initDatasets.push({
                            'y': scores[0][module],
                            'type': 'box',
                            'name': cohort,
                            'group': set,
                            'module': module
                        });
                    }
                }
            }
            createButton(numGroups)
            plotData(modules, 'start')
        }
    }
}