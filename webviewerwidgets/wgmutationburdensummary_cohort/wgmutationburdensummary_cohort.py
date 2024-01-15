import aiosqlite
import os
import json
from scipy.stats import fisher_exact
import numpy as np
async def get_data (queries):

    dbpath = queries['dbpath']
    use_filtered = eval(queries['use_filtered'])
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    # return all coding genes
    mutation_counts = {}
    query = 'select variant.base__hugo'
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
        mutation_counts[hugo] = {}
    
    # return all cohorts
    cohort_list = []
    data = []
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
    num_total_samples = {}
    for row in await cursor.fetchall():
        cohort, sample_count = row
        num_total_samples[cohort] = sample_count
        cohort_list.append(cohort)
        cohort_info = {
            'labels': [],
            'label' : cohort,
            'data' : [],
        }
        data.append(cohort_info)
    # retrieve data within each cohort
    hugos = list(mutation_counts.keys())
    if len(hugos) > 1:
        tuple_extracted_hugo = tuple(hugos)
    else:
        tuple_extracted_hugo =  "('" + hugos[0] + "')"
    for cohort in cohort_list:
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

        # find genes (if any) that are in the dataset but not found in that cohort
        missing_genes = [ele for ele in hugos if ele not in [list(row)[0] for row in rows]]
        for row in rows:
            for key, val in mutation_counts.items():
                if key == row[0]:
                    mutation_counts[key][cohort] = row[1]
        # add a count of 0 for missing genes
        for gene in missing_genes: 
            mutation_counts[gene][cohort] = 0
    pvalue_dict = {}
    for hugo, counts in mutation_counts.items():
        max_cohort = max(counts, key=counts.get)
        max_count = counts[max_cohort]
        cohort_num_samples = num_total_samples[max_cohort]
        cohort_sample_missing = cohort_num_samples - max_count
        pvalue_dict[hugo] = []
        # find cohort with max mutated sample count
        for cohort, count in counts.items():
            if cohort != max_cohort:
                # cohort with max mutated sample count count to each other phenotype pairwise
                control_sample_missing = num_total_samples[cohort] - count
                table = [
                    [max_count, cohort_sample_missing],
                    [count, control_sample_missing]
                ]
                pvalue = fisher_exact(table, alternative='greater')[1]
                pvalue_dict[hugo].append(pvalue)
    # return the top 10 genes with the most signifigant p-value
    num_gene_to_extract = 10
    sorted_hugos = sorted(pvalue_dict, key=pvalue_dict.get, reverse=False)
    extracted_hugos = sorted_hugos[:num_gene_to_extract]
    for hugo in extracted_hugos:
        for dic in data:
            cohort = dic['label']
            top_data = mutation_counts[hugo][cohort] 
            dic['labels'].append(hugo)
            dic['data'].append(top_data)
    await cursor.close()
    await conn.close()
    return {"data": {'counts': data, 'hugos': extracted_hugos}}


