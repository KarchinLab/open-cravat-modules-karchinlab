import aiosqlite
import os
import json

async def get_data (queries):
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

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


    q = 'select DISTINCT clinvar__sig from variant, variant_filtered where variant_filtered.base__uid = variant.base__uid and clinvar__sig is not null;'
    await cursor.execute(q)
    counts = {}
    perc = {}
    for row in await cursor.fetchall():
        counts[row[0]] = 0
        perc[row[0]] = 0

    #retrieve data within each cohort
    response = {}
    for _set in sets:
        data = {}
        response[_set] = []
        for cohort in sets[_set]:
            data[cohort] = []
            genesampleperc = {}
            genesamplecount = {}
            q = f'select clinvar__sig, count(distinct(sample.base__sample_id)) from  variant, variant_filtered, sample, cohorts where clinvar__sig is not null and variant_filtered.base__uid = variant.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{cohort}"  group by clinvar__sig;'
            for count in counts:
                counts[count] = 0
                perc[count] = 0
            await cursor.execute(q)
            rows = await cursor.fetchall()
            if rows:
                for row in rows:
                    counts[row[0]] = row[1]
                    perc[row[0]] = (row[1] / num_total_samples[cohort]) * 100
                data[cohort] = {'clinvar_percent': dict(sorted(perc.items())), 'clinvar_counts': dict(sorted(counts.items()))}
        response[_set].append(data)
    await cursor.close()
    await conn.close()
    return {"data": {'response': response, "sig": list(counts.keys())}}