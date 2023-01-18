import aiosqlite
import os
import json

async def get_data (queries):
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    # Select what top 10 genes to extract
    gene_var_perc = {}
    q = 'select variant.base__hugo, count(*) from variant, variant_filtered where variant.base__coding=="Y" and variant.base__uid=variant_filtered.base__uid and variant.base__hugo is not null group by variant.base__hugo'
    await cursor.execute(q)
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
    sets = {}
    q = "select distinct(cohort) from cohorts;"
    await cursor.execute(q)
    sets['default'] = []
    for row in await cursor.fetchall():
        sets['default'].append(row[0])
    q = "select set_name, cohorts from cohort_set;"
    await cursor.execute(q)
    rows = (await cursor.fetchall())
    for row in rows:
        sets[row[0]] = row[1].split(";")

    #retrieve data within each cohort
    response = {}
    for _set in sets:
        data = {}
        response[_set] = []
        for cohort in sets[_set]:
            data[cohort] = []
            genesampleperc = {}
            for hugo in extracted_hugos:
                q = f'select count(variant.base__uid), cohort from variant, variant_filtered, sample, cohorts where variant_filtered.base__uid = variant.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}" and variant.base__hugo ="' + hugo + '"'
                counts = {}
                await cursor.execute(q)
                rows = await cursor.fetchall()
                if rows:
                    for row in rows:
                        counts[hugo] = row[0]
                    data[cohort].append([hugo, counts[hugo]])
        response[_set].append(data)
    await cursor.close()
    await conn.close()
    return {"data": response}