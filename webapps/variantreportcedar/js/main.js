var CLOSURE_NO_DEPS = true;
var annotData = null;
var mqMaxMatch = window.matchMedia('(max-width: 1024px)');
var mqMinMatch = window.matchMedia('(min-width: 1024px)');
var localModuleInfo = {}
var storeLogos = {}
var storeUrl = null;
var storeurl = $.get('/store/getstoreurl').done(function (response) {
    storeUrl = response;
});

function emptyElement(elem) {
    var last = null;
    while (last = elem.lastChild) {
        elem.removeChild(last);
    }
}

function makeModuleDetailDialog(moduleName, evt) {
    var mInfo = null;
    mInfo = localModuleInfo[moduleName];
    var divId = 'moduledetaildiv'
    var div = document.getElementById(divId)
    if (div) {
        emptyElement(div);
    } else {
        div = getEl('div');
        div.id = divId
        div.className = divId
    }
    div.classList.add("show")
    currentDetailModule = moduleName;
    var table = getEl('table');
    table.style.height = '100px';
    table.style.border = '0px';
    table.style.width = 'calc(100% - 20px)';
    var tr = getEl('tr');
    tr.style.border = '0px';
    var td = getEl('td');
    td.style.border = '0px';
    var sdiv = getEl('div');
    sdiv.className = 'moduletile-logodiv';
    sdiv.style.width = '180px';
    sdiv.style.height = '85px';
    var img = addLogo(moduleName, sdiv);
    if (img != null) {
        img.style.maxHeight = '84px';
    } else {
        sdiv.style.position = 'relative';
        sdiv.children[0].style.display = 'none';
    }
    addEl(td, sdiv);
    addEl(tr, td);
    td = getEl('td');
    td.style.border = '0px';
    var span = getEl('div');
    span.style.fontSize = '30px';
    span.textContent = mInfo.title;
    addEl(td, span);
    addEl(td, getEl('br'));
    span = getEl('span');
    span.style.fontSize = '12px';
    span.style.color = 'green';
    span.textContent = mInfo.type;
    addEl(td, span);
    span = getEl('span');
    span.style.fontSize = '12px';
    span.style.color = 'green';
    span.textContent = ' | ' + mInfo.developer.organization;
    addEl(td, span);
    addEl(tr, td);
    td = getEl('td');
    td.style.border = '0px';
    td.style.verticalAlign = 'top';
    td.style.textAlign = 'right';
    var sdiv = getEl('div');
    var buttonDiv = getEl('div');
    var sdiv = getEl('div');
    sdiv.id = 'installstatdiv_' + moduleName;
    sdiv.style.marginTop = '10px';
    sdiv.style.fontSize = '12px';
    addEl(td, sdiv);
    addEl(tr, td);
    addEl(table, tr);
    addEl(div, table);
    addEl(div, getEl('hr'));
    // MD and maintainer
    table = getEl('table');
    table.style.height = 'calc(100% - 100px)';
    table.style.border = '0px';
    tr = getEl('tr');
    var tdHeight = (window.innerHeight * 0.8 - 150) + 'px';
    tr.style.border = '0px';
    td = getEl('td');
    td.style.border = '0px';
    td.style.width = '70%';
    td.style.verticalAlign = 'top';
    td.style.height = tdHeight;
    var mdDiv = getEl('div');
    mdDiv.style.height = '100%';
    mdDiv.style.overflow = 'auto';
    var wiw = window.innerWidth;
    mdDiv.style.maxWidth = (wiw * 0.8 * 0.68) + 'px';
    addEl(td, mdDiv);
    addEl(tr, td);
    $.get('/store/modules/' + moduleName + '/' + 'latest' + '/readme').done(function (data) {
        var protocol = window.location.protocol;
        var converter = new showdown.Converter({ tables: true, openLinksInNewWindow: true });
        var mdhtml = converter.makeHtml(data);
        if (protocol == 'https:') {
            mdhtml = mdhtml.replace(/http:/g, 'https:');
        }
        var $mdhtml = $(mdhtml);
        var localRoot = window.location.origin + window.location.pathname.split('/').slice(0, -1).join('/');
        for (let img of $mdhtml.children('img')) {
            var storeRoot = `/modules/annotators/${moduleName}`
            img.src = img.src.replace(localRoot, storeRoot);
            img.style.display = 'block';
            img.style.margin = 'auto';
            img.style['max-width'] = '100%';
        }
        $(mdDiv).append($mdhtml);
        // output column description
        var d = getEl('div');
        d.id = 'moduledetail-output-column-div'
        d.style.display = 'none';
        var h2 = getEl('h2');
        h2.textContent = 'Output Columns';
        addEl(d, h2);
        var otable = getEl('table');
        otable.className = 'moduledetail-output-table';
        var othead = getEl('thead');
        var otr = getEl('tr');
        var oth = getEl('td');
        oth.textContent = 'Name';
        addEl(otr, oth);
        var oth = getEl('td');
        oth.textContent = 'Description';
        addEl(otr, oth);
        addEl(othead, otr);
        addEl(otable, othead);
        var otbody = getEl('tbody');
        otbody.id = 'moduledetail-output-tbody';
        addEl(otable, otbody);
        addEl(d, otable);
        addEl(mdDiv, d);
        addClassRecursive(mdDiv, 'moduledetaildiv-elem');
        var data = mInfo;
        var outputColumnDiv = d
        var outputs = data['output_columns'];
        if (outputs != undefined) {
            var descs = [];
            for (var i1 = 0; i1 < outputs.length; i1++) {
                var o = outputs[i1];
                var desc = '';
                if (o['desc'] != undefined) {
                    desc = o['desc'];
                }
                descs.push([o['title'], desc]);
            }
            if (descs.length > 0) {
                outputColumnDiv.style.display = 'block';
                for (var i1 = 0; i1 < descs.length; i1++) {
                    var title = descs[i1][0];
                    var desc = descs[i1][1];
                    var otr = getEl('tr');
                    var otd = getEl('td');
                    var ospan = getEl('span');
                    ospan.textContent = title;
                    addEl(otd, ospan);
                    addEl(otr, otd);
                    var otd = getEl('td');
                    var ospan = getEl('span');
                    ospan.textContent = desc;
                    addEl(otd, ospan);
                    addEl(otr, otd);
                    addEl(otbody, otr);
                }
            }
        }
    });
    // Information div
    td = getEl('td');
    td.style.width = '30%';
    td.style.border = '0px';
    td.style.verticalAlign = 'top';
    td.style.height = tdHeight;
    var infodiv = getEl('div');
    infodiv.id = 'moduledetaildiv-infodiv';
    infodiv.style.maxWidth = (wiw * 0.8 * 0.3) + 'px';
    var d = getEl('div');
    span = getEl('span');
    if (mInfo.commercial_warning) {
        span.textContent = mInfo.commercial_warning;
        span.style.color = 'red';
        span.style['font-weight'] = 'bold';
    }
    addEl(d, span);
    addEl(infodiv, d);
    var d = getEl('div');
    span = getEl('span');
    span.textContent = mInfo.description;
    addEl(d, span);
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Module version: ';
    addEl(d, span);
    span = getEl('span');
    span.textContent = mInfo.version
    addEl(d, span);
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Maintainer: ';
    addEl(d, span);
    span = getEl('span');
    span.textContent = mInfo['developer']['name'];
    addEl(d, span);
    addEl(d, getEl('br'));
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'e-mail: ';
    addEl(d, span);
    span = getEl('span');
    span.textContent = mInfo['developer']['email'];
    addEl(d, span);
    addEl(d, getEl('br'));
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Citation: ';
    addEl(d, span);
    span = getEl('span');
    span.style.width = 'calc(100% - 120px)';
    span.style.wordWrap = 'break-word';
    span.style.verticalAlign = 'text-top';
    var citation = mInfo['developer']['citation'];
    if (citation != undefined && citation.startsWith('http')) {
        var a = getEl('a');
        a.href = citation;
        a.target = '_blank';
        a.textContent = citation;
        addEl(span, a);
    } else {
        span.textContent = citation;
    }
    addEl(d, span);
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Organization: ';
    addEl(d, span);
    span = getEl('span');
    span.textContent = mInfo['developer']['organization'];
    addEl(d, span);
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Website: ';
    addEl(d, span);
    span = getEl('a');
    span.textContent = mInfo['developer']['website'];
    span.href = mInfo['developer']['website'];
    span.target = '_blank';
    span.style.wordBreak = 'break-all';
    addEl(d, span);
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Type: ';
    addEl(d, span);
    span = getEl('span');
    span.textContent = mInfo['type'];
    addEl(d, span);
    addEl(infodiv, d);
    d = getEl('div');
    span = getEl('span');
    span.style.fontWeight = 'bold';
    span.textContent = 'Required modules: ';
    addEl(d, span);
    span = getEl('span');
    if (mInfo['requires'] != null) {
        span.textContent = mInfo['requires'];
    } else {
        span.textContent = 'None';
    }
    span.style.wordBreak = 'break-all';
    addEl(d, span);
    addEl(infodiv, d);
    addEl(td, infodiv);
    addEl(tr, td);
    addEl(table, tr);
    addEl(div, table);
    var el = getEl('div');
    el.style.position = 'absolute';
    el.style.top = '0px';
    el.style.right = '0px';
    el.style.fontSize = '20px';
    el.style.padding = '10px';
    el.style.cursor = 'pointer';
    el.textContent = 'X';
    el.addEventListener('click', function (evt) {
        var pel = evt.target.parentElement;
        pel.parentElement.removeChild(pel);
    });
    addEl(div, el);
    addClassRecursive(div, 'moduledetaildiv-elem');
    storeModuleDivClicked = true;
    return div;
}

function addClassRecursive(elem, className) {
    elem.classList.add(className);
    $(elem).children().each(
        function () {
            $(this).addClass(className);
            addClassRecursive(this, className);
        }
    );
}

