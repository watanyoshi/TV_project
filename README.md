# TV_project
Storage of samples to show how I love Japanese TV
Japanese TV watch system via Internet
TV Tuner: I-O Data EX-BCTX2 (https://www.iodata.jp/product/av/tuner/ex-bctx2/)
Streamin Device: Slingbox M1 (https://www.slingbox.jp/product/m1/overview.html)
Remote control file made by myself: http://www.hifi-remote.com/forums/dload.php?action=file&file_id=25623
Player software: Slingplayer (https://www.slingbox.jp/product/slingplayer.html)
The system allows to watch 60+ channels of Japanese TV program live or recorded.
Sample captured images are seen in Github here

Application to search the latest Japanese TV programs to find something fun
TV_crawl.sh - Shell script to run on Ubuntu server once a day
Excerpt of inside:
python url_read24DIGInew_add.py - Crawl Japanese TV program site called tvkingdom for one day in a week
python links_program_new_add.py - Extract links for all the programs in the scope
python url_read_pro_filterDIGI_add2.py - Read the detailed info of each program and output to one text file
python data_file_clean.py - remove the programs already broadcasted and correct format issues
python line_read_cat.py - filter and group the programs to movie, drama, etc
python list_read_multi_keywords3new.py - search the programs based on keyword file supporting multi-matching or exclusions
python ym_scoreJM2.py - Focusing Japanese movies, link to movie database in Yahoo movie and sort the programs based on the review point
python send_report_gmail.py Sending the email with the results of keyword match, movie list, Japanese drama, Japanese anime, Japanese historical drama, drama in western, drama in South Korean, drama in China.
Sample files are seen in Github here

My time is limited but I want to watch many good programs. Using Excel list to manage new dramas efficiently.
2020 Fall drama.xlsx seen in Github here

I am a fan of one of the News shows called BS NEWS and the show does not annouce the caster beforehand. I made an application to get the info from the live BBS and tweet it.
It can be seen at https://twitter.com/YoshihikoWatan2, app script can be seen in Github here
