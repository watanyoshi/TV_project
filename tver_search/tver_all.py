# -*- coding: utf-8 -*-

import urllib.request
import datetime
from datetime import datetime as dt
import socket
import time
import csv
import codecs
import copy

category = ''
url_base = "https://tver.jp/"
cat_prefix = category # drama -> anime
fixed_end_mark = '<div class="credit">'
href_a = '<a href="/feature/'
href_b = '<a href="/corner/'
href_c = '<a href="/episode/'
fixed_href_tail = '" class="detail_link" data-pos="' + category + '">' # drama -> anime
title_head_s = '<div class="progtitle" title="' # 単数の場合
title_head_p = '<div class="progtitle matome" title="' # 複数ある場合
fixed_title_tail = '">'
summary_head_a = '<p class="summary ">'
summary_head_b = '<p class="summary subtitles">'
fixed_summary_tail = '</p>'
fixed_section_end = '<p class="tv">'
prog_summary = ''
detail_page_url = ''
data_out = ''
data_out_html = ''
is_matome = False
# ['drama','variety','documentary','anime','sport','other']
dic_titles = {}
dic_titles['drama'] = ["池袋ウエストゲートパーク","タイガー&ドラゴン","うぬぼれ刑事","JIN -仁- 完結編","泣くな、はらちゃん","彼女が死んじゃった。","おじさまと猫","江戸モアゼル～令和で恋、いたしんす。～","あなた犯人じゃありません","その女、ジルバ","オー！マイ・ボス！恋は別冊で","ウチの娘は、彼氏が出来ない!!","書けないッ!?〜脚本家 吉丸圭佑の筋書きのない生活〜","天国と地獄 〜サイコな2人〜","君と世界が終わる日に","にじいろカルテ","俺の家の話","レッドアイズ 監視捜査班","アノニマス〜警視庁“指殺人”対策室〜","片恋グルメ日記","35歳の少女","姉ちゃんの恋人"] # {"key" : ["value1", "value2"]}
dic_titles['variety'] = ["吉田類の酒場放浪記","ポツンと一軒家"]
dic_titles['documentary'] = ["報道特集","深層NEWS"]
dic_titles['anime'] = ["犬と猫どっちも飼ってると毎日たのしい","鬼滅の刃","美味しんぼ","新幹線変形ロボ シンカリオン"]
dic_titles['sport'] = ["Let's!美バディ"]
dic_titles['other'] = ["きょうの健康","きょうの料理"]

