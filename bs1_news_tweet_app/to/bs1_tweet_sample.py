# -*- coding: utf-8 -*-
# bs1_tweet.py # 現在は最初に発見した適合する書き込みで即ツイートする仕様。確度を上げる必要がある場合は複数を比較カウントして最上位を取るようにする。
# copyright by Yoshihiko Watanabe 2020

import pytz
import re
import urllib.request
import time
import sys
import schedule
import gmail
import os
import datetime
from datetime import datetime as dt
from datetime import timedelta
import oauth2


headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }

def get_active_urls():
  fixed_bs_url = 'https://nhk2.5ch.net/livebs'
  fixed_head = '<p style="margin:0; padding: 0; font-size: 0.75em'
  fixed_part1 = 'background: #BEB;"><a href="' # 
  fixed_part2 = 'l50" target="body">'
  fixed_end_mark = "新規スレッド作成はこちら"
  active_urls = []
  fixed_bs_url = urllib.request.Request(url=fixed_bs_url, headers=headers)
  while True:
    try:
      fd = urllib.request.urlopen(fixed_bs_url)      
    except (IOError):
      print ('Exception. Sleep 30 sec.') # 
      time.sleep(30)
      print ('Now try again...') # until here
      continue
    else:
      line = fd.readline()
      #print (line.decode('utf-8')) # debug
      while line:
        raw_text = line.decode('shift_jis', 'ignore')
        if fixed_end_mark in raw_text:
          break
        elif fixed_head in raw_text and re.search(r'NHK BS1 \d{5} \(', raw_text):
          link_url = raw_text.split(fixed_part2)[0].split(fixed_part1)[1]
          #print (link_url) # debug
          active_urls.append(link_url)
        line = fd.readline()
      #continue
      break
  return active_urls

def get_list (thread_url):
  fixed_base_url = 'https://nhk2.5ch.net'
  fixed_head = '<div class="thread">'
  fixed_part0 = '</div></div><div class="push"></div></div><div class="post" id='
  fixed_part1 = '</div></div><br><div class="post" id=' # 
  fixed_end_mark = '</span></div></div><br></div><div class="push">'
  res_list = []
  thread_title = ''
  # print (thread_url) # debug
  target_url = urllib.request.Request(url=fixed_base_url+thread_url, headers=headers)
  # print (target_url) # DEBUG
  while True:
    try:
      fd = urllib.request.urlopen(target_url)    
    except (IOError):
      print ('Exception. Sleep 30 sec.') # 
      time.sleep(30)
      print ('Now try again...') # until here
      continue
    else:
      line = fd.readline()
      #print (line.decode('utf-8')) # debug
      while line:
        raw_text = line.decode('shift_jis', 'ignore')
        if '<title>' in raw_text:
          thread_title = raw_text.split('<title>')[1].rstrip(' \n')
        elif fixed_part0 in raw_text and fixed_head in raw_text:
          res_list.extend(raw_text.split(fixed_part0)[1].split(fixed_part1))
        elif fixed_part1 in raw_text and fixed_end_mark in raw_text:
          res_list.extend(raw_text.split(fixed_end_mark)[0].replace('<div></div>','').split(fixed_part1))
        elif fixed_part1 in raw_text:
          res_list.extend(raw_text.split(fixed_part1))
          #print (link_url) # debug
        line = fd.readline()
      #continue
      break
  return thread_title, res_list

def send_mail(body, attachment=''):
  address = 'watanyoshi@gmail.com'
  sender_address = 'watanyoshi3000@gmail.com'
  SENDER_NAME = '渡邊 由彦'
  username = '渡邊 由彦  <watanyoshi3000@gmail.com>'
  password = '' # Need the real password here
  client = gmail.GMail(username, password)
  finished = datetime.datetime.now()
  finished_f = finished.strftime("%Y/%m/%d %H:%M:%S")
  if attachment == '':
    message = gmail.Message(u'BSニュースTweet '+finished_f, to=address, text=body)
  else:
    message = gmail.Message(u'BSニュースTweet '+finished_f, to=address, text=body, attachments=[attachment])
  client.send(message)
  client.close()
  return

def write_log(thread_title, log_text):
  filename1 = thread_title + '_tweet.txt'
  if not os.path.exists(filename1):
    with open(filename1, 'w') as f:
      f.write(log_text)
  return

