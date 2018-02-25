#!/bin/bash

for((i=0;i<6;i++))
do
phantomjs new.js $i 1 1 &
done