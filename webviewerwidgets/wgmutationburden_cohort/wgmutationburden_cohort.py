import aiosqlite
import os

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
    num_gene_to_extract = 25
    sorted_hugos = sorted(gene_var_perc, key=gene_var_perc.get, reverse=True)
    extracted_hugos = sorted_hugos[:num_gene_to_extract]

    hugos = {}
    for hugo in extracted_hugos:
        hugos[hugo] = []

    #select cohorts
    sets = {}
    num_total_samples = {}
    q = "select cohort, count(sample) from cohorts group by cohort;"
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
            
            # num_total_samples[hugo] = row[1]
    #retrieve data within each cohort
    response = {}
    
    for _set in sets:
        data = {}
        response[_set] = []
        for cohort in sets[_set]:
            data[cohort] = []
            genesamplecount = {}
            genesampleperc = {}
            counts_per_gene = num_total_samples[cohort]
            for hugo in extracted_hugos:
                
                q = f'select count(distinct(sample.base__sample_id)) from sample, variant, variant_filtered, cohorts where variant.base__coding=="Y" and variant.base__so !="SYN" and variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}"and variant.base__hugo="{hugo}"'
                await cursor.execute(q)
                rows = (await cursor.fetchall())
                for row in rows:
                    num_sample = row[0]
                    hugos[hugo].append((num_sample / num_total_samples[cohort]) * 100)
                    genesampleperc[hugo] = round((num_sample / num_total_samples[cohort]) * 100)
                    genesamplecount[hugo] = num_sample
            
            data[cohort] = {'percent': genesampleperc, 'counts': genesamplecount}

        response[_set].append(data)
    
    hugo_perc = {}
    for key, value in hugos.items():
        hugo_perc[key] = max(value) - min(value)
    sorted_hugos = sorted(hugo_perc, key=hugo_perc.get, reverse=True)

    await cursor.close()
    await conn.close()
    return {"data": {'countData': response, 'hugos': sorted_hugos}}