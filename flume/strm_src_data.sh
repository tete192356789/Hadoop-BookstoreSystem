declare -a orders=("book1 65" "book2 165" "book3 55" "book4 70" "book5 130" "book6 95")

for i in $(seq 1 100)
do
    while true
    do
        id=$((1 + $RANDOM % 1000))
        if ((id >= 1 && id <= 801)) || ((id >= 5001 && id <= 5945)) || ((id >= 8000 && id <= 8501));
        then
            break
        else
            continue
        fi
    done
   timestamp=$(date +%s)
   echo "$id|${orders[$RANDOM%${#orders[@]}]}|$timestamp" >> /data/flume/source/hdfs/order_${timestamp}.txt
   echo "$id|${orders[$RANDOM%${#orders[@]}]}|$timestamp" >> /data/flume/source/hbase/order_${timestamp}.txt
   sleep 30
done