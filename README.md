# CALDERA plugin: Stockpile

A plugin supplying CALDERA with TTPs and adversary profiles.

[Read the full docs](https://github.com/mitre/caldera/wiki/Plugin:-stockpile)
# ATLAS plugin: atlas

### This plugin will help store and create adversarial TTPs defined in [`ATLAS`](https://atlas.mitre.org/) to interfeace with [`CALDERA`](https://github.com/mitre/caldera). It can be used in conjuction with the plugin [`Almanac`](https://gitlab.mitre.org/advml/almanac/-/tree/develop). 

## This is a mirror of the public [`stockpile`](https://github.com/mitre/stockpile/tree/master) repo's `master` branch

For collection and exfiltration abilities added January 2022 (see list below), additional information
for configuring these abilities can be found in the [examples](docs/Exfiltration-How-Tos.md) in the stockpile/docs/ 
folder.

*2022 Included abilities:*
- Advanced File Search and Stager
- Find Git Repositories & Compress Git Repository
- Compress Staged Directory (Password Protected)
- Compress Staged Directory (Password Protected) and Break Into Smaller Files
- Exfil Compressed Archive to FTP
- Exfil Compressed Archive to Dropbox
- Exfil Compressed Archive to GitHub Repositories | Gists
- Exfil Compressed Archive to GitHub Gist
- Exfil Directory Files to Github (this exfiltrates files without archiving)
- Exfil Compressed Archive to S3 via AWS CLI
- Transfer Compressed Archive to Separate S3 Bucket via AWS CLI
- Scheduled Exfiltration