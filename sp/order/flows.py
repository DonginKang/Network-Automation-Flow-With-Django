#-*- coding:utf-8 -*-

from viewflow import frontend, flow, lock, views as flow_views
from viewflow.activation import STATUS
from viewflow.base import Flow, this

from . import models, views

kkk = '123123'


class OrderFlow(Flow):
    """
    Acceess List 

    Configure Access List in Multi Vendor.
    """
    process_cls = models.OrderProcess
    lock_impl = lock.select_for_update_lock


    start = flow.Start(views.StartView).Next(this.config)


    config = flow.View(views.AclConfigView,
            task_description="ACl 설정 입력",
            ).Next(this.verify_config)

    verify_config = flow.View(
        views.CustomerVerificationView,
        task_description="설정 정보 확인",
    ).Next(this.check_verify)

    check_verify = flow.If(cond=lambda p: p.is_true()) \
          .OnTrue(this.end) \
          .OnFalse(this.rollback)


    rollback = flow.View(
        views.RollbackView,
        task_description=" 원상복구 "
    ).Next(this.end)

    end = flow.End()




frontend.register(OrderFlow)


