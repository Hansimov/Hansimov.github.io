
import requests
# https://www.bilibili.com/video/av75811479
av = "75811479"

proxies = {
  'http': 'http://36.250.156.100:9999',
  # 'https': 'https://117.85.105.170:808'
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36", 
       # "Connection": "keep-alive"
}
req = requests.get('http://icanhazip.com', headers=headers, proxies=proxies)
print(req.text.strip())

videoURL = "https://www.bilibili.com/video/av{}".format(av)
req2 = requests.get(videoURL,headers=headers,proxies=proxies)
print(req2)


