import aiosqlite
import os

async def get_data (queries):
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

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
    
    cohorts = {}
    q = "select count(*), sample from cohorts"
    await cursor.execute(q)
    rows = (await cursor.fetchall())
    for row in rows:
        max_rows = row[0]
        sample = row[1]
        q = f'select count(sample) from cohorts where sample = "{sample}"'
        await cursor.execute(q)
        num_cohorts = (await cursor.fetchone())[0]
        for cohort in range(1, num_cohorts + 1):
            cohorts[cohort] = set()
            nrows = tuple([i for i in range(cohort,max_rows + 1, num_cohorts)])
            q = f'SELECT ROW_NUMBER() OVER (ORDER BY (SELECT "1")) AS RowID, cohort FROM cohorts where RowID in {nrows}'
            await cursor.execute(q)
            rowsd = (await cursor.fetchall())
            for rowd in rowsd:
                cohorts[cohort].add(rowd[1])
    
    responses = {}
    for cohort in cohorts:
        respd = {}
        responses[cohort] = []
        for c in cohorts[cohort]:
            respd[c] = []
            genesampleperc = {}
            for hugo in extracted_hugos:
                q = f'select count(distinct(sample.base__sample_id)) from sample, variant, variant_filtered, cohorts where variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{c}" and variant.base__hugo="' + hugo + '"'
                await cursor.execute(q)
                num_sample = (await cursor.fetchone())[0]
                genesampleperc[hugo] = num_sample
            for hugo in genesampleperc:
                respd[c].append([hugo, genesampleperc[hugo]])
        responses[cohort].append(respd)
    await cursor.close()
    await conn.close()
    response = {"data": responses}
    return response
