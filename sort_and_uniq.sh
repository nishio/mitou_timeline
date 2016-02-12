#!/usr/bin/env bash
cat negative.txt | sort | uniq > negative2.txt
cat positive.txt | sort | uniq > positive2.txt
mv negative.txt negative.bak
mv positive.txt positive.bak
mv negative2.txt negative.txt
mv positive2.txt positive.txt

