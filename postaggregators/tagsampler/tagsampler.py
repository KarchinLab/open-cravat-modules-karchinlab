import sys
import os
from cravat import BasePostAggregator
from cravat import InvalidData
import sqlite3

class CravatPostAggregator (BasePostAggregator):

    def check(self):
        return True

    def setup (self):
        q = 'select distinct(base__sample_id) from sample'
        self.cursor.execute(q)
        sample_is_all_null = True
        for r in self.cursor:
            if r[0] is not None:
                sample_is_all_null = False
                break
        if sample_is_all_null == False:
            q = 'update sample set base__sample_id="no-sample" where base__sample_id is null'
            self.cursor.execute(q)
            self.dbconn.commit()
        self.cursor.execute('pragma synchronous=0;')
        self.cursor.execute('pragma journal_mode=WAL;')
    
    def cleanup (self):
        return
        self.cursor.execute('pragma synchronous=2;')
        self.cursor.execute('pragma journal_mode=delete;')
        
    def annotate (self, input_data):
        uid = str(input_data['base__uid'])
        q = 'select base__sample_id from sample where base__uid=' + uid + ' and base__sample_id is not null'
        self.cursor.execute(q)
        samples = {}
        for row in self.cursor:
            samples[row[0]] = True
        numsample = len(samples)
        samples = list(samples.keys())
        samples = ';'.join(samples)
        q = 'select base__tags from mapping where base__uid=' + uid
        self.cursor.execute(q)
        tags = {}
        for row in self.cursor:
            if row[0] is not None:
                tags[row[0]] = True
        tags = list(tags.keys())
        tags.sort()
        tags = ';'.join(list(tags))
        out = {'numsample': numsample, 'samples': samples, 'tags': tags}
        return out

if __name__ == '__main__':
    summarizer = CravatPostAggregator(sys.argv)
    summarizer.run()
