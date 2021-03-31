cd ../
cd lay_2.5
for ((i=0; i<20; i++)); do
    pressure=`awk -v i=$i 'BEGIN{printf("%g",100*i);}'` 
    for ((j=0; j<17; j++)); do 
        voltage=`awk -v j=$j 'BEGIN{printf("%g",0.1*j);}'`
        if [ ${pressure} -eq 0 ] || [ ${voltage} -eq 0 ]; then
            cd ./${pressure}Mpa-${voltage}V
            source $scriptsdir/residence_time/residence_time.sh
        fi
    done
done
cd ../