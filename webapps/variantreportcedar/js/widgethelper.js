var widgetGenerators = {};
var widgetTableBorderStyle = '1px solid gray';
var widgetGridSize = 10;

function getWidgetTableFrame() {
    var table = getEl('table');
    //table.style.fontSize = '12px';
    table.style.borderSpacing = '0px';
    table.style.borderCollapse = 'collapse';
    //table.style.borderTop = widgetTableBorderStyle;
    table.style.borderBottom = widgetTableBorderStyle;
    table.style.tableLayout = 'fixed';
    table.style['word-break'] = 'break-all';
    table.style.width = 'calc(100% - 0px)';
    table.style['table-layout'] = 'fixed';
    return table;
}

function getWidgetTableHead(headers, widths) {
    var thead = getEl('thead');
    thead.style.textAlign = 'left';
    thead.style['word-break'] = 'normal';
    thead.style.borderBottom = widgetTableBorderStyle;
    var tr = getEl('tr');
    var numBorder = headers.length - 1;
    for (var i = 0; i < headers.length; i++) {
        var th = getEl('th');
        if (i < numBorder) {
            th.style.borderRight = widgetTableBorderStyle;
        }
        if (widths != undefined) {
            th.style.width = widths[i];
        }
        addEl(th, getTn(headers[i]));
        addEl(tr, th);
    }
    addEl(thead, tr);
    return thead;
}

function getWidgetTableHeadTooltips(content) {
    var thead = getEl('thead');
    thead.style.textAlign = 'left';
    thead.style['word-break'] = 'normal';
    thead.style.borderBottom = widgetTableBorderStyle;
    var tr = getEl('tr');
    content.map((header) => {
        var th = getEl('th');
        if (header.info) {
            th.classList.add("th_tooltip")
            var div = getEl("div")
            div.setAttribute("id", `${header.id}_info`)
            div.classList.add("hide_tooltip")
            div.textContent = header.info
            addEl(thead, div)
            th.addEventListener('mouseover', function (evt) {
                var el = document.getElementById(`${header.id}_info`)
                el.classList.remove("hide_tooltip")
                el.classList = "show_tooltip"
            });
            th.addEventListener('mouseout', function (evt) {
                var el = document.getElementById(`${header.id}_info`)
                el.classList.remove("show_tooltip")
                el.classList = "hide_tooltip"
            });
        }
        addEl(th, getTn(header.label));
        addEl(tr, th);
    })
    addEl(thead, tr);
    return thead;
}

function getWidgetTableTr(values, linkNames) {
    var numBorder = values.length - 1;
    var linkNameItr = 0;
    var tr = getEl('tr');
    //tr.style.borderBottom = '1px solid #cccccc';
    for (var i = 0; i < values.length; i++) {
        var td = getEl('td');
        var p = getEl('p');
        p.style.wordBreak = 'break-word';
        if (i < numBorder) {
            td.style.borderRight = widgetTableBorderStyle;
        }
        var value = values[i];
        if (value == null) {
            value = '';
        }
        if (typeof value == 'string' && value.startsWith('http')) {
            spanText = document.createElement('a');
            spanText.href = value;
            spanText.target = '_blank';
            if (linkNames != undefined) {
                addEl(td, addEl(spanText, getTn(linkNames[linkNameItr])));
                linkNameItr += 1;
            } else {
                addEl(td, addEl(spanText, getTn('View')));
            }
        } else {
            addEl(td, addEl(p, getTn(value)));
        }
        addEl(tr, td);
    }
    return tr;
}

function getWidgetTableTr2(values, linkNames) {
    var numBorder = values.length - 1;
    var linkNameItr = 0;
    var tr = getEl('tr');
    //tr.style.borderBottom = '1px solid #cccccc';
    for (var i = 0; i < values.length; i++) {
        var td = getEl('td');
        var p = getEl('p');
        p.style.wordBreak = 'break-word';
        if (i < numBorder) {
            td.style.borderRight = widgetTableBorderStyle;
        }
        var value = values[i];
        if (value == null) {
            value = '';
        }
        if (typeof value == 'string' && value.startsWith('http')) {
            spanText = document.createElement('a');
            spanText.href = value;
            spanText.target = '_blank';
            spanText.classList.add('linkclass')
            if (linkNames != undefined) {
                addEl(td, addEl(spanText, getTn(linkNames[linkNameItr])));
                linkNameItr += 1;
            } else {
                addEl(td, addEl(spanText, getTn('View')));
            }
        } else {
            addEl(td, addEl(p, getTn(value)));
        }
        addEl(tr, td);
    }
    return tr;
}

