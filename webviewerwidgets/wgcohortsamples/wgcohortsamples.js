$.getScript('/result/widgetfile/wgcohortsamples/plotly-2.16.1.min.js', function() {});
widgetGenerators['cohortsamples'] = {
    'variant': {
        'width': 500,
        'height': 400,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },

        'function': function (div, row) {
            var self = this;
            var dbpath = infomgr['jobinfo']['Input file name']
			var widgetName = 'cohortsamples';
			var widgetDiv = div.parentElement;
			var toks = widgetDiv.id.split('_');
			var tabName = toks[1];
			var v = widgetGenerators[widgetName][tabName]['variables'];
			v.widgetContentDiv = div;
            v.tabName = tabName;
            var samples = getWidgetData(tabName, 'base', row, 'samples');
            var uid = getWidgetData(tabName, 'base', row, 'uid')
            var numSample = getWidgetData(tabName, 'base', row, 'numsample');
            self.runTimeout = setTimeout(function () {
                $.ajax({
                    url: '/result/runwidget/' + widgetName, 
                    data: {dbpath: dbpath, samples: samples, uid: uid},
                    success: function (data) {
                        v['data'] = data;
                        drawMain("sample_percent");
                    }
                });
            })

            
            var wrapperDiv = document.createElement('div');
            
            var chartDiv = document.getElementById("widgetcontentdiv_cohortsamples_variant");
            chartDiv.style.display = "Flex";
            wrapperDiv.style.display = "Flex";
            wrapperDiv.style.justifyContent = "center";
            chartDiv.style.alignItems = "center"
            function drawMain(scale){
            var data = v['data']['data']['counts']
            var selectedCohorts = getSelectedCohorts()
            var num_total_samples = v['data']['data']['sample_count']
            var labels = ["Sample Count"]
            var parents = []
            var counts = [numSample]
            var percents = []
            var total_percents = []
            var ids = ["Sample Count"]
            for (var set in data) {
                var row = data[set][0];
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
            for (const [key, value] of Object.entries(row)) {
                var zyg = value[0]
                var sum = Object.values(zyg).reduce((a, b) => a + b, 0);
                counts.push(sum)
                percents.push(sum / num_total_samples[key] * 100)
                labels.push(key)
                ids.push(key)
                total_percents.push((sum / num_total_samples[key] * 100))
                for (const [newkey, value] of Object.entries(zyg)) {
                    ids.push(key + "_" + newkey)
                    labels.push(newkey)
                    counts.push(value)
                    var perc = (value / num_total_samples[key]) * 100
                    percents.push(perc)
                }
                }
            }
            }
            var sum_percent = eval(total_percents.join("+"));
            percents.unshift(sum_percent)
            var cohort;
            for (var i in labels){
                if (labels[i] == "Sample Count"){
                    parents.push("")
                }
                else if ( labels[i] != 'hom' && labels[i] != 'het' ) {
                    cohort = labels[i]
                    parents.push("Sample Count")
                }else{
                    parents.push(cohort)
                }
            }
            if (scale == "sample_percent"){
                var data = [{
                    type: "sunburst",
                    ids: ids,
                    labels: labels,
                    parents: parents,
                    values: percents,
                    leaf: {"opacity": 0.4},
                    marker: {"line": {"width": 2}},
                    branchvalues: 'total',
                }];
            } else if (scale == "sample_counts"){
                var data = [{
                    type: "sunburst",
                    ids: ids,
                    labels: labels,
                    parents: parents,
                    values: counts,
                    leaf: {"opacity": 0.4},
                    marker: {"line": {"width": 2}},
                    // branchvalues: 'total',
                }];
            }
              var layout = {
                sunburstcolorway:['#B2182B','#D6604D','#5AAE61', '#F4A582', '#FDDBC7', '#1B7837', '#D1E5F0', '#92C5DE', '#4393C3', '#2166AC' ],
                margin: {l: 0, r: 0, b: 0, t: 0},
                width: 250,
                height: 250,
              };
              Plotly.newPlot(wrapperDiv, data, layout);
              addEl(chartDiv, wrapperDiv)
        }

            var container = getEl("div")
            container.className = "cohorts-toggle"
            container.style.top = "92px"
            container.style.left = "331px"

            var radioDiv = getEl("div")
            radioDiv.className = "cohorts-radio"
            var span = getEl("span")
            span.innerHTML = "View data by: "
            var label = document.createElement('label')
            label.innerHTML = "Percentage"
            var label2 = document.createElement('label')
            label2.innerHTML = "Count"
            var percRadio = document.createElement('input')
            percRadio.id = "sample_percent"
            percRadio.type = "radio"
            percRadio.value = "sample_percent"
            percRadio.checked = true
            var countRadio = document.createElement('input')
            countRadio.type = "radio"
            countRadio.value = "sample_counts"
            countRadio.id = "sample_counts"
            addEl(radioDiv, span)
            addEl(radioDiv, percRadio)
            addEl(radioDiv, label)
            addEl(radioDiv, countRadio)
            addEl(radioDiv, label2)
            addEl(container, radioDiv)
            addEl(div, container)
            

            function clicked (){
                if (this.value == "sample_counts"){
                    document.getElementById("sample_percent").checked = false
                }else if (this.value == "sample_percent"){
                    document.getElementById("sample_counts").checked = false
                }
                  drawMain(this.value)
            }
            document.getElementById("sample_percent").addEventListener("click", clicked);
            document.getElementById("sample_counts").addEventListener("click", clicked);
        }
    }
};