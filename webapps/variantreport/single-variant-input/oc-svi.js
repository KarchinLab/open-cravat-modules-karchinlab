/***
 *  OC Single Variant Input Widget
 *  This code will initialize the OC single variant input widget on a page that contains a valid container.
 *
 *  To use:
 *    1. add empty container to html file -
 *    <div id='oc-svi'></div>
 *    2. include this file as a script
 *    <script src="oc-svi.js" type="application/javascript" defer></script>
 *    3. include the stylesheet
 *    <link rel="stylesheet" type="text/css" href="oc-svi.css" />
 **/

// Base URL for the single variant page
const API_URL = 'https://run.opencravat.org/webapps/variantreport/index.html';
// types of input allowed
class TYPES {
    static DBSNP = 'dbsnp';
    static CLINGEN = 'clingen';
    static HGVS = 'hgvs';
    static COORDS = 'coords';
    static ERROR = 'error';
}

// validate rsid input
function isDbSnp(input) {
    return input.substring(0, 2) === 'rs';
}

// validate clingen allele registry input
function isClingenAlleleRegistry(input) {
    return input.substring(0, 2) === 'ca';
}

// validate hgvs input, want something of the form: AAAA:c.2134a>c
function isHGVS(input) {
    const validSequenceTypes = ['c', 'g', 'm', 'n', 'o', 'p', 'r'];
    // check that the first token is something like aaaa:X.bbb where X is a valid reference sequence type
    let parts = input.split(':');
    if (parts.length !== 2) {
        return false;
    }
    let descriptionParts = parts[1].split('.');
    if (descriptionParts.length !== 2) {
        return false;
    }
    if (!validSequenceTypes.includes(descriptionParts[0])) {
        return false;
    }
    return true;
}

// parse a chromosome for coordinate input, anything from 1-22, x, y, m, mt
// 'chr' prefix optional
function findChromosome(id) {
    const validChroms = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
        '20', '21', '22', 'x', 'y', 'm'
    ];
    let idOnly = id.startsWith('chr') ? id.substring(3) : id;
    if (idOnly === 'mt') { idOnly = 'm'; }
    if (!validChroms.includes(idOnly)) {
        return false;
    }
    return `chr${idOnly}`;
}

// parse coordinates input
// Expect four tokens corresponding to: 1. chromosome, 2. position, 3. reference base, 4. alternate base
// 1. Chromosome should be a valid chromosome (from findChromosome)
// 2. Position must be an integer
// 3. / 4. Reference and alternate bases should be in (a, c, g, t)
// Valid separators of the tokens are (' ', '\t', ':', '.', ';')
// Deletions should be written with correct reference base and '-' as alternate base
// Insertions should be written with '-' as reference base
// Duplications should be written as insertions
function parseCoordinates(input) {
    // split by multiple separator characters
    const parts = input.split(':').join(';')
        .split('.').join(';')
        .split(' ').join(';')
        .split('\t').join(';')
        .split(';');
    if (parts.length !== 4) {
        return false;
    }
    let chromosome = findChromosome(parts[0]);
    if (chromosome === false) { return false; }
    parts[0] = chromosome;
    if (Number.isNaN(Number.parseInt(parts[1]))) { return false; }
    const validBasesRegex = /^[acgt-]+$/;
    if (!validBasesRegex.test(parts[2])) { return false; }
    if (!validBasesRegex.test(parts[3])) { return false; }

    parts[2] = parts[2].toUpperCase();
    parts[3] = parts[3].toUpperCase();
    return parts;
}

function determineInputType(input) {
    if (isDbSnp(input)) {
        return TYPES.DBSNP;
    }
    if (isClingenAlleleRegistry(input)) {
        return TYPES.CLINGEN;
    }
    if (isHGVS(input)) {
        return TYPES.HGVS;
    }
    if (parseCoordinates(input)) {
        return TYPES.COORDS;
    }
    return TYPES.ERROR;
}

// format hgvs string for url
// Everything will be uppercase except for the c. prefix, then will be url encoded
function formatHgvs(hgvs) {
    const hgvsParts = hgvs.toUpperCase().split(':');
    const prefix = hgvsParts[1][0].toLowerCase();
    const end = hgvsParts[1].substring(1);
    return `${hgvsParts[0]}:${prefix}${end}`;
}

// build url based on the input type
function buildUrl(inputType, input) {
    if (inputType === TYPES.HGVS) {
        const encoded = formatHgvs(input);
        return `${API_URL}?hgvs=${encoded}`;
    }
    if (inputType === TYPES.CLINGEN) {
        return `${API_URL}?clingen=${input}`;
    }
    if (inputType === TYPES.DBSNP) {
        return `${API_URL}?dbsnp=${input}`;
    }
    if (inputType === TYPES.COORDS) {
        const parts = parseCoordinates(input);
        const assembly = document.getElementById('oc-svi-assembly').value;
        return `${API_URL}?assembly=${assembly}&chrom=${parts[0]}&pos=${parts[1]}&ref_base=${parts[2]}&alt_base=${parts[3]}`;
    }
}

function buildUrlFromPostData(data) {
    let url = `${API_URL}?`;
    for (const [key, val] of Object.entries(data)) {
        url += `${key}=${encodeURIComponent(val)}&`;
    }
    // strip last &
    url = url.substring(0, url.length -1);
    return url;
}

function buildPostData(inputType, input) {
    if (inputType === TYPES.HGVS) {
        const encoded = formatHgvs(input);
        return {'hgvs': encoded};
    }
    if (inputType === TYPES.CLINGEN) {
        return {'clingen': input};
    }
    if (inputType === TYPES.DBSNP) {
        return {'dbsnp': input};
    }
    if (inputType === TYPES.COORDS) {
        const parts = parseCoordinates(input);
        const assembly = document.getElementById('oc-svi-assembly').value;
        return {
            'chrom': parts[0],
            'pos': parts[1],
            'ref_base': parts[2],
            'alt_base': parts[3],
            'assembly': assembly
        };
    }
}

