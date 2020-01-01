#!/bin/bash
set -e
ssh root@128.199.200.47 -v exit

git config --global push.default simple
git remote add production ssh://root@128.199.200.47/perdana-indonesia
git push production master