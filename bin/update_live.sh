#!/bin/sh

cd ~/harmony-site
git pull
cp -r ~/harmony-site/build/* ~/www.harmonyagreements.org/htdocs/.
