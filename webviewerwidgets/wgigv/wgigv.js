$.getScript('/result/widgetfile/wgigv/igv.min.js', function () {});

widgetGenerators['igv'] = {
	'variant': {
        'donterase': true,
		'width': 1280,
		'height': 280,
        'variables': {'drawn': false, 'browser': null},
		'function': function (div, row, tabName) {
            var self = this;
            if (self['variables']['drawn'] == true) {
                var chrom = null;
                var pos = null;
                var genome = infomgr.jobinfo['Input genome']; 
                if (genome == 'hg19') {
                    chrom = infomgr.getRowValue(tabName, row, 'hg19__chrom');
                    pos = infomgr.getRowValue(tabName, row, 'hg19__pos');
                } else {
                    chrom = infomgr.getRowValue(tabName, row, 'base__chrom');
                    pos = infomgr.getRowValue(tabName, row, 'base__pos');
                }
                var locus = chrom + ':' + pos;
                self['variables']['browser'].search(locus);
                return;
            }

            var button = getEl('button');
            button.id = 'igv_loadtrackbtn_' + tabName;
            button.textContent = 'Load Track';
            button.addEventListener('click', function (evt) {
                var btn = evt.target;
                var ltd = document.getElementById('igv_loadtrackdiv_' + tabName);
                var display = ltd.style.display;
                if (display == 'none') {
                    display = 'block';
                    btn.style.borderStyle = 'inset';
                    btn.style.backgroundColor = '#909090';
                } else {
                    display = 'none';
                    btn.style.borderStyle = 'outset';
                    btn.style.backgroundColor = 'white';
                }
                ltd.style.display = display;
            });
            addEl(div, button);
            var loadTrackDiv = getEl('div');
            loadTrackDiv.id = 'igv_loadtrackdiv_' + tabName;
            loadTrackDiv.style.position = 'absolute';
            loadTrackDiv.style.left = '5px';
            loadTrackDiv.style.top = '55px';
            loadTrackDiv.style.zIndex = '1';
            loadTrackDiv.style.backgroundColor = 'white';
            loadTrackDiv.style.padding = '6px';
            loadTrackDiv.style.border = '1px solid #909090';
            loadTrackDiv.style.display = 'none';
            var btn = getEl('div');
            btn.textContent = 'Local file...';
            btn.style.cursor = 'default';
            btn.addEventListener('click', function (evt) {
                document.getElementById('igv_files_' + tabName).click();
            });
            addEl(loadTrackDiv, btn);
            var input = getEl('input');
            input.id = 'igv_files_' + tabName;
            input.type = 'file';
            input.multiple = 'true';
            input.accept = '.bam,.bai';
            input.addEventListener('change', function (evt) {
                var files = document.getElementById('igv_files_' + tabName).files;
                var bamFiles = [];
                var indexFiles = {};
                for (let file of files) {
                    if (file.name.endsWith(".bam")) {
                        bamFiles.push(file);
                    }
                    else if (file.name.endsWith(".bai")) {
                        var key = getKey(file.name);
                        indexFiles[key] = file;
                    }
                    else {
                        alert("Unsupported file type: " + file.name);
                    }
                }
                // Create track objects
                var trackConfigs = [];
                for (let file of bamFiles) {
                    var key = getKey(file.name);
                    var indexFile = indexFiles[key];
                    if (indexFile) {
                        trackConfigs.push({
                            name: file.name,
                            type: "alignment",
                            format: "bam",
                            url: file,
                            indexURL: indexFile
                        });
                    }
                    else {
                        alert("No index file for: " + file.name);
                    }
                }
                if (trackConfigs.length > 0) {
                    self['variables']['browser'].loadTrackList(trackConfigs);
                }
                function getKey (filename) {
                    var idx = filename.indexOf('.');
                    if (idx > 0) {
                        return filename.substring(0, idx);
                    }
                }
                document.getElementById('igv_loadtrackbtn_' + tabName).click();
            });
            input.style.display = 'none';
            addEl(loadTrackDiv, input);
            btn = getEl('div');
            btn.textContent = 'URL...';
            btn.style.cursor = 'default';
            btn.addEventListener('click', function (evt) {
                var ltd = document.getElementById('igv_loadtrackurldiv_' + tabName);
                ltd.style.display = 'block';
            });
            addEl(loadTrackDiv, btn);
            var ltd = getEl('div');
            ltd.id = 'igv_loadtrackurldiv_' + tabName;
            ltd.style.display = 'none';
            ltd.style.position = 'absolute';
            ltd.style.zIndex = '1';
            ltd.style.padding = '6px';
            ltd.style.backgroundColor = 'white';
            ltd.style.border = '1px solid #909090';
            var span = getEl('span');
            span.textContent = 'Data URL:';
            addEl(ltd, span);
            var input = getEl('input');
            input.type = 'text';
            input.size = '40';
            addEl(ltd, input);
            addEl(ltd, getEl('br'));
            span = getEl('span');
            span.textContent = 'Index URL:';
            addEl(ltd, span);
            input = getEl('input');
            input.type = 'text';
            input.size = '40';
            addEl(ltd, input);
            addEl(ltd, getEl('br'));
            var btn = getEl('button');
            btn.textContent = 'Ok';
            btn.addEventListener('click', function (evt) {
                var ltd = evt.target.parentElement;
                var inputs = ltd.getElementsByTagName('input');
                var dataUrl = inputs[0].value;
                var indexUrl = inputs[1].value;
                var trackConfigs = [{
                    name: 'Track',
                    type: "alignment",
                    format: "bam",
                    url: dataUrl,
                }];
                if (indexUrl != '') {
                    trackConfigs[0]['indexURL'] = indexUrl;
                }
                self['variables']['browser'].loadTrackList(trackConfigs);
                document.getElementById('igv_loadtrackbtn_' + tabName).click();
            });
            addEl(ltd, btn);
            var btn = getEl('button');
            btn.textContent = 'Cancel';
            btn.addEventListener('click', function (evt) {
                var ltd = evt.target.parentElement;
                ltd.style.display = 'none';
            });
            addEl(ltd, btn);
            addEl(loadTrackDiv, ltd);
            addEl(div, loadTrackDiv);
            var drawDiv = getEl('div');
            drawDiv.id = 'igv_draw_' + tabName;
            addEl(div, drawDiv);
            var chrom = null;
            var pos = null;
            var genome = infomgr.jobinfo['Input genome']; 
            if (genome == 'hg19') {
                chrom = infomgr.getRowValue(tabName, row, 'hg19__chrom');
                pos = infomgr.getRowValue(tabName, row, 'hg19__pos');
            } else {
                chrom = infomgr.getRowValue(tabName, row, 'base__chrom');
                pos = infomgr.getRowValue(tabName, row, 'base__pos');
            }
            var locus = chrom + ':' + pos;
            var options = {locus: locus, genome: genome};
            console.log('here');
            igv.createBrowser(drawDiv, options).then(function (b) {
                self['variables']['browser'] = b;
                document.getElementById('igv_draw_variant').getElementsByClassName('igv-content-div')[0].style.height = 'auto';
            });
            self['variables']['drawn'] = true;
		}
	}
}
