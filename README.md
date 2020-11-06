# TV_project
Storage of samples to show how I love Japanese TV

Japanese TV watch system via Internet
TV Tuner: I-O Data EX-BCTX2 (https://www.iodata.jp/product/av/tuner/ex-bctx2/)
Streamin Device: Slingbox M1 (https://www.slingbox.jp/product/m1/overview.html)
Remote control file made by myself: http://www.hifi-remote.com/forums/dload.php?action=file&file_id=25623
Player software: Slingplayer (https://www.slingbox.jp/product/slingplayer.html)
The system allows to watch 60+ channels of Japanese TV program live or recorded.
Other connected devices:
Network HDD- RECBOX 4TB HVL-AAS4 (https://www.amazon.co.jp/gp/product/B07VJZWW7H)
USB HDD - I-O DATA HDD EX-HD3CZ 3TB (https://www.amazon.co.jp/gp/product/B06Y46G1PX)
NAS - Synology DiskStation DS218j CS7088 6TB - Video recording storage (https://www.amazon.co.jp/gp/product/B076HJB5L1)
TV signal converter - Portta HDMI to RGB YPbPr (https://www.amazon.co.jp/gp/product/B00A8FIQXA)
Captured sample images are seen in Github (https://github.com/watanyoshi/TV_project/tree/main/TV_watch_system/to)

Self-made Application to search the latest Japanese TV programs to find something fun. Some part for movies needs access to movie database then made a small clone of the database of Yahoo movie using SQlite.\n
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
Sample files are seen in Github (https://github.com/watanyoshi/TV_project/tree/main/Search_app/to)

My time is limited but I want to watch as many good programs as possible. Using Excel list to manage watching new JP fall dramas efficiently. Also placed some list of recorded movie list and favorite documentary program.
2020 Fall drama.xlsx seen in Github (https://github.com/watanyoshi/TV_project/tree/main/2020_JP_Fall_drama/to)

Made another application to tweet automatically related to TV by some interesting trigger. I am a fan of one of the News shows called BS NEWS and the show does not annouce the caster beforehand. The application gets the posts in some live BBS to tell the caster name and makes a tweet the composed info without manual operation.
It can be seen at https://twitter.com/YoshihikoWatan2, app script can be seen in Github (https://github.com/watanyoshi/TV_project/tree/main/bs1_news_tweet_app/to)

