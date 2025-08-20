__author__ = 'dexter'

from operator import itemgetter, attrgetter
from os.path import join, isdir
from os import listdir
import sys
import os
from math import log, exp
from mpmath import loggamma
import importlib.util
script_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('fake_persistence', os.path.join(script_dir, 'fake_persistence.py'))
storage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(storage)

def logchoose(ni, ki):
    try:
        lgn1 = loggamma(ni+1)
        lgk1 = loggamma(ki+1)
        lgnk1 = loggamma(ni-ki+1)
    except ValueError:
        raise ValueError
    return lgn1 - (lgnk1 + lgk1)

def gauss_hypergeom(X, n, m, N):
    r1 = logchoose(m, X)
    try:
        r2 = logchoose(N-m, n-X)
    except ValueError:
        return 0
    r3 = logchoose(N,n)

    return exp(r1 + r2 - r3)

def hypergeo_sf(X, n, m, N):
    s = 0
    for i in range(X, min(m,n)+1):
        s += max(gauss_hypergeom(i, n, m, N), 0.0)
    return min(max(s,0.0), 1)

class Gene():
    def __init__(self, symbol, entrez_gene_id):
        self.symbol = symbol
        self.id = entrez_gene_id


class GeneNodeRelation():
    def __init__(self, symbol, entrez_gene_id, node_id):
        self.symbol = symbol
        self.id = entrez_gene_id
        self.nodes = set([node_id])

    def add_node (self, node_id):
        self.nodes.add(node_id)


class EnrichmentScore():

    def __init__(self, pv, k, overlap, set_name, set_id):
        self.k = k
        self.pv = pv
        self.overlap = overlap
        self.set_name = set_name
        self.set_id = set_id

    def format(self):
        return self.set_id + " " + self.set_name + "  pv: " + str(self.pv) + " k:" + str(self.k)

    def to_dict(self):
        return {
            "k" : self.k,
            "pv" : self.pv,
            "overlap" : self.overlap,
            "set_name" : self.set_name,
            "set_id" : self.set_id}


class IdentifierSet():
    def __init__(self, id_set_dict):
        self.name = id_set_dict.get("name")
        self.network_id = id_set_dict.get("network_id")
        self.set = set(id_set_dict.get("ids"))
        self.ndex = id_set_dict.get("ndex")
        self.e_set = id_set_dict.get("e_set")
        self.n = len(self.set)
        self.gene_set = id_set_dict.get("ids")

    def to_dict(self):
        return {
            "name": self.name,
            "ids":self.gene_set,
            "network_id": self.network_id,
            "ndex": self.ndex,
            "e_set" : self.e_set
        }

    def save(self, alt_grp_path=None):
        storage.save_id_set_dict(self.e_set, self.network_id, self.to_dict(), alt_grp_path)

    # compare this id_set to a query_id_set
    def get_enrichment_score(self, query_id_set_n, M, overlap_n):
     #   overlap = query_id_set.set & self.set
     #   k = len(overlap)
        #pv = hypergeom(M, self.n, query_id_set_n).sf(overlap_n)
        pv = hypergeo_sf(overlap_n + 1, query_id_set_n, self.n, M)
        #sys.stderr.write("m=" +str(M) + " n=" + str(self.n) + " q=" + str(query_id_set_n) + " k=" + str(overlap_n) + " pv=" + str(pv) + '\n')

        return pv # EnrichmentScore(pv, k, overlap, self.name)


class QueryIdentifierSet():
    def __init__(self, id_set_dict):
        self.set = set(id_set_dict.get("ids"))
        self.n = len(self.set)


# An instance of this class holds all the enrichment sets
class EnrichmentData():
    def __init__(self, dir_name):
        self.enrichment_set_map = {}
        self.dir_name = dir_name

    def load(self):
        for f_name in listdir(self.dir_name):
            path = join(self.dir_name, f_name)
            if isdir(path):
                e_set = self.add_e_set(f_name)
                e_set.load()

    def load_one_eset(self, eset_dir_name):
        path = join(self.dir_name, eset_dir_name)
        if isdir(path):
            e_set = self.add_e_set(eset_dir_name)
            e_set.load()

    def get_e_set_names(self):
        return self.enrichment_set_map.keys()

    def get_e_set(self, e_set_name):
        return self.enrichment_set_map.get(e_set_name)

    def get_id_set_names(self, e_set_name, url=None):
        e_set = self.get_e_set(e_set_name)
        if not e_set:
            return {}
        return e_set.get_id_set_names(url)

    def get_id_set(self, e_set_name, id_set_id):
        e_set = self.get_e_set(e_set_name)
        if not e_set:
            return False
        return e_set.get_id_set(id_set_id)

    def add_e_set (self, e_set_name):
        e_set_name = e_set_name.lower()
        e_set = EnrichmentSet(e_set_name)
        self.enrichment_set_map[e_set_name] = e_set
        return e_set

    def add_id_set(self, e_set_name, id_set_name, id_list):
        e_set_name = e_set_name.lower()
        if not e_set_name in self.enrichment_set_map.keys():
            e_set_name = self.add_e_set(e_set_name)
        if not e_set_name:
            return False
        return self.enrichment_set_map[e_set_name].add_id_set(id_set_name, id_list)

    def get_scores(self, e_set_name, query_id_set, verbose=False):
        e_set_name = e_set_name.lower()
        if e_set_name in self.enrichment_set_map.keys():
            e_set = self.enrichment_set_map.get(e_set_name)
            if verbose:
                print ("using e_set " + e_set_name)
            return e_set.get_enrichment_scores(query_id_set, verbose)
        else:
            print("unknown e_set " + e_set_name)

    def get_scores_on_standarized_query_terms(self, e_set_name, standarized_query_terms, verbose=False):
        e_set_name = e_set_name.lower()
        if e_set_name in self.enrichment_set_map.keys():
            e_set = self.enrichment_set_map.get(e_set_name)
            if verbose:
                print("using e_set " + e_set_name)
            return e_set.get_enrichment_scores_on_standardized_terms(standarized_query_terms, verbose)
        else:
            print("unknown e_set " + e_set_name)


