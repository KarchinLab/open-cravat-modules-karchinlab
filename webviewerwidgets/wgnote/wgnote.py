import aiosqlite

async def get_data (queries):
    ret = {}
    try:
        dbpath = queries['dbpath']
        tab = queries['tab']
        rowkey = queries['rowkey']
        note = queries['note']
        if len(note) == 0:
            note = None
        conn = await aiosqlite.connect(dbpath)
        c = await conn.cursor()
        if tab == 'variant':
            q = f'update {tab} set base__note_variant=? where base__uid=?'
            await c.execute(q, (note, rowkey))
        elif tab == 'gene':
            q = f'update {tab} set base__note_gene=? where base__hugo=?'
            await c.execute(q, (note, rowkey))
        await conn.commit()
        ret['status'] = 'success'
    except:
        import traceback
        traceback.print_exc()
        ret['status'] = 'fail'
    await c.close()
    await conn.close()
    return ret
