widgetGenerators['sosummary_cohort'] = {
    'cohort': {
        'name': 'Sequence Ontology by Cohort',
        'width': 880,
        'height': 380,
        'callserver': true,
        'variables': {},
        'init': function(data) {
            this['variables']['data'] = data;
        },
        'function': function(div, data) {
            var colorPalette = {
                'Frameshift insertion': '#2166AC',
                'Frameshift deletion': '#4393C3',
                'Stopgain': '#92C5DE',
                'Stoploss': '#D1E5F0',
                'Missense': '#1B7837',
                'Inframe insertion': '#FDDBC7',
                'Inframe deletion': '#F4A582',
                'Splice site': '#5AAE61',
                '2k upstream': '#D6604D',
                '2k downstream': '#B2182B',
                '3\' UTR': '#762A83',
                '5\' UTR': '#9970AB',
                'Complex substitution': '#C2A5CF',
                'Synonymous': '#E7D4E8',
                'Intron': '#D9F0D3',
                'Unknown': '#ACD39E',
                'Intergenic': '#ACD39E',
                'frameshift_elongation': '#2166AC',
                'frameshift_truncation': '#4393C3',
                'stop_gained': '#92C5DE',
                'stop_lost': '#D1E5F0',
                'missense_variant': '#1B7837',
                'inframe_insertion': '#FDDBC7',
                'inframe_deletion': '#F4A582',
                'splice_site_variant': '#5AAE61',
                '2kb_upstream_variant': '#D6604D',
                '2kb_downstream_variant': '#B2182B',
                '3_prime_UTR_variant': '#762A83',
                '5_prime_UTR_variant': '#9970AB',
                'complex_substitution': '#C2A5CF',
                'synonymous_variant': '#E7D4E8',
                'intron_variant': '#D9F0D3',
                'Unknown': '#ACD39E',
            };
            div.style.width = 'calc(100% - 37px)';
            var chartDiv = getEl('canvas');
            chartDiv.style.width = 'calc(100% - 20px)';
            chartDiv.style.height = 'calc(100% - 20px)';
            addEl(div, chartDiv);
            var data = this['variables']['data'];
            var sos = data['sos']
            var selectedCohorts = getSelectedCohorts()
            var initDatasets = [];
            for (var set in data['socountdata']) {
                var row = data['socountdata'][set];
                for (var cohort in row) {
                    if (Object.keys(row[cohort]).sort().join(',') === selectedCohorts.sort().join(',')) {
                        for (var j = 0; j < sos.length; j++) {
                            var initDatasetCounts = [];
                            var so = sos[j]
                            for (var i in row[cohort]) {
                                initDatasetCounts.push(row[cohort][i][0][so])
                            }
                            var backgroundColor = colorPalette[so];
                            initDatasets.push({
                                'label': so,
                                'backgroundColor': backgroundColor,
                                'data': initDatasetCounts,
                                'labels': selectedCohorts
                            });
                        }
                    }
                }
            }
            var chart = new Chart(chartDiv, {
                type: 'horizontalBar',
                data: {
                    labels: selectedCohorts,
                    datasets: initDatasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Number of Variants',
                            },
                            ticks: {
                                beginAtZero: true,
                            }
                        }],
                    },
                }
            })
        }
    }
}