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

            
            var myDiv = document.createElement('div');
            
            var chartDiv = document.getElementById("widgetcontentdiv_cohortsamples_variant");
            chartDiv.style.display = "Flex";
            myDiv.style.display = "Flex";
            myDiv.style.justifyContent = "center";
            chartDiv.style.alignItems = "center"
            function drawMain(scale){
            var data = v['data']['data']['counts']
            console.log(v['data']['data']['counts'])
            var selectedCohorts = getSelectedCohorts()
            console.log(selectedCohorts)
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
                console.log(key, value)
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
            console.log(labels)
            console.log(parents)
            console.log(percents)
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
                    // hovertemplate: 'Price: %{y:$.2f}<extra></extra>',
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
                    branchvalues: 'total',
                }];
            }
              var layout = {
                margin: {l: 0, r: 0, b: 0, t: 0},
                width: 250,
                height: 250,
                // hovermode: false,
              };
              console.log(data)
              Plotly.newPlot(myDiv, data, layout);
              addEl(chartDiv, myDiv)
        }

        var radioDiv = getEl()
        var label = document.createElement('label')
            label.innerHTML = "Percentage"
            var label2 = document.createElement('label')
            label2.innerHTML = "Count"
            var radio = document.createElement('input')
            radio.id = "sample_percent"
            radio.type = "radio"
            radio.value = "sample_percent"
            radio.checked = true
            radio.style.position = "relative"
            radio.style.left = "96px"
            radio.style.top = "150px"
            label.style.position = "relative"
            label.style.left = "170px"
            label.style.top = "150px"
            addEl(label, radio)
            var radio2 = document.createElement('input')
            radio2.type = "radio"
            radio2.value = "sample_counts"
            radio2.id = "sample_counts"
            radio2.style.position = "relative"
            radio2.style.left = "212px"
            radio2.style.top = "150px"
            label2.style.position = "relative"
            label2.style.left = "218px"
            label2.style.top = "150px"
            addEl(label2, radio2)
            

            function clicked (){
                if (this.value == "sample_counts"){
                    document.getElementById("sample_percent").checked = false
                }else if (this.value == "sample_percent"){
                    document.getElementById("sample_counts").checked = false
                }
                  drawMain(this.value)
            }
            document.getElementById("widgetcontentdiv_cohortsamples_variant").appendChild(label);
            document.getElementById("widgetcontentdiv_cohortsamples_variant").appendChild(radio);
            document.getElementById("widgetcontentdiv_cohortsamples_variant").appendChild(radio2);
            document.getElementById("sample_percent").addEventListener("click", clicked);
            document.getElementById("sample_counts").addEventListener("click", clicked);
            document.getElementById("widgetcontentdiv_cohortsamples_variant").appendChild(label2);
        }
    }
};