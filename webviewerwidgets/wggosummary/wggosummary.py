import aiosqlite
import os
import cravat.admin_util as au

info = au.get_local_module_info('go')
path = info.directory

async def get_data (queries):
    use_filtered = eval(queries['use_filtered'])
    response = {}
    dbpath = queries['dbpath']
    if 'numgo' in queries:
        num_go = queries['numgo']
    else:
        num_go = 10

    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    hugos = []
    query = 'select distinct base__hugo'
    if use_filtered:
        table = "gene_filtered"
    else:
        table = "gene"
    query = 'select distinct base__hugo from ' + table
    await cursor.execute(query)
    hugos = [v[0] for v in await cursor.fetchall() if len(v[0].strip()) > 0]
    await cursor.execute(query)
    await cursor.close()
    await conn.close()
    if hugos == []:
        return response

    conn = await aiosqlite.connect(os.path.join(path, 
                                        'data', 
                                        'go.sqlite'))
    cursor = await conn.cursor()

    go = {}
    for hugo in hugos:
        query = 'select go_id from go_annotation where hugo="' + hugo +\
            '" and go_aspect in ("F", "mfo")'
        await cursor.execute(query)
        for row in await cursor.fetchall():
            go_id = row[0]
            if go_id in go:
                go[go_id]['geneCount'] += 1
            else:
                go[go_id] = {'go': go_id, 'geneCount': 1}

    # Creates a list of keys.
    go_ids = [*go]

    sorted_go_ids = sorted(go_ids, key=lambda k: go[k]['geneCount'], reverse=True)

    data = []
    # Adds total genes.
    #ret.append({'go': 'Total genes', 
    #            'geneCount': len(hugos), 
    #            'description': 'Total genes'})
    for go_num in range(min(num_go, len(sorted_go_ids))):
        go_id = sorted_go_ids[go_num]
        query = 'select name from go_name where go_id="' + go_id + '"'
        await cursor.execute(query)
        for row in await cursor.fetchone():
            go_desc = row
        go[go_id]['description'] = go_desc
        data.append(go[go_id])

    
    # Remove protein_binding from the names, it crowds out all the others
    rm_index = -1
    ident_idx = -1
    for i,v in enumerate(data):
        if v['description'] == 'protein binding':
            rm_index = i
            break
        
    if rm_index != -1:
        data = data[:rm_index]+data[rm_index+1:]

    response['data'] = data

    await cursor.close()
    await conn.close()
    return response
