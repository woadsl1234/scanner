# -*- coding:utf-8 -*-
import sys
import random

VERSION = '0.0.1'
AUTHOR = 'ckj123'

# Slack webhooks for notifications
posting_webhook = "https://hooks.slack.com/services/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"
errorlogging_webhook = "https://hooks.slack.com/services/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"
test_webhook = "https://hooks.slack.com/services/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"
slack_sleep_enabled = True  # bypass Slack rate limit when using free workplace, switch to False if you're using Pro/Ent version.
at_channel_enabled = True   # Add @channel notifications to Slack messages, switch to False if you don't want to use @channel

# crtsh postgres credentials, please leave it unchanged.
DB_HOST = 'crt.sh'
DB_NAME = 'certwatch'
DB_USER = 'guest'
DB_PASSWORD = ''


# SSL证书验证 (SSL certificate verification)
allow_ssl_verify = True

# -------------------------------------------------
# requests 配置项  (Requests configuration item)
# -------------------------------------------------

# 超时时间 (overtime time)
timeout = 60

# 是否允许URL重定向 (Whether to allow URL redirection)
allow_redirects = True

# 是否使用session （Whether to use session）
allow_http_session = True

# 是否随机使用User-Agent （Whether to use User-Agent randomly）
allow_random_user_agent = False

# 是否允许随机X-Forwarded-For
allow_random_x_forward = False

# 代理配置 （Agent configuration）
allow_proxies = {

}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    "Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; "
    "Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322;"
    " .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0;"
    " .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2;"
    " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727;"
    " InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3)"
    " Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    "Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 随机生成User-Agent （Randomly Generate User-Agent）
def random_user_agent(condition=False):
    if condition:
        return random.choice(USER_AGENTS)
    else:
        return USER_AGENTS[0]

# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (random.randint(1, 254),random.randint(1, 254),random.randint(1, 254),random.randint(1, 254))
    else:
        return '8.8.8.8'

# User-Agent设置 （User-Agent settings）
headers = {
    'User-Agent': random_user_agent(allow_random_user_agent),
    'X_FORWARDED_FOR': random_x_forwarded_for(allow_random_x_forward),
    'Referer' : 'http://www.baidu.com',
}

# nmap命令设置 （Nmap command settings）
nmap_cmd_line = ""


banner_0 = """\033[01;34m
 _____________________________
< Version:%s by %s >
 -----------------------------\033[0m
     \033[01;31m\\
      \033[01;33m\\\033[0m
          oO)-.                       .-(Oo
         /__  _\                     /_  __\\
         \  \(  |     ()~()         |  )/  /
          \__|\ |    (-___-)        | /|__/
          '  '--'    ==`-'==        '--'  '

""" % (VERSION, AUTHOR)

banner_1 = """\033[01;34m
 _____________________________
< Version:%s by %s >
 -----------------------------\033[0m
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||

""" % (VERSION, AUTHOR)

banner_2 = """\033[01;34m
_____________________________
< Version:%s by %s >
-----------------------------\033[0m
  \033[01;31m\\
    \033[01;33m\\\033[0m
      .--.
     |o_o |
     |:_/ |
    //   \ \\
   (|     | )
   /'\_   _/`\\
   \___)=(___/

""" % (VERSION, AUTHOR)

banners = [banner_0, banner_1, banner_2]