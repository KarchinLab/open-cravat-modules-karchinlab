import aiosqlite
import os
import json

async def get_data (queries):
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    numsamples = {}
    q = 'select variant.base__hugo, count(*) from variant, variant_filtered where variant.base__coding=="Y" and variant.base__uid=variant_filtered.base__uid and variant.base__hugo is not null group by variant.base__hugo'
    await cursor.execute(q)
    for row in await cursor.fetchall():
        gene = row[0]
        varcount = row[1]
        numsamples[gene] = varcount
    sorted_hugos = sorted(numsamples, key=numsamples.get, reverse=True)
    extracted_hugos = sorted_hugos[:10]
    num_sample = {}
    countsofsamples = {}

    cohorts = {}
    cohort_sample = {}
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
            qq = f'SELECT ROW_NUMBER() OVER (ORDER BY (SELECT "1")) AS RowID, cohort FROM cohorts where RowID in {nrows}'
            await cursor.execute(qq)
            rowsd = (await cursor.fetchall())
            for rowd in rowsd:
                cohorts[cohort].add(rowd[1])
    q = f'select cohort, count(distinct(sample)) from cohorts group by cohort'
    await cursor.execute(q)
    rows = (await cursor.fetchall())
    for row in rows:
        cohort_sample[row[0]] = row[1]
    responses = {}
    for cohort in cohorts:
        respd = {}
        responses[cohort] = []
        for c in cohorts[cohort]:
            respd[c] = []
            genesampleperc = {}
            for hugo in extracted_hugos:
                q = f'select count(DISTINCT(variant.base__uid)), cohort from variant, variant_filtered, sample, cohorts where variant_filtered.base__uid = variant.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{c}" and variant.base__hugo ="' + hugo + '"'
                counts = {}
                await cursor.execute(q)
                rows = await cursor.fetchall()
                if rows:
                    for row in rows:
                        counts[hugo] = row[0]
                    sorted_hugos = sorted(counts, key=counts.get, reverse=True)
                    for hugo in sorted_hugos:
                        respd[c].append([hugo, counts[hugo]])
        responses[cohort].append(respd)

    response = {"data": responses}
    await cursor.close()
    await conn.close()
    return response