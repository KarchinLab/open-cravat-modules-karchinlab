widgetGenerators['rankscore'] = {
    'gene': {
        'width': undefined,
        'height': 180,
        'variables': {},
        'init': function () {
            var v = this['variables'];
            var columnnames_to_show = {};
            var module_names_pretty = {}; // real module titles
            for (var i = 0; i < infomgr.colModels.variant.length; i++) {
                var cols = infomgr.colModels.variant[i].colModel;
                for (var j = 0; j < cols.length; j++) {
                    var col = cols[j];
                    if (col.col.includes("rank") || col.col.endsWith('rscore') || col.col.endsWith('_r')) {
                        var column = col.col;
                    } else {
                        continue;
                    }
                    var module_name = col.colgroupkey;
                    column = column.replace(module_name + '__', '');
                    columnnames_to_show[module_name] = column;
                    if (module_name === "phylop" || module_name === "phastcons") {
                        module_names_pretty[module_name] = col.colgroup + " (primate)"
                    } else {
                        module_names_pretty[module_name] = col.colgroup;
                    }
                    v['columnnames'] = columnnames_to_show
                    v['module_names_pretty'] = module_names_pretty;
                }
            }
            widgetGenerators['rankscore']['gene']['width'] = (Object.keys(columnnames_to_show).length + 1) * 100;
        },
        'function': function (div, row, tabName) {
            var v = this['variables'];
            var columnnames_to_show = v['columnnames'];
            var module_names_pretty = Object.values(v['module_names_pretty'])
            if (columnnames_to_show != undefined) {
                if (Object.keys(columnnames_to_show).length == 0) {
                    var span = getEl('span');
                    span.classList.add('nodata');
                    addEl(div, addEl(span, getTn('No data')));
                    return;
                }
                titlelength = [];
                var equallen = 100 / (Object.keys(module_names_pretty).length + 2);
                var extendlen = equallen + 5;
                var module_names = Object.keys(columnnames_to_show);
                titlelength.push(equallen + '%');
                titlelength.push(equallen + '%');
                for (var i = 0; i < module_names.length; i++) {
                    var modname = module_names[i]
                    if (modname.length > 12) {
                        titlelength.push(extendlen + '%')
                    } else {
                        titlelength.push(equallen + '%')
                    }
                }
                module_names_pretty.unshift('Protein variant');
                module_names_pretty.unshift('cDNA variant');
                const achange = getWidgetData('variant', 'base', row, 'achange');
                const cchange = getWidgetData('variant', 'base', row, 'cchange');
                var data = [cchange, achange]
                var nullScores = []
                for (let module in columnnames_to_show) {
                    if (columnnames_to_show.hasOwnProperty(module)) {
                        rankscore_col = columnnames_to_show[module];
                        var rankscore = getWidgetData('variant', module, row, rankscore_col);
                        if (rankscore !== null) {
                            rankscore = rankscore.toFixed(4)
                        }else {
                            nullScores.push(rankscore)
                        }
                        data.push(rankscore)
                    }
                }
                // if all scores are null just return "No data"
                if (nullScores.length === Object.keys(columnnames_to_show).length ) {
                    var span = getEl('span');
                    span.classList.add('nodata');
                    addEl(div, addEl(span, getTn('No data')));
                    return

                } else {
                    var table = getWidgetTableFrame();
                    addEl(div, table);
                    var thead = getWidgetTableHead(module_names_pretty, titlelength);
                    addEl(table, thead);
                    var tbody = getEl('tbody');
                    addEl(table, tbody);
                    tr = getEl('tr')
                    tr = getWidgetTableTr(data);
                    for (var i = 0; i < data.length; i++) {
                        var rankscore = data[i];
                        getGradientColor = function (start_color, end_color, percent) {
                            start_color = start_color.replace(/^\s*#|\s*$/g, '');
                            end_color = end_color.replace(/^\s*#|\s*$/g, '');

                            // convert 3 char codes --> 6, e.g. `E0F` --> `EE00FF`
                            if (start_color.length == 3) {
                                start_color = start_color.replace(/(.)/g, '$1$1');
                            }

                            if (end_color.length == 3) {
                                end_color = end_color.replace(/(.)/g, '$1$1');
                            }
                            // get colors
                            var start_red = parseInt(start_color.substr(0, 2), 16),
                                start_green = parseInt(start_color.substr(2, 2), 16),
                                start_blue = parseInt(start_color.substr(4, 2), 16);

                            var end_red = parseInt(end_color.substr(0, 2), 16),
                                end_green = parseInt(end_color.substr(2, 2), 16),
                                end_blue = parseInt(end_color.substr(4, 2), 16);
                            // calculate new color
                            var diff_red = end_red - start_red;
                            var diff_green = end_green - start_green;
                            var diff_blue = end_blue - start_blue;
                            diff_red = ((diff_red * percent) + start_red).toString(16).split('.')[0];
                            diff_green = ((diff_green * percent) + start_green).toString(16).split('.')[0];
                            diff_blue = ((diff_blue * percent) + start_blue).toString(16).split('.')[0];
                            // ensure 2 digits by color
                            if (diff_red.length == 1) diff_red = '0' + diff_red
                            if (diff_green.length == 1) diff_green = '0' + diff_green
                            if (diff_blue.length == 1) diff_blue = '0' + diff_blue

                            return '#' + diff_red + diff_green + diff_blue;
                        };
                        var color = getGradientColor('#FFFFFF', '#FF0000', rankscore);
                        $(tr).children().eq(i).css("background-color", color);
                        // too dark of red, show white text
                        if (rankscore > 0.70) {
                            $(tr).children().eq(i).css("color", "white");
                        } else {
                            $(tr).children().eq(i).css("color", "black");
                        }
                        addEl(tbody, tr);
                        addEl(div, addEl(table, tbody));
                    }
                }
            }
        }
    }
}
