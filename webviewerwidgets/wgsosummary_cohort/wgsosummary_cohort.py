import aiosqlite
import os
import json
async def get_data (queries):
    '''
    so_dic = {
        'MIS':'Missense',
        'SYN':'Synonymous',
        'FSI':'Frameshift insertion',
        'FI1':'Frameshift insertion',
        'FI2':'Frameshift insertion',
        'FSD':'Frameshift deletion',
        'FD1':'Frameshift deletion',
        'FD2':'Frameshift deletion',
        'INI':'Inframe insertion',
        'IIV':'Inframe insertion',
        'IND':'Inframe deletion',
        'IDV':'Inframe deletion',
        'CSS':'Complex substitution',
        'STG':'Stopgain',
        'STL':'Stoploss',
        'SPL':'Splice site',
        '2KU':'2k upstream',
        '2KD':'2k downstream',
        'UT3':'3\' UTR',
        'UT5':'5\' UTR',
        'INT':'Intron',
        'UNK':'Unknown',
        'missense':'Missense',
        'synonymous':'Synonymous',
        'frameshift insertion':'Frameshift insertion',
        'frameshift insertion by 1':'Frameshift insertion',
        'frameshift insertion by 2':'Frameshift insertion',
        'frameshift deletion':'Frameshift deletion',
        'frameshift deletion by 1':'Frameshift deletion',
        'frameshift deletion by 2':'Frameshift deletion',
        'inframe insertion':'Inframe insertion',
        'inframe deletion':'Inframe deletion',
        'complex substitution':'Complex substitution',
        'stop gained':'Stopgain',
        'stop lost':'Stoploss',
        'splice site':'Splice site',
        '2kb upstream':'2k upstream',
        '2kb downstream':'2k downstream',
        '3-prime utr':'3\' UTR',
        '5-prime utr':'5\' UTR',
        'intron':'Intron',
        'unknown':'Unknown'
    }
    '''
    
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()
 
    # selects all the sequence ontologies and returns the ones in which are found in the database 
    q = 'select subdict from variant_reportsub where module="base"'
    await cursor.execute(q)
    r = await cursor.fetchone()
    so_dic = json.loads(r[0])['so']
    so_dic[None] = 'Intergenic'
    so_dic[''] = 'Intergenic'
    q = 'select distinct variant.base__so from variant, variant_filtered where variant.base__uid=variant_filtered.base__uid'
    await cursor.execute(q)
    sos = [so_dic[v[0]] for v in await cursor.fetchall()]
    sos.sort()
 
    #select cohorts
    sets = {}
    num_total_samples = {}
    q = 'select cohort, count(sample.base__sample_id) from sample, variant, variant_filtered, cohorts where variant.base__coding = "Y" and variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample group by cohort;'
    await cursor.execute(q)
    sets['default'] = []
    for row in await cursor.fetchall():
        sets['default'].append(row[0])
        num_total_samples[row[0]] = row[1]
    q = "select set_name, cohorts from cohort_set;"
    await cursor.execute(q)
    rows = (await cursor.fetchall())
    for row in rows:
        sets[row[0]] = row[1].split(";")
    
    # print(num_total_samples)

    sos_groups = {
        'lof': ["FSI", "FSD", "STG", "STL", "SPL"],
        'missense': ["MIS"],
        'indel': ["INI", "IND"]
    }
    #retrieve data within each cohort
    responses = {}
    for _set in sets:
        
        respd = {}
        responses[_set] = []
        for c in sets[_set]:
            # print(num_total_samples[c])
            respd[c] = []
            groups = {}
            for group in sos_groups:
                sosample_counts = {}
                sosample_perc = {}
                for so in sos_groups[group]:
                    sosample_counts[so_dic[so]] = 0
                    sosample_perc[so_dic[so]] = 0
                so_group = sos_groups[group]
                if so_group[0] == "MIS":
                    select_group = "('" + so_group[0] + "')"
                else:
                    select_group = tuple(so_group)
                q = f'select c, count(*) from (select variant.base__hugo, variant.base__cchange, cohorts.sample, variant.base__so as c from variant, variant_filtered, sample, cohorts where variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{c}") as t where c in {select_group} group by c;'
                await cursor.execute(q)
                rows = (await cursor.fetchall())
                for row in rows:
                    sosample_perc[so_dic[row[0]]] = (row[1] / num_total_samples[c]) * 100
                    sosample_counts[so_dic[row[0]]] = row[1]
                groups[group] = {'percent': sosample_perc, 'counts': sosample_counts}
            respd[c].append(groups)
        responses[_set].append(respd)
    for key, value in sos_groups.items():
        sos_groups[key] = []
        for i in value:
            sos_groups[key].append(so_dic[i])
    response = {'data': {'sos': sos_groups, 'socountdata': responses}}
    await cursor.close()
    await conn.close()
    return response

