#!/bin/bash

cd ./vCardOOo/
zip -0 vCardOOo.zip mimetype
zip -r vCardOOo.zip *
cd ..

mv ./vCardOOo/vCardOOo.zip ./vCardOOo.oxt
