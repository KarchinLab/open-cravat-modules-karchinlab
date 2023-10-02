import aiosqlite
import os
import math

async def get_data_for_sos (sos, name_prefix, cursor, use_filtered):
    hg38_chroms = [
        '1', '2', '3', '4', '5', '6', '7', 
        '8', '9', '10', '11', '12', '13', '14', 
        '15', '16', '17', '18', '19', '20', '21', 
        '22', 'X', 'Y'
    ]
    hg38_sizes = [
        248956422,
        242193529,
        198295559,
        190214555,
        181538259,
        170805979,
        159345973,
        145138636,
        138394717,
        133797422,
        135086622,
        133275309,
        114364328,
        107043718,
        101991189,
        90338345,
        83257441,
        80373285,
        56617616,
        64444167,
        46709983,
        50818468,
        156040895,
        57227415
    ]
    bin_size = 5000000
    count_data = {}
    for i in range(len(hg38_chroms)):
        chrom = hg38_chroms[i]
        size = hg38_sizes[i]
        bins = []
        no_bins = math.floor(size / bin_size) + 1
        for binno in range(no_bins):
            bins.append({'genes': [], 'count': 0})
        count_data[chrom] = bins
    if use_filtered:
        from_str = ' from variant, variant_filtered '
        where = 'where variant.base__uid=variant_filtered.base__uid and ('
    else:
        from_str = ' from variant '
        where = ' where ('
    query = 'select base__chrom, base__pos, base__so, base__hugo '
    where += 'base__so="' + sos[0] + '" '
    for so in sos[1:]:
        where += 'or base__so="' + so + '" '
    where += ')'
    query += from_str + where
    await cursor.execute(query)
    for r in await cursor.fetchall():
        (chrom, pos, so, hugo) = r
        chrom = chrom.replace('chr', '')
        if chrom not in hg38_chroms:
            continue
        binno = math.floor(pos / bin_size)
        hugos = count_data[chrom][binno]['genes']
        if hugo not in hugos:
            count_data[chrom][binno]['genes'].append(hugo)
        count_data[chrom][binno]['count'] += 1
    data = []
    for chrom in count_data:
        bins = count_data[chrom]
        chromsize = hg38_sizes[hg38_chroms.index(chrom)] - 1000000
        for binno in range(len(bins)):
            bin = bins[binno]
            start = binno * bin_size + 1
            end = (binno + 1) * bin_size
            if end >= chromsize:
                end = chromsize - 1
            hugos = bin['genes']
            name = name_prefix + '@@@' + ' '.join(hugos)
            value = bin['count']
            if value == 0:
                continue
            row = {'block_id': chrom, 
                   'start': str(start), 
                   'end': str(end), 
                   'name': name, 
                   'value': str(value)}
            data.append(row)
    return data

async def get_data (queries):
    response = {}
    use_filtered = eval(queries['use_filtered'])
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()
    data = {}
    sos = ['MIS', 'CSS', 'IIV', 'IDV', 'STL', 'SPL', 'STG', 'FSI', 'FI1', 'FI2', 'FSD', 'FD1', 'FD2']
    prefix = 'Non-silent'
    data_sos = await get_data_for_sos(sos, prefix, cursor, use_filtered)
    '''
    if len(data_sos) == 1:
        data_sos.append({'chr': '22', 'start': '1000000', 'end': '1000001', 'name': '', 'value': '0'})
    '''
    data[prefix] = data_sos
    sos = ['MIS']
    prefix = 'Missense'
    data_sos = await get_data_for_sos(sos, prefix, cursor, use_filtered)
    '''
    if len(data_sos) == 1:
        data_sos.append({'chr': '22', 'start': '1000000', 'end': '1000001', 'name': '', 'value': '0'})
    '''
    data[prefix] = data_sos
    sos = ['FSI', 'FI1', 'FI2', 'FSD', 'FD1', 'FD2', 'STG', 'STL', 'SPL']
    prefix = 'Inactivating'
    data_sos = await get_data_for_sos(sos, prefix, cursor, use_filtered)
    '''
    if len(data_sos) == 1:
        data_sos.append({'chr': '22', 'start': '1000000', 'end': '1000001', 'name': '', 'value': '0'})
    '''
    data[prefix] = data_sos
    response['data'] = data
    await cursor.close()
    await conn.close()
    return response
