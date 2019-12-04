# Script to download AVspeech Dataset

Run this script to download AVspeech dataset
```
bash script.sh <filename>
```

# Install youtube-dl
```
pip install youtube-dl
```

# To download parallel on ada

```
wget https://ftpmirror.gnu.org/parallel/parallel-20191022.tar.bz2
wget https://ftpmirror.gnu.org/parallel/parallel-20191022.tar.bz2.sig
gpg parallel-20191022.tar.bz2.sig
bzip2 -dc parallel-20191022.tar.bz2 | tar xvf -
cd parallel-20191022
./configure --prefix=$HOME && make && make install
```

## To stop parallel command citation issue

Run this command:

```
parallel --bibtex
```
and then type:- `will cite`