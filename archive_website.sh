# https://anarc.at/blog/2018-10-04-archiving-web-sites/
nice wget --mirror --execute robots=off --no-verbose --convert-links --backup-converted --page-requisites --adjust-extension --base=./ --directory-prefix=./ --no-check-certificate --span-hosts --domains=deutscher-pavillon.org https://deutscher-pavillon.org
