#-*- coding:utf-8 -*-
from django.db import models
from viewflow.models import Process, Subprocess


VENDER_CHOICES = (
    ('cisco','Cisco'),
    ('juniper','Juniper'),
    ('huawei', 'Huawei'),
    )


string = """
             
             Device information


         """



class OrderProcess(Process):
    trusted = models.NullBooleanField(default = False)
    permit_ip = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    content = models.TextField(max_length = 250, default = string , blank = True)
    content2 = models.TextField(max_length = 250, default = string, blank = True)

    def is_true(self):
        if self.trusted == True:
            print "true"
            return True
        else:
            print 'false'
            return False

# 기존의 것을 바꿈
class OrderItem(models.Model):
    order = models.ForeignKey(OrderProcess, null=True, blank = True)
    ip = models.CharField(max_length=250)
    port = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    vendor = models.CharField(max_length=250, default = 'cisco', choices = VENDER_CHOICES)
    coninfo = models.TextField(max_length = 250, default = string , blank = True)
    #count = models.DecimalField(max_digits=5,decimal_places=5)