function addLogo(moduleName, sdiv) {
    if (storeLogos[moduleName] != undefined) {
        var img = storeLogos[moduleName].cloneNode(true);
        addEl(sdiv, img);
        return img;
    }
    var moduleInfo = localModuleInfo[moduleName];
    var img = null;
    if (moduleInfo.has_logo == true) {
        img = getEl('img');
        img.className = 'moduletile-logo';
        img.src = '/store/locallogo?module=' + moduleName;
        addEl(sdiv, img);
        storeLogos[moduleName] = img;
    } else {
        sdiv.classList.add('moduletile-nologo');
        var span = getEl('div');
        span.className = 'moduletile-title';
        var title = moduleInfo.title;
        span.textContent = title
        if (title.length > 26) {
            span.style.fontSize = '30px';
        }
        addEl(sdiv, span);
    }
    return img;
}

function showModuleDetail(moduleName, evt) {
    if (moduleName in localModuleInfo) {
        var div = makeModuleDetailDialog(moduleName, evt)
        addEl(document.body, div)
        div.classList.add("show")
    } else {
        fetch("moduleinfo?module=" + moduleName)
            .then(response => {
                return response.json()
            }).then(response => {
                localModuleInfo[moduleName] = response
                var div = makeModuleDetailDialog(moduleName, evt)
                addEl(document.body, div)
                div.classList.add("show")
            })
    }
}

function makeModuleDescUrlTitle(moduleName, text) {
    var div = getEl('div')
    var el = getEl('span')
    if (text != undefined) {
        el.textContent = text
    } else {
        el.textContent = widgetInfo[moduleName]["title"]
    }
    el.classList.add('infoimg')
    addEl(div, el)
    var annotators = widgetGenerators[moduleName]['annotators']
    if (annotators == undefined) {
        annotators = moduleName
    }
    el.addEventListener('click', function (evt) {
        fetch("modulesinfo?modules=" + annotators)
            .then(response => {
                return response.json()
            }).then(moduleInfos => {
                if (moduleInfos.length == 1) {
                    showModuleDetail(moduleInfos[0].name, evt)
                } else {
                    var tdiv = document.querySelector("#tooltipdiv")
                    if (tdiv == null) {
                        tdiv = getEl('div')
                        tdiv.id = 'tooltipdiv'
                    }
                    tdiv.innerHTML = ""
                    moduleInfos.forEach(function (moduleInfo) {
                        var tsdiv = getEl('div')
                        var tspan = getEl('a')
                        tspan.textContent = moduleInfo.title
                        tspan.setAttribute("href", moduleInfo.url)
                        tspan.setAttribute("target", "_blank")
                        addEl(tsdiv, tspan)
                        tspan = getEl('div')
                        tspan.textContent = moduleInfo.desc
                        addEl(tsdiv, tspan)
                        addEl(tdiv, tsdiv)
                    })
                    tdiv.style.left = evt.target.offsetLeft + 15
                    tdiv.style.top = evt.target.offsetTop
                    addEl(evt.target.parentElement, tdiv)
                    tdiv.classList.add("show")
                }
            })
    })
    return div
}

// function mqMaxMatchHandler(e) {
//     if (e.matches) {
//         var iframe = document.querySelector('#mupitiframe');
//         var chrom = iframe.getAttribute('chrom');
//         var pos = iframe.getAttribute('pos');
//         iframe.src = location.protocol + '//www.cravat.us/MuPIT_Interactive?gm=' + chrom + ':' + pos + '&embed=true&showrightpanel=false';
//     }
// }

// function mqMinMatchHandler(e) {
//     if (e.matches) {
//         var iframe = document.querySelector('#mupitiframe');
//         var chrom = iframe.getAttribute('chrom');
//         var pos = iframe.getAttribute('pos');
//         iframe.src = location.protocol + '//www.cravat.us/MuPIT_Interactive?gm=' + chrom + ':' + pos + '&embed=true';
//     }
// }

function getInputDataFromUrl() {
    var urlParams = new URLSearchParams(window.location.search);
    var inputChrom = urlParams.get('chrom');
    var inputPos = urlParams.get('pos');
    var inputRef = urlParams.get('ref_base');
    var inputAlt = urlParams.get('alt_base');
    var assembly = urlParams.get('assembly')
    if (assembly == undefined) {
        assembly = 'hg38'
    }
    var inputData = cleanInputData(inputChrom, inputPos, inputRef, inputAlt, assembly);
    return inputData;
}

function cleanInputData(inputChrom, inputPos, inputRef, inputAlt, assembly) {
    if (inputChrom == '') {
        inputChrom = null;
    }
    if (inputPos == '') {
        inputPos = null;
    }
    if (inputRef == '') {
        inputRef = null;
    }
    if (inputAlt == '') {
        inputAlt = null;
    }
    if (assembly == undefined) {
        assembly = 'hg38'
    }
    if (inputChrom == null || inputPos == null || inputRef == null || inputAlt == null) {
        return null;
    } else {
        return {
            'chrom': inputChrom,
            'pos': inputPos,
            'ref': inputRef,
            'alt': inputAlt,
            'assembly': assembly
        };
    }
}

function submitForm() {
    // var value = document.querySelector('#input_variant').value;
    // var toks = value.split(':');
    // if (toks.length != 4 && toks.length != 5) {
    //     return;
    // }
    // var chrom = toks[0];
    // var pos = toks[1];
    // var ref = toks[2];
    // var alt = toks[3];
    // var inputData = cleanInputData(chrom, pos, ref, alt);
    // var assembly = 'hg38'
    // if (toks.length == 5) {
    //     var assembly = toks[4]
    // }
    // inputData['assembly'] = assembly
    // if (inputData != null) {
    //     showContentDiv();
    //     submitAnnotate(inputData['chrom'], inputData['pos'], inputData['ref'],
    //         inputData['alt'], 'hg38')
    //     // hideSearch();
    // }
}

function submitAnnotate(inputChrom, inputPos, inputRef, inputAlt, assembly) {
    if (assembly == undefined) {
        assembly = 'hg38'
    }
    var url = 'annotate';
    var params = {
        'chrom': inputChrom,
        'pos': parseInt(inputPos),
        'ref_base': inputRef,
        'alt_base': inputAlt,
        'assembly': assembly
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: params,
        success: function (response) {
            annotData = response;
            annotData['base'] = annotData['crx'];
            showAnnotation(response);
        }
    });
}

function getModulesData(moduleNames) {
    var data = {};
    for (var i = 0; i < moduleNames.length; i++) {
        var moduleName = moduleNames[i];
        var moduleData = annotData[moduleName];
        if (moduleData == null) {
            continue;
        }
        var moduleDataKeys = Object.keys(moduleData);
        for (var j = 0; j < moduleDataKeys.length; j++) {
            var key = moduleDataKeys[j];
            var value = moduleData[key];
            data[moduleName + '__' + key] = value;
        }
    }
    return data;
}

function showWidget(widgetName, moduleNames, level, parentDiv, maxWidth, maxHeight, showTitle) {
    var generator = widgetGenerators[widgetName];
    var divs = null;
    var maxWidthParent = null;
    var maxHeightParent = null;
    if (maxWidth != undefined || maxWidth != null) {
        generator[level]['width'] = null;
        generator[level]['max-width'] = maxWidth;
        maxWidthParent = maxWidth + 30;
    }
    if (maxHeight != undefined || maxHeight != null) {
        generator[level]['height'] = null;
        generator[level]['max-height'] = maxHeight;
        maxHeightParent = maxHeight + 30;
    }
    if (level != undefined) {
        if (widgetName == 'ncbi') {
            divs = getDetailWidgetDivs(level, widgetName, '', maxWidthParent,
                maxHeightParent, showTitle);
        } else {
            divs = getDetailWidgetDivs(level, widgetName, widgetInfo[widgetName].title,
                maxWidthParent, maxHeightParent, showTitle);
        }
    } else {
        if ('variant' in generator) {
            divs = getDetailWidgetDivs('variant', widgetName, widgetInfo[widgetName].title,
                maxWidthParent, maxHeightParent, showTitle);
            level = 'variant';
        } else if ('gene' in generator) {
            divs = getDetailWidgetDivs('gene', widgetName, widgetInfo[widgetName].title, maxWidthParent, maxHeightParent, showTitle);
            level = 'gene';
        }
    }
    var data = getModulesData(moduleNames);
    if (Object.keys(data).length == 0) {
        var dl = getEl('dl')
        divs[0].style.height = 'unset'
        addEl(divs[0], dl)
        var titleEl = makeModuleDescUrlTitle(widgetName)
        addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel());
        // var span = getEl('span');
        // span.textContent = 'No annotation available for ' + widgetInfo[widgetName]['title'];
        // addEl(divs[1], span);
    } else {
        if (level == 'gene') {
            data['base__hugo'] = annotData['crx'].hugo;
        }
        var ret = widgetGenerators[widgetName][level]['function'](
            divs[1], data, 'variant', true); // last true is to highlight if value exists.
    }
    addEl(parentDiv, divs[0]);
    return divs;
}

function showSectionTitles() {
    document.querySelectorAll('.container_titlediv').forEach(elem => {
        elem.classList.remove('hidden');
    });
}

