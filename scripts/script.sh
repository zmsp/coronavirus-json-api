#!/usr/bin/env bash
git pull
python ./download_latest_data.py
git add .
git commit -m "auto commit"
git push