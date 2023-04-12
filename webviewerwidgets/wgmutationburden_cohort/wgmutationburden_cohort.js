$.getScript('/result/widgetfile/wgmutationburden_cohort/plotly-2.16.1.min.js', function() {});
widgetGenerators['mutationburden_cohort'] = {
    'cohort': {
        'name': 'Mutation Burden',
        'width': 780,
        'height': 480,
        'callserver': true,
        'default_hidden': false,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'function': function(div, data) {
            var myDiv = document.createElement('div');
            var chartDiv = document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort");
            const titles = {"mutation_percent": "Percentage of Non-Silent Mutations", "mutation_counts": "Count of Non-Silent Mutations per Gene"}

            function leaveChange(scale) {
                var newData = []
                var layout = {
                  title: titles[scale],
                  annotations: [],
                  xaxis: {
                    ticks: '',
                    side: 'bottom',
                    autosize: true
                  },
                  yaxis: {
                    ticks: '',
                    ticksuffix: ' ',
                    autosize: true
                  }
                };
                for (var j in allData){
                  if (allData[j].includes(scale)){
                      newData.push(allData[j])
                  }
                }
                if (scale == "mutation_percent"){
                  var data = [

                    {
                      z: newData,
                      x: hugos,
                      y: selectedCohorts,
                      type: 'heatmap',
                      hoverongaps: false,
                      text: text,
                      hoverinfo: 'text',
                    }
                  ];
                }else{
                  var data = [

                    {
                      z: newData,
                      x: hugos,
                      y: selectedCohorts,
                      type: 'heatmap',
                      hoverongaps: false,
                    }
                  ];
                }
                var config = {responsive: true}
                Plotly.newPlot(div, data, layout, config);
                // addEl(chartDiv, myDiv)
            }

            var label = document.createElement('label')
            label.innerHTML = "Percentage"
            var label2 = document.createElement('label')
            label2.innerHTML = "Count"
            var radio = document.createElement('input')
            radio.id = "mutation_percent"
            radio.type = "radio"
            radio.value = "mutation_percent"
            radio.checked = true
            radio.style.position = "relative"
            radio.style.left = "460px"
            radio.style.top = "3px"
            label.style.position = "relative"
            label.style.left = "530px"
            label.style.top = "0px"
            addEl(label, radio)
            var radio2 = document.createElement('input')
            radio2.type = "radio"
            radio2.value = "mutation_counts"
            radio2.id = "mutation_counts"
            radio2.style.position = "relative"
            radio2.style.left = "550px"
            radio2.style.top = "3px"
            label2.style.position = "relative"
            label2.style.left = "555px"
            label2.style.top = "0px"
            addEl(label2, radio2)
            

            function clicked (){
                if (this.value == "mutation_counts"){
                    document.getElementById("mutation_percent").checked = false
                }else if (this.value == "mutation_percent"){
                    document.getElementById("mutation_counts").checked = false
                }
                  leaveChange(this.value)
            }
            document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort").appendChild(label);
            document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort").appendChild(radio);
            document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort").appendChild(radio2);
            document.getElementById("mutation_percent").addEventListener("click", clicked);
            document.getElementById("mutation_counts").addEventListener("click", clicked);
            document.getElementById("widgetcontentdiv_mutationburden_cohort_cohort").appendChild(label2);


            var data = this['variables']['data']['countData'];
            var hugos = this['variables']['data']['hugos']
            var selectedCohorts = getSelectedCohorts()
            var allData = []
            var firstData = []
            var scales = ["percent", "counts"]
            for (var set in data) {
                var row = data[set][0];
                if (Object.keys(row).sort().join(',') === selectedCohorts.sort().join(',')) {
                    for (var cohort in row) {
                        for (var i in row[cohort]) {
                            var scale = "mutation_" + i
                            var counts = []
                            for (var hugo in hugos){
                              var count = row[cohort][i][hugos[hugo]]
                              counts.push(count)
                            }
                            counts.push(scale)
                            allData.push(counts);
                            if (i == "percent"){
                              firstData.push(counts)
                            }
                        }
                    }
                }
            }
            var text = firstData.map((row, i) => row.map((item, j) => {
              return `${item + "%"}` 
            }))
            var data = [

                {
                  z: firstData,
                  x: hugos,
                  y: selectedCohorts,
                  type: 'heatmap',
                  scale: "percent",
                  colorscale: 'RdBu',
                  text: text,
                  hoverinfo: 'text',

                },
                
              ];
              var layout = {
                title: 'Percentage of Non-Silent Mutations',

                annotations: [],
                xaxis: {
                  ticks: '',
                  side: 'bottom'
                },
                yaxis: {
                  ticks: '',
                  ticksuffix: ' ',
                  // width: 700,
                  // height: 700,
                  // autosize: false
                }
              };
              
              // for ( var i = 0; i < selectedCohorts.length; i++ ) {
              //   for ( var j = 0; j < hugos.length; j++ ) {
              //     var currentValue = allData[i][j];
              //     if (currentValue != 0.0) {
              //       var textColor = 'white';
              //     }else{
              //       var textColor = 'black';
              //     }
              //     if (hugos[j] == "TOTAL"){
              //       var text = sums[i]
              //       var textColor = "red"
              //     }else{
              //       var text = allData[i][j]
              //     }
              //     var result = {
              //       xref: 'x1',
              //       yref: 'y1',
              //       x: hugos[j],
              //       y: selectedCohorts[i],
              //       text: text,
              //       colorscale: 'YlOrRd',
              //       font: {
              //         family: 'Arial',
              //         size: 12,
              //         color: 'rgb(50, 171, 96)'
              //       },
              //       showarrow: false,
              //       font: {
              //         color: textColor
              //       }
              //     };
              //     layout.annotations.push(result);
              //   }
              // }
              
              Plotly.newPlot(myDiv, data, layout);
              addEl(chartDiv, myDiv)
        }
    }
}