import aiosqlite
import os
import json
from collections import OrderedDict

async def get_data (queries):
    dbpath = queries['dbpath']
    use_filtered = eval(queries['use_filtered'])
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()
    hugos = []
    query = 'select variant.base__hugo, count(*)'
    if use_filtered:
        from_str = ' from variant, variant_filtered '
        where = 'where variant.base__uid=variant_filtered.base__uid and '
    else:
        from_str = ' from variant '
        where = 'where '
    where += 'variant.base__coding=="Y" and variant.base__hugo is not null group by variant.base__hugo'
    query += from_str + where
    await cursor.execute(query)
    for row in await cursor.fetchall():
        hugo = row[0]
        if hugo == '':
            continue
        hugos.append(hugo)
    genesample = {}
    totalsamples = set()
    for hugo in hugos:
        num_sample = set()
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
                    num_sample.add(s)
                    samples = list(num_sample)
                    totalsamples.add(s)
            if len(samples) < 3:
                continue
            genesample[hugo] =  samples
    genepairs = {}
    genes = {}
    num_sample = {}
    totalsamplelen = len(list(totalsamples))
    for i in range(len(genesample.keys())):
        percentages = {}
        numbersamples = {}
        for j in range(len(genesample.keys())):
            first_gene= list(genesample.keys())[i]
            first_sample = genesample[first_gene]
            first_set = set(first_sample)
            second_gene = list(genesample.keys())[j]
            second_sample = genesample[second_gene]
            second_set = set(second_sample)
            missing_samples = first_set.intersection(second_set)
            lengths = len(list(missing_samples))
            pair = first_gene + ';' + second_gene
            perc = round(lengths/totalsamplelen, 3)
            if first_gene == second_gene:
                perc = 0
                lengths = 0
            genepairs[pair] = perc
            percentages[second_gene] = perc
            numbersamples[second_gene] = lengths
            genes[first_gene] = percentages
            num_sample[first_gene] = numbersamples
    hugos = {}
    for key, value in genepairs.items():
        h = key.strip().split(';')
        hugo = h[0]
        if hugo in hugos:
            hugos[hugo].append(value)
        else:
            hugos[hugo] = [value]

    topgenes = {}
    for k, v in hugos.items():
        sums = sum(v)
        topgenes[k] = sums
    
    num_gene_to_extract = 10
    sorted_hugos = sorted(topgenes, key=topgenes.get, reverse=True)
    extracted_hugos = sorted_hugos[:num_gene_to_extract]

    final = {}
    for hugo in extracted_hugos:
        match = {}
        values = genes[hugo]
        numsam = num_sample[hugo]
        for h in extracted_hugos:
            try:
                results = values[h]
                samples = numsam[h]
            except:
                continue
            match[h] = [results, samples]
        final[hugo] = match
    response = {'data': []}
    for key, value in final.items():
        response['data'].append([key, list(value.values())])
    await cursor.close()
    await conn.close()
    return response

