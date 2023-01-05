import aiosqlite
import os
import re

async def get_data (queries):
    dbpath = queries['dbpath']
    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    cohorts = {}
    q = "select count(*), sample from cohorts"
    await cursor.execute(q)
    rows = (await cursor.fetchall())
    for row in rows:
        max_rows = row[0]
        sample = row[1]
        q = f'select count(sample) from cohorts where sample = "{sample}"'
        await cursor.execute(q)
        num_cohorts = (await cursor.fetchone())[0]
        for cohort in range(1, num_cohorts + 1):
            cohorts[cohort] = set()
            nrows = tuple([i for i in range(cohort, max_rows + 1, num_cohorts)])
            qq = f'SELECT ROW_NUMBER() OVER (ORDER BY (SELECT "1")) AS RowID, cohort FROM cohorts where RowID in {nrows}'
            await cursor.execute(qq)
            rowsd = (await cursor.fetchall())
            for rowd in rowsd:
                cohorts[cohort].add(rowd[1])

    annotators = []
    q = 'select  colval from info where colkey = "_annotators";'
    await cursor.execute(q)
    vals = (await cursor.fetchone())[0].split(",")
    for v in vals:
        if v == "extra_vcf_info:" or v == "original_input:":
            continue
        else:
            match = re.match(r'(\w+)',v)
            annotators.append(str(match.group(1)))

    responses = {}
    for cohort in cohorts:
        respd = {}
        responses[cohort] = []
        for c in cohorts[cohort]:
            respd[c] = []
            annotation = {}
            for rankscore in annotators:
                try:
                    q = f'select {rankscore + "__rankscore"} from sample, variant, variant_filtered, cohorts where variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{c}" and {rankscore + "__rankscore"} is not NULL GROUP by base__hugo, base__achange;'
                    await cursor.execute(q)
                    rows = (await cursor.fetchall())
                    annotation[rankscore] = []
                except:
                    try:
                        q = f'select {rankscore + "__fathmm_rscore"} from sample, variant, variant_filtered, cohorts where variant.base__uid=variant_filtered.base__uid and sample.base__uid=variant.base__uid and sample.base__sample_id=cohorts.sample and cohorts.cohort = "{c}" and {rankscore + "__fathmm_rscore"} is not NULL GROUP by base__hugo, base__achange;'
                        await cursor.execute(q)
                        rows = (await cursor.fetchall())
                        annotation[rankscore] = []
                    except:
                        continue
                for row in rows:
                    annotation[rankscore].append(row[0])
            respd[c].append(annotation)
        responses[cohort].append(respd)

    await cursor.close()
    await conn.close()
    response = {"data": responses}
    return response