function addInfoLine(div, row, header, col, tabName, headerMinWidth, highlightIfValue) {
    var text = null;
    if (typeof(row) != 'object') {
        text = header;
        header = row;
        headerMinWidth = tabName;
        tabName = col;
    } else {
        text = infomgr.getRowValue(tabName, row, col);
    }
    var color = 'black';
    if (text == undefined || text == '') {
        color = '#cccccc';
    }
    var table = getEl('table');
    table.style.fontSize = '12px';
    table.style.borderCollapse = 'collapse';
    var tr = getEl('tr');
    var td = getEl('td');
    td.className = 'detail-info-line-header';
    if (headerMinWidth != undefined) {
        td.style.minWidth = headerMinWidth;
    }
    var h = getLineHeader(header);
    h.style.color = color;
    addEl(td, h);
    addEl(tr, td);
    td = getEl('td');
    td.className = 'detail-info-line-content';
    var t = getEl('span');
    t.textContent = text;
    t.style.color = color;
    addEl(td, t);
    addEl(tr, td);
    if (highlightIfValue != undefined && highlightIfValue) {
        tr.style.color = '#ff0000';
    }
    addEl(table, tr);
    addEl(div, table);
}

function addInfoLineText(div, header, text) {
    addEl(div, getLineHeader(header));
    var spanText = document.createElement('span');
    if (text == undefined || text == null) {
        text = '';
    } else {
        var textLengthCutoff = 16;
        if (text.length > textLengthCutoff) {
            spanText.title = text;
            text = text.substring(0, textLengthCutoff) + '...';
        }
    }
    addEl(spanText, getTn(text));
    addEl(div, spanText);
    addEl(div, getEl('br'));
}

function addInfoLineLink(div, header, text, link, trimlen) {
    var span = getLineHeader(header);
    span.classList.add('detail-info-line-header');
    addEl(div, span);
    var spanText = null;
    if (link == undefined || link == null) {
        text = '';
        spanText = document.createElement('span');
    } else {
        spanText = document.createElement('a');
        spanText.href = link;
        spanText.target = '_blank';
        if (trimlen > 0) {
            if (text.length > trimlen) {
                spanText.title = text;
                text = text.substring(0, trimlen) + '...';
            }
        }
    }
    addEl(spanText, getTn(text));
    addEl(div, spanText);
    addEl(div, getEl('br'));
}

