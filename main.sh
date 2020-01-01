#!/bin/sh
var1 = 5
while [ $var1 ]
do
python3 ./bots/britbot.py & python3 ./bots/sender.py & python3 ./bots/randomer.py & python3 ./bots/george_bd.py & python3 ./bots/pasuk.py 
done