function showAnnotation(response) {
    document.querySelectorAll('.detailcontainerdiv').forEach(function (el) {
        $(el).empty();
    });
    hideSpinner();
    showSectionTitles();
    var parentDiv = document.querySelector('#contdiv_vinfo');
    var retDivs = showWidget('basepanel', ['base'], 'variant', parentDiv);
    var parentDiv = document.querySelector('#contdiv_clin');
    showWidget('clinpanel',
        ['base', 'clinvar', 'clinvar_acmg', 'clingen', 'dgi'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_cancerassoc');
    showWidget('cancerassocpanel', ['base', 'cgc', 'cosmic', 'cancer_genome_interpreter', 'target', 'civic', 'chasmplus', 'cscape'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_afreq');
    showWidget('allelefreqpanel', ['base', 'gnomad3', 'thousandgenomes'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_prediction');
    showWidget('predictionpanel', ['base', 'dann_coding', 'fathmm', 'fathmm_xf_coding', 'revel', 'sift', 'lrt', 'fathmm_mkl', 'metalr', 'metasvm', 'mutation_assessor', 'mutpred1', 'mutationtaster', 'polyphen2', 'provean', 'vest'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_functional');
    showWidget('functionalpanel', ['base', 'swissprot_binding', 'swissprot_domains', 'swissprot_ptm'],
        'variant', parentDiv, null, null, false);
}

function getWidgets(callback, callbackArgs) {
    $.get('/result/service/widgetlist', {}).done(function (jsonResponseData) {
        var tmpWidgets = jsonResponseData;
        var widgetLoadCount = 0;
        for (var i = 0; i < tmpWidgets.length; i++) {
            var tmpWidget = tmpWidgets[i];
            var widgetName = tmpWidget['name'];
            var widgetNameNoWg = widgetName.substring(2);
            widgetInfo[widgetNameNoWg] = tmpWidget;
            $.getScript('/result/widgetfile/' + widgetName + '/' +
                widgetName + '.js',
                function () {
                    widgetLoadCount += 1;
                    if (widgetLoadCount == tmpWidgets.length) {
                        if (callback != null) {
                            callback(callbackArgs);
                        }
                    }
                });
        }
    });
}

const getNoAnnotMsgGeneLevel = function () {
    return 'No annotation available for ' + annotData['base']['hugo']
}

function getNodataSpan(annotator_name) {
    var span = getEl('span');
    span.textContent = 'No annotation for' + annotator_name + 'available';
    return span;
}


function changeAchange3to1(achange) {
    if (achange.startsWith('p.')) {
        achange = achange.substring(2);
    }
    var aa3to1 = {
        'Ala': 'A',
        'Cys': 'C',
        'Asp': 'D',
        'Glu': 'E',
        'Phe': 'F',
        'Gly': 'G',
        'His': 'H',
        'Ile': 'I',
        'Leu': 'L',
        'Met': 'M',
        'Asn': 'N',
        'Pro': 'P',
        'Gln': 'Q',
        'Arg': 'R',
        'Ser': 'S',
        'Thr': 'T',
        'Val': 'V',
        'Trp': 'W',
        'Tyr': 'Y'
    };
    var aa3s = Object.keys(aa3to1);
    for (var i = 0; i < aa3s.length; i++) {
        achange = achange.replace(aa3s[i], aa3to1[aa3s[i]]);
    }
    return achange;
}
const getCirclePoint = function (centerx, centery, radius, angle) {
    let x = centerx + Math.cos(angle / 180 * Math.PI) * radius
    let y = centery + Math.sin(angle / 180 * Math.PI) * radius
    let xy = {
        x: x,
        y: y
    }
    return xy
}
const drawDialFragment = function (
    centerx, centery, radius1, radius2, angle0, angle1, fill, stroke) {
    let angleDiff = angle1 - angle0
    sub = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    xy = getCirclePoint(centerx, centery, radius1, angle0)
    d = `M ${xy.x} ${xy.y}`
    xy = getCirclePoint(centerx, centery, radius1, angle1)
    if (angleDiff < 180) {
        d += ` A ${radius1} ${radius1} 0 0 1 ${xy.x} ${xy.y}`
    } else {
        d += ` A ${radius1} ${radius1} 0 1 1 ${xy.x} ${xy.y}`
    }
    xy = getCirclePoint(centerx, centery, radius2, angle1)
    d += ` L ${xy.x} ${xy.y}`
    xy = getCirclePoint(centerx, centery, radius2, angle0)
    if (angleDiff < 180) {
        d += ` A ${radius2} ${radius2} 0 0 0 ${xy.x} ${xy.y}`
    } else {
        d += ` A ${radius2} ${radius2} 0 1 0 ${xy.x} ${xy.y}`
    }
    xy = getCirclePoint(centerx, centery, radius1, angle0)
    d += ` L ${xy.x} ${xy.y}`
    sub.setAttributeNS(null, 'fill', fill)
    sub.setAttributeNS(null, 'stroke', stroke)
    sub.setAttributeNS(null, 'd', d)
    return sub
}
const drawDialGraph = function (title, value, threshold) {
    let el = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    el.style.width = '6rem'
    el.style.height = '6rem'
    let centerx = 50
    let centery = 50
    let radius1 = 40
    let radius2 = 30
    let angle0 = 135
    let angle1 = 405
    let angleRange = angle1 - angle0
    let dotradius = 5
    let angleAdd = value * angleRange
    let angle = angle0 + angleAdd
    let thresholdAngle = threshold * angleRange + angle0
    // Needle
    let sub = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    let xy = getCirclePoint(centerx, centery, dotradius, angle - 90)
    let points = '' + xy.x + ',' + xy.y
    xy = getCirclePoint(centerx, centery, radius2, angle)
    let pointXy = xy
    points += ' ' + xy.x + ',' + xy.y
    xy = getCirclePoint(centerx, centery, dotradius, angle + 90)
    points += ' ' + xy.x + ',' + xy.y
    sub.setAttributeNS(null, 'points', points)
    if (value < threshold) {
        sub.setAttributeNS(null, 'stroke', 'black')
        sub.setAttributeNS(null, 'fill', 'black')
    } else {
        sub.setAttributeNS(null, 'stroke', '#ff5555')
        sub.setAttributeNS(null, 'fill', '#ff5555')
    }
    el.appendChild(sub)
    // Dot
    sub = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    sub.setAttributeNS(null, 'cx', centerx)
    sub.setAttributeNS(null, 'cy', centery)
    sub.setAttributeNS(null, 'r', dotradius)
    sub.setAttributeNS(null, 'r', dotradius)
    if (value < threshold) {
        sub.setAttributeNS(null, 'stroke', 'black')
        sub.setAttributeNS(null, 'fill', '#ffffff')
    } else {
        sub.setAttributeNS(null, 'stroke', 'black')
        sub.setAttributeNS(null, 'fill', '#ffffff')
    }
    el.appendChild(sub)
    // Circle
    if (value < threshold) {
        el.appendChild(
            drawDialFragment(
                centerx, centery, radius1, radius2, angle0, angle, '#ffaaaa', 'black'))
        el.appendChild(
            drawDialFragment(
                centerx, centery, radius1, radius2, angle, thresholdAngle, '#ffffff', 'black'))
        el.appendChild(
            drawDialFragment(
                centerx, centery, radius1, radius2, thresholdAngle, angle1, '#aaaaaa', 'black'))
    } else {
        el.appendChild(
            drawDialFragment(
                centerx, centery, radius1, radius2, angle0, thresholdAngle, '#ffaaaa', 'black'))
        el.appendChild(
            drawDialFragment(
                centerx, centery, radius1, radius2, thresholdAngle, angle, '#ff5555', 'black'))
        el.appendChild(
            drawDialFragment(
                centerx, centery, radius1, radius2, angle, angle1, '#aaaaaa', 'black'))
    }
    return el
}
const getDialWidget = function (title, value, threshold) {
    var sdiv = getEl('div');
    sdiv.classList.add('preddiv')
    sdiv.classList.add('pred_score')
    // var svg = drawDialGraph(title, value, threshold)
    // addEl(sdiv, svg)
    var ssdiv = getEl('div')
    var sssdiv = getEl('div')
    sssdiv.textContent = title
    addEl(ssdiv, sssdiv)
    sssdiv = getEl('div')
    sssdiv.textContent = prettyVal(value)
    addEl(ssdiv, sssdiv)
    addEl(sdiv, ssdiv)
    return sdiv
}

const predWidget = function (value) {
    var div = getEl('div');
    div.classList.add('preddiv')
    if (isNaN(value) == false && value != null) {
        div.textContent = prettyVal(value)
    } else {
        div.textContent = value
    }
    return div
}

const baseWidget = function (title, value) {
    var sdiv = getEl('div');
    sdiv.classList.add('basediv')
    var ssdiv = getEl('div')
    var sssdiv = getEl('div')
    sssdiv.textContent = title
    addEl(ssdiv, sssdiv)
    sssdiv = getEl('div')
    sssdiv.textContent = value
    addEl(ssdiv, sssdiv)
    addEl(sdiv, ssdiv)
    return sdiv
}

const baseWidgetlink = function (title, value, link) {
    var sdiv = getEl('div');
    sdiv.classList.add('basediv')
    var ssdiv = getEl('div')
    var sssdiv = getEl('div')
    sssdiv.textContent = title
    addEl(ssdiv, sssdiv)
    sssdiv = getEl('div')
    var a = makeA(value, link)
    a.classList.add('linkclass')
    addEl(sssdiv, a)
    addEl(ssdiv, sssdiv)
    addEl(sdiv, ssdiv)
    return sdiv
}

var widgetInfo = {};
var widgetGenerators = {};

widgetInfo['base2'] = {
    'title': ''
};
widgetGenerators['base2'] = {
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            var nref = getWidgetData(tabName, 'base', row, 'ref_base').length;
            var ref_base = getWidgetData(tabName, 'base', row, 'ref_base')
            var alt_base = getWidgetData(tabName, 'base', row, 'alt_base')
            var nalt = getWidgetData(tabName, 'base', row, 'alt_base').length;
            var chrom = getWidgetData(tabName, 'base', row, 'chrom');
            var chrom = chrom.substring(3)
            var thous_af = getWidgetData(tabName, 'thousandgenomes', row, 'af');
            var gnomad_af = getWidgetData(tabName, 'gnomad', row, 'af')
            var sdiv = getEl('div');
            sdiv.setAttribute("id", "varinfo")
            var geneName = baseWidget('Gene Symbol', hugo)
            geneName.classList.add("basepaneldiv")
            addEl(sdiv, geneName);
            var achange = getWidgetData(tabName, 'base', row, 'achange');
            achange = changeAchange3to1(achange);
            var achange = baseWidget('Protein Change', achange)
            achange.classList.add("basepaneldiv")
            addEl(sdiv, achange)
            var acc = getWidgetData(tabName, 'uniprot', row, 'acc');
            if (acc == null) {
                var uniprot = baseWidget('UniProt Accession Number', 'No UniProt available')
            } else {
                link2 = 'https://www.uniprot.org/uniprot/' + acc
                var aa = getEl('a');
                aa.href = link2
                aa.textContent = acc
                var u = getEl('div')
                var uniprot = baseWidgetlink('UniProt Accession Number', acc, link2)
            }
            uniprot.classList.add("basepaneldiv")
            addEl(sdiv, uniprot)
            var variant_type = null;
            if (nref == 1 && nalt == 1 && ref_base != '-' && alt_base != '-') {
                variant_type = 'single nucleotide variant';
            }
            if (nref > 1 && nalt == 1 && alt_base == '-') {
                variant_type = 'deletion';
            }
            if (nref == 1 && nalt > 1 && ref_base == '-') {
                variant_type = 'insertion';
            }
            if (nref > 1 && nalt > 1) {
                variant_type = 'complex substitution';
            }
            addEl(div, sdiv);
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var tbody = getEl('tbody');
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            sdiv.style.columnGap = '0.875rem'
            sdiv.style.rowGap = ".85rem"
            var variantinfo = baseWidget('Variant Type', variant_type)
            variantinfo.classList.add("basepaneldiv")
            addEl(sdiv, variantinfo)
            var baseChange = baseWidget('Base Change', ref_base + ' > ' + alt_base)
            baseChange.classList.add("basepaneldiv")
            addEl(sdiv, baseChange)

            var variant_length = null;
            if (variant_type == 'single nucleotide variant') {
                variant_length = '1';
            }
            if (variant_type == 'deletion') {
                variant_length = nref;
            }
            if (variant_type == 'insertion' && 'complex substitution') {
                variant_length = nalt;
            }
            var so = getWidgetData(tabName, 'base', row, 'so');
            var consequence = '';
            if (so == 'synonymous_variant') {
                consequence = 'synonymous';
            } else {
                consequence = 'nonsynonymous';
            }
            var sequenceOntology = baseWidget('Sequence Ontology', so.replace('_', ' '))
            sequenceOntology.classList.add("basepaneldiv")
            addEl(sdiv, sequenceOntology)
            var consequences = baseWidget('Variant consequence', consequence)
            consequences.classList.add("basepaneldiv")
            addEl(sdiv, consequences)
            var link = "https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position=" + chrom + "%3A" + getWidgetData(tabName, 'base', row, 'pos')
            var genomic_location = baseWidgetlink('Genomic location', 'chr' + chrom + ':' + getWidgetData(tabName, 'base', row, 'pos'), link)
            genomic_location.classList.add("basepaneldiv")
            addEl(sdiv, genomic_location)
            var genomeBuild = baseWidget("Genome Build", "GRCh38")
            genomeBuild.classList.add("basepaneldiv")
            addEl(sdiv, genomeBuild)
            var max_af = null;
            if (thous_af != undefined && gnomad_af != undefined) {
                if (thous_af > gnomad_af) {
                    max_af = thous_af;
                } else {
                    max_af = gnomad_af;
                }
            } else if (thous_af != undefined && gnomad_af == undefined) {
                max_af = thous_af;
            } else if (thous_af == undefined && gnomad_af != undefined) {
                max_af = gnomad_af;
            }
            var snp = getWidgetData(tabName, 'dbsnp', row, 'rsid');
            if (snp == null) {
                var dbsnp = baseWidget('dbSNP ID', 'No dbSNP ID is available')
            } else {
                link = 'https://www.ncbi.nlm.nih.gov/snp/' + snp
                var dbsnp = baseWidgetlink('dbSNP ID', snp, link)
            }
            dbsnp.classList.add("basepaneldiv")
            addEl(sdiv, dbsnp)
            div.style.backgroundColor = "white"
            div.style.maxWidth = "120vh"
            addEl(div, sdiv)
        }
    }
}

widgetInfo['chasmplus2'] = {
    'title': 'CHASMplus'
};
widgetGenerators['chasmplus2'] = {
    'annotators': 'chasmplus',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("chasmplus")
            var title = 'Target'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var all = getWidgetData(tabName, 'chasmplus', row, 'all');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Driver Mutation P-value ', 'Driver Mutation Score']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            for (var i in all) {
                var hits = all[i]
                var score = hits[1]
                var pval = hits[2]
                var tr = getWidgetTableTr([pval, score]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            }

            addDlRow(dl, titleEl, wdiv)
        }
    }
}


widgetInfo['civic2'] = {
    'title': 'CIViC'
};
widgetGenerators['civic2'] = {
    'annotators': 'civic',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("civic")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var description = getWidgetData(tabName, 'civic', row, 'description');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Description']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([description]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var description = getWidgetData(tabName, 'civic', row, 'diseases');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Diseases']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([description]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, '', wdiv)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var score = getWidgetData(tabName, 'civic', row, 'molecular_profile_score');
            var id = getWidgetData(tabName, 'civic', row, 'id');
            var webpage = 'https://civicdb.org/variants/' + id + '/summary'
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Variant Evidence Score', 'ID', 'Link']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([score, id, webpage]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, '', wdiv)
        }
    }
}

widgetInfo['cscape'] = {
    'title': 'CScape'
};
widgetGenerators['cscape'] = {
    'annotators': 'cscape',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cscape")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var score = getWidgetData(tabName, 'cscape', row, 'score');
            score = Number(score)
            let prediction;
            if (score > 0.5) {
                prediction = "Disease-driver"
            } else {
                prediction = "Neutral / Benign"
            }
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Oncogenic Status', 'Score']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([prediction, prettyVal(score)]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['clinvar2'] = {
    'title': 'ClinVar'
};
widgetGenerators['clinvar2'] = {
    'annotators': 'clinvar',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("clinvar", "ClinVar Significance")
            div.parentElement.style.paddingBottom = '0'
            var id = getWidgetData(tabName, 'clinvar', row, 'id');
            var sig = getWidgetData(tabName, 'clinvar', row, 'sig');
            var dl = getEl('dl')
            addEl(div, dl)
            var span = getEl('span');
            span.textContent = sig;
            var dd = getEl('div')
            addEl(dd, span)
            addEl(dd, getTn('\xa0'));
            var sigLower = sig == undefined ? '' : sig.toLowerCase()
            if (id != null && sigLower != 'not provided' &&
                sigLower != '' && sigLower != 'association not found') {
                var titleEl2 = makeModuleDescUrlTitle("clinvar", "ClinVar Conditions")
                link = 'https://www.ncbi.nlm.nih.gov/clinvar/variation/' + id;
                var a = makeA(id, link)
                a.classList.add('linkclass');
                addEl(dd, getTn('(ID: '));
                addEl(dd, a);
                addEl(dd, getTn(')'));
                addDlRow(dl, titleEl, dd)
                var url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=' + id + '&retmode=json'
                fetch(url).then(response => {
                    return response.json()
                }).then(response => {
                    var trait_set = response['result'][id].trait_set;
                    var traitNames = [];
                    for (var i = 0; i < trait_set.length; i++) {
                        var trait_name = trait_set[i].trait_name
                        if (trait_name == 'not provided' ||
                            trait_name == 'none provided' ||
                            trait_name == 'not specified') {
                            continue
                        }
                        traitNames.push(trait_name)
                    }
                    traitNames.sort();
                    var sdiv = getEl('div')
                    sdiv.style.display = 'flex'
                    sdiv.style.flexWrap = 'wrap'
                    for (var i = 0; i < traitNames.length; i++) {
                        var span = getEl('div')
                        span.classList.add('clinvar_traitname')
                        span.textContent = traitNames[i]
                        addEl(sdiv, span)
                    }
                    addDlRow(dl, titleEl2, sdiv)
                });
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
        }
    }
}