function addBarComponent2(outerDiv, row, header, col, tabName, barWidth, grayIfNoValue, threshold, beginText, endText, maxVal) {
    if (maxVal == undefined) {
        maxVal = 1.0
    }
    var cutoff = threshold
    // Value
    var value = null;
    if (typeof(row) === 'object' && row.constructor == Object) {
        value = row[col];
    } else {
        value = infomgr.getRowValue(tabName, row, col);
    }
    if (value == null) {
        value = '';
    } else {
        if (value == 0) {
            value = '0'
        } else if (value >= 0.01) {
            value = value.toFixed(3);
        } else {
            value = value.toExponential(1);
        }
    }
    var color = 'black';
    if (value == '') {
        color = '#aaaaaa';
    }
    var thresholdColor = '#888888';
    // Div
    var div = getEl('div');
    addEl(outerDiv, div);
    div.style.display = 'inline-block';
    div.style.margin = '2px';
    div.style.color = color;
    // Header
    if (header != null) {
        addEl(div, addEl(getEl('span'), getTn(header)));
    }
    // Paper
    if (barWidth == undefined) {
        barWidth = 200;
    }
    var paddingX = 20;
    var paddingTop = 20;
    var paddingBottom = 40;
    var barHeight = 12;
    var lineWidth = 0.25;
    var lineOverhang = 15;
    var thresholdLineHalfHeight = 10;
    var valueHeight = barHeight + (2 * lineOverhang);
    var paperWidth = barWidth + paddingX * 2;
    var paperHeight = valueHeight + paddingTop + paddingBottom;
    var subDiv = document.createElement('div');
    addEl(div, subDiv);
    subDiv.style.width = paperWidth + 'px';
    subDiv.style.height = paperHeight + 'px';
    var allele_frequencies_map_config = {};
    var paper = Raphael(subDiv, paperWidth, paperHeight);
    // Box. Red color maxes at 0.3.
    var box = paper.rect(paddingX, lineOverhang + paddingTop,
        barWidth, barHeight, 5);
    var b = box.getBBox();
    var c = null;
    if (value != '') {
        if (value < threshold) {
            c = 255
        } else {
            c = (1.0 - (value - threshold) / (maxVal - threshold)) * 255;
        }
    } else {
        c = 255;
    }
    var valueColor = 'rgb(255, ' + c + ', ' + c + ')';
    console.log('@ value=', value, 'c=', c, 'color=', color, 'valuecolor=', valueColor)
    box.attr('stroke', color);
    box.attr('fill', valueColor);
    // Value
    if (value != '') {
        var valueX = value * barWidth + paddingX;
        var bar = paper.rect(valueX, paddingTop, 1, valueHeight, lineWidth);
        bar.attr('fill', color);
        bar.attr('stroke', color);
        var text = paper.text(valueX, 8, value);
        text.attr('fill', color);
        text.attr('stroke', color);
    }
    // Threshold
    if (threshold != null) {
        var thresholdX = threshold * barWidth + paddingX;
        var bar = paper.rect(thresholdX,
            lineOverhang - thresholdLineHalfHeight + paddingTop,
            1, barHeight + thresholdLineHalfHeight * 2, lineWidth);
        //bar.attr('fill', thresholdColor);
        //bar.attr('stroke', thresholdColor);
        var text = paper.text(thresholdX, valueHeight, threshold + ' threshold');
        //text.attr('fill', thresholdColor);
        //text.attr('stroke', thresholdColor);
    }
    // Begin text
    if (beginText != null) {
        var text = paper.text(paddingX,
                paperHeight / 2 - 4, beginText)
            .attr('text-anchor', 'start');
        /*text.attr('fill', thresholdColor);
        text.attr('stroke', thresholdColor);
		var bar = paper.rect(paddingX, 
                paddingTop + lineOverhang + barHeight + lineOverhang, 
                0.5, paddingBottom / 2, 1);
        bar.attr('fill', thresholdColor);
        bar.attr('stroke', thresholdColor);*/
    }
    // End text
    if (endText != null) {
        var text = paper.text(paperWidth - paddingX,
                paperHeight / 2 - 4, endText)
            .attr('text-anchor', 'end');
        /*text.attr('fill', thresholdColor);
        text.attr('stroke', thresholdColor);
		var bar = paper.rect(paperWidth - paddingX, 
                paddingTop + lineOverhang + barHeight + lineOverhang, 
                0.5, paddingBottom / 2, 1);
        bar.attr('fill', thresholdColor);
        bar.attr('stroke', thresholdColor);*/
    }
    if (beginText != null && endText != null) {
        var centerY = paperHeight - 11;
        var arrowStartX = paddingX + barWidth / 3;
        var arrowEndX = paddingX + barWidth / 3 * 2;
        var bar = paper.path('M' + arrowStartX + ',' + centerY +
                'L' + arrowEndX + ',' + centerY)
            .attr('width', 0.25);
        var bar = paper.path('M' + arrowEndX + ',' + centerY +
                'L' + (arrowEndX - 5) + ',' + (centerY - 5))
            .attr('width', 0.25);
        var bar = paper.path('M' + arrowEndX + ',' + centerY +
                'L' + (arrowEndX - 5) + ',' + (centerY + 5))
            .attr('width', 0.25);
        /*
		var bar = paper.rect(paddingX + barWidth / 3 + barWidth / 3, centerY,
                barWidth / 3, 0.25, 0);
        bar.attr('stroke', '#000000');
		var bar = paper.rect(paddingX + barWidth / 3, centerY,
                barWidth / 3, 0.25, 0);
        bar.attr('stroke', '#000000');
        */
    }
    return paper;
}

