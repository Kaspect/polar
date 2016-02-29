#Description: Output MIME type ground truth to all the file in input_file_list
#             If tika failed to parse, it'll put a TIka Parsing Failed instead of the MIME type to the output file
#Execution: redirect error msg to a file to see files that tika failed to pasrse e.g. ./mime_type_groundtruth_generator.sh 2> err_log
#By Hang Guo

output_fn="full_file_MIME_type_groundtruth" #output file name
input_file_list="full_file_list" #the list of full paths to all the input file 
TIKA_JAR="/home/hangguo/Tika/trunk/tika-app/target/tika-app-1.12-SNAPSHOT.jar" #location of the standalone tika jar file

if [ -e $output_fn ]
then rm $output_fn 
fi

while read fn; 
do 
 MIME="$( cat $fn | java -jar $TIKA_JAR -m | grep Content-Type:)" ;
   if [ "$?" -ne "0" ]; then    #Detect Previous Command return code
     MIME="##Tika Parsing Failed##" 
     >&2 echo "Above error log belongs to file $fn"
   fi
 echo "$fn          $MIME " >> $output_fn; 
done < $input_file_list