def multi_episodes(url):
  data = ''
  prev_data = ''
  fixed_end_mark = '<!--これまでの放送-->'
  fixed_href_tail = '" class="detail_link" data-pos="sibling">'
  while True:
    try:
      fd = urllib.request.urlopen(url,timeout=3)
    except socket.timeout:
      continue
    except urllib.error.HTTPError as e:
      time.sleep(1)
      continue
    except urllib.error.URLError as e:
      time.sleep(1)
      continue
    except (IOError):
      time.sleep(1)
      continue
    else:
      line = fd.readline()
      start_on = False
      while line:
        raw_text = line.decode('utf-8', 'ignore')
        if fixed_end_mark in raw_text:
          break
        elif href_a in raw_text or href_b in raw_text or href_c in raw_text:
          detail_page_url = url_base + raw_text.split('<a href="/')[1].split(fixed_href_tail)[0]
          start_on = True
        elif start_on and title_head_p in raw_text:
          prog_title = raw_text.split(title_head_p)[1].split(fixed_title_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and title_head_s in raw_text:
          prog_title = raw_text.split(title_head_s)[1].split(fixed_title_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and summary_head_a in raw_text:
          prog_summary = raw_text.split(summary_head_a)[1].split(fixed_summary_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and summary_head_b in raw_text:
          prog_summary = raw_text.split(summary_head_b)[1].split(fixed_summary_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and fixed_section_end in raw_text:
          if prev_data != (prog_title + ' ' + prog_summary).rstrip():
            data = data + new_title_check(prog_title) + ' ' + prog_summary + '\n'
            prev_data = (prog_title + ' ' + prog_summary).rstrip()
          # print (prog_title, prog_summary, detail_page_url) # DEBUG
          start_on = False
        line = fd.readline()
    return data # text of episodes in detail page

def new_title_check(title):
  global existing_drama_titles2
  if is_drama and title not in existing_drama_titles and title not in existing_drama_titles2:
    existing_drama_titles2.append(title)
    title = '<strong>【初登場】</strong>' + title
  elif is_drama and title not in existing_drama_titles and title in existing_drama_titles2:
    title = '<strong>【初登場】</strong>' + title
  return title

def main(category):
  global cat_prefix
  global fixed_href_tail
  global is_drama

  if category == 'drama':
    is_drama = True
  else:
    is_drama = False
  url_base = "https://tver.jp/"
  cat_prefix = category # drama -> anime
  fixed_end_mark = '<div class="credit">'
  href_a = '<a href="/feature/'
  href_b = '<a href="/corner/'
  href_c = '<a href="/episode/'
  fixed_href_tail = '" class="detail_link" data-pos="' + category + '">' # drama -> anime
  title_head_s = '<div class="progtitle" title="' # 単数の場合
  title_head_p = '<div class="progtitle matome" title="' # 複数ある場合
  fixed_title_tail = '">'
  summary_head_a = '<p class="summary ">'
  summary_head_b = '<p class="summary subtitles">'
  fixed_summary_tail = '</p>'
  fixed_section_end = '<p class="tv">'
  prog_summary = ''
  detail_page_url = ''
  data_out = ''
  data_out_html = ''
  is_matome = False

  timestamp = dt.now().strftime('%Y%m%d')
  f2 = codecs.open('tver_' + category + '_' + timestamp + '.html','w', 'utf_8') # drama -> anime

  url = url_base + cat_prefix
  print (url) # DEBUG
  while True:
    try:
      fd = urllib.request.urlopen(url,timeout=3)
    except socket.timeout:
      continue
    except urllib.error.HTTPError as e:
      time.sleep(1)
      continue
    except urllib.error.URLError as e:
      time.sleep(1)
      continue
    except (IOError):
      time.sleep(1)
      continue
    else:
      line = fd.readline()
      start_on = False
      while line:
        raw_text = line.decode('utf-8', 'ignore')
        if fixed_end_mark in raw_text:
          break
        elif href_a in raw_text or href_b in raw_text or href_c in raw_text:
          detail_page_url = url_base + raw_text.split('<a href="/')[1].split(fixed_href_tail)[0]
          start_on = True
        elif start_on and title_head_p in raw_text:
          is_matome = True
          prog_title = raw_text.split(title_head_p)[1].split(fixed_title_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and title_head_s in raw_text:
          prog_title = raw_text.split(title_head_s)[1].split(fixed_title_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and summary_head_a in raw_text:
          prog_summary = raw_text.split(summary_head_a)[1].split(fixed_summary_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and summary_head_b in raw_text:
          prog_summary = raw_text.split(summary_head_b)[1].split(fixed_summary_tail)[0].replace('&amp;',"&") # .replace('㊙',"(秘)")
        elif start_on and fixed_section_end in raw_text and is_matome:
          data = new_title_check(prog_title) + ' ' + prog_summary + '\n'
          data2 = multi_episodes(detail_page_url)
          if data in data2 and data2 not in data_out:
            data_out = data_out + data2
          elif data not in data2 and data not in data_out:
            data_out = data_out + data
            # print (prog_title, prog_summary, detail_page_url) # DEBUG
          is_matome = False
          start_on = False
          data = ''; data2 = ''
        elif start_on and fixed_section_end in raw_text:
          data_out = data_out + new_title_check(prog_title) + ' ' + prog_summary + '\n'
          # print (prog_title, prog_summary, detail_page_url) # DEBUG
          start_on = False
        line = fd.readline()
      # continue
      break
  data_out_html = data_out.replace('\n','<br>')
  for tmp_title in dic_titles[category]: # marked_titles
    data_out_html = data_out_html.replace(tmp_title,'<b>' + tmp_title + '</b>')
  html1 = "<!DOCTYPE html><html lang=\"ja\"><head><META charset=\"utf-8\"></head><body>\n"
  html2 = "<br>\n<br>\n<br>\n</body></html>\n\n"
  f2.write(html1 + data_out_html + html2) ###
  f2.close() ###
  return

existing_drama_titles2 = []
with codecs.open('existing_drama_titles.csv', 'r', 'utf_8') as f:
  tmp_buffer = csv.reader(f)
  for tmp_title in tmp_buffer:
    # print (tmp_title) # DEBUG
    existing_drama_titles = copy.copy(tmp_title)
existing_drama_titles2 = copy.copy(existing_drama_titles)
# print (existing_drama_titles2) # DEBUG
# exit () # DEBUG

is_drama = False
category = ['drama','variety','documentary','anime','sport','other']
# category = ['drama']

for cat in category:
  main (cat)

if existing_drama_titles2 != existing_drama_titles:
  with codecs.open('existing_drama_titles.csv', 'w', 'utf_8') as f: # for real run
  # with codecs.open('existing_drama_titles1.csv', 'w', 'utf_8') as f: # with ...1 file for test 
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(existing_drama_titles2)





