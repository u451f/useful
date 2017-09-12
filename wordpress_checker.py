#!/usr/bin/env python 
# -*- coding: latin-1 -*-

import subprocess 
import os
import filecmp
import sys
import argparse

from ngmod.wordpress import Wordpress
import contextlib
@contextlib.contextmanager

def cd(path):
   old_path = os.getcwd()
   os.chdir(path)
   try:
       yield
   finally:
       os.chdir(old_path)
"""
 zum Language Check:
 bei veränderte Dateien zusätzlich in diff files
 /var/www/dl0te.de/docs/wp-config-sample.php  lang = en
 /var/www/dl0te.de/docs/wp-includes/version.php lang = de
"""
def downloadUrl(wp): 
    if lang == "en" or lang == 0:
        return "https://wordpress.org/wordpress-%s.tar.gz"%(wp.version())
    else:
        return "https://%s.wordpress.org/wordpress-%s-%s.tar.gz"%(lang, wp.version(),lang + "_" + lang.upper())
Wordpress.downloadUrl = downloadUrl

def wp_downloader():
    print "Der Download von %s wird gestartet"%(wp.downloadUrl())
    subprocess.call(["wget", "-O", "/tmp/wp.tar.gz", wp.downloadUrl()])
    with cd("/tmp"):
        subprocess.call(["tar", "-xaf", "/tmp/wp.tar.gz"])
 
def ignore():
        #.ignore list erweitern
        global ignoredFolders
        ignoredFolders = [
                        "uploads", 
                  #      "plugins",
                        "themes",
                        "languages"]
        diffObj.ignore.extend(os.path.join(path, i) for i in ignoredFolders)

def addDiff(diff, diffObj, path):
        diff.diff_files.extend([os.path.join(path, i) for i in diffObj.diff_files])
        diff.right_only.extend([os.path.join(path, i) for i in diffObj.right_only])
        for sub in diffObj.subdirs:
            if sub in ignoredFolders and path.endswith("wp-content"):
                continue    
            addDiff(diff,diffObj.subdirs[sub], os.path.join(path,sub))
               
def printmime():
        global count_right_only
        count_right_only = 0
        for i in diff.right_only:
                if not os.path.isdir(i):
                    mime_type = subprocess.check_output(['file', '-ib', i]).strip()
                    count_right_only += 1
                    print str(count_right_only) + ") ", i, mime_type

def inspector(pattern):
    #Durchsucht alle Dateien in diff_files und right_only nach pattern
    patterns = ["--->TestPattern: Sollte Nicht Gefunden werden<---",
            # "php",
            # "evil string here",
            ]
    if pattern:
        for i in pattern:
            for j in i:
                patterns.append(j)
    for i in patterns:
        countDiff = 0
        countRightOnly  = 0
        print "\nSuche nach Pattern %s"%(i)
        for j in diff.diff_files:
            if os.path.isfile(j):
                filetext = open(j, 'r').read()
                if i in filetext:
                    if countDiff == 0:
                        print "%s in veränderten Dateien gefunden:"%(i)
                    countDiff += 1
                    if not summary:
                        print j
        print 
        for k in diff.right_only:
            if os.path.isfile(k):
                filetext = open(j, 'r').read()
                if i in filetext:
                    if countRightOnly == 0:
                        print "%s in neu erstellten Dateien gefunden:"%(i)           
                    countRightOnly += 1
                    if not summary:
                        print k
        print
        if countDiff == 0 and countRightOnly == 0:
            print "%s nicht gefunden"%(i)
        else:
            print "Pattern %s wurde in %s veränderten Dateien gefunden."%(i, countDiff)
            print "Pattern %s wurde in %s neu erstellten Dateien gefunden."%(i, countRightOnly)

class Diff:
        diff_files=[]
        right_only=[]
        subdirs=[]
        pass
diff = Diff()

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', help = 'Domain des zu untersuchenenden Wordpress')
parser.add_argument('-l', '--lang', default = 0, help = 'Sprache des Wordpress: de, en, ...')
parser.add_argument('--pattern', action = 'append', nargs='*', help = 'Dateien nach Pattern durchsuchen')
parser.add_argument('-s', '--summary', action = 'store_true', help = 'zeigt eine Übersicht an')
parser.add_argument('-p', '--path' , help = 'Pfad des zu untersuchenenden Wordpress.')
parser.add_argument('-o', '--offline', action = 'store_true', help = 'WP wird nicht heruntergeladen. Erwartet WP in /tmp/wordpress')
args = parser.parse_args()
if not (args.domain or args.path):
    parser.error("Gebe als Option --domain oder --path an.")

domain = args.domain
lang = args.lang
pattern = args.pattern
summary = args.summary
if args.path:
    path = args.path
else:
    path = os.path.join("/var/www", domain, "docs")

wp = Wordpress(path)

##In Domain eingetragenes Wordpress downloaden und entpacken:
if not args.offline:
    wp_downloader()

diffObj = filecmp.dircmp("/tmp/wordpress", path)
ignore()
addDiff(diff,diffObj,path)
diff.diff_files.sort()
diff.right_only.sort()
count_diff_files = len(diff.diff_files)
count_right_only = len(diff.right_only)

if __name__ == "__main__":
    print "Dieses wordpress wird gecheckt:\n" + str(wp)
    if lang:
        print "Sprache: " + lang + "\n"
    else:
        print "Sprache: en (default)\n"
    if summary:
        print "Anzahl unterschiedlicher Dateien:\t%s"%(count_diff_files) 
        print "Anzahl neu erstellter Dateien:\t\t%s"%(count_right_only)
        inspector(pattern)
    else:
        print "Alle Dateien mit unterschiedlichem Inhalt:"
        for i in xrange(0,count_diff_files):
            print str(i + 1) + ") ", (diff.diff_files[i])
        print "\nAlle neu erstellten Dateien und Ordner:"
        printmime()                    
        print "\nAnzahl unterschiedlicher Dateien:\t%s"%(count_diff_files)
        print "Anzahl neu erstellter Dateien:\t\t%s"%(count_right_only)
        inspector(pattern)
        
        #sys.exit("STOP")

