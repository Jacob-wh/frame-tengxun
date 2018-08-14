# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsBkLogin(object):
    """Collections of bk_login APIS"""

    def __init__(self, client):
        self.client = client

        self.get_user = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/bk_login/get_user/',
            description=u'获取用户信息',
        )

        """
        app_code	string	
        应用标识，即应用 ID
        
        app_secret	string	
        应用私密 key，即应用 APP_TOKEN，可以通过 蓝鲸智云开发者中心 -> 点击应用ID -> 基本信息 获取
    
        bk_token 可选	string	
        当前用户登录态，bk_token可以通过Cookie获取
        
        username 可选	string	
        当前用户用户名，白名单中app可使用
        """
        self.get_all_user = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/bk_login/get_all_user/',
            description=u'获取所有用户信息',
        )

        self.get_batch_user = ComponentAPI(
            client=self.client, method='GET', path='/api/c/compapi/bk_login/get_batch_user/',
            description=u'获取多个用户信息',
        )