function addBarComponent(outerDiv, row, header, col, tabName, barWidth, grayIfNoValue, cutoff) {
    //var cutoff = 0.01;
    var barStyle = {
        "top": 0,
        "height": lineHeight,
        "width": 1,
        "fill": 'black',
        "stroke": 'black',
        "round_edge": 1
    };

    // Value
    var value = null;
    if (typeof(row) === 'object' && row.constructor == Object) {
        value = row[col];
    } else {
        value = infomgr.getRowValue(tabName, row, col);
    }
    if (value == null) {
        value = '';
    } else {
        if (value == 0) {
            value = '0'
        } else if (value >= 0.01) {
            value = value.toFixed(3);
        } else {
            value = value.toExponential(1);
        }
    }
    var color = 'black';
    if (value == '') {
        color = '#aaaaaa';
    }

    // Div
    var div = getEl('div');
    div.style.display = 'inline-block';
    div.style.margin = '2px';
    div.style.color = color;

    // Header
    var sdiv = getEl('div')
    sdiv.style.fontSize = '0.9rem'
    addEl(sdiv, addEl(getEl('span'), getTn(header + ': ')));
    addEl(sdiv, addEl(getEl('span'), getTn(value)));
    addEl(div, sdiv)
    //addEl(div, getEl('br'));

    // Paper
    if (barWidth == undefined) {
        barWidth = 108;
    }
    var barHeight = 12;
    var lineOverhang = 3;
    var lineHeight = barHeight + (2 * lineOverhang);
    var paperHeight = lineHeight + 4;
    var subDiv = document.createElement('div');
    addEl(div, subDiv);
    subDiv.style.width = (barWidth + 10) + 'px';
    subDiv.style.height = paperHeight + 'px';
    var allele_frequencies_map_config = {};
    var paper = Raphael(subDiv, barWidth, paperHeight);

    // Box. Red color maxes at 0.3.
    var box = paper.rect(0, lineOverhang, barWidth, barHeight, 4);
    var c = null;
    if (value != '') {
        c = (1.0 - Math.min(1.0, value / 0.3)) * 255;
    } else {
        c = 255;
    }
    box.attr('fill', 'rgb(255, ' + c + ', ' + c + ')');
    box.attr('stroke', color);

    // Bar
    if (value != '') {
        var bar = paper.rect(value * barWidth, 0, 1, lineHeight, 1);
        bar.attr('fill', color);
        bar.attr('stroke', color);
    }

    addEl(outerDiv, div);
}

