import aiosqlite
import os
import datetime

async def get_data (queries):
    dbpath = queries['dbpath']
    use_filtered = eval(queries['use_filtered'])
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    # Select what top 10 genes to extract
    gene_var_perc = {}
    query = 'select variant.base__hugo, count(*)'
    if use_filtered:
        from_str = ' from variant, variant_filtered '
        where = 'where variant.base__uid=variant_filtered.base__uid and '
    else:
        from_str = ' from variant '
        where = 'where '
    where += 'variant.base__coding=="Y" and variant.base__hugo is not null group by variant.base__hugo;'
    query += from_str + where
    await cursor.execute(query)
    for row in await cursor.fetchall():
        hugo = row[0]
        if hugo == '':
            continue
        count = row[1]
        gene_var_perc[hugo] = count
    num_gene_to_extract = 10
    sorted_hugos = sorted(gene_var_perc, key=gene_var_perc.get, reverse=True)
    extracted_hugos = sorted_hugos[:num_gene_to_extract]

    #select cohorts
    num_total_samples = {}
    cohort_list = []
    base_set = []
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
        num_total_samples[row[0]] = row[1]
        cohort_list.append(row[0])
        cohort_info = {
            'labels': extracted_hugos,
            'label': row[0],
            'data': [],
            'count_data': [],
            'perc_data': []
        }
        base_set.append(cohort_info)
    if len(extracted_hugos) > 1:
        tuple_extracted_hugo = tuple(extracted_hugos)
    else:
        tuple_extracted_hugo =  "('" + extracted_hugos[0] + "')"
    for record in base_set:
        cohort = record['label']
        query = 'select variant.base__hugo, count(distinct(sample.base__sample_id))'
        if use_filtered:
            from_str = ' from variant, variant_filtered, sample, cohorts '
            where = 'where variant.base__uid=variant_filtered.base__uid and '
        else:
            from_str = ' from variant, sample, cohorts '
            where = 'where '
        where += f'sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}" and variant.base__hugo in {tuple_extracted_hugo} group by variant.base__hugo;'
        query += from_str + where
        await cursor.execute(query)
        rows = (await cursor.fetchall())
        dictionary = {}
        for key, val in rows:
            dictionary.setdefault(key, val)
        sorted_results = [(key, dictionary[key]) for key in extracted_hugos if key in dictionary]
        for row in sorted_results:
            record['data'].append(row[1])
            record['count_data'].append(row[1])
            record['perc_data'].append((row[1] / num_total_samples[cohort]) * 100)

    await cursor.close()
    await conn.close()
    return {"data":{ 'counts': base_set,'hugos': extracted_hugos}}

