# encoding: UTF-8
__author__ = 'Justin'

from WindPy import *
from eventEngine import *
import threading

class WindApi:

    def __init__(self, eventEngine):
        self.__eventEngine = eventEngine

    # 开启
    def start(self):
        event = Event(type_=EVENT_LOG)
        log = u'正在连接服务器，请稍候'
        event.dict_['log'] = log
        self.__eventEngine.put(event)
        w.start()
        if self.isConnected():
            log = u'服务器连接成功，现在可以登录'
        else:
            log = u'未连接服务器，请重启'
        event.dict_['log'] = log
        self.__eventEngine.put(event)

    # 停止
    def stop(self):
        w.stop()

    # 判断是否连接
    def isConnected(self):
        return w.isconnected()

    # 取消订阅
    def cancelSubscribe(self, id):
        w.cancelRequest(id)

    # 获取历史序列数据
    def getHistorySequenceData(self, security, fields, startDate, endDate, *option):
        data = w.wsd(security, fields, startDate, endDate, *option)
        event = Event(type_=EVENT_HISTORYSEQUENCEDATA)
        event.dict_['data'] = data
        self.__eventEngine.put(event)

    # 获取分钟数据
    def getMinuteData(self, security, fields, startTime, endTime, *option):
        data = w.wsi(security, fields, startTime, endTime, *option)
        event = Event(type_=EVENT_MINUTEDATA)
        event.dict_['data'] = data
        self.__eventEngine.put(event)

    # 获取日内tick级别数据
    def getTickData(self, security, fields, startTime, endTime, *option):
        data = w.wst(security, fields, startTime, endTime, *option)
        event = Event(type_=EVENT_TICKDATA)
        event.dict_['data'] = data
        self.__eventEngine.put(event)

    # 获取历史截面数据
    def getHistorySectionData(self, security, fields, *option):
        data = w.wss(security, fields, *option)
        event = Event(type_=EVENT_HISTORYSECTIONDATA)
        event.dict_['data'] = data
        self.__eventEngine.put(event)

    # 获取和订阅实时行情数据
    def subscribe(self, security, fields):
        
        return w.wsq(security, fields, func=self.onSubscribe)

    def onSubscribe(self, indata):
        #print indata
        if indata.ErrorCode == 0:
            
            event = Event(type_=EVENT_LOG)
            log = u'合约查询成功'
            event.dict_['log'] = log
            self.__eventEngine.put(event)
            event = Event(type_=EVENT_MARKETDATA)
            event.dict_['data'] = indata.Data
            event.dict_['code'] = indata.Codes
            event.dict_['time'] = indata.Times
            event.dict_['field'] = indata.Fields
            self.__eventEngine.put(event)
            event = Event(type_=EVENT_MARKETDATA_CONTRACT)
            event.dict_['data'] = indata.Data
            event.dict_['code'] = indata.Codes
            event.dict_['time'] = indata.Times
            event.dict_['field'] = indata.Fields
            self.__eventEngine.put(event)
        else:
            event = Event(type_=EVENT_LOG)
            log = u'合约查询错误，错误代码：' + unicode(indata.ErrorCode) + u',' + u'错误信息：' + unicode(indata.Data[0][0])
            event.dict_['log'] = log
            self.__eventEngine.put(event)
    # 获取板块、指数等成分数据
    def getMemberData(self):
        pass

    # 获取条件选股结果
    def getConditionalSelectStock(self):
        pass

    # 获取资产管理、组合管理数据
    def getManageData(self):
        pass

    # 交易相关函数

    #交易登录
    def tLogon(self, brokerId, departmentId, accountId, password, accountType):
        LogonID = w.tlogon(brokerId, departmentId, accountId, password, accountType)
        if LogonID.ErrorCode != 0:
            event = Event(type_=EVENT_LOG)
            log = u'登陆错误，'
            event.dict_['log'] = log
            self.__eventEngine.put(event)
        else:
            event1 = Event(type_=EVENT_LOG)
            log = u'登陆成功'
            event1.dict_['log'] = log
            self.__eventEngine.put(event1)
            event2 = Event(type_=EVENT_TLOGON)
            event2.dict_['data'] = LogonID
            self.__eventEngine.put(event2)
            
    # 交易登出
    def tLogout(self):
        w.tlogout()

    # 委托下单
    def tOrder(self, securityCode, tradeSide, orderPrice, orderVolume, **option):
        message = w.torder(securityCode, tradeSide, orderPrice, orderVolume, **option)
        print message
        if message.ErrorCode != 0:
            event = Event(type_=EVENT_LOG)
            log = u'发单错误，错误代码：' + unicode(message.ErrorCode) + u',' + u'错误信息：' + unicode(message.Data[1][0])
            event.dict_['log'] = log
            self.__eventEngine.put(event)
        else:
            event = Event(type_=EVENT_LOG)
            log = u'发单成功'
            event.dict_['log'] = log
            self.__eventEngine.put(event)
            
            event1 = Event(type_=EVENT_ORDER)
            #options = 'LogonID='+str(w.tquery('LogonID').Data[0][0])+';WindCode='+str(securityCode)
            #ReOrder = w.tquery('Order', options)
            #print ReOrder
            event1.dict_['data'] = message.Data
            event1.dict_['code'] = securityCode
            self.__eventEngine.put(event1)
            
            event2 = Event(type_=EVENT_TRADE)
            self.__eventEngine.put(event2)
    # 撤销委托
    def tCancel(self, orderNum, *option):
        w.tcancel(orderNum, *option)
        

    # 交易查询
    def tQuery(self, qryCode, *option):
        if qryCode == 'LogonID':
            return w.tquery(qryCode, *option)
        elif qryCode == 'Order':
            return w.tquery(qryCode, *option)
        elif qryCode == 'Trade':
            return w.tquery(qryCode, *option)
        elif qryCode == 'Account':
            data = w.tquery('Capital', *option)
            event = Event(type_=EVENT_ACCOUNT)
            event.dict_['data'] = data
            self.__eventEngine.put(event)
        elif qryCode == 'Position':
            data = w.tquery(qryCode, *option)
            event = Event(type_=EVENT_POSITION)
            event.dict_['data'] = data
            self.__eventEngine.put(event)

    # 日期函数

    # 返回区间内日期序列
    def getDateSequence(self):
        pass

    # 返回偏移值对应日期
    def getDateOffset(self):
        pass

    # 返回某个区间内日期数量
    def getDateNum(self):
        pass

