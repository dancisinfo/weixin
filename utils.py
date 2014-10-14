from Crypto import Random
from Crypto.Cipher import AES

import json
import base64
import urllib2


def get_wxname(token,openid):
    url = 'https://api.weixin.qq.com/sns/userinfo?lang=zh_CN&access_token='+token+'&openid='+openid
    resp = urllib2.urlopen(url)
    result = json.loads(resp.read())
    return result['nickname']

def get_id(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx7c3f3c56f8353b85&secret=90782a588b1c5b9d24bedfc9703852c6&grant_type=authorization_code&code='+code
    resp = urllib2.urlopen(url)
    result = json.loads(resp.read())
    return result

def get_rid(openid):
    appid = '2c1d34426f330241'
    app_secret = '2e87d969a327c73d'
    raw = openid+(16-len(openid)%16)*chr(16-len(openid)%16)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(app_secret,AES.MODE_CBC,iv)
    return urllib.quote_plus(appid+base64.b64encode(iv+cipher.encrypt(raw)))