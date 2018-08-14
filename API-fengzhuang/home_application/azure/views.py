# -*- coding: utf-8 -*-

import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from common.mymako import render_mako_context, render_json


#azure参数
AZURE_SUBSCRIPTION_ID=''
AZURE_CLIENT_ID=''
AZURE_CLIENT_SECRET=''
AZURE_TENANT_ID=''

def azure(request):
    # 这里开始触发缓存数据，确保后续页面访问流畅。
    return render_mako_context(
        request, '/home_application/azure/azure.html'
    )


def get_credentials():
    subscription_id = os.environ[AZURE_SUBSCRIPTION_ID]
    credentials = ServicePrincipalCredentials(
        client_id=os.environ[AZURE_CLIENT_ID],
        secret=os.environ[AZURE_CLIENT_SECRET],
        tenant=os.environ[AZURE_TENANT_ID]
    )
    return credentials, subscription_id


def getAzureVmList(request):

    credentials, subscription_id = get_credentials()
    compute_client = ComputeManagementClient(credentials, subscription_id)
    result={}
    # List VMs in subscription
    print('List VMs in subscription')
    for vm in compute_client.virtual_machines.list_all():
        print("\tVM: {}".format(vm.name))

    return result


#同步微软云 虚拟机
def syncAzure(accountModel):

    return 1