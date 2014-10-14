# coding=utf-8
import httplib
import urllib2
import hashlib
import datetime
import json
import uuid
from lxml import etree
from Crypto import Random
from Crypto.Cipher import AES
from utils import get_wxname,get_id,get_rid
from zhengqian.account.models import account,mission
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext

def access(request):
    code = request.GET.get('code')
    result = get_id(code)
    token = result['access_token']
    openid = result['openid']
    try:
        account.objects.get(openid=openid)
    except:
        wxname = get_wxname(token,openid)
        account.objects.create(openid=openid,wxname=wxname,point=0)
    rid = get_rid(openid)
    youmi_url = r'http://w.ymapp.com/wx/ios/lists.html?r='+rid
    return HttpResponseRedirect(youmi_url)


def rec_point(request):
    user = request.GET.get('user')
    task = request.GET.get('ad')
    point = request.GET.get('points')
    a = account.objects.get(openid=user)
    a.point += int(point)
    a.save()
    mission.objects.create(user_id=a.id,task=task,point=point)
    return HttpResponse(' ')


def pay(request):
    result={}
    code = request.GET.get('code')
    user = get_id(code)['openid']
    pay = account.objects.get(openid=user)
    if pay.alipay:
        HttpResponseRedirect('/pay_apply?user='+user)
    else:
        HttpResponseRedirect('/reg?user='+user)

def reg(request):
    user = request.GET.get('user')
    name = request.GET.get('name')
    mobile = request.GET.get('mobile')
    alipay = request.GET.get('account')
    people = account.objects.get(openid=user)
    people.name = name
    people.mobile = mobile
    people.alipay = alipay
    people.save()
    return HttpResponse('done!')


def pay_reg(request):
    user = request.GET.get('user')
    name = request.GET.get('name')
    alipay = request.GET.get('account')
    mobile = request.GET.get('mobile')
    try:
        people = account.objects.get(name = user)
        people.name = name
        people.alipay = alipay
        people.mobile = mobile
        people.save()
        resultCode = 1
    except:
        resultCode = 0
    return HttpResponse(resultCode)

def pay_get(request):
    user = request.GET.get('user')
    people = account.objects.get(openid=user)


def pay_apply(user):
    people = account.objects.get(user)
    pay.objects.create(user_id=people.id,point=people.point,Status=0,orderID=uuid.uuid1().time_low)


def pay_deal(request):
    orderID = request.GET.get('id')
    action = request.GET.get('action')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        pay = pay.objects.get(orderID=orderID)
        people = account.objects.get(pay.id)
        if action == 1:
            people.point = 0
            people.save()
        else:
            pass
        pay.dealtime = time
        pay.Status = action
        pay.save()
        response = 1
    except:
        response = 0
    return HttpResponse(response)


def weixin(request): 
    if request.method == 'GET':
        signature=request.GET.get('signature')
        timestamp=request.GET.get('timestamp')
        nonce=request.GET.get('nonce')
        echostr=request.GET.get('echostr')
        token="zhijianzhuanqian" 
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        if hashcode == signature:
            return HttpResponse(echostr)
    else:
        xml = etree.fromstring(request.body)
        fromUser = xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        CreateTime = xml.find('CreateTime').text
        key = xml.find('EVENTKEY').text
        if key == 'view':
            user = account.objects.get(openid=fromUser)
            reply_text = '用户'+user.wxname+'，当前积分：'+user.point
        elif key == 'get':
            pay_apply(fromUser)
            reply_text = '您的提现请求已发送，我们将尽快进行审核并完成发放'
        reply_xml = """<xml>
       <ToUserName><![CDATA[%s]]></ToUserName>
       <FromUserName><![CDATA[%s]]></FromUserName>
       <CreateTime>%s</CreateTime>
       <MsgType><![CDATA[text]]></MsgType>
       <Content><![CDATA[%s]]></Content>
       </xml>"""%(fromUser,toUser,CreateTime,reply_text)
        return HttpResponse(reply_xml)