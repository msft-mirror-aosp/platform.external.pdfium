#!/usr/bin/python

import urllib2
import os
import sys
from subprocess import call

CHROMIUM_VERSION_TRACKING_URL = "https://omahaproxy.appspot.com/all"
CHROMIUM_BUILD_TYPE = "stable"
CHROMIUM_OS = "android"

CHROMIUM_SOURCE_URL = "https://chromium.googlesource.com/chromium/src/+/refs/tags"
CHROMIUM_DEPS_FILE = "DEPS"

PDFIUM_GIT_REPO = "https://pdfium.googlesource.com/pdfium.git"

MAKE_FILES = ["Android.bp",
              "constants/Android.bp",
              "core/fdrm/Android.bp",
              "core/fpdfapi/cmaps/Android.bp",
              "core/fpdfapi/edit/Android.bp",
              "core/fpdfapi/font/Android.bp",
              "core/fpdfapi/page/Android.bp",
              "core/fpdfapi/parser/Android.bp",
              "core/fpdfapi/render/Android.bp",
              "core/fpdfdoc/Android.bp",
              "core/fpdftext/Android.bp",
              "core/fxcodec/Android.bp",
              "core/fxcrt/Android.bp",
              "core/fxge/Android.bp",
              "fpdfsdk/Android.bp",
              "fpdfsdk/formfiller/Android.bp",
              "fpdfsdk/pwl/Android.bp",
              "fxjs/Android.bp",
              "third_party/Android.bp"]

OWNERS_FILES = ["OWNERS", "docs/OWNERS", "third_party/base/numerics/OWNERS"]

COPY_FILES = [os.path.basename(__file__), ".git", "MODULE_LICENSE_BSD"] + MAKE_FILES
REMOVE_FILES = [os.path.basename(__file__), ".git", ".gitignore"] + OWNERS_FILES

def getStableChromiumVersion():
   """ :return the latest chromium version """

   chromiumVersions = urllib2.urlopen(CHROMIUM_VERSION_TRACKING_URL)

   for chromiumVersionStr in chromiumVersions.read().split("\n"):
       chromiumVersion = chromiumVersionStr.split(",")

       if chromiumVersion[0] == CHROMIUM_OS and chromiumVersion[1] == CHROMIUM_BUILD_TYPE:
           return chromiumVersion[2]

   raise Exception("Could not find latest %s chromium version for %s at %s"
                   % (CHROMIUM_BUILD_TYPE, CHROMIUM_OS, CHROMIUM_VERSION_TRACKING_URL))


def getPdfiumRevision():
    """ :return the pdfium version used by the latest chromium version """

    try:
        deps = urllib2.urlopen("%s/%s/%s" % (CHROMIUM_SOURCE_URL, getStableChromiumVersion(),
                                             CHROMIUM_DEPS_FILE))

        # I seem to not be able to get the raw file, hence grep the html file
        return deps.read().split("pdfium_revision&")[1].split("&#39;")[1]
    except Exception as e:
        raise Exception("Could not extract pdfium revision from %s/%s/%s: %s"
                       % (CHROMIUM_SOURCE_URL, getStableChromiumVersion(), CHROMIUM_DEPS_FILE, e))


def downloadPdfium(newDir, rev):
    """ Download the newest version of pdfium to the new directory

    :param newDir: The new files
    :param rev: The revision to change to
    """

    call(["git", "clone", PDFIUM_GIT_REPO, newDir])
    os.chdir(newDir)
    call(["git", "reset", "--hard", rev])


def removeFiles(newDir):
    """ Remove files that should not be checked in from the original download

    :param newDir: The new files
    """

    for fileName in REMOVE_FILES:
        call(["rm", "-rf", os.path.join(newDir, fileName)])


def copyFiles(currentDir, newDir):
    """ Copy files needed to make pdfium work with android

    :param currentDir: The current files
    :param newDir: The new files
    """

    for fileName in COPY_FILES:
        call(["cp", "-r", os.path.join(currentDir, fileName), os.path.join(newDir, fileName)])


def exchange(currentDir, newDir, oldDir):
    """ Update current to new and save current in old.

    :param currentDir: The current files
    :param newDir: The new files
    :param oldDir: The old files
    """

    call(["mv", currentDir, oldDir])
    call(["mv", newDir, currentDir])


if __name__ == "__main__":
   rev = getPdfiumRevision()
   targetDir = os.path.dirname(os.path.realpath(__file__))
   newDir = targetDir + ".new"
   oldDir = targetDir + ".old"

   try:
       downloadPdfium(newDir, rev)
       removeFiles(newDir)
       copyFiles(targetDir, newDir)
       exchange(targetDir, newDir, oldDir)
       print("Updated pdfium to " + rev + " (Chrome " + getStableChromiumVersion() + "). Old files "
             "are in " + oldDir + ". Please verify if build files need to be updated.")

       sys.exit(0)
   except:
       call(["rm", "-rf", newDir])
       sys.exit(1)

