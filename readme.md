# DBLP CLI

`dblp.py` is a small command line utitlity that can search and fetch bibtex entries from [dblp.org](https://dblp.org/).

## Installation

Requires `python3` and the python libraries `bibtexparser ` and `requests `, which can be installed using `pip3 install bibtexparser requests`.

## Usage

	./dblp.py search "[SEARCHTERM]"

for example

```
./dblp.py search "detecting unrealizability of distributed fault-tolerant systems"
- "Detecting Unrealizability of Distributed Fault-tolerant Systems." by Bernd Finkbeiner, Leander Tentrup
  journals/corr/FinkbeinerT15
```

The bibtex entry can then be derived using the DBLP key

```
./dblp.py get journals/corr/FinkbeinerT15
@article{journals/corr/FinkbeinerT15,
 author = {Bernd Finkbeiner and
Leander Tentrup},
 bibsource = {dblp computer science bibliography, https://dblp.org},
 biburl = {https://dblp.org/rec/bib/journals/corr/FinkbeinerT15},
 doi = {10.2168/LMCS-11(3:12)2015},
 journal = {Logical Methods in Computer Science},
 number = {3},
 timestamp = {Tue, 14 May 2019 16:31:14 +0200},
 title = {Detecting Unrealizability of Distributed Fault-tolerant Systems},
 volume = {11},
 year = {2015}
}
```
