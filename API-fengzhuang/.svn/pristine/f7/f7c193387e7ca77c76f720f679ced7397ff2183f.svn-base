# -*- coding: utf-8 -*-
from ..base import ComponentAPI


# 系统组件集合类的名称，一般为 Collections + 系统名
class CollectionsOpsDemo(object):

    def __init__(self, client):
        self.client = client

        # create_task为组件名，method为请求组件使用的方法，path为组件路径，组件域名为系统默认域名
        self.listHost = ComponentAPI(
            client=self.client, method='POST', path='/api/c/self-service-api/opsdemo/getapphostlist/',
            description=u'',
        )