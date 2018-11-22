#!/bin/bash 

files=`ls | grep csv | grep -v format`
echo $files
for f in $files 
do 
    echo $f
    line_nr=`cat $f | wc -l`
    let "line_nr=line_nr-1"
    echo "day,time,direction,linkid,travel_time,volumn,speed,occupancy,congestion_level" > ${f}123456789
    cat $f | tail -n ${line_nr} >> ${f}123456789
    rm ${f}
    mv ${f}123456789 ${f}
done