class EnrichmentSet():

    def __init__(self, name):
        self.id_set_map = {}
        self.objects = set()
        self.name = name

    def load(self):
        if storage.e_set_exists(self.name):
            for f_name in storage.get_id_set_file_names(self.name):
                id_set_dict = storage.get_id_set_data(self.name, f_name)
                id_set = IdentifierSet(id_set_dict)
                self.add_id_set(id_set)

    def save(self, alt_grp_path=None):
        storage.ensure_e_set_dir(self.name)
        for set_name, id_set in self.id_set_map.iteritems():
            id_set.save(alt_grp_path)

    def get_id_set_names(self, request_url=None):
        urls = []
        for id_set_id in self.id_set_map.keys():
            if request_url:
                urls.append(request_url + "/idsets/" + id_set_id)
            else:
                urls.append(id_set_id)
        return {'id_sets': urls}

    def get_id_set(self, id_set_id):
        return self.id_set_map.get(id_set_id)

    def get_id_set_by_network_id(self, network_id):
        for id_set in self.id_set_map.values():
            if id_set.network_id == network_id:
                return id_set
        return None

    # create a new id_set in this e_set based on
    # a name and a list of id strings
    def add_id_set (self, id_set):
        self.id_set_map[id_set.network_id] = id_set
        self.update()

    def update(self):
        # calculate the set of all objects - across all id_sets in the e_set

        # first clear the set of all objects in the e_set
        self.objects = set()

        # now merge in each id set
        for id_set in self.id_set_map.values():
            self.objects = self.objects | id_set.set

    def get_enrichment_scores(self, query_id_set_raw, verbose=False):
        scores = []

        coverage = Coverage(query_id_set_raw)
        query_id_set = IdentifierSet({"ids": (query_id_set_raw.set & self.objects)})
        M = len(self.objects)
        count = 0
        for set_id, id_set in self.id_set_map.iteritems():
            overlap = query_id_set.set & id_set.set
            k = len(overlap)
            if k > 0 :
                score = id_set.get_enrichment_score(query_id_set.n, M, k)
                coverage.add_score(overlap)
                scores.append( EnrichmentScore( score, k, overlap, id_set.name, set_id).to_dict())
                count += 1

        if verbose:
            print("Processed " + str(count) + " id_sets, M = " + str(M))
        scores = sorted(scores, key=itemgetter('pv'))
        result = {"scores" : scores, "coverage" : coverage.to_dict()}
        
        return result


    def get_enrichment_scores_on_standardized_terms(self, standarized_search_terms, verbose=False):
        scores = []

        matched_genes= standarized_search_terms['matched']
        query_id_set_raw = QueryIdentifierSet({"ids": matched_genes.keys()})

        coverage = Coverage(query_id_set_raw)
        query_id_set = QueryIdentifierSet({"ids": (query_id_set_raw.set & self.objects)})
        M = len(self.objects)
        count = 0;
        for set_id in self.id_set_map:
            id_set = self.id_set_map[set_id]
            overlap = query_id_set.set & id_set.set
            k = len(overlap)
            if k > 0 :
                score = id_set.get_enrichment_score(query_id_set.n, M, k)
                coverage.add_score(overlap)
                overlap_table = {}
                for symbol in overlap:
                    gene_table = id_set.gene_set
                    overlap_table[symbol] = 1
                scores.append( EnrichmentScore( score, k, overlap_table, id_set.name, set_id).to_dict())
                count += 1

        if verbose:
            print("Processed " + str(count) + " id_sets, M = " + str(M))
        scores = sorted(scores, key=itemgetter('pv'))
        result = {"scores" : scores, "coverage" : coverage.to_dict(), "query": standarized_search_terms}
        return result


class Coverage():

    def __init__(self, id_set):
        self.map = {}
        for id in id_set.set:
            self.map[id] = 0

    def add_score(self, overlap):
        for id in overlap:
            if id in self.map.keys():
                self.map[id] += 1

    def get_sorted_ids(self):
        return sorted(self.map.items(), key=itemgetter(1))

    def to_dict(self):
        return self.get_sorted_ids()








