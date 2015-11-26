#!/bin/sh

# modify needed language code
# weblate discovers files which have been added to Git automatically
# Just create them and then add them.
lang="ar"
WEBLATE_DIR="/var/www/weblate"
WEBLATE_VCS_DIR="$WEBLATE_DIR/data/vcs/project/index"

cd $WEBLATE_VCS_DIR

# copy pot files
ret=0
FILES=`find . -type f -iname '*.pot'`
for file in $FILES ; do
    dir=$(dirname -- "$file")
    case $dir in
      (*[!/]*) dir=$dir/ # handle / and //
    esac
    base=$(basename -- "$file")
    name=${base%.*}
    name=${name:-$base} # don't consider .bashrc the extension in /foo/.bashrc
    ext=${base#"$name"}
    newfile=$dir${name}.$lang.po
    echo $newfile || ret=$?
    msginit -l $lang --no-translator -i $file  -o $newfile || ret=$?
done

# setup language
cd $WEBLATE_DIR
./manage.py setuplang $lang

exit "$ret"
