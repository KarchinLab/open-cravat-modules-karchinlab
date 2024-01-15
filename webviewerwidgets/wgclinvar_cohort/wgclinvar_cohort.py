import aiosqlite
import os
import json

async def get_data (queries):
    dbpath = queries['dbpath']
    use_filtered = eval(queries['use_filtered'])
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

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
        cohort_list.append(row[0])
        num_total_samples[row[0]] = row[1]

    # select clinvar significance
    query = 'select DISTINCT clinvar__sig'
    if use_filtered:
        from_str = ' from variant, variant_filtered '
        where = 'where variant.base__uid=variant_filtered.base__uid and '
    else:
        from_str = ' from variant '
        where = 'where '
    where += 'clinvar__sig is not null'
    query += from_str + where
    await cursor.execute(query)
    all_sigs = set()
    for row in await cursor.fetchall():
        all_sigs.add(row[0])
        base_clinvar_info = {
            'labels': cohort_list,
            'label': row[0],
            'data': [],
            'count_data': [],
            'perc_data': []
        }
        base_set.append(base_clinvar_info)
    # select number of variants found in at least one sample in clinvar for each cohort in each significane level
    for cohort in cohort_list:
        query = 'select clinvar__sig, count(distinct(sample)) '
        if use_filtered:
            from_str = ' from variant, variant_filtered, sample, cohorts '
            where = 'where variant.base__uid=variant_filtered.base__uid and '
        else:
            from_str = ' from variant, sample, cohorts '
            where = 'where '
        where += f'clinvar__sig is not null and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}"  group by clinvar__sig;'
        query += from_str + where
        await cursor.execute(query)
        rows = (await cursor.fetchall())
        array = set(list(zip(*rows))[0])
        missing = list(sorted(all_sigs - array))
        for record in base_set:
            for row in rows:
                label = row[0]
                if record['label'] == label:
                    record['data'].append(row[1]) 
                    record['count_data'].append(row[1])
                    record['perc_data'].append((row[1] / num_total_samples[cohort]) * 100)
            for sig in missing:
                if record['label'] == sig:
                    record['data'].append(0) 
                    record['count_data'].append(0)
                    record['perc_data'].append(0)
    await cursor.close()
    await conn.close()
    return {"data": base_set}