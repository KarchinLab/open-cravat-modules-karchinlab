import aiosqlite
import os
import json
async def get_data (queries):

    dbpath = queries['dbpath']
    use_filtered = eval(queries['use_filtered'])
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()
 
    # selects all the sequence ontologies and returns the ones in which are found in the database 
    q = 'select subdict from variant_reportsub where module="base"'
    await cursor.execute(q)
    r = await cursor.fetchone()
    so_dic = json.loads(r[0])['so']
    so_dic[None] = 'Intergenic'
    so_dic[''] = 'Intergenic'
    query = 'select distinct variant.base__so'
    if use_filtered:
        from_str = ' from variant, variant_filtered '
        where = 'where variant.base__uid=variant_filtered.base__uid '
    else:
        from_str = ' from variant '
        where = ''
    query += from_str + where
    await cursor.execute(query)
    sos = [so_dic[v[0]] for v in await cursor.fetchall()]
    sos.sort()
    
    base_set = []
    complete_set = []
    cohort_list =[]
    num_total_samples = {}
    query = 'select cohort, count(distinct(sample.base__sample_id))'
    if use_filtered:
        from_str = ' from variant, variant_filtered, sample, cohorts '
        where = 'where variant.base__uid=variant_filtered.base__uid and '
    else:
        from_str = ' from variant, sample, cohorts '
        where = 'where '
    where += 'variant.base__coding=="Y" and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample group by cohort'
    query += from_str + where
    await cursor.execute(query)
    for row in await cursor.fetchall():
        cohort_list.append(row[0])
        num_total_samples[row[0]] = row[1]

    sos_groups = {
        'Loss of Function': ["FSI", "FSD", "STG", "STL", "SPL"],
        'Missense': ["MIS"],
        'Insertion / Deletions': ["INI", "IND"]
    }
    color_palette = {
        'FSI': '#2166AC',
        'FSD': '#4393C3',
        'STG': '#92C5DE',
        'STL': '#D1E5F0',
        'MIS': '#B2182B',
        'INI': '#FDDBC7',
        'IND': '#F4A582',
        'SPL': '#D1E5F0',
        'Loss of Function': '#92C5DE',
        'Missense': '#B2182B',
        'Insertion / Deletions': '#5AAE61'
    }

    for sos in sos_groups:
        base_so_info ={
            'label': sos,
            'backgroundColor': color_palette[sos],
            'labels': cohort_list
        }
        base_set.append(base_so_info)
        for so in sos_groups[sos]:
            complete_so_info = {
                'label': so,
                'backgroundColor': color_palette[so],
                'labels': cohort_list
            }
            complete_set.append(complete_so_info)
    for record in base_set:
        count_data = []
        perc_data = []
        for cohort in record['labels']:
            if sos_groups[record['label']][0] == "MIS":
                select_group = "('" + sos_groups[record['label']][0] + "')"
            else:
                select_group = tuple(sos_groups[record['label']])
            query = 'select count(distinct(samp)) from (select variant.base__hugo, variant.base__cchange, cohorts.sample as samp, variant.base__so as c '
            if use_filtered:
                from_str = ' from variant, variant_filtered, sample, cohorts '
                where = 'where variant.base__uid=variant_filtered.base__uid and '
            else:
                from_str = ' from variant, sample, cohorts '
                where = 'where '
            where += f'sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}" and c in {select_group} group by cohorts.sample, c)'
            query += from_str + where
            await cursor.execute(query)
            rows = (await cursor.fetchall())
            for row in rows:
                count_data.append(row[0])
                perc_data.append((row[0] / num_total_samples[cohort]) * 100)
        record['count_data'] = count_data
        record['perc_data'] = perc_data
        record['data'] = count_data

    for record in complete_set:
        count_data = []
        perc_data = []
        for cohort in record['labels']:
            select_groups = record['label']
            query = 'select c, count(*) from (select variant.base__hugo, variant.base__cchange, cohorts.sample, variant.base__so as c'
            if use_filtered:
                from_str = ' from variant, variant_filtered, sample, cohorts '
                where = 'where variant.base__uid=variant_filtered.base__uid and '
            else:
                from_str = ' from variant, sample, cohorts '
                where = 'where '
            where += f'sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}" group by cohorts.sample, c) as t where c = "{select_groups}"'
            query += from_str + where
            await cursor.execute(query)
            rows = (await cursor.fetchall())
            for row in rows:
                count_data.append(row[1])
                perc_data.append((row[1] / num_total_samples[cohort]) * 100)
        record['count_data'] = count_data
        record['perc_data'] = perc_data
        record['data'] = count_data
    response = {'data': {'base_data': base_set, 'complete_data': complete_set}}
    await cursor.close()
    await conn.close()
    return response

