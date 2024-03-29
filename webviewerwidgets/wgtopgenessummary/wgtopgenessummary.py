import aiosqlite
import os

async def get_data (queries):
    # hugo - aalen
    use_filtered = eval(queries['use_filtered'])
    dbpath = os.path.join(os.path.dirname(__file__), 
                          'data',
                          'wgtopgenessummary.sqlite')
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()
    # q = 'select hugo, aalen from genelen'
    # await cursor.execute(q)
    # genelen = {}
    # for row in await cursor.fetchall():
    #     genelen[row[0]] = row[1]
    await cursor.close()
    await conn.close()
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    # 1 sample?
    q = 'select count(distinct(base__sample_id)) from sample'
    await cursor.execute(q)
    #num_total_sample = len(await cursor.fetchall())
    num_total_sample = (await cursor.fetchone())[0]
    if num_total_sample == 1:
        response = {'data': None}
        await cursor.close()
        await conn.close()
        return response

    gene_var_perc = {}
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
        count = row[1]
        # if hugo in genelen:
        gene_var_perc[hugo] = count
    num_gene_to_extract = 10
    sorted_hugos = sorted(gene_var_perc, key=gene_var_perc.get, reverse=True)
    extracted_hugos = sorted_hugos[:num_gene_to_extract]

    genesampleperc = {}
    for hugo in extracted_hugos:
        query = 'select count(distinct(sample.base__sample_id))'
        if use_filtered:
            from_str = ' from sample, variant, variant_filtered '
            where = 'where variant.base__uid=variant_filtered.base__uid and '
        else:
            from_str = ' from sample, variant '
            where = 'where '
        where += 'sample.base__uid=variant.base__uid and variant.base__hugo="' + hugo + '"'
        query += from_str + where
        # q = 'select count(distinct(sample.base__sample_id)) from sample, variant, variant_filtered where variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and variant.base__hugo="' + hugo + '"'
        await cursor.execute(query)
        num_sample = (await cursor.fetchone())[0]
        if num_sample == 0:
            continue
        genesampleperc[hugo] = num_sample
    sorted_hugos = sorted(genesampleperc, key=genesampleperc.get, reverse=True)
    response = {'data': []}
    for hugo in sorted_hugos:
        response['data'].append([hugo, genesampleperc[hugo]])
    await cursor.close()
    await conn.close()
    return response