def tweet(text):
  ConsumerAPIkey = 'd6HruVLfddfd4884fdfdT4j9KP' # This is fake. Need actual key here
  APIsecretkey = 'Eoi5jKifjd799A3ypcW5RdXHlMNR89898QoczeX3PG4ySALJ4sb0' # This is fake. Need actual token here
  Accesstoken = '13158415622247234-NcNENW9dfdfdooMMMes55RmBAhWhdlStiy1qfJ' # This is fake. Need actual token here
  Accesstokensecret = 'LomUOkokoDIF8899895DIUHHHUSUHJJJJDJJDHr20Y1' # This is fake. Need actual key here
  url = "https://api.twitter.com/1.1/statuses/update.json?status={}".format(text)
  consumer = oauth2.Consumer(key=ConsumerAPIkey, secret=APIsecretkey)
  token = oauth2.Token(key=Accesstoken, secret=Accesstokensecret)
  client = oauth2.Client(consumer, token)
  resp, content = client.request( url, method="POST")
  return content

def compose (title, shift, caster, delayed):
  jpn_time_raw = dt.utcnow() + datetime.timedelta(hours=9)
  #jpn_date_dm = jpn_time_raw.strftime('%#m/%#d(%a)').replace('Sun','日').replace('Mon','月').replace('Tue','火').replace('Wed','水').replace('Thu','木').replace('Fri','金').replace('Sat','土') # Windows
  jpn_date_dm = jpn_time_raw.strftime('%-m月%-d日(%a)').replace('Sun','日').replace('Mon','月').replace('Tue','火').replace('Wed','水').replace('Thu','木').replace('Fri','金').replace('Sat','土') # Linux
  shifts = {"weekd1":"5:50～10:00","weekd2":"10:50～正午, 13:50～15:00","weekd3":"15:50～17:00, 18:50～20:00","weekd4":"20:50～深夜0:00","weekd4k":"12:45～13:00, 17:45～18:00","weeke1":"8:50～13:00","weeke2":"13:50～18:00","weeke3":"18:50～深夜0:00"}
  # compose text for tweet
  if delayed:
    text2 = ("今日の"+ title +"の担当女性キャスターをお知らせ（試験運用中）\n"+ jpn_date_dm + shifts[shift] +" の担当は"+ caster +"キャスター\n特番やスポーツ番組の都合でイレギュラーな時間帯があります"+"\n@BSニュース  @"+ caster)
  else:
    text2 = ("今日の"+ title +"の担当女性キャスターをお知らせ（試験運用中）\n"+ jpn_date_dm + shifts[shift] +" の担当は"+ caster +"キャスター\n@BSニュース  @"+ caster)
  text = text2.replace(":",'%3A').replace("\n",'%0D').replace("@",'%23').replace("/",'%2F').replace("(",'%28').replace(")",'%29').replace(",",'%2C').replace(" ",'%20')
  print (text) # DEBUG
  return (text, text2)

def is_ca_dst():
  tz = pytz.timezone("US/Pacific")
  return dt.now().astimezone(tz).dst() != timedelta(0)

