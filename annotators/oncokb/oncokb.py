import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import requests

class CravatAnnotator(BaseAnnotator):
    def setup(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        datafile_path = os.path.join(dir_path, "data", "oncokb.txt")
        with open(datafile_path) as f:
            for l in f:
                self.token = l
        pass
    def annotate(self, input_data):
        self.uid = input_data["uid"]
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        return {
            'chrom': chrom,
            'pos': pos,
            'ref': ref,
            'alt': alt
        }

    def _get_hgvs_g(self, chrom, pos, ref, alt):
        hgvs_g = f'{chrom}:g.'
        hgvs_g += self._get_hgvs_nuc(pos, ref, alt)
        return hgvs_g

    def _get_hgvs_nuc(self, pos, ref, alt):
        hgvs_nuc = ''
        start = pos
        end = str(int(pos) + len(ref) - 1)
        if ref == '-':
            hgvs_nuc += '%s_%sins%s' %(str(int(start) - 1), start, alt)
        elif alt == '-':
            if len(ref) == 1:
                hgvs_nuc += '%sdel' %start
            else: 
                hgvs_nuc += '%s_%sdel' %(start, end)
        else:
            if len(ref) == 1 and len(alt) == 1:
                hgvs_nuc += '%s%s>%s' %(start, ref, alt)
            else:
                hgvs_nuc += '%s_%sdelins%s' %(start, end, alt)
        return hgvs_nuc

    def postprocess(self):
        batch = []
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json',
        }
        max_lnum = self.uid - 1
        uids = []
        keys = {}
        count = 0
        for lnum, line, input_data, secondary_data in self._get_input():
            try:
                chrom = input_data['chrom']
                pos = str(input_data['pos'])
                ref = input_data['ref_base']
                alt = input_data['alt_base']
                uid = input_data["uid"]
                uids.append(uid)
                count = count + 1
                hgvs_g = self._get_hgvs_g(chrom, pos, ref, alt)
                batch.append(hgvs_g)
                datas = ''
                if count % 100 == 0 and lnum != 0 or lnum == max_lnum:
                    data =  "[ "
                    for b in batch:
                        data = data + '{ "evidenceTypes": [ "GENE_SUMMARY", "MUTATION_SUMMARY", "TUMOR_TYPE_SUMMARY", "PROGNOSTIC_SUMMARY", "DIAGNOSTIC_SUMMARY", "ONCOGENIC", "MUTATION_EFFECT", "PROGNOSTIC_IMPLICATION", "DIAGNOSTIC_IMPLICATION", "STANDARD_THERAPEUTIC_IMPLICATIONS_FOR_DRUG_SENSITIVITY", "STANDARD_THERAPEUTIC_IMPLICATIONS_FOR_DRUG_RESISTANCE"], "hgvsg":' + '"' + b + '"' + ', "id": "", "referenceGenome": "GRCh38"}, '
                    data = data[:-2]
                    data = data + "]" 
                    response = requests.post('https://www.oncokb.org/api/v1/annotate/mutations/byHGVSg', headers=headers, data=data)
                    datas = response.json()
                    batch = []
                if len(datas) > 0:
                    for n, x  in enumerate(datas):
                        oncogenic = x['oncogenic']
                        mutaff = x['mutationEffect']
                        knownEffect = mutaff["knownEffect"]
                        citations = mutaff['citations']
                        if len(citations["pmids"]) < 1:
                            pmids = ""
                        pmids = '; '.join(citations["pmids"])
                        highestSensitiveLevel = x['highestSensitiveLevel']
                        if highestSensitiveLevel:
                            highestSensitiveLevel = highestSensitiveLevel.replace('LEVEL_', '')
                        highestResistanceLevel = x['highestResistanceLevel']
                        if highestResistanceLevel:
                            highestResistanceLevel = highestResistanceLevel.replace("LEVEL_R", '')
                        highestDiagnosticImplicationLevel = x['highestDiagnosticImplicationLevel']
                        if highestDiagnosticImplicationLevel:
                            highestDiagnosticImplicationLevel = highestDiagnosticImplicationLevel.replace("LEVEL_Dx", "")
                        highestPrognosticImplicationLevel= x['highestPrognosticImplicationLevel']
                        if highestPrognosticImplicationLevel:
                            highestPrognosticImplicationLevel = highestPrognosticImplicationLevel.replace("LEVEL_Px", "")
                        hotspot= x['hotspot']
                        geneSummary = x['geneSummary']
                        variantSummary = x['variantSummary']
                        tumorSummary = x["tumorTypeSummary"]
                        diagnosticImplications = x["diagnosticImplications"]
                        precomp_data = []
                        for i in range(len(diagnosticImplications)):
                            dd = diagnosticImplications[i]
                            level = dd['levelOfEvidence'].replace("LEVEL_Dx", "")
                            diagnostic_data = [level, dd['tumorType']['mainType']['name'], dd['tumorType']['mainType']['tumorForm'], dd['pmids']]
                            precomp_data.append([{"diagnostic_data": diagnostic_data}])
                        treatments = x["treatments"]
                        for i in range(len(treatments)):
                            tt = treatments[i]
                            drugs = tt["drugs"]
                            code = [x['ncitCode'] for x in drugs]
                            drugname = [x['drugName'] for x in drugs]
                            approved_indications = tt['approvedIndications']
                            treatment_pmids = tuple(tt['pmids'])
                            levelAssociatedCancerType = tt["levelAssociatedCancerType"]
                            levelAssociatedCancerType_level = levelAssociatedCancerType["level"]
                            cancer_name = levelAssociatedCancerType["name"]
                            cancer_tissue = levelAssociatedCancerType["tissue"]
                            cancer_tumor = levelAssociatedCancerType["tumorForm"]
                            treatment_data = [code, drugname, approved_indications, treatment_pmids, levelAssociatedCancerType_level, cancer_name, cancer_tissue, cancer_tumor]
                            precomp_data.append([{"treatment_data":treatment_data}])
                        prognosticImplications = x["prognosticImplications"]
                        for p in range(len(prognosticImplications)):
                            prog = prognosticImplications[p]
                            progLevelOfEvidence = prog["levelOfEvidence"].replace("LEVEL_Px", "")
                            progTumorType= prog["tumorType"]['mainType']['name']
                            progTumorForm = prog["tumorType"]['mainType']['tumorForm']
                            progTissue = prog["tumorType"]["tissue"]
                            progPmids = prog["pmids"]
                            prognostic_data = [progLevelOfEvidence, progTumorType, progTumorForm, progTissue, progPmids]
                            precomp_data.append([{"prognostic_data": prognostic_data}])
                        if len(precomp_data) < 1:
                            precomp_data = None
                        output_dict = {
                            'oncogenic': oncogenic,
                            'knownEffect': knownEffect,
                            'pmids': pmids,
                            'highestSensitiveLevel': highestSensitiveLevel,
                            'highestResistanceLevel': highestResistanceLevel,
                            'highestDiagnosticImplicationLevel': highestDiagnosticImplicationLevel,
                            'highestPrognosticImplicationLevel': highestPrognosticImplicationLevel,
                            'hotspot': hotspot,
                            'geneSummary': geneSummary,
                            'tumorSummary': tumorSummary,
                            'variantSummary': variantSummary,
                            'all': precomp_data
                        }
                        output_dict = self.handle_jsondata(output_dict)
                        if n in keys:
                            keys[n] = keys[n] + 100
                            output_dict['uid'] = uids[keys[n]]
                        else:
                            output_dict['uid'] = uids[n]
                            keys[n] = n
                        output_dict = self.fill_empty_output(output_dict)
                        self.output_writer.write_data(output_dict)
                    
            except Exception as e:
                self._log_runtime_exception(lnum, line, input_data, e)

    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()