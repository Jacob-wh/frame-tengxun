#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = CXH
# __time__ = 17/11/3 下午3:22


from django.conf.urls import patterns, url

urlpatterns = patterns(
    'home_application.api.views',
    url(r'get_vms_list', 'getVirtualMachineList'),
    url(r'close_vm', 'closeVirtualMachine'),
    url(r'start_vm', 'startVirtualMachine'),
    url(r'reboot_vm', 'rebootVirtualMachine'),
    url(r'destroy_vm', 'destroyVirtualMachine'),

    url(r'get_val_list','getVcenterAccountList'),
    url(r'get_dc_list', 'getDatacenterList'),
    url(r'get_ct_list', 'getClusterList'),
    url(r'get_ds_list', 'getDatastoreList'),

    url(r'get_fa_list', 'getFlowAnalysisList'),
    url(r'get_ma_list','getMemoryAnalysisList'),

    url(r'clone_vm','cloneVm'),
    url(r'updata_vm_cfg','updateVMConfiguration'),
    url(r'sync_cloud_account','syncCloudAccount')

)