#----------- main ---------------------
def job(title, shift): # title BSニュース or BSニュース4K. スタート時間, 時間帯＆平日、休日
  holidays = ['2020/11/03','2020/11/23','2021/01/01','2021/01/11','2021/02/11','2021/02/23','2021/03/20','2021/04/29','2021/05/03','2021/05/04','2021/05/05','2021/07/19','2021/08/11','2021/09/20','2021/09/23','2021/10/11','2021/11/03','2021/11/23']
  jpn_time_raw = dt.utcnow() + datetime.timedelta(hours=9)
  jpn_date_dmh = jpn_time_raw.strftime('%Y/%m/%d')
  jpn_date_dow = jpn_time_raw.weekday() # Day of the week
  if (any (jpn_date_dmh == i for i in holidays or jpn_date_dow > 4)) and 'weekd' in shift: # Holidays or weekends reject weekday schedules
    return
  elif (not any (jpn_date_dmh == i for i in holidays) and (jpn_date_dow < 5)) and 'weeke' in shift: # Weekdays except holidays reject weekend schedules
    return
  start_time = dt.utcnow() + datetime.timedelta(hours=9)
  time_limit = dt.now() + datetime.timedelta(minutes=25)
  time_limit_a = dt.now() + datetime.timedelta(minutes=5)
  delayed = False
  not_done = True
  if __name__ == "__main__":
    param = sys.argv
  #print (len(param))
  #print (param)
  #print (param[1])
  #print (param[2])
  global ended_thread
  kw = []
  body = title + '\n'
  log_text = title + '\n'
  count = 1
  if len(param) < 2:
    # kw = "笠井","美穂","みぽ"] # name variations
    # kw = ["笠井","美穂","みぽ","長谷川さん","静香","御前","佐久川","智さん","さとい","サトイ","瑠音","阪田","陽子","超熟","襟立","秋山さん","千鶴","チヅル","ちづる","徳田","琴美","ことみ","琴み","細谷","翠","ペコちゃん","福永","美春","みはる","ミハル","岡さん","裕美","ひろみ"] # "るね" is treated by kw2 and kw3
    kw2 = "るね"
    kw_dx = ["あるね","いるね","えるね","かるね","すぎるね","するね","てるね","とるね","めるね","るねえ","るねん","れるね","出るね","出てるね","喋るね","になるね","見るね"] # exclusions for "るね" as variation of "瑠音"
    kw_ng = ["かな","じゃなくて","休み","来ねー","ｺﾈｰ","コネー","待っていたら","基地外","中傷","捏造","自作自演","嫉妬","犯罪行為","荒らし","粘着","キモオタ","おっぱい番付","河野千秋","卑怯","狡猾","ダメだこりゃ","笠井オタ","笠井美穂オタ","木下瑠音オタ","本性","低スペック","キチガイ","自分をガンガン","ケツが","内臓","胃腸","夜の時間は","アピール","イップス","限界","下品","AAAAAカップ","腹黒","クビに","醜い","作り笑い","自分アピ","売れ残り","ニート","ハゲ","アンチ","笠井は","笠井を","笠井さんが見たいなぁ","氏ね","死ね","癌"] # NG words
    kw_a = ["笠井","美穂","みぽ"] # 笠井美穂
    kw_b = ["長谷川さん","静香","御前"] # 長谷川静香
    kw_c = ["佐久川","智さん","さとい","サトイ"] # 佐久川智
    kw_d = ["るね","瑠音"] # 木下瑠音
    kw_e = ["阪田","陽子","超熟","襟立"] # 阪田陽子
    kw_f = ["秋山さん","千鶴","チヅル","ちづる"] # 秋山千鶴
    kw_g = ["徳田","琴美","ことみ","琴み"] # 徳田琴美
    kw_h = ["細谷","翠","ペコちゃん"] # 細谷翠
    kw_i = ["福永","美春","みはる","ミハル"] # 福永美春
    kw_j = ["岡さん","裕美","ひろみ"] # 岡裕美

  else:
    for i in param:
      if count >= 2:
        kw.append(i)
      count += 1
  # print (kw) # DEBUG
  # print (title) # 

  temp_urls = get_active_urls()
  fixed_str1 = 'class="number">'
  fixed_str2 = '</span><span class="name">'
  fixed_str3 = '<span class="date">'
  fixed_str4 = '</span><span class="uid">'
  fixed_str5a = '<span class="escaped"><span class="AA"> '
  fixed_str5b = '<span class="escaped"> '
  fixed_str6 = ' </span>'
  # attacment_flag = False

  while not_done and dt.now() < time_limit:
    delayed = dt.now() >= time_limit_a
    for tmp_url in temp_urls:
      thread_title, res_list = get_list (tmp_url)
      # body = body + thread_title + '\n'
      log_text = thread_title + ' ' + title + '\n'
      for i in res_list:
        #if any((x in i for x in kw)): # any() and List comprehension
        if "Over 1000" in i:
          break
        tmp_num = i.split(fixed_str2)[0].split(fixed_str1)[1]
        tmp_time = i.split(fixed_str4)[0].split(fixed_str3)[1]
        tmp_time2 = re.sub(r'\([日月火水木金土]\)', '',tmp_time)
        post_time = dt.strptime(tmp_time2,"%Y/%m/%d %H:%M:%S.%f")
        if post_time < start_time:
          continue
        # else: # DEBUG
        #   print (post_time, start_time) # DEBUG
        elif fixed_str5a in i:
          tmp_text = i.split(fixed_str5a)[1].replace(fixed_str6,'').replace(" <br>",'').replace("</span>",'')
        else:
          tmp_text = i.split(fixed_str5b)[1].replace(fixed_str6,'').replace(" <br>",'').replace("</span>",'')
        tmp_text = re.sub(r'<a .+</a>', '',tmp_text)
        tmp_text = re.sub(r'</div></div><br>.+', '',tmp_text).lstrip(' ')
        log_text = log_text + tmp_num + " " + tmp_time + " " + tmp_text + "\n"
        #if any((x in i for x in kw)): # any() and List comprehension ORG
        #if any((x in i for x in kw)) or (kw2 in i and not any((x in i for x in kw3))): # any() and List comprehension to support "るね" with many exceptions
        if any (x in i for x in kw_a) and not any (x in i for x in kw_ng): # 笠井美穂
          t_text, text2 = compose (title, shift, "笠井美穂", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_b) and not any (x in i for x in kw_ng): # 長谷川静香
          t_text, text2 = compose (title, shift, "長谷川静香", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_c) and not any (x in i for x in kw_ng): # 佐久川智
          t_text, text2 = compose (title, shift, "佐久川智", delayed)
          print (tweet (t_text))
          not_done = False
        elif (kw2 in i and not any(x in i for x in kw_dx)) and (not any(x in i for x in kw_ng)): # "るね" 木下瑠音
          t_text, text2 = compose (title, shift, "木下瑠音", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_e) and not any (x in i for x in kw_ng): # 阪田陽子
          t_text, text2 = compose (title, shift, "阪田陽子", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_f) and not any (x in i for x in kw_ng): # 秋山千鶴
          t_text, text2 = compose (title, shift, "秋山千鶴", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_g) and not any (x in i for x in kw_ng): # 徳田琴美
          t_text, text2 = compose (title, shift, "徳田琴美", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_h) and not any (x in i for x in kw_ng): # 細谷翠
          t_text, text2 = compose (title, shift, "細谷翠", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_i) and not any (x in i for x in kw_ng): # 福永美春
          t_text, text2 = compose (title, shift, "福永美春", delayed)
          print (tweet (t_text))
          not_done = False
        elif any (x in i for x in kw_j) and not any (x in i for x in kw_ng): # 岡裕美
          t_text, text2 = compose (title, shift, "岡裕美", delayed)
          print (tweet (t_text))
          not_done = False
        
        if not not_done:
          body = thread_title + '\n' + body + tmp_num + " " + tmp_time + " " + tmp_text + "\n"
          print (tmp_num, tmp_time, tmp_text)
          write_log(thread_title, log_text + text2)
          send_mail(body)
          break

    # print ('\n')
    time.sleep(20) # Adjust for the best wait time