//Default color gradeint is white to red from 0.0 to 1.0
function addGradientBarComponent(outerDiv, row, header, col, tabName, colors = {
    '0.0': [255, 255, 255],
    '1.0': [255, 0, 0]
}, minval = 0.0, maxval = 1.0) {
    var cutoff = 0.01;
    var barStyle = {
        "top": 0,
        "height": lineHeight,
        "width": 1,
        "fill": 'black',
        "stroke": 'black',
        "round_edge": 1
    };

    var dtype = null;
    var orderedPivots = [];
    for (pivot in colors) {
        orderedPivots.push(pivot)
    }
    orderedPivots.sort(function(a, b) {
        return a - b
    })

    // Value
    var value = null;
    if (typeof(row) === 'object' && row.constructor == Object) {
        value = row[col];
    } else {
        value = infomgr.getRowValue(tabName, row, col);
    }
    if (value == null) {
        value = '';
    } else if (typeof value == 'string') {
        dtype = 'string'
    } else {
        value = value.toFixed(3);
    }

    // Div
    var div = getEl('div');
    div.style.display = 'inline-block';
    div.style.margin = '2px';

    // Header
    var span = getEl('span');
    addEl(div, addEl(span, getTn(header + ': ')));
    if (value == undefined || value == '') {
        span.classList.add('nodata');
    }
    var span = getEl('span');
    addEl(div, addEl(span, getTn(value)));
    if (value == undefined || value == '') {
        span.classList.add('nodata');
    }
    addEl(div, getEl('br'));
    if (value !== '') {
        value = parseFloat(value);
    }

    // Paper
    var barWidth = 108;
    var barHeight = 12;
    var lineOverhang = 3;
    var lineHeight = barHeight + (2 * lineOverhang);
    var paperHeight = lineHeight + 4;
    var subDiv = document.createElement('div');
    addEl(div, subDiv);
    subDiv.style.width = (barWidth + 10) + 'px';
    subDiv.style.height = paperHeight + 'px';
    var allele_frequencies_map_config = {};
    var paper = Raphael(subDiv, barWidth, paperHeight);

    // Box.
    var box = paper.rect(0, lineOverhang, barWidth, barHeight, 4);
    var c = [];
    if (value !== '') {
        if (value <= orderedPivots[0]) {
            var piv = orderedPivots[0];
            c = colors['%s', piv];
        } else if (value >= orderedPivots[orderedPivots.length - 1]) {
            var piv = orderedPivots[orderedPivots.length - 1];
            c = colors['%s', piv];
        } else {
            var boundColors = {
                color1: [],
                color2: []
            };
            var boundPivots = [];
            for (var i = 0; i < (orderedPivots.length - 1); i++) {
                if (orderedPivots[i] <= value && value < orderedPivots[i + 1]) {
                    boundPivots[0] = orderedPivots[i];
                    boundPivots[1] = orderedPivots[i + 1];
                    boundColors.color1 = colors[boundPivots[0]];
                    boundColors.color2 = colors[boundPivots[1]];
                    break;
                }
            }
            //semi-broken when values are negative
            var ratio = (value - boundPivots[0]) / (boundPivots[1] - boundPivots[0]);
            c[0] = Math.round(boundColors.color1[0] * (1.0 - ratio) + boundColors.color2[0] * ratio);
            c[1] = Math.round(boundColors.color1[1] * (1.0 - ratio) + boundColors.color2[1] * ratio);
            c[2] = Math.round(boundColors.color1[2] * (1.0 - ratio) + boundColors.color2[2] * ratio);
        }

    } else {
        c = [255, 255, 255];
    }
    box.attr('fill', 'rgb(' + c.toString() + ')');
    if (value == undefined || value == '') {
        color = '#cccccc';
    } else {
        color = 'black';
    }
    box.attr('stroke', color);

    // Bar
    if (value !== '' && dtype != 'string') {
        //Convert values onto 0 to 1 scale depending on min and max val provided (defaults to 0 and 1)
        value = (value - parseFloat(minval)) / (Math.abs(parseFloat(minval)) + Math.abs(parseFloat(maxval)));
        var bar = paper.rect(value * barWidth, 0, 1, lineHeight, 1);
        bar.attr('fill', color);
        bar.attr('stroke', color);
    }

    addEl(outerDiv, div);
}

function getLineHeader(header) {
    var spanHeader = document.createElement('span');
    spanHeader.classList.add('detail-info-line-header');
    spanHeader.appendChild(document.createTextNode('  ' + header + ': '));
    return spanHeader;
}

