#!/bin/bash

Months=(20150101 20150301 4 5 6) 

Year=2014
Month=1
Day=1

function fun()
{
    echo "python test.py $1 $2"
    python test.py $1 $2
}

cnt=0
declare -a arr

for year in {2014..2015}
do
    for month in {1..12..2}
    do
        num=$(($year*10000+$month*100+$Day))
        arr[$cnt]=$num
        b=${arr[$cnt]}
        #echo $b
        cnt=$(($cnt+1))
        #echo  $num
    done
done

size=${#arr[@]}

for (( x=0; x<size; x++ ))
do
    #echo ${arr[$x]}
    fun ${arr[$x]} ${arr[$(($x+1))]}&
done
wait
