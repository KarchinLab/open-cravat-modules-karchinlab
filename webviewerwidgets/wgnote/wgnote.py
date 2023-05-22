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
        variant_cname = 'base__note_variant'
        gene_cname = 'base__note_gene'
        await c.execute('pragma table_info(variant)')
        variant_cols = [_[1] for _ in await c.fetchall()]
        if variant_cname not in variant_cols:
            variant_cname = 'base__note'
        await c.execute('pragma table_info(gene)')
        gene_cols = [_[1] for _ in await c.fetchall()]
        if gene_cname not in gene_cols:
            gene_cname = 'base__note'        
        if tab == 'variant':
            q = f'update {tab} set {variant_cname}=? where base__uid=?'
            await c.execute(q, (note, rowkey))
        elif tab == 'gene':
            q = f'update {tab} set {gene_cname}=? where base__hugo=?'
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
