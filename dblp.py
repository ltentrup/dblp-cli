#!/usr/bin/env python3

""" Fixes some verbose parts in the DBLP bibtex entries. """

__author__ = "Leander Tentrup <tentrup@react.uni-saarland.de>"
__copyright__ = "Copyright 2015, Saarland University"

import argparse
import re
import sys

import bibtexparser
import requests


def main():

    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(help='Available actions')

    # create the parser for the "get" command
    parser_get = subparsers.add_parser('get', help='Get bibtex entry from DBLP key')
    parser_get.add_argument('id', help='DBLP id, e.g., "journals/corr/FinkbeinerT15"')
    parser_get.add_argument('--keep-booktitle', dest='keep_booktitle', action='store_true', help="do not shorten conference names")
    parser_get.add_argument('--raw', dest='raw', action='store_true', help="print raw entry from dblp.org")
    parser_get.set_defaults(func=get)

    # create the parser for the "search" command
    parser_search = subparsers.add_parser('search', help='Search for entries in the DBLP database')
    parser_search.add_argument('keywords', help='Search terms')
    parser_search.set_defaults(func=search)

    args = parser.parse_args()
    if args.func is None:
        parser.print_usage()
    else:
        args.func(args)

def search(args):
    r = requests.get('http://dblp.uni-trier.de/search/publ/api', params={'q': args.keywords, 'h':100, 'format': 'json'})
    json_answer = r.json()

    if int(json_answer['result']['hits']['@total']) == 0:
        print('No results found')
        return

    for hit in json_answer['result']['hits']['hit']:
        info = hit['info']
        authors = info['authors']['author']
        if not isinstance(authors, list):
            authors = [authors]
        print('- "{}" by {}\n  {}'.format(info['title'], ', '.join(authors), info['url'].replace('https://dblp.org/rec/', '')))

def get(args):
    r = requests.get('http://dblp.uni-trier.de/rec/bib2/{}.bib'.format(args.id))
    #print(r.text)

    bib_database = bibtexparser.loads(r.text)
    assert len(bib_database.entries) <= 2
    
    if args.raw:
        print(bibtexparser.dumps(bib_database))
        return
    
    if len(bib_database.entries) == 2:
        inproceedings, proceedings = bib_database.entries
        remove_dblp_cite_prefix(inproceedings)
        if not args.keep_booktitle:
            correct_proceedings_name(inproceedings)
        merge_with_proceedings(inproceedings, proceedings)
        remove_doi_url(inproceedings)
        shorten_lncs(inproceedings)

        bib_database.entries = [inproceedings]

    else:
        article = bib_database.entries[0]
        remove_dblp_cite_prefix(article)
        remove_doi_url(article)

    print(bibtexparser.dumps(bib_database))

def remove_dblp_cite_prefix(entry):
    assert entry['ID'].startswith('DBLP:')
    entry['ID'] = entry['ID'][5:]

def correct_proceedings_name(entry):
    ''' Assumes that the first string written in braces {CONF} is the conference name.
        Modifies the booktitle to "Proceedings of {CONF}".
        Assumes that conference name {CONF} is uppercase. '''
    match = re.findall(r"\{([A-Z]+)\}", entry['booktitle'])
    if len(match) == 0:
        sys.stderr.write('Could not determine short proceedings name\n')
        return
    name = match[0]
    if name == 'IEEE' or name == 'ACM':
        if len(match) > 1:
            name = match[1]
            if name == 'USA':
                sys.stderr.write('Could not determine short proceedings name\n')
                return
        else:
            sys.stderr.write('Could not determine short proceedings name\n')
            return
    entry['booktitle'] = "Proceedings of {{{}}}".format(name)

def merge_with_proceedings(inproceedings, proceedings):
    if 'volume' in proceedings:
        inproceedings['volume'] = proceedings['volume']
    if 'series' in proceedings:
        inproceedings['series'] = proceedings['series']
    if 'publisher' in proceedings:
        inproceedings['publisher'] = proceedings['publisher']

    del inproceedings['crossref']

def remove_doi_url(entry):
    if 'link' in entry and 'doi' in entry['link']:
        del entry['link']
    if 'url' in entry and 'doi' in entry['url']:
        del entry['url']

def remove_month(entry):
    if 'month' in entry:
        del entry['month']

def shorten_lncs(entry):
    if 'series' in entry and entry['series'] == 'Lecture Notes in Computer Science':
        entry['series'] = 'LNCS'

if __name__ == "__main__":
    main()
