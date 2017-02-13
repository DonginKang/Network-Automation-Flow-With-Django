#-*- coding:utf-8 -*-

import extra_views

from django import forms
from django.forms.models import modelform_factory
from django.views import generic

from viewflow import flow, views as flow_views
from material import LayoutMixin, Layout, Row, Inline

from . import models
from models import OrderItem, OrderProcess
from . import test



model = " views.py model" # 이 변수는 이 안에 있는 get_object 함수가 모두 공유 
 #여기서 리스트에 딕셔너리 형식으로 메모리상 으로 올린다음 이걸로 하면 될듯
devices_info = []



# Inline 은 속성을 하나하나 추가할떄 필요한 기능
class ItemInline(extra_views.InlineFormSet):
    model = models.OrderItem
    fields = ['ip', 'port','username','password','vendor']



class StartView(LayoutMixin,
                flow.ManagedStartViewActivation,
                flow_views.StartActivationViewMixin,
                extra_views.NamedFormsetsMixin,
                extra_views.UpdateWithInlinesView,
                ):
    model = models.OrderProcess
    model2 = models.OrderItem
    layout = Layout(
        Inline('Device Info', ItemInline),
    )


    count = 0 # get_object 가 한번 만 실행되게 만들어주는것 

    def get_object(self):
        if self.count == 1: # 두번째  config save 하면서 시작 하는것 
            print 'start second' 
            StartView.count = 0
            return self.process
        
        # 첫번째 start 누르면서 시작할거 
        StartView.count += 1
        print 'start first'
        devices_info[:] = []
        print devices_info
        return self.process


class AclConfigView(flow_views.TaskViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        models.OrderProcess,
        fields=['permit_ip','host'],
        )

    count = 0


    def get_object(self):
        if self.count == 1: # 두번째  config save 하면서 시작 하는것 
            print 'config second' 
            AclConfigView.count = 0
            return self.activation.process

        
        # 첫번째 start 누르면서 시작할거 
        AclConfigView.count += 1
        print 'config first'
        return self.activation.process



class CustomerVerificationView(flow_views.TaskViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        models.OrderProcess,
        fields=['content','content2','trusted'],
        widgets={"trusted": forms.CheckboxInput, "content":forms.Textarea})


    count = 0 # get_object 가 한번 만 실행되게 만들어주는것 
    DBInitial = 0
    

    def get_object(self):
        if self.count == 1: # 두번째  config save 하면서 시작 하는것 
            CustomerVerificationView.count = 0
            print 'verify second' 
            print devices_info
            return self.activation.process
        
        # 첫번째 start 누르면서 시작할거
        print 'verify first'
        for number in range(self.DBInitial,OrderItem.objects.count()):
            Device(number)
        
        for i in range(0,len(devices_info)):
            ConfigLast(i)           


        CustomerVerificationView.DBInitial = OrderItem.objects.count()         
        CustomerVerificationView.count += 1
        return self.activation.process


class RollbackView(flow_views.TaskViewMixin, generic.UpdateView):
    form_class = modelform_factory(
        models.OrderProcess,
        fields=['content','content2','trusted'],
        widgets={"trusted": forms.CheckboxInput, "content":forms.Textarea})

    def get_object(self):
        return self.activation.process


############################## test #################################

def Device(number):
    dic = {}
    
    link_number = OrderItem.objects.all()[number].order_id
    orderprocess = OrderProcess.objects.filter(process_ptr_id=link_number)

    dic['id'] = str(OrderItem.objects.all()[number].id)
    dic['ip'] = str(OrderItem.objects.all()[number].ip)
    dic['port'] = str(OrderItem.objects.all()[number].port)
    dic['username'] = str(OrderItem.objects.all()[number].username)
    dic['password'] = str(OrderItem.objects.all()[number].password)
    dic['vendor'] = str(OrderItem.objects.all()[number].vendor)
    dic['permit_ip'] = str(list(orderprocess.values())[0]['permit_ip'])   #나중에 따로 빼야함 
    dic['host'] = str(list(orderprocess.values())[0]['host']) #나중에 따로 빼야함
    devices_info.append(dic)

def ConfigLast(i):
    ip = devices_info[i]['ip']
    user = devices_info[i]['username']
    passwd = devices_info[i]['password']
    permit = devices_info[i]['permit_ip']
    host = devices_info[i]['host']
    vendor = devices_info[i]['vendor']
    port = devices_info[i]['port']
    test.acl(ip,user,passwd,permit,host,vendor,port)      


