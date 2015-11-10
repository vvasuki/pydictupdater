# import urllib2
import os
from urllib2 import urlopen, URLError, HTTPError
import tarfile

indexlistBase = "https://raw.githubusercontent.com/sanskrit-coders/"
listOfIndexes = [
    "stardict-sanskrit/master/sa-head/tars/tars.MD",
    "stardict-sanskrit/master/en-head/tars/tars.MD",
    # "stardict-kannada/master/en-head/tars/tars.MD",
    # "stardict-kannada/master/kn-head/tars/tars.MD",
    "stardict-pali/master/en-head/tars/tars.MD",
    "stardict-hindi/master/dev-head/tars/tars.MD",
]


# create the directory if it does not exist already
def createDirectory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


# download the url into dir
# if dir does not exist create it
def dlfile(url, dir, forcedownload=True):
    createDirectory(dir)
    # Open the url
    try:
        f = urlopen(url)
        localpath = dir + "/" + os.path.basename(url)
        # Open our local file for writing
        if not forcedownload:
            if os.path.isfile(localpath):  # check if this file exists
                print "skipped %s as it already exists" % localpath
                return
        with open(localpath, "wb") as local_file:
            local_file.write(f.read())

    # handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


# Use the listOfIndexes to
# a. download each index into tmpDirectory
# b. extract each dictionary (i.e. .tar.gz file into downloadDir)
# If tmpDirectory or downloadDir are not already existing,
# they get created

def downloadDictionaries(base, listOfIndexes, tmpDirectory, downloadDir,
                         maxcount=1, forcedownload=True):
    count = 0
    for indexUrl in listOfIndexes:
        fullIndexPath = base + indexUrl
        # download this index
        print "============================================"
        print "Processing index %s" % fullIndexPath
        response = urlopen(fullIndexPath)
        for line in response:
            line = line.rstrip()
            linelen = len(line)
            dictURL = line[1:linelen-1]
            # dictURL is a URl to a .tar.gz file
            # this needs to be extracted in a subdirectory of downloadsDir
            dictfilename = os.path.basename(dictURL)
            print "downloading file=%s, to dir=%s" % (
                dictfilename,
                tmpDirectory)

            dlfile(dictURL, tmpDirectory, forcedownload)
            assert(dictfilename[-7:] == ".tar.gz")
            t = tarfile.open(tmpDirectory + "/" + dictfilename, 'r')
            thedictfilenamelen = len(dictfilename)
            subDirnameToExtract = dictfilename[:thedictfilenamelen - 7]
            fullpathofsubdir = downloadDir + subDirnameToExtract
            print "extract to %s" % fullpathofsubdir
            t.extractall(fullpathofsubdir)
            count += 1
            if count == -1:
                continue  # no limit to download
            if count == maxcount:
                return
        print "============================================"


if __name__ == '__main__':
    onCompu = True
    tmpDir = "/sdcard/Download/dicttars"
    dictDir = "/sdcard/dictdata/"
    if onCompu:
        tmpDir = "." + tmpDir
        dictDir = "." + dictDir
    downloadDictionaries(indexlistBase, listOfIndexes,
                         tmpDir, dictDir, maxcount=-1, forcedownload=False)