function getDetailWidgetDivs(tabName, widgetName, title, maxWidth, maxHeight, showTitle) {
    var div = document.createElement('fieldset');
    div.id = 'detailwidget_' + tabName + '_' + widgetName;
    div.className = 'detailwidget';
    var width = null;
    var height = null;
    var maxWidth = null;
    var maxHeight = null;
    var top = null;
    var left = null;
    var wordBreak = 'break-all';
    if (typeof(viewerWidgetSettings) != 'undefined' && viewerWidgetSettings['info'] != undefined) {
        for (var i = 0; i < viewerWidgetSettings['info'].length; i++) {
            var setting = viewerWidgetSettings['info'][i];
            if (setting['widgetkey'] == widgetName) {
                if (setting['width'] != undefined) {
                    width = parseInt(setting['width'].replace('px', ''));
                }
                if (setting['max-height'] != undefined) {
                    maxHeight = parseInt(setting['max-height'].replace('px', ''));
                }
                if (setting['height'] != undefined) {
                    height = parseInt(setting['height'].replace('px', ''));
                }
                if (setting['word-break'] != undefined) {
                    wordBreak = setting['word-break'];
                }
                top = setting['top'];
                left = setting['left'];
                break;
            }
        }
    } else {
        width = widgetGenerators[widgetName][tabName]['width'];
        height = widgetGenerators[widgetName][tabName]['height'];
        maxWidth = widgetGenerators[widgetName][tabName]['max-width'];
        maxHeight = widgetGenerators[widgetName][tabName]['max-height'];
        if (widgetGenerators[widgetName][tabName]['word-break'] != undefined) {
            wordBreak = widgetGenerators[widgetName][tabName]['word-break'];
        }
    }
    var maxWidthFieldset = maxWidth;
    if (maxWidth != undefined && maxWidth != null) {
        div.style.maxWidth = maxWidthFieldset + 'px';
    } else {
        div.clientWidth = width;
        div.style.width = width + 'px';
    }
    var maxHeightFieldset = maxHeight + 30;
    if (maxHeight != undefined && maxHeight != null) {
        div.style.maxHeight = maxHeightFieldset + 'px';
    } else {
        div.clientHeight = height;
        div.style.height = height + 'px';
    }
    div.style.wordBreak = wordBreak;
    if (top) {
        div.style.top = top;
    }
    if (left) {
        div.style.left = left;
    }
    div.setAttribute('widgetkey', widgetName);

    // Header
    var header = getEl('div');
    header.className = 'detailwidgetheader';
    addEl(div, header);

    // Title
    var titleDiv = getEl('legend');
    titleDiv.className = 'detailwidgettitle';
    titleDiv.style.cursor = 'move';
    addEl(header, addEl(titleDiv, getTn(title)));

    // Div for pin and x icons
    var iconDiv = getEl('div');
    iconDiv.className = 'detailwidgeticondiv';
    addEl(header, iconDiv);

    // Help button
    if (widgetInfo[widgetName]['helphtml_exists']) {
        var btn = getEl('span');
        btn.className = 'detailwidgetpinbutton';
        btn.style.position = 'relative';
        btn.style.top = '-4px';
        btn.style.backgroundColor = 'white';
        btn.textContent = '\u2754';
        btn.addEventListener('click', function(evt) {
            onClickWidgetHelpButton(evt, tabName);
        });
        addEl(iconDiv, btn);
    }

    // Camera button
    var button = getEl('img');
    button.src = '/result/images/camera.png';
    button.className = 'detailwidget-camerabutton';
    button.setAttribute('widgetname', widgetName);
    button.addEventListener('click', function(evt) {
        onClickWidgetCameraButton(tabName, evt);
    });
    addEl(iconDiv, button);

    // Pin button
    var pinButton = getEl('img');
    pinButton.src = '/result/images/pin.png';
    pinButton.className = 'detailwidgetpinbutton';
    pinButton.classList.add('unpinned');
    pinButton.setAttribute('widgetname', widgetName);
    pinButton.addEventListener('click', function(evt) {
        onClickWidgetPinButton(evt, tabName);
    });
    addEl(iconDiv, pinButton);

    // Close button
    var closeButton = getEl('img');
    closeButton.src = '/result/images/close-button.png';
    closeButton.className = 'detailwidget-closebutton';
    closeButton.setAttribute('widgetname', widgetName);
    closeButton.addEventListener('click', function(evt) {
        onClickWidgetCloseButton(tabName, evt);
    });
    addEl(iconDiv, closeButton);

    /*
	var hr = getEl('hr');
    hr.className = 'detailwidget-hr';
	addEl(div, hr);
    */
    if (showTitle == false) {
        header.style.display = 'none';
    }

    // Content div
    var detailContentDiv = getEl('div');
    detailContentDiv.id = 'widgetcontentdiv_' + widgetName + '_' + tabName;
    detailContentDiv.className = 'detailcontentdiv';
    //detailContentDiv.style.height = 'calc(100% - 32px)';
    //detailContentDiv.style.padding = '0px';
    if (maxHeight != undefined && maxHeight != null) {
        detailContentDiv.style.maxHeight = maxHeight + 'px';
        detailContentDiv.style.overflow = 'auto';
    }
    addEl(div, detailContentDiv);

    return [div, detailContentDiv];
}

function getWidgetData(tabName, moduleName, row, col) {
    if (row == null) {
        return null;
    }
    if (typeof(row) === 'object' && row.constructor == Object) {
        return row[moduleName + '__' + col];
    } else {
        return infomgr.getRowValue(tabName, row, moduleName + '__' + col);
    }
}

function getSpinner() {
    var spinner = getEl('img');
    spinner.src = '/result/images/spinner.gif';
    spinner.style.width = '15px';
    return spinner;
}