// try to determine the input type and do some quick validation, then either show an error or
// open a link to the single variant page
function handleSubmit(event) {
    const originalInput = document.getElementById('oc-svi-input').value;
    const input = originalInput.trim().toLowerCase();
    const inputType = determineInputType(input);

    if (inputType === TYPES.ERROR) {
        let error = document.getElementById('oc-svi-error');
        error.style.display = '';
    } else {
        // close example modal
        document.getElementById('oc-svi-examples-close-btn').click();
        // Emit event for other pages to handle
        const parameters = buildPostData(inputType, input);
        const event = new CustomEvent('variantSubmit', {'bubbles': true, 'detail': parameters})
        const form = document.getElementById('oc-svi-form');
        form.dispatchEvent(event);
    }
    event.preventDefault();
}

function navigateToSingleVariantPage(event) {
    if (!event.detail) { return; }

    const parameters = event.detail;
    // const url = buildUrl(inputType, input);
    const url = buildUrlFromPostData(parameters);
    window.open(url, '_blank');
}

function showExamples() {
    document.getElementById('oc-svi-examples').classList.add('show-examples');
}

function hideExamples() {
    document.getElementById('oc-svi-examples').classList.remove('show-examples');
}

function handleExampleButton(evt) {
    const value = evt.currentTarget.value;
    if (value) {
        document.getElementById('oc-svi-input').value = value;
    }
}

// entry point, on document.ready, find the oc-svi container and replace it's html content with our
// single input form and attach handlers to the newly created objects.
document.addEventListener('DOMContentLoaded', ()  => {
    let inputContainer = document.getElementById('oc-svi');
    if (!inputContainer) return;
    let title = inputContainer.getAttribute('title');
    if (!title) {
        title = 'OpenCRAVAT';
    }

    inputContainer.innerHTML = `
        <div id="oc-svi-container">
            <h1 id="oc-svi-header" class="oc-svi-text-block">${title}</h1>
            <div class="oc-svi-text-block">Open Custom Ranked Analysis of Variants Toolkit</div>
            <div id="oc-svi-examples-container" class="oc-svi-text-block">
                <div id="oc-svi-examples">
                    <div id="oc-svi-examples-close-btn" title="Close"></div>
                    <div class="top-list">
                        <button class="example oc-svi-text-button" value="NM_000051.4:c.2413C>T">
                            <div class="example-label">HGVS</div>
                            <div>NM_000051.4:c.2413C&gt;T</div>
                        </button>
                        <button class="example oc-svi-text-button" value="rs121913514">
                            <div class="example-label">dbSNP</div>
                            <div>rs121913514</div></button>
                        <button class="example oc-svi-text-button" value="CA10578967">
                            <div class="example-label">ClinGen Allele Registry</div>
                            <div class="">CA10578967</div>
                        </button>
                        <button class="example oc-svi-text-button" value="chr3 179218293 G A">
                            <div class="example-label">SNV</div><div>
                            <div>chr3 179218293 G A</div></div>
                        </button>
                            <button class="example oc-svi-text-button" value="chr10 87960891 - T">
                            <div class="example-label">Insertion</div>
                            <div>chr10 87960891 - T</div>
                        </button>
                        <button class="example oc-svi-text-button" value="chr10 87961046 ACTT -">
                            <div class="example-label">Deletion</div>
                            <div>chr10 87961046 ACTT -</div>
                        </button>
                    </div>
                </div>
                <button class="oc-svi-text-button oc-svi-light" id="oc-svi-examples-btn">Examples</button>
            </div>
            <form id="oc-svi-form">
                <input id="oc-svi-input" type="text" placeholder="Enter variant HGVS, rsID, Allele Registry ID, or genomic coordinates." />
                <div class="oc-svi-select-container">
                    <label for="oc-svi-assembly" id="oc-svi-assembly-label">Assembly</label>
                    <select name="oc-svi-assembly" id="oc-svi-assembly">
                        <option value="hg38">hg38</option>
                        <option value="hg19">hg19</option>
                    </select>
                </div>
                <button id="oc-svi-submit-button" type="submit" title="Search"></button>
            </form>
            <div id="oc-svi-error" class="oc-svi-text-block" style="display: none">
                Could not determine input type. Please see our <button id="oc-svi-examples-error-btn" class="oc-svi-text-button oc-svi-light" type="button">examples</button>.
            </div>
            <div class="oc-svi-text-block">Need to annotate more variants? Try our <a href="https://run.opencravat.org" target="_blank" class="oc-svi-text-button oc-svi-light">web app</a> or <a href="https://www.opencravat.org/#get-started" target="_blank" class="oc-svi-text-button oc-svi-light">install locally.</a></divc>
        </div>
        `;
    document.getElementById('oc-svi-form').addEventListener('submit', handleSubmit);
    document.getElementById('oc-svi-submit-button').addEventListener('click', handleSubmit);
    document.getElementById('oc-svi-examples-btn').addEventListener('click', showExamples);
    document.getElementById('oc-svi-examples-error-btn').addEventListener('click', showExamples);
    document.getElementById('oc-svi-examples-close-btn').addEventListener('click', hideExamples);
    Array.from(document.getElementsByClassName('example')).forEach(btn => {
        btn.addEventListener('click', handleExampleButton);
    });

    // handle the form submission with a page navigation *unless* a custom handler is indicated
    if (!inputContainer.classList.contains('custom-handler')) {
        inputContainer.addEventListener('variantSubmit', navigateToSingleVariantPage)
    }
});