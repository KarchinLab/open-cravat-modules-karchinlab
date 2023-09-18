import aiosqlite
import os
import json

async def get_data (queries):
    use_filtered = eval(queries['use_filtered'])
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    numsamples = {}
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
        gene = row[0]
        varcount = row[1]
        numsamples[gene] = varcount
    sorted_hugos = sorted(numsamples, key=numsamples.get, reverse=True)
    extracted_hugos = sorted_hugos[:10]

    num_sample = {}
    countsofsamples = {}
    for hugo in extracted_hugos:
        samples = {}
        query = 'select variant.tagsampler__samples'
        if use_filtered:
            from_str = ' from variant, variant_filtered '
            where = 'where variant.base__uid=variant_filtered.base__uid and '
        else:
            from_str = ' from variant '
            where = 'where '
        where += 'variant.base__hugo ="' + hugo + '"'
        query += from_str + where
        await cursor.execute(query)
        rows = await cursor.fetchall()
        if rows:
            for row in rows:
                for s in row[0].split(';'):
                    if s in samples:
                        samples[s].append(s)
                    else:
                        samples[s] = [s]
                    if s in countsofsamples:
                        countsofsamples[s].append(s)
                    else:
                        countsofsamples[s] = [s]
        num_sample[hugo] = samples
    samplevarcount = {}
    for k, v in countsofsamples.items():
        samplevarcount[k] = len(v)
    sorted_samples = sorted(samplevarcount, key=samplevarcount.get, reverse=True)
    extracted_samples = sorted_samples[:10]
    
    samplecount = {}
    for k, v in num_sample.items():
        s = {}
        for key, value in v.items():
            s[key] = len(value)
        samplecount[k] = s

    final = {}
    for samp in extracted_samples:
        for hugo in extracted_hugos:
            values = samplecount[hugo]
            try:
                val = [samp, values[samp]]
            except:
                val = [samp, 0]
            if hugo in final:
                    final[hugo].append(val)
            else:
                final[hugo] = [val]
    response = {'data': final}
    await cursor.close()
    await conn.close()
    return response