function addGradientStopBarComponent(outerDiv, row, header, col, tabName, colors = {
    '0.0': [255, 255, 255],
    '1.0': [255, 0, 0]
}, minval = 0.0, maxval = 1.0) {
    var cutoff = 0.01;
    var barStyle = {
        "top": 0,
        "height": lineHeight,
        "width": 1,
        "fill": 'black',
        "stroke": 'black',
        "round_edge": 1
    };

    var dtype = null;
    var orderedPivots = [];
    for (pivot in colors) {
        orderedPivots.push(pivot)
    }
    orderedPivots.sort(function(a, b) {
        return a - b
    })

    // Value
    var value = null;
    if (typeof(row) === 'object' && row.constructor == Object) {
        value = row[col];
    } else {
        value = infomgr.getRowValue(tabName, row, col);
    }
    if (value == null) {
        value = '';
    } else if (typeof value == 'string') {
        dtype = 'string'
    } else {
        value = value.toFixed(3);
    }
    // Div
    var div = getEl('div');
    div.style.display = 'inline-block';
    div.style.margin = '2px';

    // Header
    var span = getEl('span');
    addEl(div, addEl(span, getTn(header + ': ')));
    if (value == undefined || value == '') {
        span.classList.add('nodata');
    }
    var span = getEl('span');
    addEl(div, addEl(span, getTn(value)));
    if (value == undefined || value == '') {
        span.classList.add('nodata');
    }
    addEl(div, getEl('br'));
    if (value !== '') {
        value = parseFloat(value);
    }

    // Paper
    var barWidth = 108;
    var barHeight = 12;
    var lineOverhang = 3;
    var lineHeight = barHeight + (2 * lineOverhang);
    var paperHeight = lineHeight + 4;
    var subDiv = document.createElement('div');
    addEl(div, subDiv);
    subDiv.style.width = (barWidth + 10) + 'px';
    subDiv.style.height = paperHeight + 'px';
    var allele_frequencies_map_config = {};
    var paper = Raphael(subDiv, barWidth, paperHeight);

    // Box with remainder white
    var box = paper.rect(0, lineOverhang, barWidth, barHeight, 4);
    box.attr('fill', 'white');

    // Box.
    var value = (value - parseFloat(minval)) / (Math.abs(parseFloat(minval)) + Math.abs(parseFloat(maxval)));
    var box = paper.rect(0, lineOverhang, value * barWidth, barHeight, 4);
    var c = [];
    if (value !== '') {
        if (value <= orderedPivots[0]) {
            var piv = orderedPivots[0];
            c = colors['%s', piv];
        } else if (value >= orderedPivots[orderedPivots.length - 1]) {
            var piv = orderedPivots[orderedPivots.length - 1];
            c = colors['%s', piv];
        } else {
            var boundColors = {
                color1: [],
                color2: []
            };
            var boundPivots = [];
            for (var i = 0; i < (orderedPivots.length - 1); i++) {
                if (orderedPivots[i] <= value && value < orderedPivots[i + 1]) {
                    boundPivots[0] = orderedPivots[i];
                    boundPivots[1] = orderedPivots[i + 1];
                    boundColors.color1 = colors[boundPivots[0]];
                    boundColors.color2 = colors[boundPivots[1]];
                    break;
                }
            }
            //semi-broken when values are negative
            var ratio = (value - boundPivots[0]) / (boundPivots[1] - boundPivots[0]);
            c[0] = Math.round(boundColors.color1[0] * (1.0 - ratio) + boundColors.color2[0] * ratio);
            c[1] = Math.round(boundColors.color1[1] * (1.0 - ratio) + boundColors.color2[1] * ratio);
            c[2] = Math.round(boundColors.color1[2] * (1.0 - ratio) + boundColors.color2[2] * ratio);
        }

    } else {
        c = [255, 255, 255];
    }
    box.attr('fill', 'rgb(' + c.toString() + ')');
    if (value == undefined || value == '') {
        color = '#cccccc';
    } else {
        color = 'black';
    }
    box.attr('stroke', color);

    // Bar.
    if (value !== '' && dtype != 'string') {
        //Convert values onto 0 to 1 scale depending on min and max val provided (defaults to 0 and 1)
        value = (value - parseFloat(minval)) / (Math.abs(parseFloat(minval)) + Math.abs(parseFloat(maxval)));
        var bar = paper.rect(value * barWidth, 0, 1, lineHeight, 1);
        bar.attr('fill', color);
        bar.attr('stroke', color);
    }
    addEl(outerDiv, div);
}