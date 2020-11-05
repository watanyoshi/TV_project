#!/bin/bash

cd /py
tmp_time=$(date '+%Y/%m/%d %T')
echo "Reading Digi raw data now... at ${tmp_time}"
python url_read24DIGInew_add.py
tmp_time=$(date '+%Y/%m/%d %T')
echo "Reading BS raw data now... at ${tmp_time}"
python url_read24BSnew_add.py
tmp_time=$(date '+%Y/%m/%d %T')
echo "Reading CS raw data now... at ${tmp_time}"
python url_read24CSnew.py
tmp_time=$(date '+%Y/%m/%d %T')
echo "Extracting links for Digi program now... at ${tmp_time}"
python links_program_new_add.py
echo "Extracting links for BS program now..."
python links_program_BSnew_add.py
echo "Extracting links for CS program now..."
python links_program_CSnew_add.py
echo "Loading program data from links..."
cp output_new_data.txt output_new_data_bk_DG.txt
rm -f flag.txt
while :
do
  tmp_time=$(date '+%Y/%m/%d %T')
  echo "Reading Digi program data now... at ${tmp_time}"
  python url_read_pro_filterDIGI_add2.py
  if [ -e flag.txt ]; then
    echo "Sleep 1 minute..."
    rm -f flag.txt
    rm -f output_new_data.txt
    cp output_new_data_bk_DG.txt output_new_data.txt
    sleep 1m
    echo "Now retry..."
    continue
  fi
  echo "No exceptions in DG !!"
  break
done
cp output_new_data.txt output_new_data_bk_BS.txt
while :
do
  tmp_time=$(date '+%Y/%m/%d %T')
  echo "Reading BS program data now... at ${tmp_time}"
  python url_read_pro_filterBS_add2.py # 2 -> 3 for test
  if [ -e flag.txt ]; then
    echo "Sleep 1 minute..."
    rm -f flag.txt
    rm -f output_new_data.txt
    cp output_new_data_bk_BS.txt output_new_data.txt
    sleep 1m
    echo "Now retry..."
    continue
  fi
  echo "No exceptions in BS !!"
  break
done
#read -p "Enter" #debug
cp output_new_data.txt output_new_data_bk_CS.txt
while :
do
  tmp_time=$(date '+%Y/%m/%d %T')
  echo "Reading CS program data now... at ${tmp_time}"
  python url_read_pro_filterCS_add2.py # 2 -> 3 for test
  if [ -e flag.txt ]; then
    echo "Sleep 1 minute..."
    rm -f flag.txt
    rm -f output_new_data.txt
    cp output_new_data_bk_CS.txt output_new_data.txt
    sleep 1m
    echo "Now retry..."
    continue # continue
  fi
  echo "No exceptions in CS !!"
  break
done
tmp_time=$(date '+%Y/%m/%d %T')
echo "Data reading done. Now cleaning the data... at ${tmp_time}"
python data_file_clean.py
tmp_time=$(date '+%Y/%m/%d %T')
echo "Categorizing to groups... at ${tmp_time}"
python line_read_cat.py
#echo "Keyword serch 1 of 2..."
tmp_time=$(date '+%Y/%m/%d %T')
echo "Keyword search ... at ${tmp_time}"
python list_read_multi_keywords3new.py #New version with html format
python ym_scoreJM2.py
python ym_score2_debug.py
python ym_score2_anime.py
#cat "/Users/yopio/py/movie_search_result.txt"
python send_report_gmail.py
tmp_time=$(date '+%Y/%m/%d %T')
echo "Completed !!! at ${tmp_time}"
chown yoshi.yoshi ./output_new_data.txt
