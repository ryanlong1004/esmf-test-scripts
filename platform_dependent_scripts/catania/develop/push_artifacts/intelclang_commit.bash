#!/bin/bash

cd /project/esmf/himanshu/storage/esmf-test-artifacts/
git pull


cd /project/esmf/himanshu/storage/esmf-test-artifacts/develop/catania/intelclang/
touch a.sh
git rm *.html
git rm commit.log
cp -rf /project/esmf/himanshu/esmf_test/cronjobs/daily/intelclang/esmf_logs/2102_test/ESMFdailyLog result.html
{ echo -n '<pre> '; cat result.html; } > result.html.new
mv result.html{.new,}
rm a.sh


cd /project/esmf/himanshu/storage/esmf-test-artifacts/develop/catania/intelclang/
git log --since=6.days --grep='Catania IntelClang commit log' >  commit.log


cd /project/esmf/himanshu/storage/esmf-test-artifacts/
git add .
git commit -m " Catania IntelClang commit log pushed at `date` [ci skip] "
#git commit -m " Catania IntelClang commit log pushed at Fri Dec 4 11:10:05 MST 2020"
git push origin master
