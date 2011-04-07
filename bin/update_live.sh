#!/bin/sh

cd ~/harmony-site
git pull
cp -r build/* ~/www.harmonyagreements.org/htdocs/.
