Some scripts to collect information from twiki.cern.ch

Example (pass a different `--login-url` and topic if not in CMS):
```bash
pipenv run ./cli_tests.py --dumpheaders CMS.SiStripLocalReconstructionPage --rawcache=cache/raw_debug
pipenv run ./cli_tests.py -v --backlinks CMS.SiStripLocalReconstructionPage --backlinkscache=cache/backlinks
```
