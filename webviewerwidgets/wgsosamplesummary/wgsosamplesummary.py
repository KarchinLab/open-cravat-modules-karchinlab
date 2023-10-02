import aiosqlite
import os
import json

async def get_data (queries):
    '''
    so_dic = {
        None: 'Intergenic',
        '':'Intergenic',
        'MIS':'Missense',
        'SYN':'Synonymous',
        'FSI':'Frameshift insertion',
        'FI1':'Frameshift insertion',
        'FI2':'Frameshift insertion',
        'FSD':'Frameshift deletion',
        'FD1':'Frameshift deletion',
        'FD2':'Frameshift deletion',
        'INI':'Inframe insertion',
        'IIV':'Inframe insertion',
        'IND':'Inframe deletion',
        'IDV':'Inframe deletion',
        'CSS':'Complex substitution',
        'STG':'Stopgain',
        'STL':'Stoploss',
        'SPL':'Splice site',
        '2KU':'2k upstream',
        '2KD':'2k downstream',
        'UT3':'3\' UTR',
        'UT5':'5\' UTR',
        'INT':'Intron',
        'UNK':'Unknown',
        'missense':'Missense',
        'synonymous':'Synonymous',
        'frameshift insertion':'Frameshift insertion',
        'frameshift insertion by 1':'Frameshift insertion',
        'frameshift insertion by 2':'Frameshift insertion',
        'frameshift deletion':'Frameshift deletion',
        'frameshift deletion by 1':'Frameshift deletion',
        'frameshift deletion by 2':'Frameshift deletion',
        'inframe insertion':'Inframe insertion',
        'inframe deletion':'Inframe deletion',
        'complex substitution':'Complex substitution',
        'stop gained':'Stopgain',
        'stop lost':'Stoploss',
        'splice site':'Splice site',
        '2kb upstream':'2k upstream',
        '2kb downstream':'2k downstream',
        '3-prime utr':'3\' UTR',
        '5-prime utr':'5\' UTR',
        'intron':'Intron',
        'unknown':'Unknown'
    }
    '''
    use_filtered = eval(queries['use_filtered'])
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    q = 'select distinct base__sample_id from sample where base__sample_id is not null'
    await cursor.execute(q)
    samples = [v[0] for v in await cursor.fetchall() if v[0]]
    if len(samples) == 1:
        response = {'data': None}
        await cursor.close()
        await conn.close()
        return response
    samples.sort()
    q = 'select subdict from variant_reportsub where module="base"'
    await cursor.execute(q)
    r = await cursor.fetchone()
    so_dic = json.loads(r[0])['so']
    so_dic[None] = 'Intergenic'
    so_dic[''] = 'Intergenic'
    if use_filtered:
        from_str = ' from variant, variant_filtered '
        where = 'where variant.base__uid=variant_filtered.base__uid'
    else:
        from_str = 'from variant '
        where = ''
    query = 'select distinct variant.base__so '
    query += from_str + where
    await cursor.execute(query)
    sos = [so_dic[v[0]] for v in await cursor.fetchall()]
    sos.sort()
    
    sosample = {}
    for so in sos:
        sosample[so] = []
        for sample in samples:
            sosample[so].append(0)
    
    for i in range(len(samples)):
        sample = samples[i]
        query = 'select variant.base__so, count(*)'
        if use_filtered:
            from_str = ' from variant, variant_filtered, sample '
            where = 'where variant.base__uid=variant_filtered.base__uid and '
        else:
            from_str = 'from variant, sample '
            where = 'where '
        where += 'sample.base__uid=variant.base__uid and sample.base__sample_id="' + sample + '" group by variant.base__so order by variant.base__so'
        query += from_str + where
        await cursor.execute(query)
        for row in await cursor.fetchall():
            (so, count) = row
            so = so_dic[so]
            sosample[so][i] = count

    data = {}
    for so in sos:
        row = []
        for i in range(len(samples)):
            row.append(sosample[so][i])
        data[so] = row
    
    response = {'data': {'samples': samples, 'sos': sos, 'socountdata': data}}

    await cursor.close()
    await conn.close()
    return response
