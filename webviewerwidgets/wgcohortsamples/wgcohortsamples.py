import aiosqlite
import os
import json
from cravat import admin_util as au
async def get_data (queries):
    dbpath = queries['dbpath'] + ".sqlite"
    samples = queries['samples'].split(";")
    uid = queries['uid']
    if len(samples) > 1:
        request_samples = tuple(samples)
    else:
        request_samples = samples
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

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

    response = {}
    for _set in sets:
        data = {}
        response[_set] = []
        for cohort in sets[_set]:
            z = {'het': [], 'hom': []}
            data[cohort] = []
            genesampleperc = {}
            if len(request_samples) > 1:
                q = f'select sample, tagsampler__samples , vcfinfo__zygosity, base__uid from cohorts, variant where cohort = "{cohort}" and base__uid = "{uid}" and sample in {request_samples}'
            else:
                q = f'select sample, tagsampler__samples , vcfinfo__zygosity, base__uid from cohorts, variant where cohort = "{cohort}" and base__uid = "{uid}" and sample = "{request_samples[0]}"'
            data[cohort] = []
            await cursor.execute(q)
            rows = await cursor.fetchall()
            if rows:
                for row in rows:
                    sample = row[0]
                    allSamples = row[1].split(";")
                    index = allSamples.index(sample)
                    zygosity = row[2].split(';')[index]
                    z[zygosity].append(zygosity)
            for key, value in z.items():
                z[key] = len(value)
            data[cohort].append(z)
        response[_set].append(data)
    await cursor.close()
    await conn.close()
    return {'data': {'counts': response, 'sample_count': num_total_samples}}