widgetInfo['cosmic2'] = {
    'title': 'Catalog of somatic mutations in cancer (COSMIC)'
};
widgetGenerators['cosmic2'] = {
    'annotators': 'cosmic',
    'variant': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cosmic")
            var title = 'COSMIC'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var cosmic_id = getWidgetData(tabName, 'cosmic', row, 'cosmic_id');
            var tissue = getWidgetData(tabName, 'cosmic', row, 'variant_count_tissue');
            var tissue2 = []
            for (var i in tissue) {
                tissue2.push(tissue[i].filter(x => isNaN(x)))
            }

            var link = 'https://cancer.sanger.ac.uk/cosmic/search?q=' + cosmic_id
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['COSMIC ID', 'Variant Type (Tissue)']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr2([link, tissue2], [cosmic_id]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)

        }
    }
}

widgetInfo['cgi2'] = {
    'title': 'Cancer Genome Interpreter'
};
widgetGenerators['cgi2'] = {
    'annotators': 'cancer_genome_interpreter',
    'variant': {
        'width': '100%',
        'height': 'unset',
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cancer_genome_interpreter")
            var title = 'Cancer Genome Interpreter'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var resistant = getWidgetData(tabName, 'cancer_genome_interpreter', row, 'resistant');
            var responsive = getWidgetData(tabName, 'cancer_genome_interpreter', row, 'responsive');
            var other = getWidgetData(tabName, 'cancer_genome_interpreter', row, 'other');
            var all = getWidgetData(tabName, 'cancer_genome_interpreter', row, 'all');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Number of Drug Resistant Effects', 'Number of Drug Responsive Effects', 'Number of Other Effects']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([resistant, responsive, other]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Drug Response', "Drug Name", 'Guidelines', 'Reference', 'Disease', 'Study']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            for (var i in all) {
                var annotation = all[i]
                var response = annotation[0]
                var study = annotation[1]
                var drug = annotation[2]
                var guidelines = annotation[3]
                var pmid = annotation[4]
                var disease = annotation[5]
                var tr = getWidgetTableTr2([response, drug, guidelines, pmid, disease, study]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            }
            addDlRow(dl, '', wdiv)
        }
    }
}

