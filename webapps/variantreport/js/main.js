var CLOSURE_NO_DEPS = true;
var annotData = null;
var mqMaxMatch = window.matchMedia('(max-width: 1024px)');
var mqMinMatch = window.matchMedia('(min-width: 1024px)');
var localModuleInfo = {}
var storeLogos = {}
var storeUrl = null;
var storeurl = $.get('/store/getstoreurl').done(function(response) {
    storeUrl = response;
});

function emptyElement (elem) {
	var last = null;
    while (last = elem.lastChild) {
    	elem.removeChild(last);
    }
}

function makeModuleDetailDialog (moduleName, evt) {
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
	$.get('/store/modules/'+moduleName+'/'+'latest'+'/readme').done(function(data){
        var protocol = window.location.protocol;
        var converter = new showdown.Converter({tables:true,openLinksInNewWindow:true});
        var mdhtml = converter.makeHtml(data);
        if (protocol == 'https:') {
            mdhtml = mdhtml.replace(/http:/g, 'https:');
        }
        var $mdhtml = $(mdhtml);
        var localRoot = window.location.origin + window.location.pathname.split('/').slice(0,-1).join('/');
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
    addEl(d,span);
    addEl(infodiv,d);
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

function addClassRecursive (elem, className) {
    elem.classList.add(className);
    $(elem).children().each(
        function () {
            $(this).addClass(className);
            addClassRecursive(this, className);
        }
    );
}

function addLogo (moduleName, sdiv) {
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
    if (text) {
        el.textContent = text
    } else {
        if (widgetInfo[moduleName]) {
            el.textContent = widgetInfo[moduleName]["title"];
        } else {
            el.textContent = moduleName;
        }
    }
    el.classList.add('infoimg')
    addEl(div, el)
    let annotators = null;
    if (widgetGenerators[moduleName] && widgetGenerators[moduleName]['annotators']) {
        annotators = widgetGenerators[moduleName]['annotators'];
    } else {
        annotators = moduleName;
    }
    el.addEventListener('click', function(evt) {
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
                    moduleInfos.forEach(function(moduleInfo) {
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

function mqMaxMatchHandler(e) {
    if (e.matches) {
        var iframe = document.querySelector('#mupitiframe');
        var chrom = iframe.getAttribute('chrom');
        var pos = iframe.getAttribute('pos');
        iframe.src = location.protocol + '//www.cravat.us/MuPIT_Interactive?gm=' + chrom + ':' + pos + '&embed=true&showrightpanel=false';
    }
}

function mqMinMatchHandler(e) {
    if (e.matches) {
        var iframe = document.querySelector('#mupitiframe');
        var chrom = iframe.getAttribute('chrom');
        var pos = iframe.getAttribute('pos');
        iframe.src = location.protocol + '//www.cravat.us/MuPIT_Interactive?gm=' + chrom + ':' + pos + '&embed=true';
    }
}

function getInputDataFromUrl() {
    var urlParams = new URLSearchParams(window.location.search);
    var inputChrom = urlParams.get('chrom');
    var inputPos = urlParams.get('pos');
    var inputRef = urlParams.get('ref_base');
    var inputAlt = urlParams.get('alt_base');
    var assembly = urlParams.get('assembly');
    var hgvs = urlParams.get('hgvs') ? decodeURIComponent(urlParams.get('hgvs')) : null;
    var clingen = urlParams.get('clingen');
    var dbsnp = urlParams.get('dbsnp');
    if (assembly == undefined) {
        assembly = 'hg38'
    }
    var inputData = cleanInputData(inputChrom, inputPos, inputRef, inputAlt, assembly, hgvs, clingen, dbsnp);
    return inputData;
}

function cleanInputData(inputChrom, inputPos, inputRef, inputAlt, assembly, inputHgvs, inputClingen, inputDbsnp) {
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
    if (inputChrom !== null && inputPos !== null && inputRef !== null && inputAlt !== null) {
        return {
            'chrom': inputChrom,
            'pos': inputPos,
            'ref': inputRef,
            'alt': inputAlt,
            'assembly': assembly
        };
    } else if (inputHgvs !== null && inputHgvs !== '') {
        return {
            'hgvs': inputHgvs
        }
    } else if (inputClingen !== null && inputClingen !== '') {
        return {
            'clingen': inputClingen
        }
    } else if (inputDbsnp !== null && inputDbsnp !== '') {
        return {
            'dbsnp': inputDbsnp
        }
    } else {
        return null;
    }
}

function submitForm() {
    var chrom = document.querySelector('#input_variant_chrom').value;
    var pos = document.querySelector('#input_variant_pos').value;
    var ref = document.querySelector('#input_variant_ref').value;
    var alt = document.querySelector('#input_variant_alt').value;
    let hgvs = document.querySelector('#input_variant_hgvs').value;
    var inputData = cleanInputData(chrom, pos, ref, alt, '', hgvs);
    if (inputData != null) {
        showContentDiv();
        submitAnnotate(inputData['chrom'], inputData['pos'], inputData['ref'],
            inputData['alt'], inputData['assembly'], inputData['hgvs'])
    } else {
        alert('No variant input.');
    }
}

function submitAnnotate(inputChrom, inputPos, inputRef, inputAlt, assembly, inputHgvs, inputClingen, inputDbsnp) {
    showSpinner();
    if (assembly == undefined) {
        assembly = 'hg38'
    }
    var url = 'annotate';
    var params = {
        'chrom': inputChrom,
        // 'pos': parseInt(inputPos),
        'pos': inputPos,
        'ref_base': inputRef,
        'alt_base': inputAlt,
        'assembly': assembly,
        'hgvs': inputHgvs,
        'clingen': inputClingen,
        'dbsnp': inputDbsnp
    };
    $.ajax({
        type: 'POST',
        url: url,
        data: params,
        success: function(response) {
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

function buildAlternateAlleleButton(allele) {
    const label = `${allele['chrom']} ${allele['pos']} ${allele['ref_base']} ${allele['alt_base']}`;
    return `
        <a class="header-button alternate-allele" target="_blank"
        href="/webapps/variantreport/index.html?assembly=hg38&chrom=${allele['chrom']}&pos=${allele['pos']}&ref_base=${allele['ref_base']}&alt_base=${allele['alt_base']}">
            ${label}
        </a>`;
}

function showAlternateAlleles(response) {
    if ('alternateAlleles' in response && response['alternateAlleles']) {
        const alternateAllelesDiv = document.getElementById('alternate-variants');
        let markup = `Alternate Alleles for ${response['originalInput']['input']}: `;
        for (const allele of response['alternateAlleles']) {
            const btn = buildAlternateAlleleButton(allele);
            markup += btn;
        }
        alternateAllelesDiv.innerHTML = markup;
        alternateAllelesDiv.style.display = 'flex';
    }
}

function hideAlternateAlleles() {
    document.getElementById('alternate-variants').innerHTML = '';
    document.getElementById('alternate-variants').style.display = 'none';
}

function showAnnotation(response) {
    let errorDiv = document.getElementById('annotation_errors');
    errorDiv.textContent = '';
    errorDiv.style.display = 'none';
    document.querySelectorAll('.detailcontainerdiv').forEach(function(el) {
        $(el).empty();
    });
    hideSpinner();

    if ('error' in response) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = response['error'];
        hideContentDiv();
        return;
    }

    showAlternateAlleles(response);

    showSectionTitles();
    var parentDiv = document.querySelector('#contdiv_vinfo');
    var retDivs = showWidget('basepanel', ['base'], 'variant', parentDiv);
    var parentDiv = document.querySelector('#contdiv_gene'); 
    showWidget('genepanel', ['base', 'ncbigene', 'ess_gene', 'gnomad_gene', 'go', 'loftool', 'prec', 'phi', 'interpro', 'pangalodb'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_clin');
    showWidget('clinpanel',
        ['base', 'clinvar', 'clinvar_acmg', 'clingen', 'denovo', 'omim', 'cardioboost', 'cvdkp', 'arrvars', 'pharmgkb', 'dgi'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_assoc');
    showWidget('assocpanel', ['base', 'geuvadis', 'gwas_catalog', 'grasp', 'gtex'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_vizualization');
    showWidget('vizualizationpanel', ['base', 'lollipop2'], 'variant', parentDiv);
    var parentDiv = document.querySelector('#contdiv_afreq');
    showWidget('allelefreqpanel', ['base', 'gnomad3', 'thousandgenomes'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_evolution');
    showWidget('evolutionpanel', ['base', 'rvis', 'ghis', 'go', 'aloft', 'gerp', 'linsight', 'phastcons', 'phylop', 'siphy'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_studies');
    showWidget('studiespanel', ['base', 'mavedb'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_interactions');
    showWidget('interactionspanel', ['base', 'biogrid', 'ndex', 'ndex_chd', 'ndex_signor', 'intact'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_literature');
    showWidget('literaturepanel', ['base', 'litvar', 'dbsnp'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_noncoding');
    showWidget('noncodingpanel', ['base', 'ccre_screen', 'encode_tfbs', 'genehancer', 'vista_enhancer', 'ensembl_regulatory_build', 'trinity', 'segway', 'javierre_promoters'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_prediction');
    const predictionPanelModules = ['alphamissense', 'bayesdel', 'cadd', 'cadd_exome', 'esm1b', 'fathmm', 'gerp', 'phylop', 'primateai', 'revel', 'sift', 'varity_r', 'vest'];
    showWidget('predictionpanel', predictionPanelModules,
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_functional');
    showWidget('functionalpanel', ['base', 'swissprot_binding', 'swissprot_domains', 'swissprot_ptm'],
        'variant', parentDiv, null, null, false);
    var parentDiv = document.querySelector('#contdiv_cancerassoc');
    showWidget('cancerassocpanel', ['base', 'cgc', 'cosmic', 'cancer_genome_interpreter', 'target', 'civic', 'chasmplus', 'cscape_coding', 'cedar'],
        'variant', parentDiv, null, null, false);
    const input = response['originalInput'];
    writeToVariantArea(input);
    showContentDiv();
}

function getWidgets(callback, callbackArgs) {
    $.get('/result/service/widgetlist', {}).done(function(jsonResponseData) {
        var tmpWidgets = jsonResponseData;
        var widgetLoadCount = 0;
        for (var i = 0; i < tmpWidgets.length; i++) {
            var tmpWidget = tmpWidgets[i];
            var widgetName = tmpWidget['name'];
            var widgetNameNoWg = widgetName.substring(2);
            widgetInfo[widgetNameNoWg] = tmpWidget;
            $.getScript('/result/widgetfile/' + widgetName + '/' +
                widgetName + '.js',
                function() {
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

const getNoAnnotMsgGeneLevel = function() {
    return 'No annotation available for ' + annotData['base']['hugo']
}

function getNodataSpan(annotator_name) {
    var span = getEl('span');
    span.textContent = 'No annotation for' + annotator_name + 'available';
    return span;
}

function addInfoLine2(div, row, col, tabName, headerMinWidth, highlightIfValue) {
    var span = getEl("span")
    span.textContent = header
    addEl(div, span);
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

function addInfoLine3(div, row, header, col, tabName, headerMinWidth, highlightIfValue) {
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
    var sdiv = getEl('div');
    var td = getEl('span');
    td.className = 'detail-info-line-header';
    if (headerMinWidth != undefined) {
        td.style.minWidth = headerMinWidth;
    }
    var h = getLineHeader(header);
    h.style.color = color;
    addEl(td, h);
    addEl(sdiv, td);
    td = getEl('span');
    td.className = 'detail-info-line-content';
    var t = getEl('span');
    t.textContent = text;
    t.style.color = color;
    addEl(td, t);
    addEl(sdiv, td);
    if (highlightIfValue != undefined && highlightIfValue) {
        sdiv.style.color = '#ff0000';
    }
    addEl(div, sdiv);
}

function addInfoLineLink2(div, header, text, link, trimlen) {
    var span = getEl("span")
    span.textContent = header
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
const getCirclePoint = function(centerx, centery, radius, angle) {
    let x = centerx + Math.cos(angle / 180 * Math.PI) * radius
    let y = centery + Math.sin(angle / 180 * Math.PI) * radius
    let xy = {
        x: x,
        y: y
    }
    return xy
}
const drawDialFragment = function(
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
const drawDialGraph = function(title, value, threshold) {
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
const getDialWidget = function(title, value, threshold) {
    var sdiv = getEl('div');
    sdiv.classList.add('dialdiv')
    var svg = drawDialGraph(title, value, threshold)
    addEl(sdiv, svg)
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
const getDialWidget2 = function(title, value, threshold, score) {
    var sdiv = getEl('div');
    sdiv.classList.add('dialdiv2')
    var svg = drawDialGraph(title, value, threshold)
    addEl(sdiv, svg)
    var ssdiv = getEl('div')
    var sssdiv = getEl('div')
    sssdiv.textContent = title
    addEl(ssdiv, sssdiv)
    sssdiv = getEl('div')
    var span = getEl('span');
    span.textContent = prettyVal(value);
    span.style.fontSize = '1.250rem'
    addEl(sssdiv, span)
    var sspan = getEl('span')
    sspan.textContent = ' rankscore'
    sspan.style.fontSize = '0.75rem'
    addEl(sssdiv, sspan)
    addEl(ssdiv, sssdiv)
    sssdiv = getEl('div')
    var span = getEl('span');
    span.textContent = prettyVal(score)
    span.style.fontSize = '1rem'
    addEl(sssdiv, span)
    var sspan = getEl('span')
    sspan.textContent = ' score'
    sspan.style.fontSize = '0.75rem'
    addEl(sssdiv, sspan)
    addEl(ssdiv, sssdiv)
    addEl(sdiv, ssdiv)
    return sdiv
}
const predWidget = function (value) {
    var div = getEl('div');
    div.classList.add('preddiv')
    let number = value;
    if (typeof value === 'string' || value instanceof String) {
        number = parseFloat(value);
    }
    if (isNaN(number) === false && number !== null) {
        div.textContent = prettyVal(number)
    } else {
        div.textContent = value;
    }
    return div;
}

const contentWidget = function(title, value) {
    var sdiv = getEl('div');
    sdiv.classList.add('contentdiv')
    var ssdiv = getEl('div')
    var sssdiv = getEl('div')
    sssdiv.textContent = title
    addEl(ssdiv, sssdiv)
    sssdiv = getEl('div')
    sssdiv.textContent = value
    if (isNaN(value) == false && value != null) {
        sssdiv.textContent = prettyVal(value)
    } else {
        sssdiv.textContent = value
    }
    addEl(ssdiv, sssdiv)
    addEl(sdiv, ssdiv)
    return sdiv
}
const baseWidget = function(title, value) {
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

const baseWidgetlink = function(title, value, link) {
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

const barWidget = function(title, scoretitle, value, rankscore, minval, maxval, significance, other, otherscore, colors = {'0.0': [255, 255, 255], '1.0': [255, 0, 0]}){
    // Bar setup
    var maindiv = getEl('div')
    maindiv.classList.add("barWidget")
    var div = getEl('div')
    div.classList.add('barDivTitle')
    var sdiv = getEl('div')
    sdiv.classList.add('barDiv')

    // Title
    var titleSpan = getEl('span')
    titleSpan.textContent = title
    addEl(maindiv, titleSpan)
    
    // Significance
    var bottomdiv = getEl('div')
    bottomdiv.innerHTML = significance
    bottomdiv.style.display = "flex"
    if (title == "LoFtool"){
        bottomdiv.style.justifyContent = "flex-start"
    }else{
        bottomdiv.style.justifyContent = "flex-end"
    }
    bottomdiv.style.fontSize = ".75rem"
    
    //Score
    sdiv.innerHTML = value;
    sdiv.style.fontSize = "1rem"
    sdiv.style.width = value * 100 + "%"
    var percvalue = (value - parseFloat(minval)) / (Math.abs(parseFloat(minval)) + Math.abs(parseFloat(maxval)));
    sdiv.style.width = percvalue * 100 + "%"

    // Rankscore 
    if (rankscore != null){
        var rankDiv = getEl('div')
        var rankSpan = getEl("span")
        rankSpan.textContent = " rankscore"
        rankSpan.style.fontSize = "0.750rem"
        var rscore = getEl("span")
        rscore.style.fontSize = "1rem"
        rscore.textContent = rankscore
        addEl(rankDiv, rscore)
        addEl(rankDiv, rankSpan)
        addEl(maindiv, rankDiv)
    }

    // other score
    if (other != null){
        var otherDiv = getEl('div')
        var otherSpan = getEl("span")
        otherSpan.textContent = other
        otherSpan.style.fontSize = "0.750rem"
        var ospan= getEl("span")
        ospan.style.fontSize = "1rem"
        ospan.textContent = otherscore
        addEl(otherDiv, ospan)
        addEl(otherDiv, otherSpan)
        addEl(maindiv, otherDiv)
    }

    // Score span
    var scoreSpan = getEl("span")
    scoreSpan.textContent = scoretitle
    scoreSpan.style.fontSize = "0.750rem"
    addEl(maindiv, scoreSpan)
    addEl(maindiv, div)

    // make arrow
    var arrow = getEl('div')
    arrow.classList.add("arrow")
    var line = getEl('div')
    line.classList.add('line')
    var point = getEl('div')
    if (title == "LoFtool"){
        point.classList.add("pointRight")
        addEl(arrow, point)
        addEl(arrow, line)
        
    }else{
        point.classList.add('point')
        addEl(arrow, line)
        addEl(arrow, point)
    }
    
    // minimum score range
    var minSpan = getEl("span")
    minval = minval.toString()
    minSpan.textContent = minval
    minSpan.style.fontSize = "12px"

    // maximum score range
    var maxSpan = getEl("span")
    maxSpan.textContent = maxval
    
    // color of bar
    // negative values
    if (minval < 0 ){
        var difference = 0 - Number(minval)
        minval = Number(minval) + difference
        maxval = Number(maxval) + difference
        value = Number(value) + difference
    }
    if (title == "LoFtool"){
        var range = [0, 235]
    }else{
        var range = [235, 0]
    }
    var pow = d3.scalePow()
        .domain([Number(minval), Number(maxval)])
        .range(range)
        .exponent(Math.E);

    var scale = pow(Number(value))
    c = [235, scale, scale]
    var color = 'rgb(' + c.toString() + ')'
    sdiv.style.backgroundColor = color
    addEl(div, sdiv)

    // arrow with range
    var linediv = getEl('div')
    linediv.style.display = "flex"
    linediv.flex = "0 auto 0"

    addEl(linediv, minSpan)
    addEl(linediv, arrow)
    addEl(linediv, maxSpan)
    addEl(maindiv, linediv)
    addEl(maindiv, bottomdiv)

    return maindiv
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
        'function': function(div, row, tabName) {
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            var transcript = getWidgetData(tabName, 'base', row, 'transcript');
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
            div.style.maxWidth = "80vw"
            addEl(div, sdiv)
        }
    }
}

widgetInfo['ncbi'] = {
    'title': ''
};
widgetGenerators['ncbi'] = {
    'annotators': 'ncbigene',
    'gene': {
        'width': '100%',
        'height': undefined,
        'word-break': 'break-word',
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("ncbigene")
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            var dl = getEl('dl')
            addEl(div, dl)
            var desc = getWidgetData(tabName, 'ncbigene', row, 'ncbi_desc')
            if (desc != undefined || desc != null) {
                desc = desc.split(/\[.*\]$/)[0]
            }
            if (desc == null) {
                addDlRow(dl, titleEl, getNoAnnotMsgGeneLevel())
            } else {
                addDlRow(dl, titleEl, desc)
            }
        }
    }
}

widgetInfo['cgc2'] = {
    'title': 'Relation to tumor and tissue types (Cancer Gene Census)'
};
widgetGenerators['cgc2'] = {
    'gene': {
        'width': undefined,
        'height': undefined,
        'word-break': 'break-word',
        'function': function(div, row, tabName) {
            var cgc_class = getWidgetData(tabName, 'cgc', row, 'class');
            var inheritance = getWidgetData(tabName, 'cgc', row, 'inheritance');
            var tts = getWidgetData(tabName, 'cgc', row, 'tts');
            var ttg = getWidgetData(tabName, 'cgc', row, 'ttg');
            addInfoLineLink2(div, cgc_class + ' with inheritance ' + inheritance + '. Somatic types are ' + tts + '. Germline types are ' + ttg + '.');
        }
    }
}

widgetInfo['cgl2'] = {
    'title': 'Oncogenes and tumor suppressor genes (Cancer Gene Landscape)'
};
widgetGenerators['cgl2'] = {
    'gene': {
        'width': '100%',
        'height': 200,
        'function': function(div, row, tabName) {
            addInfoLineLink2(div, 'Identified as ' + getWidgetData(tabName, 'cgl', row, 'class') + '.', tabName);
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
widgetInfo['siphy2'] = {
    'title': 'SiPhy'
};
widgetGenerators['siphy2'] = {
    'annotators': 'siphy',
    'variant': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("siphy")
            var title = 'SiPhy'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            wdiv.style.overflow = 'hidden'
            var divHeight = '400px';
            var log = getWidgetData(tabName, 'siphy', row, 'logodds');
            var rank = getWidgetData(tabName, 'siphy', row, 'logodds_rank');
            if (rank != null || rank != undefined) {
                var sdiv = barWidget("SiPhy","score", prettyVal(log), prettyVal(rank), 0, 37.9718, "More" + "<br />" + "Conserved", null, null)
            } else {
                var sdiv = `No annotation is available for ${annotData["base"]["hugo"]} ${annotData["base"]["achange"]}`
            }
            sdiv.style.width = '250px'
            addDlRow(dl, titleEl, sdiv);
            var pis = getWidgetData(tabName, 'siphy', row, 'pi');
            var pils = pis != null ? pis.split(';') : [];
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '47rem'
            sdiv.style.minWidth = '20rem'
            sdiv.style.maxHeight = '400px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Nucleobase', 'Stationary Distribution']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var bases = ['A', 'C', 'G', 'T']
            for (var i = 0; i < pils.length; i++) {
                var pi = pils[i]
                var base = bases[i]
                var tr = getWidgetTableTr([base, pi]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            }
            addDlRow(dl, '', wdiv)
        }
    }
}
widgetInfo['aloft2'] = {
    'title': 'Aloft'
};
widgetGenerators['aloft2'] = {
    'annotators': 'aloft',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("aloft")
            var title = 'Aloft'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var allMappings = getWidgetData(tabName, 'aloft', row, 'all');
            if (allMappings != undefined && allMappings != null) {
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '80rem'
                sdiv.style.minWidth = '60rem'
                sdiv.style.maxHeight = '250px'
                sdiv.style.minHeight = '120px'
                sdiv.style.marginRight = '5rem'
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                var thead = getWidgetTableHead(['Transcript', 'Transcripts Affected', 'Tolerated Probability', 'Recessive Probability', 'Dominant Probability', 'Classification', 'Confidence']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                for (var i = 0; i < allMappings.length; i++) {
                    var row = allMappings[i];
                    var transcript = row[0];
                    var affect = row[1];
                    var tolerated = row[2];
                    var recessive = row[3];
                    var dominant = row[4];
                    var pred = row[5];
                    var conf = row[6];
                    var tr = getWidgetTableTr([transcript, affect, tolerated, recessive, dominant, pred, conf]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }

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
        'function': function(div, row, tabName) {
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
                    var trait_set = response['result'][id].clinical_impact_classification.trait_set;
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
                    if (traitNames.length > 0 ) {
                        addDlRow(dl, titleEl2, sdiv)
                    }
                });
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
        }
    }
}


widgetInfo['clinvar_acmg'] = {
    'title': 'ClinVar ACMG'
};
widgetGenerators['clinvar_acmg'] = {
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEll = makeModuleDescUrlTitle("clinvar_acmg", "ClinVar ACMG PM5 Conditions")
            var titleEl = makeModuleDescUrlTitle("clinvar_acmg", "ClinVar ACMG PS1 Conditions")
            var titleElps1 = makeModuleDescUrlTitle("clinvar_acmg", "ClinVar ACMG PM5 ID")
            div.parentElement.style.paddingBottom = '0'
            var ps1 = getWidgetData(tabName, 'clinvar_acmg', row, 'ps1_id');
            var pm5 = getWidgetData(tabName, 'clinvar_acmg', row, 'pm5_id');
            var dl = getEl('dl')
            addEl(div, dl)
            if (ps1 != null) {
                var link = 'https://www.ncbi.nlm.nih.gov/clinvar/variation/' + ps1;
                var a = makeA(ps1, link)
                a.classList.add('linkclass')
                addDlRow(dl, titleElps1, a)
                var url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=' + ps1 + '&retmode=json'
                fetch(url).then(response => {
                    return response.json()
                }).then(response => {
                    var trait_set = response['result'][ps1].clinical_impact_classification.trait_set;
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
                    if (traitNames.length > 0 ) {
                        addDlRow(dl, titleEl, sdiv)
                    }
                });
            } else if (pm5 != null) {
                var link = 'https://www.ncbi.nlm.nih.gov/clinvar/variation/' + pm5;
                var a = makeA(pm5, link)
                a.classList.add('linkclass')
                addDlRow(dl, 'ClinVar ACMG PM5 ID', a)
                var url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=' + pm5 + '&retmode=json'
                fetch(url).then(response => {
                    return response.json()
                }).then(response => {
                    var trait_set = response['result'][pm5].clinical_impact_classification.trait_set;
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
                    if (traitNames.length > 0 ) {
                        addDlRow(dl, titleEll, sdiv)
                    }
                });
            } else {
                addDlRow(dl, 'ClinVar', getNoAnnotMsgVariantLevel())
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

widgetInfo['clingen2'] = {
    'title': 'ClinGen Gene'
};
widgetGenerators['clingen2'] = {
    'annotators': 'clingen',
    'gene': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function(div, row, tabName) {
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

widgetInfo['pharmgkb2'] = {
    'title': 'PharmGKB'
};
widgetGenerators['pharmgkb2'] = {
    'annotators': 'pharmgkb',
    'variant': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function(div, row, tabName) {
            var title = 'PharmGKB'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var divHeight = '400px';
            var titleEl = makeModuleDescUrlTitle("pharmgkb")
            var chemical = getWidgetData(tabName, 'pharmgkb', row, 'chemicals');
            var assocs = getWidgetData(tabName, 'pharmgkb', row, 'drug_assoc');
            if (assocs != undefined && assocs != null) {

                var pharmId = getWidgetData(tabName, 'pharmgkb', row, 'id');
                link = 'https://pharmgkb.org/variant/' + pharmId;
                var a = makeA(pharmId, link)
                a.classList.add('linkclass');
                addDlRow(dl, 'PharmGKB Variant', a)
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '84rem'
                sdiv.style.minWidth = '44rem'
                sdiv.style.maxHeight = '250px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");

                addEl(div, table);
                table.style.tableLayout = 'auto';
                table.style.width = '100%';
                var thead = getWidgetTableHead(
                    ['Chemicals', 'Description', 'Category', 'Significant', 'Study', 'Notes'],
                    ['10%', '30%', '8%', '8%', '8%', '36%']
                );
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                for (let row of assocs) {
                    var study = row[4];
                    link2 = 'https://pharmgkb.org/variant/' + study;
                    var aa = makeA(study, link2)
                    for (let i = 0; i < row[0].length; i++) {
                        let chemInfo = row[0][i];
                        for (let j = 0; j < chemInfo.length; j++) {
                            var tr = getWidgetTableTr2([chemInfo[i], row[1], row[2], row[3], study, row[5]]);
                        }
                    }
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
        'function': function(div, row, tabName) {
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
                var thead = getWidgetTableHead(['Category', 'Interaction', 'Drug Name', 'Score', 'ChEMBL ID', 'Pubmed']);
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
widgetInfo['gwas_catalog2'] = {
    'title': 'GWAS Catalog'
};
widgetGenerators['gwas_catalog2'] = {
    'annotators': 'gwas_catalog',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("gwas_catalog")
            var title = 'GWAS Catalog'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var risk = getWidgetData(tabName, 'gwas_catalog', row, 'risk_allele');
            var riskAllele = getWidgetData(tabName, 'gwas_catalog', row, 'risk_allele');
            var pval = getWidgetData(tabName, 'gwas_catalog', row, 'pval');
            var isamp = getWidgetData(tabName, 'gwas_catalog', row, 'init_samp');
            var rsamp = getWidgetData(tabName, 'gwas_catalog', row, 'rep_samp');
            var conf = getWidgetData(tabName, 'gwas_catalog', row, 'ci');
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Risk Allele', 'P-value', 'Initial Sample', 'Replication Sample', 'Confidence Interval']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var sdiv = getEl('div')
            sdiv.style.width = '80rem'
            sdiv.style.maxHeight = '150px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var tr = getWidgetTableTr2([riskAllele, pval, isamp, rsamp, conf]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));

            addDlRow(dl, titleEl, wdiv)
        }
    }
}
widgetInfo['grasp2'] = {
    'title': 'GRASP'
};
widgetGenerators['grasp2'] = {
    'annotators': 'grasp',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("grasp")
            var title = 'GRASP'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var hits = getWidgetData(tabName, 'grasp', row, 'all');
            if (hits != undefined && hits != null) {
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '70rem'
                sdiv.style.minWidth = '30rem'
                sdiv.style.maxHeight = '250px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                addEl(div, table);
                var thead = getWidgetTableHead(['Pval', 'Phenotype', 'NHLBI', 'PubMed']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                for (var i = 0; i < hits.length; i++) {
                    var hit = hits[i];
                    var pheno = hit[2];
                    var pval = hit[3];
                    var nhlbi = hit[0];
                    var pmid = hit[1];
                    var pmLink = 'https://www.ncbi.nlm.nih.gov/pubmed/' + pmid
                    var tr = getWidgetTableTr2([pval, pheno, nhlbi, pmLink], [pmid]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}
widgetInfo['gtex2'] = {
    'title': 'GTEX'
};
widgetGenerators['gtex2'] = {
    'annotators': 'gtex',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("gtex")
            var title = 'GTEX'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var genes = getWidgetData(tabName, 'gtex', row, 'gtex_gene');
            var genels = genes != null ? genes.split('|') : [];
            var tissues = getWidgetData(tabName, 'gtex', row, 'gtex_tissue');
            var tissuels = tissues != null ? tissues.split('|') : [];
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Target Gene', 'Tissue Type']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '50rem'
            sdiv.style.minWidth = '20rem'
            sdiv.style.maxHeight = '150px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            for (var i = 0; i < genels.length; i++) {
                var geneitr = genels[i];
                var tissueitr = tissuels[i];
                tissueitr = tissueitr.replace("_", " ")
                var ensLink = 'https://ensembl.org/Homo_sapiens/Gene/Summary?g=' + geneitr;
                var tr = getWidgetTableTr2([ensLink, tissueitr], [geneitr]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            }
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['rvis2'] = {
    'title': 'RVIS'
};
widgetGenerators['rvis2'] = {
    'annotators': 'rvis',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle('rvis')
            var title = 'RVIS'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var evs = getWidgetData(tabName, 'rvis', row, 'rvis_evs');
            if (evs != null || evs != undefined) {
                evs = prettyVal(evs)
            }
            var exac = getWidgetData(tabName, 'rvis', row, 'rvis_exac');
            if (exac != null || exac != undefined) {
                exac = prettyVal(exac)
            }
            var perc_evs = getWidgetData(tabName, 'rvis', row, 'rvis_perc_evs');
            if (perc_evs != null || perc_evs != undefined) {
                perc_evs = prettyVal(perc_evs)
            }
            var perc_exac = getWidgetData(tabName, 'rvis', row, 'rvis_perc_exac');
            if (perc_exac != null || perc_exac != undefined) {
                perc_exac = prettyVal(perc_exac)
            }
            var pvalue = getWidgetData(tabName, 'rvis', row, 'rvis_fdr_exac');
            if (pvalue != null || pvalue != undefined) {
                pvalue = prettyVal(pvalue)
            }
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Score', 'Percentile Rank', 'ExAC-based RVIS', 'ExAC-based Percentile', 'FDR p-value']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '80rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '150px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var tr = getWidgetTableTr2([evs, exac, perc_evs, perc_exac, pvalue]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['gnomad_gene2'] = {
    'title': 'gnomAD Gene'
};
widgetGenerators['gnomad_gene2'] = {
    'annotators': 'gnomad_gene',
    'gene': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function(div, row, tabName) {
            var title = 'gnomAD Gene'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var divHeight = '250px';
            var titleEl = makeModuleDescUrlTitle("gnomad_gene")
            var results = getWidgetData(tabName, 'gnomad_gene', row, 'all');
            if (results != undefined && results != null && typeof(results) == 'object') {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                addEl(div, table);
                var thead = getWidgetTableHead(['Transcript', 'Obv/Exp LoF', 'Obv/Exp Mis', 'Obv/Exp Syn', 'LoF Z-Score', 'Mis Z-Score', 'Syn Z-Score', 'pLI', 'pRec', 'pNull'], ['15%']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '72rem'
                sdiv.style.minWidth = '52rem'
                sdiv.style.maxHeight = '250px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'
                for (var i = 0; i < results.length; i++) {
                    var row = results[i];
                    var tr = getWidgetTableTr(row);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            } else {
                var trx = getWidgetData(tabName, 'gnomad_gene', row, 'transcript');
                var trxls = trx != null ? trx.split(';') : [];
                var oelof = getWidgetData(tabName, 'gnomad_gene', row, 'oe_lof');
                var oelofls = oelof != null ? oelof.split(';').map(Number) : [];
                var oemis = getWidgetData(tabName, 'gnomad_gene', row, 'oe_mis');
                var oemisls = oemis != null ? oemis.split(';').map(Number) : [];
                var oesyn = getWidgetData(tabName, 'gnomad_gene', row, 'oe_syn');
                var oesynls = oesyn != null ? oesyn.split(';').map(Number) : [];
                var lofz = getWidgetData(tabName, 'gnomad_gene', row, 'lof_z');
                var lofzls = lofz != null ? lofz.split(';').map(Number) : [];
                var misz = getWidgetData(tabName, 'gnomad_gene', row, 'mis_z');
                var miszls = misz != null ? misz.split(';').map(Number) : [];
                var synz = getWidgetData(tabName, 'gnomad_gene', row, 'syn_z');
                var synzls = synz != null ? synz.split(';').map(Number) : [];
                var pli = getWidgetData(tabName, 'gnomad_gene', row, 'pLI');
                var plils = pli != null ? pli.split(';').map(Number) : [];
                var prec = getWidgetData(tabName, 'gnomad_gene', row, 'pRec');
                var precls = prec != null ? prec.split(';').map(Number) : [];
                var pnull = getWidgetData(tabName, 'gnomad_gene', row, 'pNull');
                var pnullls = pnull != null ? pnull.split(';').map(Number) : [];
                var table = getWidgetTableFrame();
                addEl(div, table);
                var thead = getWidgetTableHead(['Transcript', 'Obv/Exp LoF', 'Obv/Exp Mis', 'Obv/Exp Syn', 'LoF Z-Score', 'Mis Z-Score', 'Syn Z-Score', 'pLI', 'pRec', 'pNull'], ['20%']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                var sdiv = getEl('div')
                sdiv.style.width = '47rem'
                sdiv.style.maxHeight = '400px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'
                for (var i = 0; i < trxls.length; i++) {
                    var tr = getWidgetTableTr([trxls[i], oelofls[i], oemisls[i], oesynls[i], lofzls[i], miszls[i], synzls[i], plils[i], precls[i], pnullls[i]]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}
widgetInfo['go2'] = {
    'title': 'Gene Ontology'
};
widgetGenerators['go2'] = {
    'annotators': 'go',
    'gene': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("go")
            var title = 'Gene Ontology'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var cco = getWidgetData(tabName, 'go', row, 'cco_id');
            var ccols = cco != null ? cco.split(';') : [];
            var cname = getWidgetData(tabName, 'go', row, 'cco_name');
            var cnames = cname != null ? cname.split(';') : [];
            var bpo = getWidgetData(tabName, 'go', row, 'bpo_id');
            var bpols = bpo != null ? bpo.split(';') : [];
            var bname = getWidgetData(tabName, 'go', row, 'bpo_name');
            var bnames = bname != null ? bname.split(';') : [];
            var mfo = getWidgetData(tabName, 'go', row, 'mfo_id')
            var mfols = mfo != null ? mfo.split(';') : [];
            var mname = getWidgetData(tabName, 'go', row, 'mfo_name')
            var mnames = mname != null ? mname.split(';') : [];
            if (cco != null && bpo != null && mfo != null){
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                addEl(div, table);
                var thead = getWidgetTableHead(['Biological Process', 'Cellular Component', 'Molecular Function']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '72rem'
                sdiv.style.minWidth = '52rem'
                sdiv.style.maxHeight = '250px'
                sdiv.style.overflow = 'auto'
                sdiv.style.marginRight = '5rem'

                if (ccols.length > bpols.length) {
                    var max = ccols.length
                } else if (bpols.length > ccols.length) {
                    max = bpols.length
                } else if (mfols.length > bpols.length) {
                    max = mfols.length
                } else if (mfols.length > ccols.length) {
                    max = mfols.length
                } else if (ccols.length > mfols.length) {
                    max = ccols.length
                } else if (bpols.length > mfols.length) {
                    max = bpols.length
                }else {
                    max = bpols.length
                }
                for (let i = 0; i < max; i++) {
                    var link = `http://amigo.geneontology.org/amigo/term/${ccols[i]}`;
                    if (ccols[i] == undefined) {
                        link = 'http://amigo.geneontology.org/amigo/term/'
                        var ccols_val = ''
                        var cname_val = ''
                    } else {
                        ccols_val = ccols[i]
                        cname_val = cnames[i]
                    }

                    var link2 = `http://amigo.geneontology.org/amigo/term/${bpols[i]}`;
                    if (bpols[i] == undefined) {
                        link2 = 'http://amigo.geneontology.org/amigo/term/'
                        var bpols_val = ''
                        var bname_val = ''
                    } else {
                        bpols_val = bpols[i]
                        bname_val = bnames[i]
                    }
                    var link3 = `http://amigo.geneontology.org/amigo/term/${mfols[i]}`;
                    if (mfols[i] == undefined) {
                        link3 = 'http://amigo.geneontology.org/amigo/term/'
                        var mfols_val = ''
                        var mname_val = ''
                    } else {
                        mfols_val = mfols[i]
                        mname_val = mnames[i]
                    }
                    var tr = getWidgetTableTr2([link2, link, link3], [bname_val, cname_val, mname_val]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }else{
                
                addDlRow(dl, titleEl, getNoAnnotMsgGeneLevel())
            }
        }
    }
}
widgetInfo['interpro2'] = {
    'title': 'Interpro'
}
widgetGenerators['interpro2'] = {
    'annotators': 'interpro',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("interpro2")
            var title = 'InterPro'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var hits = getWidgetData(tabName, 'interpro', row, 'all')
            if (hits != undefined && hits != null && typeof(hits) == 'object') {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable")
                addEl(div, table);
                var thead = getWidgetTableHead(['Domain', 'UniProt', 'Ensembl', 'Link'], ['55%', '13%', '22%', '10%']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                addEl(table, tbody);
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '72rem'
                sdiv.style.minWidth = '45rem'
                sdiv.style.maxHeight = '250px';
                for (let i = 0; i < hits.length; i++) {
                    var hit = hits[i];
                    var link = 'https://www.ebi.ac.uk/interpro/protein/' + hit[1];
                    var tr = getWidgetTableTr2([hit[0], hit[1], hit[2], link]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
            }
        }
    }
}
widgetInfo['biogrid2'] = {
    'title': 'BioGRID'
}
widgetGenerators['biogrid2'] = {
    'annotators': 'biogrid',
    'gene': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("biogrid", "BioGRID ID")
            var titleEll = makeModuleDescUrlTitle("biogrid")
            var title = 'BioGRID Interactors'
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var divHeight = '400px';
            var value = getWidgetData(tabName, 'biogrid', row, 'id');
            var id = getWidgetData(tabName, 'biogrid', row, 'id');
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            var acts = getWidgetData(tabName, 'biogrid', row, 'acts');
            var head = 'BioGRID';
            if (hugo != null) {
                var head = hugo + ' BioGRID'
            }
            var link = '';
            if (id != null) {
                link = 'https://thebiogrid.org/' + id;
                var a = makeA(id, link);
                a.classList.add('linkclass')
                addDlRow(dl, titleEl, a)
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgGeneLevel())
            }

            var actsls = acts != null ? acts.split(';') : [];
            if (actsls.length > 0) {
                var sdiv = getEl('div');
                sdiv.style.display = 'flex'
                sdiv.style.flexWrap = 'wrap'
                for (var j = 0; j < actsls.length; j++) {
                    var span = getEl('div')
                    span.classList.add('clinvar_traitname')
                    span.textContent = actsls[j]
                    addEl(sdiv, span);
                }
                addDlRow(dl, titleEll, sdiv)
            }
        }
    }
}
widgetInfo['intact2'] = {
    'title': 'IntAct'
}
widgetGenerators['intact2'] = {
    'annotators': 'intact',
    'gene': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("intact")
            var title = 'IntAct Interactors'
            var dl = getEl('dl')
            addEl(div, dl)
            var value = getWidgetData(tabName, 'intact', row, 'acts');
            var hugo = getWidgetData(tabName, 'base', row, 'hugo');
            if (hugo) {
                link = 'https://www.ebi.ac.uk/intact/query/geneName:' + hugo;
                var a = makeA(title, link)
                a.classList.add('linkclass');
            }
            var acts = getWidgetData(tabName, 'intact', row, 'acts');
            var actsls = acts != null ? acts.split(';') : [];
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            for (var j = 0; j < actsls.length; j++) {
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                span.textContent = actsls[j]
                addEl(sdiv, span);
            }
            addDlRow(dl, titleEl, sdiv)
        }
    }
}
widgetInfo['litvar'] = {
    'title': 'LitVar'
};
widgetGenerators['litvar'] = {
    'annotators': 'litvar',
    'variant': {
        'width': undefined,
        'height': undefined,
        'variables': {
            'rsids2pmids': {},
        },
        'word-break': 'break-word',
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("litvar", 'Publication(s) for this mutation (LitVar)')
            var dl = getEl('dl')
            addEl(div, dl)
            var title = 'LitVar'
            var widgetName = 'litvar';
            var v = widgetGenerators[widgetName][tabName]['variables'];
            var rsid = getWidgetData(tabName, 'dbsnp', row, 'rsid');
            if (rsid == null) {
                addDlRow(dl, title, getNoAnnotMsgVariantLevel())
                return;
            }
            var link = `https://www.ncbi.nlm.nih.gov/research/litvar2/docsum?variant=litvar@${rsid}%23%23&query=${rsid}`
            var a = makeA(rsid, link)
            addDlRow(dl, title, a)
            // if (n != undefined) {
            //     if (n == 0) {
            //         var a = getNoAnnotMsgVariantLevel()
            //     } else if (n == 1) {
            //         var a = makeA(n + ' publication for the variant (' + rsid + ')', link)
            //     } else {
            //         var a = makeA(n + ' publications for the variant (' + rsid + ')', link)
            //     }
            //     addDlRow(dl, title, a)
            // }
            // } else {
            //     var url = 'litvar?rsid=' + rsid
            //     var xhr = new XMLHttpRequest();
            //     xhr.open('GET', url, true);
            //     xhr.onreadystatechange = function() {
            //         if (xhr.readyState == XMLHttpRequest.DONE) {
            //             if (xhr.status == 200) {
            //                 var response = JSON.parse(xhr.responseText);
            //                 n = response['n']
            //                 v['rsids2pmids'][rsid] = n;
            //                 if (n == 0) {
            //                     var a = getNoAnnotMsgVariantLevel()
            //                 } else if (n == 1) {
            //                     var a = makeA(
            //                         n + ' publication for the variant (' + rsid + ')', link)
            //                     a.classList.add('linkclass')
            //                 } else {
            //                     var a = makeA(
            //                         n + ' publications for the variant (' + rsid + ')', link)
            //                     a.classList.add('linkclass')
            //                 }

            //                 addDlRow(dl, titleEl, a)
            //             }
            //         }
            //     }
            //     xhr.send();
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
        'function': function(div, row, tabName) {
            var generator = widgetGenerators['base2']['variant'];
            var divs = showWidget('base2', ['base', 'dbsnp', 'thousandgenomes', 'gnomad', 'uniprot'], 'variant', div, null, null, false);
            div.style.backgroundColor = "white"
            addEl(div, getEl('br'));
        }
    }
}
widgetInfo['phastcons3'] = {
    'title': 'Phast Cons'
};
widgetGenerators['phastcons3'] = {
    'annotators': 'phastcons',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("phastcons")
            var dl = getEl('dl')
            addEl(div, dl)
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            sdiv.style.overflow = 'hidden'
            var vert_r = getWidgetData(tabName, 'phastcons', row, 'phastcons100_vert_r');
            var vert = getWidgetData(tabName, 'phastcons', row, 'phastcons100_vert');
            var mamm_r = getWidgetData(tabName, 'phastcons', row, 'phastcons470_mamm_r');
            var mamm = getWidgetData(tabName, 'phastcons', row, 'phastcons470_mamm');
            var v = barWidget("Vertebrate", "Score", vert, prettyVal(vert_r), 0.0, 1, "More " + "<br />" + "Conserved", null, null)
            var m = barWidget("Mammalian", "Score", prettyVal(mamm), prettyVal(mamm_r),  0.0, 1, "More " + "<br />" + "Conserved", null, null)
            v.style.paddingRight = '40px'
            addEl(sdiv, v)
            addEl(sdiv, m)
            addDlRow(dl, titleEl, sdiv)
        }
    }
}
widgetInfo['phylop2'] = {
    'title': 'PhyloP'
};
widgetGenerators['phylop2'] = {
    'annotators': 'phylop',
    'variant': {
        'width': undefined,
        'height': undefined,
        'word-break': 'normal',
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var titleEl = makeModuleDescUrlTitle("phylop")
            var vert_r = getWidgetData(tabName, 'phylop', row, 'phylop100_vert_r');
            var vert = getWidgetData(tabName, 'phylop', row, 'phylop100_vert');
            if (vert_r != null || vert_r != undefined) {
                var v = barWidget("Vertebrate", "Score", prettyVal(vert), prettyVal(vert_r), -20, 10.003, "More"  + "<br />" + "Conserved", null, null)
            } else {
                var v = `No annotation is available for ${annotData["base"]["hugo"]} ${annotData["base"]["achange"]}`
            }
            var mamm_r = getWidgetData(tabName, 'phylop', row, 'phylop470_mamm_r');
            var mamm = getWidgetData(tabName, 'phylop', row, 'phylop470_mamm');
            if (mamm_r != null || mamm_r != undefined) {
                var m = barWidget("Mammalian", "Score", prettyVal(mamm), prettyVal(mamm_r), -20, 1.312, "More"  + "<br />" + "Conserved", null, null)
            } else {
                var m = `No annotation is available for ${annotData["base"]["hugo"]} ${annotData["base"]["achange"]}`
            }
            var prim_r = getWidgetData(tabName, 'phylop', row, 'phylop17_primate_r');
            var prim = getWidgetData(tabName, 'phylop', row, 'phylop17_primate');
            if (prim_r != null || prim_r != undefined) {
                var p = barWidget("Primate", "Score", prettyVal(prim), prettyVal(prim_r), -13.362, 0.756, "More"  + "<br />" + "Conserved", null, null)
            } else {
                var p = `No annotation is available for ${annotData["base"]["hugo"]} ${annotData["base"]["achange"]}`
            }
            v.style.paddingRight = '40px';
            m.style.paddingRight = '40px';
            v.style.paddingBottom = '10px';
            v.style.paddingTop = '10px';
            m.style.paddingBottom = '10px';
            m.style.paddingTop = '10px';
            p.style.paddingBottom = '10px';
            p.style.paddingTop = '10px';
            addEl(sdiv, v)
            addEl(sdiv, m)
            addEl(sdiv, p)
            addDlRow(dl, titleEl, sdiv)
        }
    }
}
widgetInfo['ccre_screen2'] = {
    'title': 'Candidate cis_Regulatory Elements by ENCODE (SCREEN)'
};
widgetGenerators['ccre_screen2'] = {
    'annotators': 'ccre_screen',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("ccre_screen")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var divHeight = '400px';
            var e_id = getWidgetData(tabName, 'ccre_screen', row, 'acc_e');
            var group = getWidgetData(tabName, 'ccre_screen', row, '_group');
            var bound = getWidgetData(tabName, 'ccre_screen', row, 'bound');
            link = 'https://screen.encodeproject.org/search/?q=' + e_id + '&assembly=GRCh38';
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Classification', 'CTCF Bound', 'cCRE Accession ID']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '60rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var tr = getWidgetTableTr2([group, bound, link], [e_id]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['encode_tfbs2'] = {
    'title': 'ENCODE TFBS'
};
widgetGenerators['encode_tfbs2'] = {
    'annotators': 'encode_tfbs',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("encode_tfbs")
            var title = 'ENCODE TFBS';
            var wdiv = getEl('div')
            var allMappings = getWidgetData(tabName, 'encode_tfbs', row, 'factor');
            if (allMappings != undefined && allMappings != null) {
                var table = getWidgetTableFrame();
                var thead = getWidgetTableHead(['Factor', 'Cell', 'Quality', 'Antibody', 'Study'], ['20%', '20%', '15%', '20%', '25%']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var sdiv = getEl('div')

                for (var i = 0; i < allMappings.length; i++) {
                    var row = allMappings[i];
                    var factor = row[4];
                    var cell = row[0];
                    var quality = row[1];
                    var antibody = row[2];
                    var study = row[3];
                    var tr = getWidgetTableTr([factor, cell, quality, antibody, study]);
                    addEl(tbody, tr);
                    addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                }
                addDlRow(dl, titleEl, wdiv)
                addEl(div, addEl(table, tbody));
            }
        }
    }
}
widgetInfo['genehancer2'] = {
    'title': 'GeneHancer'
};
widgetGenerators['genehancer2'] = {
    'annotators': 'genehancer',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("genehancer", "GeneHancer Type")
            var titleEll = makeModuleDescUrlTitle("genehancer")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var divHeight = '250px';
            var featureName = getWidgetData(tabName, 'genehancer', row, 'feature_name');
            var targetsStr = getWidgetData(tabName, 'genehancer', row, 'target_genes');
            if (!targetsStr) return
            addDlRow(dl, titleEl, featureName);
            var targets = targetsStr.split(',')
                .map(tmp => tmp.split(': '))
                .sort((a, b) => {
                    parseFloat(b[1]) - parseFloat(a[1])
                })
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['Target Gene', 'Link Strength']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '60rem'
            sdiv.style.maxWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto';
            for (var [gene, score] of targets) {
                var tr = getWidgetTableTr([gene, score]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            }
            addDlRow(dl, titleEll, wdiv)
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
        'function': function(div, row, tabName) {
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


widgetInfo['ess_gene2'] = {
    'title': 'Essential Genes'
};
widgetGenerators['ess_gene2'] = {
    'annotators': 'ess_gene',
    'gene': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("ess_gene2")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            var thead = getWidgetTableHead(['Essential', 'CRISPR', 'CRISPR2', 'Gene Trap', 'Indespensibility Score', 'Indespensibility Prediction']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '72rem'
            sdiv.style.minWidth = '50rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var ess = getWidgetData(tabName, 'ess_gene', row, 'ess_gene');
            if (ess == 'E') {
                ess = 'Essential'
            } else if (ess == 'N') {
                ess = 'Non-essential'
            }
            var crisp = getWidgetData(tabName, 'ess_gene', row, 'ess_gene_crispr');
            if (crisp == 'E') {
                crisp = 'Essential'
            } else if (crisp == 'N') {
                crisp = 'Non-essential phenotype-changing'
            }
            var crisp2 = getWidgetData(tabName, 'ess_gene', row, 'ess_gene_crispr2');
            if (crisp2 == 'E') {
                crisp2 = 'Essential'
            } else if (crisp2 == 'N') {
                crisp2 = 'Non-essential phenotype-changing'
            } else if (crisp2 == 'S') {
                crisp2 = 'context-Specific essential'
            }
            var trap = getWidgetData(tabName, 'ess_gene', row, 'ess_gene_gene_trap');
            if (trap == 'E') {
                trap = 'Essential'
            } else if (trap == 'N') {
                trap = 'Non-essential phenotype-changing'
            } else if (trap == 'H') {
                trap = 'HAP1-Specific essential'
            } else if (trap == 'K') {
                trap = 'KBM7-Specific essential'
            }
            var score = getWidgetData(tabName, 'ess_gene', row, 'indispensability_score');
            var pred = getWidgetData(tabName, 'ess_gene', row, 'indispensability_pred');
            if (pred == 'E') {
                pred = 'Essential'
            } else if (pred == 'N') {
                pred = 'Loss-of-function tolerant'
            }
            if (score != undefined || score != null) {
                score = Number(score)
                score = prettyVal(score)
                var tr = getWidgetTableTr([ess, crisp, crisp2, trap, score, pred]);
                addEl(tbody, tr);
            }
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
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
        'function': function(div, row, tabName) {
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


widgetInfo['arrvars'] = {
    'title': 'Arrythmia Channelopathy Variants'
};
widgetGenerators['arrvars'] = {
    'annotators': 'arrvars',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle('arrvars')
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var lqt = getWidgetData(tabName, 'arrvars', row, 'lqt');
            var brs = getWidgetData(tabName, 'arrvars', row, 'brs');
            var unaff = getWidgetData(tabName, 'arrvars', row, 'unaff');
            var other = getWidgetData(tabName, 'arrvars', row, 'other');
            var bpen = getWidgetData(tabName, 'arrvars', row, 'brs_penetrance');
            var lpen = getWidgetData(tabName, 'arrvars', row, 'lqt_penetrance');
            var func = getWidgetData(tabName, 'arrvars', row, 'function');
            var bstr = getWidgetData(tabName, 'arrvars', row, 'brs_structure');
            var lstr = getWidgetData(tabName, 'arrvars', row, 'lqt_structure');
            var link = getWidgetData(tabName, 'arrvars', row, 'link');
            if (lqt != undefined && lqt != null) {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                var thead = getWidgetTableHead(['LQT', 'BrS', 'Function', 'LQT Hotspot', 'BrS Hotspot', 'Unaffected', 'Other', 'BrS Penetrance', 'LQT Penetrance', 'More Information']);
                addEl(table, thead);
                var tbody = getEl('tbody');
                var sdiv = getEl('div')
                sdiv.style.maxWidth = '80rem'
                sdiv.style.minWidth = '55rem'
                sdiv.style.display = 'flex'
                sdiv.style.flexWrap = 'wrap'
                var tr = getWidgetTableTr([lqt, brs, func, lstr, bstr, unaff, other, bpen, lpen, link]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            }
            addDlRow(dl, titleEl, wdiv)
        }
    }
}
widgetInfo['cvdkp'] = {
    'title': 'Cardiovascular Disease Knowledge Portal'
};
widgetGenerators['cvdkp'] = {
    'annotators': 'cvdkp',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cvdkp")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var ibs = getWidgetData(tabName, 'cvdkp', row, 'ibs');
            if (ibs != undefined) {
                ibs = prettyVal(ibs)
            }
            var cad = getWidgetData(tabName, 'cvdkp', row, 'cad');
            if (cad != undefined) {
                cad = prettyVal(cad)
            }
            var bmi = getWidgetData(tabName, 'cvdkp', row, 'bmi');
            if (bmi != undefined) {
                bmi = prettyVal(bmi)
            }
            var afib = getWidgetData(tabName, 'cvdkp', row, 'afib');
            if (afib != undefined) {
                afib = prettyVal(afib)
            }
            var diabetes = getWidgetData(tabName, 'cvdkp', row, 'diabetes');
            if (diabetes != undefined) {
                diabetes = prettyVal(diabetes)
            }
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            var thead = getWidgetTableHead(['IBS', 'CAD', 'BMI', 'Atrial Fibrillation', 'Type 2 Diabetes']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '80rem'
            sdiv.style.minWidth = '35rem'
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var tr = getWidgetTableTr([ibs, cad, bmi, afib, diabetes]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['cardioboost'] = {
    'title': 'CardioBoost'
};
widgetGenerators['cardioboost'] = {
    'annotators': 'cardioboost',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle('cardioboost')
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            var card = getWidgetData(tabName, 'cardioboost', row, 'cardiomyopathy1');
            if (card != undefined) {
                card = prettyVal(card)
            }
            var card2 = getWidgetData(tabName, 'cardioboost', row, 'cardiomyopathy');
            var arr = getWidgetData(tabName, 'cardioboost', row, 'arrhythmias1');
            var arr2 = getWidgetData(tabName, 'cardioboost', row, 'arrhythmias');

            if (arr2 != undefined) {
                arr2 = prettyVal(arr2)
            }
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            var thead = getWidgetTableHead(['Cradiomyopathy Score', 'Cardiomyopathy Class', 'Arrhythmia Score', 'Arrhythmia Class']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '80rem'
            sdiv.style.minWidth = '35rem'
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var tr = getWidgetTableTr([card, card2, arr2, arr]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
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
        'function': function(div, row, tabName) {
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

widgetInfo['gerp2'] = {
    'title': 'GERP++'
};
widgetGenerators['gerp2'] = {
    'annotators': 'gerp',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("gerp")
            var dl = getEl('dl')
            addEl(div, dl)
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            sdiv.style.overflow = 'hidden'
            var rs = getWidgetData(tabName, 'gerp', row, 'gerp_rs');
            var rank = getWidgetData(tabName, 'gerp', row, 'gerp_rs_rank');
            var nr = getWidgetData(tabName, 'gerp', row, 'gerp_nr');
            var rsScore = barWidget("GERP++", "RS score", prettyVal(rs), prettyVal(rank), -12.3, 6.17, "More"  + "<br />" + "Conserved", " neutral rate",prettyVal(nr))
            addEl(sdiv, rsScore)
            addDlRow(dl, titleEl, sdiv)
        }
    }
}
widgetInfo['prec2'] = {
    'title': 'P(rec)'
};
widgetGenerators['prec2'] = {
    'annotators': 'prec',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var sdiv = getEl('div');
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            
            var titleEl = makeModuleDescUrlTitle('prec')
            var prec = getWidgetData(tabName, 'prec', row, 'prec');
            var ssdiv = barWidget("P(rec)", "Probability", prec, null, 0.0001, 0.9998, "Recessive"+ "<br>" +  "Disease Gene", null, null)
            var stat = getWidgetData(tabName, 'prec', row, 'stat')
            if (stat != null || stat != undefined) {
                var stats = contentWidget('Known Status', stat)
            } else {
                var stats = contentWidget('Known Status', "No Annotation")
            }
            ssdiv.style.display = "flex"
            ssdiv.style.flexWrap = "wrap"
            ssdiv.style.flexDirection = "column"
            ssdiv.style.width = "fit-content"
            stats.style.paddingLeft = '40px'
            addEl(sdiv, ssdiv)
            addEl(sdiv, stats)
            addDlRow(dl, titleEl, sdiv)
        }
    }
}
widgetInfo['denovo'] = {
    'title': 'Denovo-DB'
};
widgetGenerators['denovo'] = {
    'annotators': 'denovo',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("denovo", "Denovo-DB Phenotype")
            var phenotype = getWidgetData(tabName, 'denovo', row, 'PrimaryPhenotype');
            if (phenotype != null) {
                addDlRow(dl, titleEl, phenotype);
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel());
            }
        }
    }
}

widgetInfo['geuvadis'] = {
    'title': 'Geuvadis eQTLs'
};
widgetGenerators['geuvadis'] = {
    'annotators': 'geuvadis',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("geuvadis", "Geuvadis eQTLs Target Gene")
            var risk = getWidgetData(tabName, 'geuvadis', row, 'gene');
            if (risk != null || risk != undefined) {
                var sdiv = getEl('div')
                sdiv.style.display = 'flex'
                sdiv.style.flexWrap = 'wrap'
                var span = getEl('div');
                span.classList.add('clinvar_traitname');
                span.textContent = risk
                addEl(sdiv, span)
                addDlRow(dl, titleEl, sdiv);
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
        }
    }
}
widgetInfo['linsight'] = {
    'title': 'LINSIGHT'
};
widgetGenerators['linsight'] = {
    'annotators': 'linsight',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("linsight")
            var value = getWidgetData(tabName, 'linsight', row, 'value');
            if (value != null || value != undefined) {
                addDlRow(dl, titleEl, prettyVal(value) )
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
        }
    }
}

widgetInfo['mavedb2'] = {
    'title': 'MaveDB'
};
widgetGenerators['mavedb2'] = {
    'annotators': 'mavedb',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("mavedb", "MaveDB Score and Set")
            var score = getWidgetData(tabName, 'mavedb', row, 'score')
            if (score != null || score != undefined) {
                score = prettyVal(score)
            }
            var acc = getWidgetData(tabName, 'mavedb', row, 'accession')
            var dl = getEl('dl')
            addEl(div, dl)
            if (acc != null || acc != undefined) {
                var link = 'https://www.mavedb.org/scoreset/' + acc;
                var a = makeA(acc, link);
                a.classList.add('linkclass');
                var sdiv = getEl('div')
                sdiv.style.display = 'flex'
                sdiv.style.flexWrap = 'wrap'
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                span.textContent = score
                addEl(sdiv, span)
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                addEl(span, a)
                addEl(sdiv, span)
                addDlRow(dl, titleEl, sdiv);
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
        }
    }
}

widgetInfo['loftool2'] = {
    'title': 'LoFtool'
};
widgetGenerators['loftool2'] = {
    'annotators': 'loftool',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("loftool2", "LoFtool")
            var score = getWidgetData(tabName, 'loftool', row, 'loftool_score');
            if (score != null || score != undefined){
                var sdiv = barWidget('LoFtool', 'Score', prettyVal(score),null, 0.0, 1.0, "Greater Gene"  + "<br />" + "Tolerance", null, null)
                
            } else {
                var sdiv = `No annotation is available for ${annotData["base"]["hugo"]} ${annotData["base"]["achange"]}`
            }
            sdiv.style.display = "flex"
            sdiv.style.flexWrap = "wrap"
            sdiv.style.flexDirection = "column"
            sdiv.style.width = "fit-content"
            addDlRow(dl, titleEl, sdiv);
        }
    }
}
widgetInfo['javierre_promoters'] = {
    'title': 'Promoter IR Regions'
};
widgetGenerators['javierre_promoters'] = {
    'annotators': 'javierre_promoters',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("javierre_promoters", "Promoter IR Regions")
            var regions = getWidgetData(tabName, 'javierre_promoters', row, 'regions')
            if (regions != null || regions != undefined) {
                addDlRow(dl, titleEl, regions)
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }

        }
    }
}
widgetInfo['vista_enhancer'] = {
    'title': 'VISTA Enhancer Browser'
};
widgetGenerators['vista_enhancer'] = {
    'annotators': 'vista_enhancer',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("vista_enhancer", "VISTA Enhancer Browser Element")
            var element = getWidgetData(tabName, 'vista_enhancer', row, 'element');
            if (element != null || element != undefined) {
                element = element.replace('element ', '')
                var link = 'https://enhancer.lbl.gov/cgi-bin/imagedb3.pl?form=presentation&show=1&experiment_id=' + element + '&organism_id=1';
                var a = makeA('element ' + element, link);
                a.classList.add('linkclass');
                var features = getWidgetData(tabName, 'vista_enhancer', row, 'features');
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                span.textContent = features
                addEl(sdiv, span)
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                addEl(span, a)
                addEl(sdiv, span)
                addDlRow(dl, titleEl, sdiv)
            }
        }
    }
}
widgetInfo['ensembl_regulatory_build2'] = {
    'title': 'VEnsembl Regulatory Build'
};
widgetGenerators['ensembl_regulatory_build2'] = {
    'annotators': 'ensembl_regulatory_build',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("ensembl_regulatory_build")
            var dl = getEl('dl')
            addEl(div, dl)
            var id = getWidgetData(tabName, 'ensembl_regulatory_build', row, 'ensr');
            var region = getWidgetData(tabName, 'ensembl_regulatory_build', row, 'region');
            var sdiv = getEl('div')
            var link = '';
            if (id != null) {
                link = 'http://www.ensembl.org/Homo_sapiens/Regulation/Context?db=core;fdb=funcgen;rf=' + id;
                var a = makeA(id, link);
                a.classList.add('linkclass');
            }
            if (region != null || region != undefined) {
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                span.textContent = region
                addEl(sdiv, span)
                var span = getEl('div')
                span.classList.add('clinvar_traitname')
                addEl(span, a)
                addEl(sdiv, span)
                sdiv.style.maxWidth = '20rem'
                addDlRow(dl, titleEl, sdiv)
            }
        }
    }
}
widgetInfo['trinity'] = {
    'title': 'Trinity CTAT RNA Editing Database'
};
widgetGenerators['trinity'] = {
    'annotators': 'trinity',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("trinity")
            var rnaedit = getWidgetData(tabName, 'trinity', row, 'Rnaedit');
            if (rnaedit != null || rnaedit != undefined) {
                addDlRow(dl, titleEl, rnaedit);
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }

        }
    }
}
widgetInfo['segway'] = {
    'title': 'Segway'
};
widgetGenerators['segway'] = {
    'annotators': 'segway',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle('segway')
            var dl = getEl('dl')
            addEl(div, dl)
            var sdiv = getEl('div');
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var tr = document.createElement('tr');
            var sum = getWidgetData(tabName, 'segway', row, 'sum_score');
            var mean = getWidgetData(tabName, 'segway', row, 'mean_score');
            if (sum != null || mean != null) {
                var sums = contentWidget('Sum Score', sum)
                var means = contentWidget('Mean Score', mean)
                sums.style.paddingRight = '40px';
                sums.style.paddingBottom = '20px';
                sdiv.style.border = 'solid gray 1px';
                sdiv.style.maxWidth = '20rem'
                addEl(sdiv, sums)
                addEl(sdiv, means)
                addDlRow(dl, titleEl, sdiv)
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel());
            }
        }
    }
}
widgetInfo['mirbase2'] = {
    'title': 'miRBase'
};
widgetGenerators['mirbase2'] = {
    'annotators': 'mirbase',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("mirbase")
            var id = getWidgetData(tabName, 'mirbase', row, 'id');
            var name = getWidgetData(tabName, 'mirbase', row, 'name');
            var trans = getWidgetData(tabName, 'mirbase', row, 'transcript');
            var derive = getWidgetData(tabName, 'mirbase', row, 'derives_from');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '60rem'
            sdiv.style.minWidth = '40rem'
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            if (id != null) {
                var table = getWidgetTableFrame();
                table.setAttribute("id", "newtable");
                var thead = getWidgetTableHead(['ID', 'Name', 'Transcript', 'Derives From']);
                addEl(table, thead);
                var tbody = getEl('tbody');

                link = 'http://www.mirbase.org/cgi-bin/mirna_entry.pl?acc=' + id;
                var tr = getWidgetTableTr([link, name, trans, derive], [id]);
                addEl(tbody, tr);
                addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
                addDlRow(dl, titleEl, wdiv)

            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel())
            }
        }
    }
}

widgetInfo['omim2'] = {
    'title': 'OMIM'
};
widgetGenerators['omim2'] = {
    'annotators': 'omim2',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            addEl(div, dl)
            var titleEl = makeModuleDescUrlTitle("omim2")
            let ids = getWidgetData(tabName, 'omim', row, 'omim_id');
            if (ids != null || ids != undefined) {
                ids = ids !== null ? ids.split('; ') : [];
                var sdiv = getEl('div')
                sdiv.style.display = 'flex'
                sdiv.style.flexWrap = 'wrap'
                for (let i = 0; i < ids.length; i++) {
                    let link = 'https://omim.org/entry/' + ids[i];
                    var a = makeA(ids[i], link);
                    var span = getEl('div');
                    span.classList.add('clinvar_traitname');
                    a.classList.add('linkclass')
                    addEl(span, a)
                    addEl(sdiv, span)
                }
                addDlRow(dl, titleEl, sdiv);
            } else {
                addDlRow(dl, titleEl, getNoAnnotMsgVariantLevel());
            }
        }
    }
}

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

widgetInfo['cscape_coding'] = {
    'title': 'CScape Coding'
};
widgetGenerators['cscape_coding'] = {
    'annotators': 'cscape_coding',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cscape_coding")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var score = getWidgetData(tabName, 'cscape_coding', row, 'score');
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

widgetInfo['cedar'] = {
    'title': 'CEDAR'
};
widgetGenerators['cedar'] = {
    'annotators': 'cedar',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function (div, row, tabName) {
            var titleEl = makeModuleDescUrlTitle("cedar")
            var dl = getEl('dl')
            addEl(div, dl)
            var wdiv = getEl('div')
            wdiv.style.display = 'flex'
            wdiv.style.flexWrap = 'wrap'
            var epi_id = getWidgetData(tabName, 'cedar', row, 'epi_id');
            var link_id = `https://cedar.iedb.org/epitope/${epi_id}`
            var pubmed_id = getWidgetData(tabName, 'cedar', row, 'pubmed_id');
            var link_pubmed = `https://pubmed.ncbi.nlm.nih.gov/${pubmed_id}`
            var epi_ref = getWidgetData(tabName, 'cedar', row, 'epi_ref');
            var epi_alt = getWidgetData(tabName, 'cedar', row, 'epi_alt');
            var sdiv = getEl('div')
            sdiv.style.maxWidth = '70rem'
            sdiv.style.minWidth = '30rem'
            sdiv.style.maxHeight = '250px'
            sdiv.style.overflow = 'auto'
            sdiv.style.marginRight = '5rem'
            var table = getWidgetTableFrame();
            table.setAttribute("id", "newtable");
            addEl(div, table);
            var thead = getWidgetTableHead(['CEDAR ID','PubMed ID','Reference Epitope','Mutated Epitope']);
            addEl(table, thead);
            var tbody = getEl('tbody');
            addEl(table, tbody);
            var tr = getWidgetTableTr([link_id, link_pubmed, epi_ref, epi_alt],[epi_id, pubmed_id]);
            addEl(tbody, tr);
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            addDlRow(dl, titleEl, wdiv)
        }
    }
}

widgetInfo['dann_coding'] = {
    'title': 'DANN'
};
widgetGenerators['dann_coding'] = {
    'annotators': 'dann_coding',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
    }
}
widgetInfo['mutpred1'] = {
    'title': 'Mutation Assessor'
};
widgetGenerators['mutation_assessor'] = {
    'annotators': 'mutation_assessor',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {}
    }
}

widgetInfo['mutationtaster2'] = {
    'title': 'Mutation Taster'
};
widgetGenerators['mutationtaster2'] = {
    'annotators': 'mutationtaster',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
    }
}

widgetInfo['revel2'] = {
    'title': 'REVEL'
};
widgetGenerators['revel2'] = {
    'annotators': 'revel',
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
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
        'function': function(div, row, tabName) {}
    }
}

widgetInfo['genepanel'] = {
    'title': ''
};
widgetGenerators['genepanel'] = {
    'variant': {
        'width': 'unset',
        'height': 'unset',
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var generator = widgetGenerators['ncbi']['gene'];
            var divs = showWidget('ncbi', ['base', 'ncbigene'], 'gene', div, null, null);
            var dl = getEl('dl')
            addEl(div, dl)
            var divs = showWidget('ess_gene2', ['ess_gene'], 'gene', div, null, null, false);
            addEl(div, getEl('br'))
            var divs = showWidget('gnomad_gene2', ['gnomad_gene'], 'gene', div, null, null, false);
            addEl(div, getEl('br'));
            var divs = showWidget('go2', ['go'], 'gene', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'))
            var divs = showWidget('loftool2', ['loftool'], 'variant', div, null, null, false);
            addEl(div, getEl('br'))
            var divs = showWidget('prec2', ['prec'], 'variant', div, null, null, false);

            addEl(div, getEl('br'));
            var divs = showWidget('interpro2', ['interpro'], 'variant', div, null, null, false);
        }
    }
}

widgetInfo['assocpanel'] = {
    'title': ''
};
widgetGenerators['assocpanel'] = {
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            addEl(div, getEl('br'));
            var divs = showWidget('geuvadis', ['geuvadis'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'));
            var divs = showWidget('gwas_catalog2', ['gwas_catalog'], 'variant', div, null, null, false);
            var divs = showWidget('grasp2', ['grasp'], 'variant', div, null, null, false);
            var divs = showWidget('gtex2', ['gtex'], 'variant', div, null, null, false);
        }
    }
}
widgetInfo['evolutionpanel'] = {
    'title': ''
};
widgetGenerators['evolutionpanel'] = {
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            addEl(div, getEl('br'))
            var divs = showWidget('gerp2', ['gerp'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            var divs = showWidget('rvis2', ['rvis'], 'variant', div, null, null, false);
            var titleEl = makeModuleDescUrlTitle("ghis")
            if (annotData['ghis'] != null) { 
                var sdiv = barWidget('GHIS', 'Score', prettyVal(annotData['ghis']['ghis']), null, 0.358, 0.987, "More" + "<br />" + "haploinsufficient", null, null)
                sdiv.style.display = "flex"
                sdiv.style.flexWrap = "wrap"
                sdiv.style.flexDirection = "column"
                sdiv.style.width = "fit-content"
            } else {
                var sdiv = `No annotation is available for ${annotData["base"]["hugo"]} ${annotData["base"]["achange"]}`
            }
            
            addDlRow(dl, titleEl, sdiv)
            var divs = showWidget('aloft2', ['aloft'], 'variant', div, null, null, false);
            addEl(div, getEl('br'))
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'))
            var divs = showWidget('linsight', ['linsight'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'))
            var divs = showWidget('phastcons3', ['phastcons'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'))
            var divs = showWidget('phylop2', ['phylop'], 'variant', div, null, null, false);
            addEl(div, getEl('br'));
            var divs = showWidget('siphy2', ['siphy'], 'variant', div, null, null, false);
        }
    }
}

widgetInfo['studiespanel'] = {
    'title': ''
};
widgetGenerators['studiespanel'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function(div, row, tabName) {
            addEl(div, getEl('br'))
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var divs = showWidget('mavedb2', ['mavedb'], 'variant', div, null, null, false);
            addEl(div, getEl('br'))
        }
    }
}
widgetInfo['interactionspanel'] = {
    'title': ''
};
widgetGenerators['interactionspanel'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            addEl(div, getEl('br'))
            var divs = showWidget('biogrid2', ['biogrid'], 'gene', div, null, null, false);
            addEl(div, getEl('br'))
            var divs = showWidget('intact2', ['intact'], 'gene', div, null, null, false);
            var sdiv = getEl('div')
            var wdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var button = document.createElement('button');
            button.onclick = function() {
                ndex()
            };
            button.innerHTML = 'NDEx NCI Cancer Pathways';
            button.id = "ndex";
            button.classList.add("ndexbutton");
            sdiv.appendChild(button);
            addEl(wdiv, sdiv)
            addEl(wdiv, getEl('br'))
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var button2 = document.createElement('button');
            button2.onclick = function() {
                ndex_chd()
            };
            button2.innerHTML = 'NDEx Congenital Heart Disease';
            button2.id = "chd";
            button2.classList.add("ndexbutton");
            sdiv.appendChild(button2);
            addEl(wdiv, sdiv)
            addEl(wdiv, getEl('br'))
            var sdiv = getEl('div')
            sdiv.style.display = 'flex'
            sdiv.style.flexWrap = 'wrap'
            var button3 = document.createElement('button');
            button3.onclick = function() {
                ndex_signor()
            };
            button3.innerHTML = 'NDEx SIGNOR';
            button3.id = "sig";
            button3.classList.add("ndexbutton");
            sdiv.appendChild(button3);
            addEl(wdiv, sdiv)
            var divs = showWidget('ndex', ['ndex'], 'gene', div, null, null, false);
            divs[0].style.width = undefined;
            divs[0].style.position = 'relative';
            divs[0].style.maxWidth = '800px';
            divs[0].style.minWidth = '600px';
            addDlRow(dl, wdiv, divs[0])

            function ndex() {
                dl.innerHTML = ''
                var divs = showWidget('ndex', ['ndex'], 'gene', div, null, null, false);
                divs[0].style.position = 'relative';
                divs[0].style.maxWidth = '800px';
                divs[0].style.minWidth = '600px';
                addEl(wdiv, sdiv)
                addDlRow(dl, wdiv, divs[0])
            }

            function ndex_chd() {
                dl.innerHTML = ''
                var divs = showWidget('ndex_chd', ['ndex_chd'], 'gene', div, null, null, false);
                divs[0].style.position = 'relative';
                divs[0].style.maxWidth = '800px';
                divs[0].style.minWidth = '600px';
                addEl(wdiv, sdiv)
                addDlRow(dl, wdiv, divs[0])
            }

            function ndex_signor() {
                dl.innerHTML = ''
                var divs = showWidget('ndex_signor', ['ndex_signor'], 'gene', div, null, null, false);
                divs[0].style.position = 'relative';
                divs[0].style.maxWidth = '800px';
                divs[0].style.minWidth = '600px';
                addEl(wdiv, sdiv)
                addDlRow(dl, wdiv, divs[0])
            }
        }
    }
}
widgetInfo['literaturepanel'] = {
    'title': ''
};
widgetGenerators['literaturepanel'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            addEl(div, getEl('br'))
            var divs = showWidget('litvar', ['litvar', 'dbsnp'], 'variant', div, null, null, false);
        }
    }
}
widgetInfo['noncodingpanel'] = {
    'title': ''
};
widgetGenerators['noncodingpanel'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            var br = getEl("br");
            addEl(div, br);
            var divs = showWidget('ccre_screen2', ['ccre_screen'], 'variant', div, null, null, false);
            var br = getEl("br");
            addEl(div, br);
            var divs = showWidget('encode_tfbs2', ['encode_tfbs'], 'variant', div, null, null, false);
            var divs = showWidget('genehancer2', ['genehancer'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            var br = getEl("br");
            addEl(div, br);
            var divs = showWidget('javierre_promoters', ['javierre_promoters'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'));
            var divs = showWidget('vista_enhancer', ['vista_enhancer'], 'variant', div, null, null, false);
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
            let benign = [];
            let pathogenic = [];
            const names = ['alphamissense', 'bayesdel', 'cadd', 'cadd_exome', 'esm1b', 'fathmm', 'gerp', 'phylop', 'primateai', 'revel', 'sift', 'varity_r', 'vest'];
            const scoreIds = ['am_pathogenicity', 'bayesdel_noAF_score', 'score', 'score', 'score', 'fathmm_score', 'gerp_rs', 'phylop100_vert', 'primateai_score', 'score', 'score', 'varity_r', 'score'];
            const multiValuePredictors = ['fathmm'];

            for (let i=0; i<names.length; i++) {
                const name = names[i];
                const scoreId = scoreIds[i];

                if (multiValuePredictors.indexOf(name) > -1) {
                    // Fathmm
                    const rawScoreString = getWidgetData(tabName, name, row, scoreId);
                    if (rawScoreString !== undefined || rawScoreString != null) {
                        let scoreArray = rawScoreString.split(";").map(Number);
                        let maxIndex;
                        if (rawScoreString.endsWith(';.')) {
                            maxIndex = 0
                        } else {
                            maxIndex = scoreArray.indexOf(Math.max(...scoreArray));
                        }
                        const b = getWidgetData(tabName, name, row, 'bp4_benign');
                        const p = getWidgetData(tabName, name, row, 'pp3_pathogenic');
                        const pathogenicArray = p.split(";");
                        const pathogenicText = pathogenicArray[maxIndex];
                        const benignArray = b.split(";");
                        const benignText = benignArray[maxIndex];
                        scores.push(predWidget(scoreArray[maxIndex]));
                        benign.push(predWidget(benignText));
                        pathogenic.push(predWidget(pathogenicText));
                    } else {
                        scores.push(predWidget(null));
                        benign.push(predWidget(null));
                        pathogenic.push(predWidget(null));
                    }
                } else {
                    const score = getWidgetData(tabName, name, row, scoreId);
                    const b = getWidgetData(tabName, name, row, 'bp4_benign');
                    const p = getWidgetData(tabName, name, row, 'pp3_pathogenic');
                    scores.push(predWidget(score));
                    benign.push(predWidget(b));
                    pathogenic.push(predWidget(p));
                }
            }

            var table = getWidgetTableFrame();
            table.setAttribute("id", "pred");
            var tbody = getEl('tbody');
            tooltipContent = [
                {id: "source", label: "Source", info: null},
                {id: "score", label: "Score", info: "Raw scores reported by the method."},
                {id: "benign", label: "ACMG/AMP Benign (BP4)", info: "Strength of evidence for benignity. Based on scores that do not include the background population frequency of the variant."},
                {id: "pathogenic", label: "ACMG/AMP Pathoginic (PP3)", info: "Strength of evidence for pathogenicity. Based on scores that do not include the background population frequency of the variant."},
            ]
            var thead = getWidgetTableHeadTooltips(tooltipContent);
            addEl(table, thead);
            var sdiv = getEl('div');
            var sdiv = getEl('div')
            sdiv.style.maxHeight = '100%'
            sdiv.style.overflow = 'auto'
            sdiv.style.paddingLeft = '1em';
            sdiv.style.paddingRight = '1em';
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

                const score = scores[i];
                var td = document.createElement('td');
                addEl(td, score)
                addEl(tr, td);

                if (score.textContent !== "") {
                    score.classList.add('pred_score');
                } else {
                    score.textContent = getNoAnnotMsgVariantLevel()
                    score.classList.add("pred_noanno")
                }

                const benignWidget = benign[i];
                const benignText = benignWidget.textContent;
                var td = document.createElement('td');
                if (benignText) {
                    benignWidget.classList.add('pred_benign');
                }
                addEl(tr, td);
                addEl(td, benignWidget);

                const pathogenicWidget = pathogenic[i];
                const pathogenicText = pathogenicWidget.textContent;
                var td = document.createElement('td');
                if (pathogenicText) {
                    pathogenicWidget.classList.add('pred_damaging');
                }
                addEl(td, pathogenicWidget);
                addEl(tr, td);
                addEl(tbody, tr);
            }
            addEl(wdiv, addEl(sdiv, addEl(table, tbody)));
            var sdiv = 'Variant Effect Predictions';
            addEl(dl, wdiv);
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
        'function': function(div, row, tabName) {
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
widgetInfo['vizualizationpanel'] = {
    'title': ''
};
widgetGenerators['vizualizationpanel'] = {
    'variant': {
        'width': undefined,
        'height': undefined,
        'function': function(div, row, tabName) {
            var generator = widgetGenerators['lollipop2']['variant'];
            generator['width'] = 'calc(100% - 1vw)';
            generator['height'] = 260;
            generator['variables']['hugo'] = '';
            annotData['base']['numsample'] = 1;
            var divs = showWidget('lollipop2', ['base'], 'variant', div);
            divs[0].style.position = 'relative';
            divs[0].style.top = '0px';
            divs[0].style.left = '0px';
            var generator = widgetGenerators['mupit2']['variant'];
            var height = null;
            showWidget('mupit2', ['base', 'mupit'], 'variant', div);
        }
    }
}

widgetInfo['structurepanel'] = {
    'title': ''
};
widgetGenerators['structurepanel'] = {
    'variant': {
        'width': undefined,
        'height': 'unset',
        'function': function(div, row, tabName) {
            var dl = getEl('dl')
            dl.style.width = 'calc(100% - 1rem)'
            addEl(div, dl)
            div.style.marginTop = '2vh';
            div.style.overflow = 'unset';
            var generator = widgetGenerators['mupit2']['variant'];
            var height = null;
            showWidget('mupit2', ['base', 'mupit'], 'variant', div);
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
        'function': function(div, row, tabName) {
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
            var dl = getEl('dl')
            addEl(div, dl)
            addEl(div, getEl('br'));
            var divs = showWidget('denovo', ['denovo'], 'variant', div, null, null, false);
            var dl = getEl('dl')
            addEl(div, dl)
            var divs = showWidget('omim2', ['omim'], 'variant', div, null, null, false)
            addEl(div, getEl('br'));
            var generator = widgetGenerators['clingen2']['gene'];
            var divs = showWidget('clingen2', ['clingen'], 'gene', div, null, null, false);
            var button = document.createElement('button');
            button.onclick = function() {
                cardio()
            };
            button.innerHTML = 'Cardiovascular';
            button.style.marginRight = '50px'
            var img = document.createElement("img");
            img.classList.add('triangle-right')
            addEl(button, img)
            button.classList.add('clinbutton')
            div.appendChild(button);

            var button2 = document.createElement('button');

            button2.onclick = function() {
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
            var divs = showWidget('arrvars', ['arrvars'], 'variant', sdiv, null, null, false);
            var divs = showWidget('cvdkp', ['cvdkp'], 'variant', sdiv, null, null, false);
            var divs = showWidget('cardioboost', ['cardioboost'], 'variant', sdiv, null, null, false);
            var cardio = function() {
                img.classList.remove('triangle-down')
                var mydiv = document.getElementById('contents');
                if (mydiv.style.display === 'none' || mydiv.style.display === '') {
                    mydiv.style.display = 'block'
                    img.classList.add('triangle-down')
                } else
                    mydiv.style.display = 'none'
            }
            var ssdiv = getEl('div')
            ssdiv.id = 'contentss'
            ssdiv.style.display = 'none'
            addEl(div, ssdiv)
            var divs = showWidget('pharmgkb2', ['pharmgkb'], 'variant', ssdiv, null, null, false);
            var divs = showWidget('dgi2', ['dgi'], 'gene', ssdiv, null, null, false);
            var pharm = function() {
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

const getHugoAchange = function() {
    return annotData['base']['hugo'] + ' ' + changeAchange3to1(annotData['base']['achange'])
}
const getNoAnnotMsgVariantLevel = function() {
    return 'No annotation available for ' + getHugoAchange()
}
const prettyVal = function(val) {
    if (val == '') {
        return val
    } else if (val < 0.01 && val > -0.01) {
        return val.toExponential(2)
    } else {
        return val.toPrecision(3)
    }
}

const addDlRow = function(dl, title, content) {
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

const makeA = function(text, url) {
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
        'function': function(div, row, tabName) {
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
                            onComplete: function() {
                                var ctx = this.chart.ctx
                                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily)
                                ctx.fillStyle = this.chart.config.options.defaultFontColor
                                ctx.textAlign = 'center'
                                ctx.textBaseline = 'bottom'
                                this.data.datasets.forEach(function(dataset) {
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
                            onComplete: function() {
                                var ctx = this.chart.ctx
                                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, 'normal', Chart.defaults.global.defaultFontFamily)
                                ctx.fillStyle = this.chart.config.options.defaultFontColor
                                ctx.textAlign = 'center'
                                ctx.textBaseline = 'bottom'
                                this.data.datasets.forEach(function(dataset) {
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

widgetInfo['cancerassocpanel'] = {
    'title': ''
};
widgetGenerators['cancerassocpanel'] = {
    'variant': {
        'width': null,
        'height': null,
        'function': function (div, row, tabName) {
            div.style.marginTop = '2vh';
            var divs = showWidget('cgc2', ['cgc'], 'gene', div, null, null, false);
            var divs = showWidget('cosmic2', ['cosmic'], 'variant', div, null, null, false);
            var divs = showWidget('cgi2', ['cancer_genome_interpreter'], 'variant', div, null, null, false);
            var divs = showWidget('target2', ['target'], 'variant', div, null, null, false);
            var divs = showWidget('civic2', ['civic'], 'variant', div, null, null, false);
            var divs = showWidget('chasmplus2', ['chasmplus'], 'variant', div, null, null, false);
            var divs = showWidget('cscape_coding', ['cscape_coding'], 'variant', div, null, null, false);
            var divs = showWidget('cedar', ['cedar'], 'variant', div, null, null, false);
        }
    }
}

widgetInfo['mupit2'] = {
    'title': ''
};
widgetGenerators['mupit2'] = {
    'variant': {
        'width': '100%',
        'height': undefined,
        'function': function(div, row, tabName) {
            var chrom = getWidgetData(tabName, 'base', row, 'chrom');
            var pos = getWidgetData(tabName, 'base', row, 'pos');
            var url = location.protocol + '//www.cravat.us/MuPIT_Interactive/rest/showstructure/check?pos=' + chrom + ':' + pos;
            var iframe = getEl('iframe');
            iframe.id = 'mupitiframe';
            iframe.setAttribute('crossorigin', 'anonymous');
            iframe.setAttribute('chrom', chrom);
            iframe.setAttribute('pos', pos);
            iframe.style.width = '100%';
            iframe.style.height = '500px';
            iframe.style.border = '0px';
            addEl(div, iframe);
            $.get(url).done(function(response) {
                if (response.hit == true) {
                    if (window.innerWidth > 1024) {
                        url = location.protocol + '//www.cravat.us/MuPIT_Interactive?gm=' + chrom + ':' + pos + '&embed=true';
                    } else {
                        url = location.protocol + '//www.cravat.us/MuPIT_Interactive?gm=' + chrom + ':' + pos + '&embed=true&showrightpanel=false';
                    }
                    iframe.src = url;
                } else {
                    iframe.parentElement.removeChild(iframe);
                    var sdiv = getEl('div');
                    sdiv.textContent = 'No annotation available for MuPIT';
                    addEl(div, sdiv);
                    div.parentElement.style.height = '50px';
                }
            });
        }
    }
}

widgetInfo['cancer_hotspots2'] = {
    'title': 'Hotspot mutation per cancer type (Cancer Hotspots)'
};
widgetGenerators['cancer_hotspots2'] = {
    variant: {
        width: 180,
        height: 180,
        cancerTypes: [
            'adrenagland', 'ampullaofvater', 'billarytract', 'bladder',
            'blood', 'bone', 'bowel', 'breast', 'cervix', 'csnbrain',
            'esophagussstomach', 'eye', 'headandneck', 'kidney', 'liver',
            'lung', 'lymph', 'ovaryandfallopiantube', 'pancreas', 'penis',
            'peritoneum', 'prostate', 'skin', 'softtissue', 'testis', 'unk',
            'uterus'
        ],
        function: function(div, row, tabName) {
            let samples = getWidgetData(tabName, 'cancer_hotspots', row, 'samples');
            if (samples == null) {
                var span = getEl('span');
                span.classList.add('nodata');
                addEl(div, addEl(span, getTn('No data')));
                return;
            }
            if (samples != undefined && samples != null && samples.indexOf('[[') == 0) {
                if (!samples) {
                    return;
                }
                samples = JSON.parse(samples);
                samples.sort(function(a, b) {
                    return a[1] - b[1];
                });
                const table = getWidgetTableFrame();
                addEl(div, table);
                const thead = getWidgetTableHead(['Cancer Type', 'Count']);
                addEl(table, thead);
                const tbody = getEl('tbody');
                addEl(table, tbody);
                for (var i = 0; i < samples.length; i++) {
                    let tr = getWidgetTableTr(samples[i]);
                    addEl(tbody, tr);
                }
            } else {
                let samples = getWidgetData(tabName, 'cancer_hotspots', row, 'samples');
                if (!samples) {
                    return;
                }
                samples.sort(function(a, b) {
                    return b[1] - a[1];
                });
                const table = getWidgetTableFrame();
                addEl(div, table);
                const thead = getWidgetTableHead(['Cancer Type', 'Count']);
                addEl(table, thead);
                const tbody = getEl('tbody');
                addEl(table, tbody);
                for (var i = 0; i < samples.length; i++) {
                    let tr = getWidgetTableTr(samples[i]);
                    if (samples[i][1] > 25) {
                        tr.style.backgroundColor = 'rgba(254, 202, 202, 255)';
                    }
                    addEl(tbody, tr);
                }
            }
        }
    }
}

function writeToVariantArea(inputData) {
    if (inputData) {
        let value = '';
        if ('chrom' in inputData) {
            value = `${inputData['assembly']} ${inputData['chrom']} ${inputData['pos']} ${inputData['ref']} ${inputData['alt']}`;
        } else if ('dbsnp' in inputData) {
            value = inputData['dbsnp'];
        } else if ('clingen' in inputData) {
            value = inputData['clingen'];
        } else if ('hgvs' in inputData) {
            value = inputData['hgvs'];
        } else if ('input' in inputData) {
            value = inputData['input'];
        }
        document.getElementById('current-input').textContent = value;
        document.getElementById('variant-header').style.visibility = 'visible';
    } else {
        document.getElementById('current-input').textContent = '';
        document.getElementById('variant-header').style.visibility = 'hidden';
    }
}

function hideSpinner() {
    document.querySelector('#spinnerdiv').style.display = 'none';
}

function showSpinner() {
    document.querySelector('#spinnerdiv').style.display = 'flex';
}

function processUrl() {
    var inputData = getInputDataFromUrl();
    if (inputData != null) {
        writeToVariantArea(inputData);
        submitAnnotate(inputData['chrom'], inputData['pos'],
            inputData['ref'], inputData['alt'], inputData['assembly'], inputData['hgvs'], inputData['clingen'], inputData['dbsnp']);
    }
}

function fillExampleCoordinates() {
    document.querySelector('#input_variant_chrom').value = 'chr6';
    document.querySelector('#input_variant_pos').value = '31946402';
    document.querySelector('#input_variant_ref').value = 'C';
    document.querySelector('#input_variant_alt').value = 'T';
    document.querySelector('#input_variant_hgvs').value = '';
}

function fillExampleHgvs() {
    document.querySelector('#input_variant_chrom').value = '';
    document.querySelector('#input_variant_pos').value = '';
    document.querySelector('#input_variant_ref').value = '';
    document.querySelector('#input_variant_alt').value = '';
    document.querySelector('#input_variant_hgvs').value = 'NM_000051.4:c.2413C>T';
}

function variantSubmitHandler(event) {
    const inputData = event.detail;
    if (inputData != null) {
        showContentDiv();
        submitAnnotate(inputData['chrom'], inputData['pos'], inputData['ref_base'],
            inputData['alt_base'], inputData['assembly'], inputData['hgvs'], inputData['clingen'], inputData['dbsnp'])
    } else {
        alert('No variant input.');
    }
}

function searchBackButtonHandler(event) {
    hideSpinner();
    document.getElementById('annotation_errors').style.display = 'none';
    hideContentDiv();
    writeToVariantArea(null);
}

function ocSVIReadyHandler() {
    alert('oc svi ready');
    document.getElementById('oc-svi-header').innerText = 'Single Variant Page';
}

function setupEvents() {
    document.querySelector("body").addEventListener("click", function(evt) {
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
    });
    document.getElementById('oc-svi').addEventListener('variantSubmit', variantSubmitHandler);
    document.getElementById('oc-svi').addEventListener('ready', ocSVIReadyHandler);
    document.getElementById('back-search').addEventListener('click', searchBackButtonHandler);
}


function showContentDiv() {
    document.getElementById('bottom-div').style.display = 'grid';
    document.querySelector('#detaildiv_variant').style.display = 'block';
    document.querySelector('#detaildiv_documentation').style.display = 'none';
}

function hideContentDiv() {
    hideAlternateAlleles();
    document.getElementById('bottom-div').style.display = 'none';
    document.querySelector('#detaildiv_variant').style.display = 'none';
    document.querySelector('#detaildiv_documentation').style.display = 'block';
}

function showSearch () {
    // document.querySelector('#inputdiv').style.display = 'flex';
}

function run() {
    mqMaxMatch.addListener(mqMaxMatchHandler);
    mqMinMatch.addListener(mqMinMatchHandler);
    var params = new URLSearchParams(window.location.search);
    if ((params.get('chrom') != null && params.get('pos') != null && params.get('ref_base') != null && params.get('alt_base') != null)
        || params.get('hgvs') != null || params.get('clingen') != null || params.get('dbsnp') != null) {
        showContentDiv();
        showSpinner();
        // hideSearch();
        showSearch();
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

window.onload = function() {
    run();
}
