#!/bin/bash
set -e

git config --global push.default simple
git remote add production ssh://root@128.199.200.47/root/perdana-indonesia
git push production master