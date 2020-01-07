Some scripts to collect information from twiki.cern.ch

Example (pass a different `--login-url` and topic if not in CMS):
```bash
pipenv run ./twiki_cli_tests.py --dumpheaders CMS.SiStripLocalReconstructionPage
```
