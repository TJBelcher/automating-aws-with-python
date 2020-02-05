#!/bin/sh
pycodestyle webotron/ > pyout.txt
pydocstyle webotron/ >> pyout.txt
pylint webotron/ >> pyout.txt
pyflakes webotron/ >> pyout.txt
