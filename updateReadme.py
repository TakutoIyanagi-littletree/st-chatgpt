import datetime
import requests

# 日付を指定する
date = datetime.datetime.now()
queryDate= "{0:%Y%m}".format(date)

# URL組み立てる
url = "https://connpass.com/api/v1/event/?nickname=TakutoIyanagi-littletree&ym="+ queryDate

# リクエストを投げる
res = requests.get(url)

# レスポンスをJSONに変換する
jsonData = res.json()

# 配列宣言
titleList = []
urlList = []
classTimeList = []
resultList = []

# 整形する
for item in jsonData["events"]:
  title = item['title']
  url = item['event_url']
  # 時間整形
  date = datetime.datetime.fromisoformat(item['started_at'])
  classTime = str(date.month) + "月"+ str(date.day) + "日" + str(date.hour) + "時" + str(date.minute) + "分〜"

  titleList.append(title)
  urlList.append(url)
  classTimeList.append(classTime)

# loopさせる
for (title, url, day) in zip(titleList, urlList, classTimeList):
  allList = ("- " + day + " [" + title + "](" + url + ")")
  resultList.append(allList)

# 結果
resultList = '\n'.join(resultList)

import textwrap

docs_str = textwrap.dedent('''\
## 今月の視聴・参加イベント

{conpassList}

''').format(conpassList=resultList).strip()

with open('README.md', 'w') as f:
    f.write(docs_str)