widgetInfo['target2'] = {
    'title': 'TARGET'
};
widgetGenerators['target2'] = {
    'annotators': 'target',
    'variant': {
        'width': undefined,
        'height': undefined,
        'word-break': 'break-word',
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("target")
            var title = 'Target'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var therapy = getWidgetData(tabName, 'target', row, 'therapy');
            var rationale = getWidgetData(tabName, 'target', row, 'rationale');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Recommended Therapy', 'Rationale']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([therapy, rationale]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['dann_coding'] = {
    'title': 'Dann Coding'
};
widgetGenerators['dann_coding'] = {
    'annotators': 'DANN',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['fathmm'] = {
    'title': 'FATHMM'
};
widgetGenerators['fathmm'] = {
    'annotators': 'fathmm',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['fathmm_mkl'] = {
    'title': 'FATHMM MKL'
};
widgetGenerators['fathmm_mkl'] = {
    'annotators': 'fathmm_mkl',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['fathmm_xf_coding'] = {
    'title': 'FATHMM XF'
};
widgetGenerators['fathmm_xf_coding'] = {
    'annotators': 'fathmm_xf_coding',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['lrt'] = {
    'title': 'LRT'
};
widgetGenerators['lrt'] = {
    'annotators': 'lrt',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['metalr'] = {
    'title': 'MetaLR'
};
widgetGenerators['metalr'] = {
    'annotators': 'metalr',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['mutation_assessor'] = {
    'title': 'Mutation Assessor'
};
widgetGenerators['mutation_assessor'] = {
    'annotators': 'mutation_assessor',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['metasvm'] = {
    'title': 'MetaSVM'
};
widgetGenerators['metasvm'] = {
    'annotators': 'metasvm',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['mutationtaster2'] = {
    'title': 'Mutation Taster'
};
widgetGenerators['mutationtaster2'] = {
    'annotators': 'mutationtaster2',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['provean'] = {
    'title': 'PROVEAN'
};
widgetGenerators['provean'] = {
    'annotators': 'provean',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['revel2'] = {
    'title': 'REVEL'
};
widgetGenerators['revel2'] = {
    'annotators': 'revel2',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
        }
    }
}

widgetInfo['polyphen2hdiv'] = {
    'title': 'PolyPhen2 HDIV'
};
widgetGenerators['polyphen2hdiv'] = {
    'annotators': 'polyphen2',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) { }
    }
}

widgetInfo['polyphen2hvar'] = {
    'title': 'PolyPhen2 HVAR'
};
widgetGenerators['polyphen2hvar'] = {
    'annotators': 'polyphen2',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) { }
    }
}

widgetInfo['provean2'] = {
    'title': 'PROVEAN'
};
widgetGenerators['provean2'] = {
    'annotators': 'provean',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) { }
    }
}

widgetInfo['vest2'] = {
    'title': 'VEST 4.0'
};
widgetGenerators['vest2'] = {
    'annotators': 'vest',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) { }
    }
}

widgetInfo['sift2'] = {
    'title': 'SIFT'
};
widgetGenerators['sift2'] = {
    'annotators': 'sift',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) { }
    }
}


