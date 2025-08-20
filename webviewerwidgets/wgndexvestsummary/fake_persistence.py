__author__ = 'dexter'

from os import listdir, makedirs
from os.path import isfile, isdir, join, abspath, dirname, exists, basename, splitext
import csv
import json
from os import remove
import os
import sys

# e_data persistence
# This persistence system uses a local directory
# has a structure of:
#
# e_sets
#       /e_set_name
#                  /id_set_name.json
#

def e_set_dir_name(e_set_name):
    current_directory = dirname(abspath(__file__))
    return join(current_directory, "data", e_set_name)

def e_data_dir_name():
    current_directory = dirname(abspath(__file__))
    return join(current_directory, "data")

def e_set_exists(e_set_name):
    return isdir(e_set_dir_path(e_set_name))

def e_set_dir_path(e_set_name):
    return join(e_data_dir_name(), e_set_name)

def get_e_set_names():
    return listdir(e_data_dir_name())

def get_id_set_file_names(e_set_name):
    path = e_set_dir_name(e_set_name)
    return listdir(path)

def ensure_e_set_dir(e_set_name):
    path = e_set_dir_path(e_set_name)
    if not e_set_exists(e_set_name):
        makedirs(path)
    return path

def save_id_set(e_set_name, id_set):
    e_set_dir = ensure_e_set_dir(e_set_name)
    filename = join(e_set_dir, id_set.name + ".json")
    file = open(filename, "w")
    json.dump(id_set.to_dict(), file)
    file.close()

def save_e_set(e_set, e_set_name):
    for id_set_name, id_set in e_set.id_set_map:
        save_id_set(e_set_name, id_set)

def remove_id_set(e_set_name, id_set_name):
    e_set_dir = e_set_dir_name(e_set_name)
    filename = join(e_set_dir, id_set_name + ".json")
    remove(filename)

def remove_all_id_sets(e_set_name):
    dirpath = e_set_dir_name(e_set_name)
    for filename in listdir(dirpath):
        path = join(dirpath, filename)
        remove(path)

def get_id_set_data(e_set_name, id_set_file_name):
    base = basename(id_set_file_name)
    name = splitext(base)[0]
    e_set_dir = e_set_dir_name(e_set_name)
    filename = join(e_set_dir, name + ".json")
    if(isfile(filename)):
        file = open(filename, "r")
        data = json.load(file)
        file.close()
        return data
    else:
        return None

def save_id_set_dict(e_set_name, id_set_id, id_set_dict, alt_grp_path=None):
    e_set_dir = ensure_e_set_dir(e_set_name)
    filename = join(e_set_dir, id_set_id + ".json")
    file = open(filename, "w")
    json.dump(id_set_dict, file)
    file.close()

    #===========================
    # Save GSEA file
    #===========================
    '''
    gseafilename = ''
    if alt_grp_path is not None:
        if not os.path.exists(alt_grp_path):
            os.makedirs(alt_grp_path)
        gseafilename = join(alt_grp_path, id_set_dict.get("name") + ".grp")
    else:
        if not os.path.exists(join(e_set_dir + '..','grp')):
            os.makedirs(join(e_set_dir + '..','grp'))
        gseafilename = join(e_set_dir + '..','grp', id_set_dict.get('name') + '.grp')
    gseafile = open(gseafilename, "w")
    if id_set_dict.get("ids") is not None:
        for gene in id_set_dict.get("ids"):
            gseafile.write(gene + "\n")

    gseafile.close()
    '''

def get_e_set_configs(name="config"):
    current_directory = dirname(abspath(__file__))
    filename = join(current_directory, "e_service_configuration", name + ".json")
    file = open(filename, "r")
    data = json.load(file)
    file.close()
    return data


# gene_report persistence

def gene_report_file_path(name):
    gene_report_dir = ensure_gene_report_dir()
    return join(gene_report_dir, name + ".txt")

def ensure_gene_report_dir():
    current_directory = dirname(abspath(__file__))
    path = join(current_directory, "gene_reports")
    if not isdir(path):
        makedirs(path)
    return path

def gene_list_file_path(name):
    gene_list_dir = ensure_gene_list_dir()
    return join(gene_list_dir, name + ".txt")

def ensure_gene_list_dir():
    current_directory = dirname(abspath(__file__))
    path = join(current_directory, "gene_lists")
    if not isdir(path):
        makedirs(path)
    return path

def save_gene_report(report, mode):
    if mode is 'tabular':
        path = gene_report_file_path(report.name)
        with open(path, 'w') as csvfile:
            fieldnames = report.fields
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore', dialect='excel-tab')
            writer.writeheader()
            for row in report.get_rows():
                writer.writerow(row)
    if mode is 'json':
        path = gene_list_file_path(report.name)
        with open(path, 'w') as file:
            file.write(json.dumps(report.get_network_summary(), indent=4))