# ---------------------------------------------------------------------------------------------------
ended_thread = ['NHK BS1 10174']
# Schedule current time is based on Daylight saving hours needs 1 hour shift after 2020/11/01
# if not is_ca_dst():
weekd_a = "12:50:00" # 5:50 weekdays Regular hours 2020/11/1 - 2021/3/13
weekd_b = "17:50:00" # 10:50 weekdays Regular hours
weekd_c = "19:45:00" # 12:45 weekdays Regular hours
weekd_d = "22:50:00" # 15:50 weekdays Regular hours
weekd_e = "03:50:00" # 20:50 weekdays Regular hours
weeke_a = "15:50:00" # 8:50 weekends Regular hours
weeke_b = "20:50:00" # 13:50 weekends Regular hours
weeke_c = "01:50:00" # 18:50 weekends Regular hours
# else:
  # weekd_a = "13:50:00" # 5:50 weekdays DST
  # weekd_b = "18:50:00" # 10:50 weekdays DST
  # weekd_c = "20:45:00" # 12:45 weekdays DST
  # weekd_d = "23:50:00" # 15:50 weekdays DST
  # weekd_e = "04:50:00" # 20:50 weekdays DST
  # weeke_a = "16:50:00" # 8:50 weekends DST
  # weeke_b = "21:50:00" # 13:50 weekends DST
  # weeke_c = "02:50:00" # 18:50 weekends DST

# Caution - National holiday needs to be treared as weekends
schedule.every().day.at(weeke_a).do(job, "BSニュース",'weeke1') # 8:50 weekends or holiday
schedule.every().day.at(weeke_b).do(job, "BSニュース",'weeke2') # 13:50 weekends or holiday
schedule.every().day.at(weeke_c).do(job, "BSニュース",'weeke3') # 18:50 weekends or holiday
#-------------------------------------------------------------------
schedule.every().day.at(weekd_a).do(job,"BSニュース",'weekd1') # 5:50 weekdays
schedule.every().day.at(weekd_b).do(job, "BSニュース",'weekd2') # 10:50 weekdays
schedule.every().day.at(weekd_c).do(job, "BSニュース4K",'weekd4k') # 12:45 weekdays
schedule.every().day.at(weekd_d).do(job, "BSニュース",'weekd3') # 15:50 weekdays
schedule.every().day.at(weekd_e).do(job, "BSニュース",'weekd4') # 20:50 weekdays

while True:
  schedule.run_pending()
  time.sleep(10)

