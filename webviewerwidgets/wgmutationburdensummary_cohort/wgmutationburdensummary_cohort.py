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

    hugo_perc = {}
    for hugo in extracted_hugos:
        q = f'select sum(tagsampler__numsample) from variant where variant.base__hugo ="{hugo}"'
        await cursor.execute(q)
        rows = await cursor.fetchall()
        for row in rows:
            num = row[0]
            hugo_perc[hugo] = num
    #retrieve data within each cohort
    response = {}
    hugos = set()
    tuple_extracted_hugo = tuple(extracted_hugos)
    for _set in sets:
        data = {}
        response[_set] = []
        for cohort in sets[_set]:
            data[cohort] = []
            genesampleperc = {}
            # for hugo in extracted_hugos:
            q = f'select variant.base__hugo, count(variant.base__uid) from variant, variant_filtered, sample, cohorts where variant_filtered.base__uid = variant.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}" and variant.base__hugo in {tuple_extracted_hugo} group by variant.base__hugo'
            counts = []
            await cursor.execute(q)
            rows = await cursor.fetchall()
            if rows:
                for row in rows:
                    hugos.add(row[0])
                    counts.append(row[1])
                data[cohort].append(counts)
        response[_set].append(data)
    await cursor.close()
    await conn.close()
    extracted_hugos.sort()
    return {"data": {'counts': response, 'hugos': extracted_hugos}}