widgetInfo['clingen2'] = {
    'title': 'ClinGen Gene'
};
widgetGenerators['clingen2'] = {
    'annotators': 'clingen',
    'gene': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function (div, row, tabName) {
            var title = 'ClinGen Gene'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var titleEl = makeModuleDescUrlTitle("clingen")
            var disease = getWidgetData(tabName, 'clingen', row, 'disease');
            if (disease == null) {
                addDlRow(dl, titleEl, 'No annotation available');
            }
            if (disease != undefined && disease != null) {
                var diseases = getWidgetData(tabName, 'clingen', row, 'disease').split(';');
                var classifications = getWidgetData(tabName, 'clingen', row, 'classification').split(';');
                var links = getWidgetData(tabName, 'clingen', row, 'link').split(';');
                var mondos = getWidgetData(tabName, 'clingen', row, 'mondo').split(';');
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '47rem'
                sdiv.style.minWidth = '32rem'
                sdiv.style.maxHeight = '200px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                addEl(div, table);
                var thead = getWidgetTableHead(['Disease', 'Classification', 'ClinGen', 'Monarch'], ['35%', '30%']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                for (var i = 0; i < diseases.length; i++) {
                    var disease = diseases[i];
                    var classification = classifications[i];
                    var mondo = mondos[i];
                    var mondo_link = `https://monarchinitiative.org/disease/${mondo}`
                    var link = links[i]
                    var tr = getWidgetTableTr2([disease, classification, link, mondo_link]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }

        }
    }
}

widgetInfo['dgi2'] = {
    'title': 'DGIdb: The Drug Interaction Database'
};
widgetGenerators['dgi2'] = {
    'annotators': 'dgi',
    'gene': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("dgi")
            var title = 'DGIdb: The Drug Interaction Database'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var divHeight = '250px';
            var allMappings = getWidgetData(tabName, 'dgi', row, 'all');
            if (allMappings != undefined && allMappings != null) {
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '84rem'
                sdiv.style.minWidth = '54rem'
                sdiv.style.maxHeight = '250px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                addEl(div, table);
                table.style.tableLayout = 'auto';
                table.style.width = '100%';
                var thead = getWidgetTableHead(['Category', 'Interaction', 'Drug Name', 'Score', 'ChEMBL ID', 'Pubmed'], ["16%", "16%", "16%", "16%", "16%", "16%"]);
                addEl(table, thead);
                var tbody = getEl('tbody');
                for (var i = 0; i < allMappings.length; i++) {
                    var row = allMappings[i];
                    var cat = row[0];
                    var inter = row[1];
                    var name = row[2];
                    var score = row[3];
                    var chem = row[4];
                    var pubs = row[5].toString();
                    pubs = pubs.split(',')
                    for (var j = 0; j < pubs.length; j++) {
                        var pub = pubs[j];
                        var link = `https://www.ebi.ac.uk/chembl/g/#search_results/compounds/query=${chem}`
                        var link2 = `https://pubmed.ncbi.nlm.nih.gov/${pub}`
                        var tr = getWidgetTableTr2([cat, inter, name, score, link, link2], [chem, pub]);
                        addEl(tbody, tr);
                        addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                    }
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}

widgetInfo['cgc2'] = {
    'title': 'Cancer Genome Census'
};
widgetGenerators['cgc2'] = {
    'annotators': 'cgc',
    'gene': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cgc")
            var title = 'CGC'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var driver_class = getWidgetData(tabName, 'cgc', row, 'class');
            var inheritance = getWidgetData(tabName, 'cgc', row, 'inheritance');
            var tts = getWidgetData(tabName, 'cgc', row, 'tts');
            var ttg = getWidgetData(tabName, 'cgc', row, 'ttg');
            var gene_link = getWidgetData(tabName, 'cgc', row, 'link');
            var link = 'https://cancer.sanger.ac.uk/cosmic/gene/analysis?ln=' + gene_link
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Driver Class', 'Inheritence', 'Tumor Types Somatic', 'Tumor Types Germline', 'Link']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr2([driver_class, inheritance, tts, ttg, link], [gene_link]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}


widgetInfo['basepanel'] = {
    'title': ''
};
widgetGenerators['basepanel'] = {
    'variant': {
        'width': '100%',
        'height': '100%',
        'function': function (div, row, tabName) {
            var generator = widgetGenerators['base2']['variant'];
            var divs = showWidget('base2', ['base', 'dbsnp', 'thousandgenomes', 'gnomad', 'uniprot'], 'variant', div, null, null, false);
            div.style.backgroundColor = "white"
            addEl(div, getEl('br'));
        }
    }
}

widgetInfo['swissprot_binding2'] = {
    'title': 'Swiss-Prot Binding'
};
widgetGenerators['swissprot_binding2'] = {
    'annotators': 'swissprot_binding',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("swissprot_binding")
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var divHeight = '400px';
            var allMappings = getWidgetData(tabName, 'swissprot_binding', row, 'all');
            if (allMappings != undefined && allMappings != null) {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                var thead = getWidgetTableHead(['UniprotKB ID', 'Active Binding Site', 'Binding Site', 'Calcium Binding Site', 'DNA Binding Site', 'Metal Ion Binding Site', 'Nucleotide Phosphate Binding Site', 'Zinc Finger Binding Site', 'Pubmed']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '80rem'
                sdiv.style.minWidth = '60rem'
                for (var i = 0; i < allMappings.length; i++) {
                    var row = allMappings[i];
                    var id = row[0];
                    var act = row[1];
                    var bind = row[2];
                    var ca = row[3];
                    var dna = row[4];
                    var metal = row[5]
                    var np = row[6]
                    var zn = row[7]
                    var pub = row[8]
                    var link = `https://www.uniprot.org/uniprot/${id}`
                    var link2 = `https://pubmed.ncbi.nlm.nih.gov/${pub}`
                    var tr = getWidgetTableTr2([link, act, bind, ca, dna, metal, np, zn, link2], [id, pub]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}

widgetInfo['swissprot_domains2'] = {
    'title': 'Swiss-Prot Domains'
};
widgetGenerators['swissprot_domains2'] = {
    'annotators': 'swissprot_domains',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var titleEl = makeModuleDescUrlTitle("swissprot_domains")
            var allMappings = getWidgetData(tabName, 'swissprot_domains', row, 'all');
            if (allMappings != undefined && allMappings != null) {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                var thead = getWidgetTableHead(['UniprotKB ID', 'Pubmed']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                for (var i = 0; i < allMappings.length; i++) {
                    var sdiv = getEl('div')
                    sdiv.style.maxWidth = '40rem'
                    sdiv.style.minWidth = '30rem'
                    sdiv.style.maxHeight = '250px'
                    var row = allMappings[i];
                    var id = row[0];
                    var pub = row[8]
                    var link = `https://www.uniprot.org/uniprot/${id}`
                    var link2 = `https://pubmed.ncbi.nlm.nih.gov/${pub}`
                    var tr = getWidgetTableTr2([link, link2], [id, pub]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}

widgetInfo['swissprot_ptm2'] = {
    'title': 'Swiss-Prot PTM'
};
widgetGenerators['swissprot_ptm2'] = {
    'annotators': 'swissprot_ptm',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var titleEl = makeModuleDescUrlTitle("swissprot_ptm")
            var allMappings = getWidgetData(tabName, 'swissprot_ptm', row, 'all');
            if (allMappings != undefined && allMappings != null) {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                var thead = getWidgetTableHead(['UniprotKB ID', 'Crosslink', 'Disulfid Bond', 'Glycosylation', 'Initiator Methionine', 'Lipid Groups', 'Modified Residue', 'Polypeptide', 'Signal Sequence', 'Transit Peptides', 'Pubmed']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '80rem'
                sdiv.style.minWidth = '60rem'
                sdiv.style.maxHeight = '250px'
                for (var i = 0; i < allMappings.length; i++) {
                    var row = allMappings[i];
                    var id = row[0];
                    var cross = row[1];
                    var gly = row[2];
                    var init = row[3];
                    var lg = row[4];
                    var mod = row[5]
                    var poly = row[6]
                    var ss = row[7]
                    var tp = row[8]
                    var dis = row[9]
                    var pub = row[10]
                    var link = `https://www.uniprot.org/uniprot/${id}`
                    var link2 = `https://pubmed.ncbi.nlm.nih.gov/${pub}`
                    var tr = getWidgetTableTr2([link, cross, dis, gly, init, lg, mod, poly, ss, tp, link2], [id, pub]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}

widgetInfo['cancerassocpanel'] = {
    'title': ''
};
widgetGenerators['cancerassocpanel'] = {
    'variant': {
        'width': null,
        'height': null,
        'function': function (div, row, tabName) {
            var divs = showWidget('cgc2', ['cgc'], 'gene', div, null, null, false);
            var divs = showWidget('cosmic2', ['cosmic'], 'variant', div, null, null, false);
            var divs = showWidget('cgi2', ['cancer_genome_interpreter'], 'variant', div, null, null, false);
            var divs = showWidget('target2', ['target'], 'variant', div, null, null, false);
            var divs = showWidget('civic2', ['civic'], 'variant', div, null, null, false);
            var divs = showWidget('chasmplus2', ['chasmplus'], 'variant', div, null, null, false);
            var divs = showWidget('cscape', ['cscape'], 'variant', div, null, null, false);
        }
    }
}


widgetInfo['predictionpanel'] = {
    'title': ''
};
widgetGenerators['predictionpanel'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var br = getEl("br");
            addEl(div, br);
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var scores = [];
            var rankscores = [];
            var predictions = [];
            var names = ['dann_coding', 'fathmm', 'fathmm_mkl', 'fathmm_xf_coding', 'lrt', 'metalr', 'metasvm', 'mutation_assessor', 'mutpred1', 'mutationtaster2', 'polyphen2hdiv', 'polyphen2hvar', 'provean2', 'revel2', 'sift2', 'vest2'];
            
            // Dann Coding
            // no prediction for Dann Coding
            predictions.push(predWidget(null));
            var dann_score = getWidgetData(tabName, 'dann_coding', row, 'dann_coding_score');
            var dann_rankscore = getWidgetData(tabName, 'dann_coding', row, 'dann_rankscore');
            scores.push(predWidget(dann_score));
            rankscores.push(predWidget(dann_rankscore));

            // Fathmm
            var fathmm_score = getWidgetData(tabName, 'fathmm', row, 'fathmm_score');
            if (fathmm_score != undefined || fathmm_score != null) {
                let scoreArray = fathmm_score.split(";").map(Number);
                let maxIndex;
                if (fathmm_score.endsWith(';.')) {
                    maxIndex = 0
                } else {
                    maxIndex = scoreArray.indexOf(Math.max(...scoreArray));
                }
                scores.push(predWidget(scoreArray[maxIndex]));
                var fathmm_pred = getWidgetData(tabName, 'fathmm', row, 'fathmm_pred');
                var predArray = fathmm_pred.split(";");
                let prediction;
                if (predArray[maxIndex] === "T") {
                    prediction = "Tolerated"
                } else if (predArray[maxIndex] === "D") {
                    prediction = "Damaging"
                }
                predictions.push(predWidget(prediction));
            } else {
                scores.push(predWidget(null));
                predictions.push(predWidget(null));
            }
            var fathmm_rankscore = getWidgetData(tabName, 'fathmm', row, 'fathmm_rscore');
            if (fathmm_rankscore != undefined || fathmm_rankscore != null) {
                rankscores.push(predWidget(fathmm_rankscore));
            } else {
                rankscores.push(predWidget(null));
            }

            // Fathmm Mkl
            var mkl_pred = getWidgetData(tabName, 'fathmm_mkl', row, 'fathmm_mkl_coding_pred');
            predictions.push(predWidget(mkl_pred))
            var mkl_score = getWidgetData(tabName, 'fathmm_mkl', row, 'fathmm_mkl_coding_score');
            scores.push(predWidget(mkl_score));
            var mkl_rankscore = getWidgetData(tabName, 'fathmm_mkl', row, 'fathmm_mkl_coding_rankscore');
            rankscores.push(predWidget(mkl_rankscore))

            // Fathmm xf
            var xf_pred = getWidgetData(tabName, 'fathmm_xf_coding', row, 'fathmm_xf_coding_pred');
            predictions.push(predWidget(xf_pred))
            var xf_score = getWidgetData(tabName, 'fathmm_xf_coding', row, 'fathmm_xf_coding_score');
            scores.push(predWidget(xf_score))
            var xf_rankscore = getWidgetData(tabName, 'fathmm_xf_coding', row, 'fathmm_xf_coding_rankscore');
            rankscores.push(predWidget(xf_rankscore))

            // lrt
            var lrt_pred = getWidgetData(tabName, 'lrt', row, 'lrt_pred');
            predictions.push(predWidget(lrt_pred))
            var lrt_score = getWidgetData(tabName, 'lrt', row, 'lrt_score');
            scores.push(predWidget(lrt_score))
            var lrt_rankscore = getWidgetData(tabName, 'lrt', row, 'lrt_converted_rankscore');
            rankscores.push(predWidget(lrt_rankscore))

            // metalr
            var metalr_pred = getWidgetData(tabName, 'metalr', row, 'pred');
            predictions.push(predWidget(metalr_pred));
            var metalr_score = getWidgetData(tabName, 'metalr', row, 'score');
            scores.push(predWidget(metalr_score))
            var metalr_rankscore = getWidgetData(tabName, 'metalr', row, 'rankscore');
            rankscores.push(predWidget(metalr_rankscore))
    
            // metasvm
            var metasvm_pred = getWidgetData(tabName, 'metasvm', row, 'pred');
            predictions.push(predWidget(metasvm_pred))
            var metasvm_score = getWidgetData(tabName, 'metasvm', row, 'score');
            scores.push(predWidget(metasvm_score))
            var metasvm_rankscore = getWidgetData(tabName, 'metasvm', row, 'rankscore');
            rankscores.push(predWidget(metasvm_rankscore))

            // Mutation Assessor
            var muta_pred = getWidgetData(tabName, 'mutation_assessor', row, 'impact');
            predictions.push(predWidget(muta_pred))
            var muta_score = Number(getWidgetData(tabName, 'mutation_assessor', row, 'score'));
            scores.push(predWidget(muta_score))
            var muta_rankscore = Number(getWidgetData(tabName, 'mutation_assessor', row, 'rankscore'));
            rankscores.push(predWidget(muta_rankscore))

            // mutpred
            // mutpred offers no prediction
            predictions.push(predWidget(null))
            var mutpred_score = getWidgetData(tabName, 'mutpred1', row, 'mutpred_general_score');
            scores.push(predWidget(mutpred_score))
            var mutpred_rankscore = getWidgetData(tabName, 'mutpred1', row, 'mutpred_rankscore');
            rankscores.push(predWidget(mutpred_rankscore))

            // mutation taster
            var taster_pred = getWidgetData(tabName, 'mutationtaster', row, 'prediction');
            predictions.push(predWidget(taster_pred))
            var taster_score = getWidgetData(tabName, 'mutationtaster', row, 'score');
            scores.push(predWidget(taster_score))
            var taster_rankscore = getWidgetData(tabName, 'mutationtaster', row, 'rankscore');
            rankscores.push(predWidget(taster_rankscore))
            
            // polyphen hdiv
            let hdiv_pred = getWidgetData(tabName, 'polyphen2', row, 'hdiv_pred');
            if (hdiv_pred == 'D') {
                hdiv_pred = 'Probably Damaging';
            } else if (hdiv_pred == 'P') {
                hdiv_pred = 'Possibly Damaging';
            } else if (hdiv_pred == 'B') {
                hdiv_pred = 'Benign';
            }
            predictions.push(predWidget(hdiv_pred))
            var hdiv_score = getWidgetData(tabName, 'polyphen2', row, 'hdiv_score');
            scores.push(predWidget(hdiv_score))
            var hdiv_rankscore = getWidgetData(tabName, 'polyphen2', row, 'hdiv_rank');
            rankscores.push(predWidget(hdiv_rankscore))
            
            // polyphen hvar
            let hvar_pred = getWidgetData(tabName, 'polyphen2', row, 'hvar_pred');
            if (hvar_pred == 'D') {
                hvar_pred = 'Probably Damaging';
            } else if (hvar_pred == 'P') {
                hvar_pred = 'Possibly Damaging';
            } else if (hvar_pred == 'B') {
                hvar_pred = 'Benign';
            }
            predictions.push(predWidget(hvar_pred))
            var hvar_score = getWidgetData(tabName, 'polyphen2', row, 'hvar_score');
            scores.push(predWidget(hvar_score))
            var hvar_rankscore = getWidgetData(tabName, 'polyphen2', row, 'hvar_rank');
            rankscores.push(predWidget(hvar_rankscore))
            
            // provean
            var provean_pred = getWidgetData(tabName, 'provean', row, 'prediction');
            predictions.push(predWidget(provean_pred))
            var provean_score = getWidgetData(tabName, 'provean', row, 'score');
            scores.push(predWidget(provean_score))
            var provean_rankscore = getWidgetData(tabName, 'provean', row, 'rankscore');
            rankscores.push(predWidget(provean_rankscore))

            // revel
            var revel_score = getWidgetData(tabName, 'revel', row, 'score');
            scores.push(predWidget(revel_score))
            var revel_rankscore = getWidgetData(tabName, 'revel', row, 'rankscore');
            rankscores.push(predWidget(revel_rankscore))
            let revel_pred = null
            if (revel_score !== null) {
                if (revel_score <= 0.183) {
                    revel_pred = "Benign"
                } else if (revel_score >= 0.773) {
                    revel_pred = "Pathogenic"
                } else {
                    revel_pred = "Uncertain"
                }
            }
            predictions.push(predWidget(revel_pred))

            // sift
            var sift_pred = getWidgetData(tabName, 'sift', row, 'prediction');
            predictions.push(predWidget(sift_pred))
            var sift_score = getWidgetData(tabName, 'sift', row, 'score');
            scores.push(predWidget(sift_score))
            var sift_rankscore = getWidgetData(tabName, 'sift', row, 'rankscore');
            rankscores.push(predWidget(sift_rankscore))
            
            // vest
            var vest_score = getWidgetData(tabName, 'vest', row, 'score');
            scores.push(predWidget(vest_score))
            // vest provides no rank score
            rankscores.push(predWidget(null))
            let vest_pred = null
            if (vest_score != null) {
                if (vest_score <= 0.302) {
                    vest_pred = "Benign"
                } else if ( vest_score >= 0.861) {
                    vest_pred = "Pathogenic"
                } else {
                    vest_pred = "Uncertain"
                }
            }
            predictions.push(predWidget(vest_pred));

            var table = getWidgetTableFrame();
            table.setAttribute("id", "pred");
            var tbody = getEl('tbody');
            tooltipContent = [
                {id: "source", label: "Source", info: null},
                {id: "prediction", label: "Prediction", info: "Predictions, when provided, indicate the predicted outcome or impact of the variant."},
                {id: "score", label: "Score", info: "Raw scores reported by the method."},
                {id: "rankscore", label: "Rankscore", info: "When provided rankscores closer to 0 are considered more tolerated, while rankscores closer to 1 are considered more damaging."}
            ]
            var thead = getWidgetTableHeadTooltips(tooltipContent);
            addEl(table, thead);
            var sdiv = getEl('div');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '75rem'
            sdiv.style.minWidth = '45rem'
            sdiv.style.maxHeight = '100%'
            sdiv.style.overflow = 'auto'
            var counts = [];
            var dam_count = 0;
            var tol_count = 0;
            var uncertain_count = 0;
            for (var i = 0; i < names.length; i++) {
                var name = names[i];
                var titleEl = makeModuleDescUrlTitle(name)
                var tr = document.createElement('tr');
                var td = document.createElement('td');
                td.style.textAlign = 'center';
                td.style.verticalAlign = 'middle';
                addEl(tr, td);
                addEl(td, titleEl)
                var pred = predictions[i];
                var p = pred.textContent
                var score = scores[i];
                if (score.textContent !== "") {
                    score.classList.add('pred_score');
                } else {
                    pred.textContent = getNoAnnotMsgVariantLevel()
                    pred.classList.add("pred_noanno")
                }
                var td = document.createElement('td');
                if (p.includes('Damaging') || p == 'Medium' || p == 'Disease Causing' ||  p == "Pathogenic") {
                    dam_count = dam_count + 1;
                    pred.classList.add('pred_damaging');
                } else if ( p === "Uncertain") {
                    uncertain_count = uncertain_count + 1
                    pred.classList.add('pred_uncertain');
                } else if (p != "") {
                    tol_count = tol_count + 1;
                    pred.classList.add('pred_tol');
                }
                addEl(tr, td);
                addEl(td, pred)
                var td = document.createElement('td');
                addEl(td, score)
                addEl(tr, td);
                var rank = rankscores[i];
                var td = document.createElement('td');
                addEl(td, rank);
                addEl(tr, td);
                addEl(tbody, tr);
            }
            counts.push(dam_count);
            counts.push(tol_count);
            counts.push(uncertain_count);
            var total_count = dam_count + tol_count + uncertain_count
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            var sdiv = getEl('div');
            sdiv.className = "prediction"
            var chartDiv = getEl('canvas');
            var span = getEl('span')
            span.innerHTML = tol_count + "/" + total_count + " Tolerated or Benign"
            addEl(sdiv, chartDiv);
            addEl(sdiv, span)
            var chart = new Chart(chartDiv, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: counts,
                        backgroundColor: ['rgba(153, 27, 27, 1)', 'rgba(6, 95, 70, 1)', 'black']
                    }],
                    labels: ['Damaging / Pathogenic', 'Tolerated / Benign', 'Uncertain']
                },
                options: {
                    responsive: true,
                    responsiveAnimationDuration: 500,
                    maintainAspectRatio: false,
                    legend: {
                        display: false,
                        position: 'right',
                    },
                    plugins: {
                        labels: {
                            render: 'label',
                            fontColor: 'white',
                            overlap: false,
                            outsidePadding: 4,
                        }
                    },
                },
            });
            addDlRow(dl, sdiv, wdiv)
            var br = getEl("br");
            addEl(div, br);
        }
    }
}

widgetInfo['functionalpanel'] = {
    'title': ''
};
widgetGenerators['functionalpanel'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var br = getEl("br");
            addEl(div, br);
            var divs = showWidget('swissprot_binding2', ['swissprot_binding'], 'variant', div, null, null, false);
            var divs = showWidget('swissprot_domains2', ['swissprot_domains'], 'variant', div, null, null, false);
            var divs = showWidget('swissprot_ptm2', ['swissprot_ptm'], 'variant', div, null, null, false);
        }
    }
}


widgetInfo['clinpanel'] = {
    'title': ''
};
widgetGenerators['clinpanel'] = {
    'annotators': 'clinvar',
    'variant': {
        'width': null,
        'height': null,
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var id = getWidgetData(tabName, 'clinvar', row, 'id');
            var sig = getWidgetData(tabName, 'clinvar', row, 'sig');
            var ps1 = getWidgetData(tabName, 'clinvar_acmg', row, 'ps1_id');
            var pm5 = getWidgetData(tabName, 'clinvar_acmg', row, 'pm5_id');
            var titleEl = makeModuleDescUrlTitle("clinpanel", "ClinVar")
            if (id != undefined && sig != 'Uncertain significance' || sig != undefined) {
                var divs = showWidget('clinvar2', ['clinvar'], 'variant', div, null, null, false);
            } else if (ps1 != undefined || pm5 != undefined && sig == undefined) {
                var divs = showWidget('clinvar_acmg', ['clinvar_acmg'], 'variant', div, null, null, false);
            } else if (sig == 'Uncertain significance' && ps1 != undefined || pm5 != undefined) {
                var divs = showWidget('clinvar2', ['clinvar'], 'variant', div, null, null, false);
                var divs = showWidget('clinvar_acmg', ['clinvar_acmg'], 'variant', div, null, null, false);
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'));
            var generator = widgetGenerators['clingen2']['gene'];
            var divs = showWidget('clingen2', ['clingen'], 'gene', div, null, null, false);

            var button2 = document.createElement('button');

            button2.onclick = function () {
                pharm()
            };
            button2.innerHTML = 'Pharmacogenomics';
            button2.style.position = 'relative'
            var img2 = document.createElement("img");
            img2.classList.add('triangle-right')
            addEl(button2, img2)
            button2.classList.add('clinbutton')
            div.appendChild(button2);

            var sdiv = getEl('div')
            sdiv.id = 'contents'
            sdiv.style.display = 'none'
            addEl(div, sdiv)
            var ssdiv = getEl('div')
            ssdiv.id = 'contentss'
            ssdiv.style.display = 'none'
            addEl(div, ssdiv)
            var divs = showWidget('dgi2', ['dgi'], 'gene', ssdiv, null, null, false);
            var pharm = function () {
                img2.classList.remove('triangle-down')
                var mydiv = document.getElementById('contentss');
                if (mydiv.style.display === 'none' || mydiv.style.display === '') {
                    mydiv.style.display = 'block'
                    img2.classList.add('triangle-down')
                } else
                    mydiv.style.display = 'none'
            }

        }
    }
}

const getHugoAchange = function () {
    return annotData['base']['hugo'] + ' ' + changeAchange3to1(annotData['base']['achange'])
}
const getNoAnnotMsgVariantLevel = function () {
    return 'No annotation available for ' + getHugoAchange()
}
const prettyVal = function (val) {
    if (val == '') {
        return val
    } else if (val < 0.01 && val > -0.01) {
        return val.toExponential(2)
    } else {
        return val.toPrecision(3)
    }
}

const addDlRow = function (dl, title, content) {
    var ddiv = getEl('div')
    var dt = getEl('dt')
    if (typeof title == 'string') {
        dt.textContent = title
    } else {
        addEl(dt, title)
    }
    var dd = getEl('dd')
    var contentType = typeof content
    if (contentType == 'string') {
        dd.textContent = content
    } else if (contentType == 'number') {
        dd.textContent = '' + content
    } else {
        addEl(dd, content)
    }
    addEl(ddiv, dt)
    addEl(ddiv, dd)
    addEl(dl, ddiv)
}

const makeA = function (text, url) {
    var a = getEl('a')
    a.href = url
    a.textContent = text
    a.target = '_blank'
    return a
}
widgetInfo['allelefreqpanel'] = {
    'title': ''
};
widgetGenerators['allelefreqpanel'] = {
    'variant': {
        'width': undefined,
        'height': 'unset',
        'function': function (div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var hugoAchange = getHugoAchange()
            var titleEl = makeModuleDescUrlTitle("gnomad3", "gnomADv3 Allele Frequency")
            if (annotData['gnomad3'] == null) {
                var td = getNoAnnotMsgVariantLevel()
                addDlRow(dl, titleEl, td)
            } else {
                let af = annotData['gnomad3']['af']
                let afr = annotData['gnomad3']['af_afr']
                let asj = annotData['gnomad3']['af_asj']
                let eas = annotData['gnomad3']['af_eas']
                let fin = annotData['gnomad3']['af_fin']
                let amr = annotData['gnomad3']['af_amr']
                let nfe = annotData['gnomad3']['af_nfe']
                let oth = annotData['gnomad3']['af_oth']
                let sas = annotData['gnomad3']['af_sas']
                var tableData = [af, afr, asj, eas, fin, amr, nfe, oth, sas]
                var barColors = [
                    `rgba(255, ${(1 - af) * 255}, ${(1 - af) * 240}, 1)`,
                    `rgba(255, ${(1 - afr) * 255}, ${(1 - afr) * 240}, 1)`,
                    `rgba(255, ${(1 - asj) * 255}, ${(1 - asj) * 240}, 1)`,
                    `rgba(255, ${(1 - eas) * 255}, ${(1 - eas) * 240}, 1)`,
                    `rgba(255, ${(1 - fin) * 255}, ${(1 - fin) * 240}, 1)`,
                    `rgba(255, ${(1 - amr) * 255}, ${(1 - amr) * 240}, 1)`,
                    `rgba(255, ${(1 - nfe) * 255}, ${(1 - nfe) * 240}, 1)`,
                    `rgba(255, ${(1 - oth) * 255}, ${(1 - oth) * 240}, 1)`,
                    `rgba(255, ${(1 - sas) * 255}, ${(1 - sas) * 240}, 1)`,
                ]
                var labels = [
                    'Total',
                    'African/African American',
                    'Ashkenazi Jewish',
                    'East Asian',
                    'Finnish',
                    'Latino/Admixed American',
                    'Non-Finnish European',
                    'Other',
                    'South Asian',
                ]
                var td = getEl('canvas')
                td.id = 'gnomad3_chart'
                td.style.width = '100%'
                td.style.height = '24rem'
                td.style.backgroundColor = 'white'
                td.style.borderRadius = '9px'
                addDlRow(dl, titleEl, td)
                var chart = new Chart(td, {
                    type: 'horizontalBar',
                    data: {
                        datasets: [{
                            data: tableData,
                            backgroundColor: barColors,
                        }],
                        labels: labels,
                    },
                    options: {
                        animation: {
                            onComplete: function () {
                                var ctx = this.chart.ctx
                                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily)
                                ctx.fillStyle = this.chart.config.options.defaultFontColor
                                ctx.textAlign = 'center'
                                ctx.textBaseline = 'bottom'
                                this.data.datasets.forEach(function (dataset) {
                                    for (var i = 0; i < dataset.data.length; i++) {
                                        var model = dataset._meta[
                                            Object.keys(dataset._meta)[0]].data[i]._model;
                                        if (dataset.data[i] != undefined) {
                                            ctx.fillText(
                                                prettyVal(dataset.data[i]),
                                                Math.max(model.base + 30, model.x - 20),
                                                model.y + 5
                                            )
                                        }
                                    }
                                })
                            }
                        },
                        scales: {
                            xAxes: [{
                                ticks: {
                                    max: 1.0,
                                    min: 0.0,
                                }
                            }],
                        },
                        responsive: true,
                        responsiveAnimationDuration: 500,
                        maintainAspectRatio: false,
                        legend: {
                            display: false,
                            position: 'right',
                        },
                        plugins: {
                            labels: {
                                render: 'label',
                                fontColor: '#000000',
                                overlap: false,
                                outsidePadding: 4,
                            }
                        },
                    },
                })
            }
            var titleEl = makeModuleDescUrlTitle("thousandgenomes", "1000 Genomes Allele Frequency")
            if (annotData['thousandgenomes'] == null) {
                var td = getNoAnnotMsgVariantLevel()
                addDlRow(dl, titleEl, td)
            } else {
                let af = annotData['thousandgenomes']['af']
                let amr = annotData['thousandgenomes']['amr_af']
                let afr = annotData['thousandgenomes']['afr_af']
                let eas = annotData['thousandgenomes']['eas_af']
                let eur = annotData['thousandgenomes']['eur_af']
                let sas = annotData['thousandgenomes']['sas_af']
                var tableData = [af, amr, afr, eas, eur, sas]
                var barColors = [
                    `rgba(255, ${(1 - af) * 255}, ${(1 - af) * 240}, 1)`,
                    `rgba(255, ${(1 - amr) * 255}, ${(1 - amr) * 240}, 1)`,
                    `rgba(255, ${(1 - afr) * 255}, ${(1 - afr) * 240}, 1)`,
                    `rgba(255, ${(1 - eas) * 255}, ${(1 - eas) * 240}, 1)`,
                    `rgba(255, ${(1 - eur) * 255}, ${(1 - eur) * 240}, 1)`,
                    `rgba(255, ${(1 - sas) * 255}, ${(1 - sas) * 240}, 1)`,
                ]
                var labels = [
                    'Total',
                    'Ad Mixed American',
                    'African',
                    'East Asian',
                    'European',
                    'South Asian',
                ]
                var td = getEl('canvas')
                td.id = 'thousandgenomes_chart'
                td.style.width = '100%'
                td.style.height = '17rem'
                td.style.backgroundColor = 'white'
                td.style.borderRadius = '9px'
                addDlRow(dl, titleEl, td)
                var chart = new Chart(td, {
                    type: 'horizontalBar',
                    data: {
                        datasets: [{
                            data: tableData,
                            backgroundColor: barColors,
                        }],
                        labels: labels,
                    },
                    options: {
                        animation: {
                            onComplete: function () {
                                var ctx = this.chart.ctx
                                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily)
                                ctx.fillStyle = this.chart.config.options.defaultFontColor
                                ctx.textAlign = 'center'
                                ctx.textBaseline = 'bottom'
                                this.data.datasets.forEach(function (dataset) {
                                    for (var i = 0; i < dataset.data.length; i++) {
                                        var model = dataset._meta[
                                            Object.keys(dataset._meta)[0]].data[i]._model;
                                        if (dataset.data[i] != undefined) {
                                            ctx.fillText(
                                                prettyVal(dataset.data[i]),
                                                Math.max(model.base + 30, model.x - 20),
                                                model.y + 5
                                            )
                                        }
                                    }
                                })
                            }
                        },
                        scales: {
                            xAxes: [{
                                ticks: {
                                    max: 1.0,
                                    min: 0.0,
                                }
                            }],
                        },
                        responsive: true,
                        responsiveAnimationDuration: 500,
                        maintainAspectRatio: false,
                        legend: {
                            display: false,
                            position: 'right',
                        },
                        plugins: {
                            labels: {
                                render: 'label',
                                fontColor: '#000000',
                                overlap: false,
                                outsidePadding: 4,
                            }
                        },
                    },
                })
            }
        }
    }
}

// function writeToVariantArea(inputData) {
//     var value = inputData['chrom'] + ':' + inputData['pos'] +
//         ':' + inputData['ref'] + ':' + inputData['alt'] + ':' + inputData['assembly']
//     document.querySelector('#input_variant').value = value;
// }

function hideSpinner() {
    document.querySelector('#spinnerdiv').style.display = 'none';
}

function showSpinner() {
    document.querySelector('#spinnerdiv').style.display = 'flex';
}

function processUrl() {
    var inputData = getInputDataFromUrl();
    if (inputData != null) {
        // writeToVariantArea(inputData);
        submitAnnotate(inputData['chrom'], inputData['pos'],
            inputData['ref'], inputData['alt'], inputData['assembly']);
    }
}

function setupEvents() {
    // document.querySelector('#input_variant').addEventListener('keyup', function (evt) {
    //     evt.stopPropagation();
    //     if (evt.keyCode == 13) {
    //         document.querySelector('#input_submit').click();
    //     }
    // });
    document.querySelector("body").addEventListener("click", function (evt) {
        var tooltipdiv = document.querySelector("#tooltipdiv")
        if (tooltipdiv != null) {
            if (tooltipdiv.classList.contains("show")) {
                tooltipdiv.classList.remove("show")
            }
        }
        var moduledetaildiv = document.querySelector("#moduledetaildiv")
        if (moduledetaildiv != null) {
            moduledetaildiv.classList.remove("show")
        }
    })
}


function showContentDiv() {
    document.querySelector('#detaildiv_variant').style.display = 'block';
}

function hideContentDiv() {
    document.querySelector('#detaildiv_variant').style.display = 'none';
}

function showSearch() {
    document.querySelector('#inputdiv').style.display = 'flex';
}

function run() {
    // mqMaxMatch.addListener(mqMaxMatchHandler);
    // mqMinMatch.addListener(mqMinMatchHandler);
    var params = new URLSearchParams(window.location.search);
    if (params.get('chrom') != null && params.get('pos') != null && params.get('ref_base') != null && params.get('alt_base') != null) {
        showSpinner();
        setupEvents();
        getWidgets(processUrl, null);
    } else {
        hideSpinner();
        hideContentDiv();
        showSearch();
        setupEvents();
        getWidgets(null, null);
    }
}

window.onload = function () {
    run();
}
