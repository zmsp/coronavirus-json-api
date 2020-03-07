#!/usr/bin/env bash
git pull
python ./update_data.py
git add .
git commit -m "auto commit"
git push