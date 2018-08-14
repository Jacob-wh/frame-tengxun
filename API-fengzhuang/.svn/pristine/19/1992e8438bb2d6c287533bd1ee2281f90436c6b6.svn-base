# -*- coding: utf-8 -*-
import json

from django.db import models
from django.utils import timezone
from django.db import connection, transaction

"""
vcenter账号信息对象
"""
class VcenterAccount(models.Model):
    account_name = models.CharField(max_length=60)
    account_password = models.CharField(max_length=60,null=True,default="")
    vcenter_host = models.CharField(max_length=30,null=True,default="")
    vcenter_port = models.IntegerField(default=443,null=True)
    vcenter_version = models.CharField(max_length=10,null=True,default="")
    cloud_provider = models.CharField(u'云提供商',max_length=20,null=True,default="")
    cloud_private_key = models.CharField(u'云私钥匙',max_length=60,null=True,default="")
    cloud_public_key = models.CharField(u'云公钥匙',max_length=60,null=True,default="")
    cloud_region = models.CharField(u'云区域',max_length=20,null=True,default="")
    project_id = models.CharField(u'云项目',max_length=20,null=True,default="")

    #自定义表名称
    class Meta:
        db_table = 'vcenter_account'

        """
数据中心,与虚拟机是一对多的关系
        与集群是一对多的关系
"""
class VcenterDatacenter(models.Model):
    #数据中心名称
    name = models.CharField(max_length=60)

    #存储节点总量
    datastoreTotal = models.IntegerField(default=0)

    #存储节点个数
    datastoreNum = models.IntegerField(default=0)

    #主机个数
    hostNum = models.IntegerField(default=0)

    #网络个数
    networkNum = models.IntegerField(default=0)

    #虚拟机个数
    vmNum = models.IntegerField(default=0)

    #集群个数
    clusterNum = models.IntegerField(default=0)

    #自定义表名称
    class Meta:
        db_table = 'vcenter_datacenter'

"""
集群，与数据中心是一对多关系
"""
class VcenterCluster(models.Model):
    #集群所在的数据中心
    datacenter = models.ForeignKey(VcenterDatacenter, related_name='vcenter_cluster_ref_datacenter')

    #集群名称
    name = models.CharField(max_length=60)

    #集群操作历史次数
    actionHistoryNum = models.IntegerField(default=0)

    #集群迁移历史次数
    migrationHistoryNum = models.IntegerField(default=0)

    #drs推荐次数
    drsRecommendationNum = models.IntegerField(default=0)

    #集群是否开启HA
    enabledClusterHa  = models.BooleanField(default=False)

    #自定义表名称
    class Meta:
        db_table = 'vcenter_cluster'

"""
存储节点，与数据中心是一对多关系
"""
class VcenterDatastore(models.Model):
    #存储所在的数据中心
    datacenter = models.ForeignKey(VcenterDatacenter, related_name='vcenter_datastore_ref_datacenter')
    #存储节点名称
    name = models.CharField(max_length=60)

    #存储挂载主机数
    mountHostNum = models.IntegerField(default=0)

    #存储节点容器id
    datastoreContainerId = models.CharField(default="",max_length=60,null=True)

    #是否可访问
    accessible = models.BooleanField(default=True)

    #容量大小
    capacity = models.IntegerField(default=0)

    #剩余空间
    freeSpace = models.IntegerField(default=0)

    #维护模式
    maintenanceMode = models.CharField(default="",max_length=20)

    #多主机访问是否开启
    multipleHostAccess = models.BooleanField(default=True,max_length=20)

    #文件系统类型
    filesystemType = models.CharField(default="",max_length=20)

    #存储节点路径
    url = models.CharField(default="",max_length=120)

    #自定义表名称
    class Meta:
        db_table = 'vcenter_datastore'

"""
网络信息
"""
class VcenterNetwork(models.Model):
    #vswitch名称
    name = models.CharField(max_length=60,default="")

    #属于哪一台主机
    host = models.CharField(max_length=32,default="")

    #最大传输数
    mtu = models.IntegerField(default=0)

    #端口数
    num_ports = models.IntegerField(default=0)

    #可用端口数
    num_ports_available = models.IntegerField(default=0)

    #端口组名称信息
    portgroup = models.CharField(max_length=120,default="")

    #虚拟机网卡个数
    vnic = models.IntegerField(default=0)

    #自定义表名称
    class Meta:
        db_table = 'vcenter_network'

"""
主机对象
"""
class VcenterHost(models.Model):
    #host名称
    name = models.CharField(max_length=60,default="")

    api_type = models.CharField(max_length=20,default="")

    api_version = models.CharField(max_length=20,default="")

    build = models.CharField(max_length=20,default="")

    full_name = models.CharField(max_length=60,default="")

    instance_uuid = models.CharField(max_length=40,default="")

    license_product_name = models.CharField(max_length=20,default="")

    license_product_version = models.CharField(max_length=20,default="")

    locale_build = models.CharField(max_length=20,default="")

    locale_version = models.CharField(max_length=20,default="")

    os_type = models.CharField(max_length=20,default="")

    product_line_id = models.CharField(max_length=20,default="")

    vendor = models.CharField(max_length=20,default="")

    version = models.CharField(max_length=20,default="")

    #自定义表名称
    class Meta:
        db_table = 'vcenter_host'

"""
定义vm管理器
"""
class VmManager(models.Manager):
    pass


"""
vcenter虚拟机对象
"""
class VcenterVirtualMachine(models.Model):
    #属于哪一个vcenter 账号
    account = models.ForeignKey(VcenterAccount, related_name='vcenter_virtualmachine_ref_account')

    #虚拟机所在的数据中心
    datacenter = models.ForeignKey(VcenterDatacenter, related_name='vcenter_virtualmachine_ref_datacenter',null=True)

    #虚拟机所在集群
    cluster = models.ForeignKey(VcenterCluster, related_name='vcenter_virtualmachine_ref_cluster',null=True)

    #虚拟机名称
    name = models.CharField(max_length=60)
    #虚拟机路径名称
    vm_pathname = models.CharField(max_length=120)
    #虚拟机操作系统名称
    guest_fullname = models.CharField(max_length=60)
    #虚拟机运行状态
    power_state = models.CharField(max_length=50)
    #虚拟机IP
    ipaddress = models.CharField(max_length=30)
    #实例uuid
    instance_uuid = models.CharField(max_length=40,unique=True)
    #最后启动时间
    boot_time = models.TimeField(null=True)

    #是否为模版
    template = models.BooleanField(default=False)

    #最大cpu使用
    maxCpuUsage = models.IntegerField(default=0)
    #最大内存使用
    maxMemoryUsage = models.IntegerField(default=0)
    #内存大小
    memorySizeMB = models.IntegerField(default=0)
    #cpu个数
    numCpu = models.IntegerField(default=0)

    numEthernetCards = models.IntegerField(default=0)

    numVirtualDisks = models.IntegerField(default=0)

    instanceUuid = models.CharField(max_length=60)

    #操作系统Id
    guestId = models.CharField(max_length=60)

    #存储信息
    storage_committed = models.IntegerField(default=0,null=True),
    storage_uncommitted = models.IntegerField(default=0,null=True),
    storage_unshared = models.IntegerField(default=0,null=True),

    overallStatus = models.CharField(max_length=10)

    #自定义表名称
    class Meta:
        db_table = 'vcenter_virtualmachine'



'''
快照数据表管理方法
'''
class VcenterVirtualMachineSnapshot_Manager(models.Manager):
    '''
    根据虚拟机id获取快照信息
    '''
    def getListByVmId(self, vmId):
        queryStr = 'SELECT vvs.id,vvs.`name`,vvs.description,date_format(vvs.create_time,"%%Y-%%m-%%d %%H:%%i:%%s") as create_time,vvs.account_id,vvs.virtualmachine_id,vvs.result FROM vcenter_virtualMachine_snapshot AS vvs WHERE vvs.virtualmachine_id = %s' % vmId
        print queryStr
        cursor = connection.cursor()
        cursor.execute(queryStr)
        column_names = [d[0] for d in cursor.description]
        return [Row(zip(column_names, row)) for row in cursor]

    # def deleteAllByVmId(self,vmId):


"""
虚拟机快照，与虚拟机是多对一的关系
"""
class VcenterVirtualMachineSnapshot(models.Model):
    #快照属于哪一个虚拟机
    virtualmachine = models.ForeignKey(VcenterVirtualMachine, related_name='vcenter_virtualMachine_napshot_ref_virtualmachine')
    # 属于哪一个vcenter 账号
    account = models.ForeignKey(VcenterAccount, related_name='vcenter_virtualMachine_napshot_ref_account')
    #快照名称
    name = models.CharField(u"快照名称", max_length=120)
    description = models.CharField(u"快照描述", max_length=500, null=True)
    create_time = models.DateTimeField(u"创建时间", default=timezone.now)
    result = models.CharField(u"创建快照结果:running表示正在创建中，success表示创建快照成功，failed表示创建失败", max_length=20, default='running')
    #自定义表名称
    class Meta:
        db_table = 'vcenter_virtualmachine_snapshot'

    objects = VcenterVirtualMachineSnapshot_Manager()

"""
ucloud  虚拟机实例
{
    "Action": "DescribeUHostInstanceResponse",
    "RetCode": 0,
    "TotalCount": 1,
    "UHostSet": [
        {
            "AutoRenew": "Yes",
            "BasicImageId": "uimage-5sr2eq",
            "BasicImageName": "CentOS 6.5 64\u4f4d",
            "BootDiskState": "Normal",
            "CPU": 1,
            "ChargeType": "Dynamic",
            "CreateTime": 1502442535,
            "DiskSet": [
                {
                    "BackupType": "BASIC_SNAPSHOT",
                    "DiskId": "bsi-moipen",
                    "Drive": "/dev/vda",
                    "Encrypted": "No",
                    "Size": 20,
                    "Type": "Boot"
                }
            ],
            "ExpireTime": 1502446138,
            "GPU": 0,
            "HostType": "N1",
            "HotplugFeature": false,
            "IPSet": [
                {
                    "IP": "10.23.42.149",
                    "SubnetId": "subnet-own13y",
                    "Type": "Private",
                    "VPCId": "uvnet-lb4hjg"
                },
                {
                    "Bandwidth": 2,
                    "IP": "120.132.23.55",
                    "IPId": "eip-kzbrfa",
                    "Type": "Bgp",
                    "Weight": 50
                }
            ],
            "ImageId": "bsi-moipen",
            "IsExpire": "No",
            "Memory": 2048,
            "Name": "xiaoming",
            "NetCapFeature": true,
            "NetCapability": "Normal",
            "NetworkState": "NotConnected",
            "OsName": "CentOS 6.5 64\u4f4d",
            "OsType": "Linux",
            "Remark": "",
            "State": "Initializing",
            "StorageType": "UDisk",
            "SubnetType": "Default",
            "Tag": "Default",
            "TimemachineFeature": "no",
            "TotalDiskSpace": 0,
            "UHostId": "uhost-wgasee",
            "UHostType": "Normal",
            "Zone": "cn-sh2-02"
        }
    ]
}
"""
class UcloudInstance(models.Model):
    autoRenew = models.CharField(default="",max_length=5,null=True)
    basicImageId = models.CharField(default="",max_length=15,null=True)
    basicImageName = models.CharField(default="",max_length=30,null=True)
    bootDiskState = models.CharField(default="",max_length=10,null=True)
    cpu= models.IntegerField(default=0,null=True)
    chargeType = models.CharField(default="",max_length=15,null=True)
    createTime = models.TimeField(null=True)
    backupType = models.CharField(default="",max_length=15,null=True)
    diskId = models.CharField(u'磁盘id',default="",max_length=15,null=True)
    drive = models.CharField(u'磁盘驱动',default="",max_length=15,null=True)
    encrypted = models.CharField(u'磁盘是否加密',default="No",max_length=5,null=True)
    size = models.IntegerField(u'磁盘大小',default=0,null=True)
    type = models.CharField(u'磁盘类型',default="Boot",max_length=10,null=True)
    expireTime = models.TimeField(u'过期时间',null=True)
    gpu = models.IntegerField(u'是否开启GPU',default=0,null=True)
    hostType = models.CharField(u'主机类型',default="",max_length=10,null=True)
    hotplugFeature = models.BooleanField(u'是否热插拔特性',default=False,max_length=10)
    privateSubnetId = models.CharField(u'私有子网id',default="",max_length=20,null=True)
    privateIP = models.CharField(u'',default="",max_length=20,null=True)
    privateVPCId = models.CharField(u'子网VPCid',default="",max_length=20,null=True)
    publicBandwidth = models.IntegerField(u'公共带宽',default=0,null=True)
    publicIP = models.CharField(u'公共IP',default="",max_length=20,null=True)
    publicIPId = models.CharField(u'公共IPid',default="",max_length=20,null=True)
    publicType = models.CharField(u'公共IP类型',default="",max_length=20,null=True)
    publicWeight = models.IntegerField(u'权重',default=0,null=True)
    imageId = models.CharField(u'镜像ID',default="",max_length=20,null=True)
    isExpire = models.CharField(u'是否过期',default="No",max_length=5,null=True)
    memory = models.IntegerField(u'内存',default=0,null=True)
    name = models.CharField(u'名称',default="",max_length=40,null=False)
    netCapFeature = models.BooleanField(default=False)
    netCapability = models.CharField(default="Normal",max_length=20,null=True)
    networkState = models.CharField(default="NotConnected",max_length=20,null=True)
    osName = models.CharField(default="",max_length=30,null=True)
    osType = models.CharField(default="",max_length=10,null=True)
    remark = models.CharField(default="",max_length=100,null=True)
    state = models.CharField(default="",max_length=15,null=True)
    storageType = models.CharField(default="",max_length=15,null=True)
    subnetType = models.CharField(default="",max_length=15,null=True)
    tag = models.CharField(default="",max_length=15,null=True)
    timemachineFeature = models.CharField(default="",max_length=5,null=True)
    totalDiskSpace = models.IntegerField(default=0,null=True)
    uHostId = models.CharField(default="",max_length=15,null=True)
    uHostType = models.CharField(default="",max_length=15,null=True)
    zone = models.CharField(default="",max_length=20,null=True)

    class Meta:
        db_table = 'ucloud_instance_info'


'''
腾讯云镜像model管理
'''
class QcloudImageInfo_Manager(models.Manager):
    pass


'''
腾讯云镜像相关信息
"ImageId": "img-50mr2ow7",
"OsName": "CentOS 6.2 64位",
"ImageSize": 50,
"ImageType": "PUBLIC_IMAGE",
"CreatedTime": null,
"ImageState": "NORMAL",
"ImageSource": "OFFICIAL",
"ImageName": "CentOS 6.2 64位",
"ImageDescription": "CentOS 6.2 64位",
"ImageCreator": null,
"OperationMask": 7
名称 	            类型 	是否必选 	描述
ImageId 	        String 	    否 	    镜像ID
OsName 	            String 	    否 	    操作系统名称
ImageSize 	        String 	    否 	    操作系统容量（GiB）
ImageType 	        Integer 	否 	    镜像类型
CreatedTime 	    String 	    否 	    创建时间
ImageState 	        String 	    否 	    镜像状态
ImageName 	        String 	    否 	    镜像名称
ImageDescription 	String 	    否 	    镜像详细描述
ImageSource 	    String 	    否 	    镜像来源。
ImageCreator 	    String 	    否 	    镜像创建者
'''
class QcloudImageInfo (models.Model):
    image_id = models.CharField(u"镜像id", max_length=50)
    osname = models.CharField(u"操作系统名称", max_length=50)
    image_size = models.CharField(u"操作系统容量（GiB）", max_length=50)
    image_type = models.IntegerField(u"镜像类型")
    created_time = models.CharField(u"镜像创建时间", max_length=50)
    image_state = models.CharField(u"镜像状态", max_length=50)
    image_source = models.CharField(u"镜像来源", max_length=50)
    image_name = models.CharField(u"镜像名称", max_length=50)
    image_description = models.CharField(u"镜像详细描述", max_length=50)
    image_creator = models.CharField(u"镜像创建者", max_length=50)
    operation_mask = models.CharField(u"", max_length=50)
    # 自定义表名称
    class Meta:
        db_table = 'qcloud_image_info'

    objects = QcloudImageInfo_Manager()

"""
腾讯云实例model管理
"""
class QcloudInstanceInfo_Manager(models.Manager):
    def findAllInstanceIds(self):
        queryStr = 'SELECT qii.instance_id FROM qcloud_instance_info qii '
        print queryStr
        cursor = connection.cursor()
        cursor.execute(queryStr)
        column_names = [d[0] for d in cursor.description]
        return [Row(zip(column_names, row)) for row in cursor]

    def findAllInstances(self):
        queryStr = "SELECT id,instance_id AS instanceId,instance_name AS instanceName,instance_type AS instanceType,cpu,memory,`status`,zone,instance_charge_type AS instanceChargeType,private_ip_addresses AS privateIpAddresses,public_ip_addresses AS publicIpAddresses,image_id AS imageId,os_name AS osName,system_disk_type AS systemDiskType,system_disk_size AS systemDiskSize,renew_flag AS renewFlag,internet_max_bandwidth_out AS internetMaxBandwidthOut,instance_charge_type AS instanceChargeType,date_format(created_time, '%Y-%m-%d %H:%i:%s') AS createdTime,date_format(expired_time, '%Y-%m-%d %H:%i:%s') AS expiredTime FROM qcloud_instance_info"
        print queryStr
        cursor = connection.cursor()
        cursor.execute(queryStr)
        column_names = [d[0] for d in cursor.description]
        return [Row(zip(column_names, row)) for row in cursor]

"""
腾讯云  虚拟机实例
{
    "Placement": {
        "Zone": "ap-shanghai-1",
        "HostId": null,
        "ProjectId": 0
    },
    "InstanceId": "ins-42jzxh5x",
    "InstanceType": "S1.SMALL1",
    "CPU": 1,
    "Memory": 1,
    "InstanceName": "qcloud_test",
    "InstanceChargeType": "PREPAID",
    "SystemDisk": {
        "DiskType": "CLOUD_BASIC",
        "DiskId": "disk-g6l12c05",
        "DiskSize": 50
    },
    "DataDisks": null,
    "PrivateIpAddresses": [
        "172.17.16.17"
    ],
    "PublicIpAddresses": [
        "182.254.155.148"
    ],
    "InternetAccessible": {
        "InternetMaxBandwidthOut": 1,
        "InternetChargeType": "BANDWIDTH_PREPAID"
    },
    "VirtualPrivateCloud": {
        "VpcId": "vpc-06b67wju",
        "SubnetId": "subnet-68qy40hn",
        "AsVpcGateway": false
    },
    "ImageId": "img-31tjrtph",
    "OsName": "CentOS 7.2 64位",
    "RenewFlag": "NOTIFY_AND_MANUAL_RENEW",
    "CreatedTime": "2017-08-08T02:13:18Z",
    "ExpiredTime": "2017-09-08T02:13:22Z"
Placement 	            Placement 	            否 	实例所在的位置。
InstanceId 	            String 	                否 	实例ID。
InstanceType 	        String 	                否 	实例机型。
CPU 	                Integer 	            否 	实例的CPU核数，单位：核。
Memory 	                Integer 	            否 	实例内存容量，单位：GB。
InstanceName 	        String 	                否 	实例名称。
InstanceChargeType 	    String 	                否 	实例计费模式。取值范围：PREPAID：表示预付费，即包年包月
                                                                           POSTPAID_BY_HOUR：表示后付费，即按量计费
                                                                           CDHPAID：CDH付费，即只对CDH计费，不对CDH上的实例计费。
SystemDisk 	            SystemDisk 	            否 	实例系统盘信息。
DataDisks 	            array of DataDisk objects 	否 	实例数据盘信息。只包含随实例购买的数据盘。
PrivateIpAddresses 	    array of Strings 	    否 	实例主网卡的内网IP列表。
PublicIpAddresses 	    array of Strings 	    否 	实例主网卡的公网IP列表。
InternetAccessible 	    InternetAccessible 	    否 	实例带宽信息。
VirtualPrivateCloud 	VirtualPrivateCloud 	否 	实例所属虚拟私有网络信息。
ImageId 	            String 	                否 	生产实例所使用的镜像ID。
RenewFlag 	            String 	                否 	自动续费标识。取值范围：NOTIFY_AND_MANUAL_RENEW：表示通知即将过期，但不自动续费
                                                                          NOTIFY_AND_AUTO_RENEW：表示通知即将过期，而且自动续费
                                                                          DISABLE_NOTIFY_AND_MANUAL_RENEW：表示不通知即将过期，也不自动续费。
CreatedTime 	        Timestamp 	            否 	创建时间。按照ISO8601标准表示，并且使用UTC时间。格式为：YYYY-MM-DDThh:mm:ssZ。
ExpiredTime 	        Timestamp 	            否 	到期时间。按照ISO8601标准表示，并且使用UTC时间。格式为：YYYY-MM-DDThh:mm:ssZ。
}

PENDING 	准备中
RUNNING 	运行中
STOPPED 	已停止
REBOOTING 	重启中
STARTING 	启动中
STOPPING 	停止中
EXPIRED 	已过期
TERMINATING 	退还中
TERMINATED 	已退还
"""
class QcloudInstanceInfo (models.Model):
    instance_id = models.CharField(u"实例id", max_length=50 ,unique= True)
    instance_name = models.CharField(u"实例名称", max_length=50)
    instance_type = models.CharField(u"实例类型", max_length=50)
    cpu = models.IntegerField(u"cpu")
    memory = models.IntegerField(u"内存")
    status = models.CharField(u"实例状态(PENDING准备中,RUNNING运行中,STOPPED已停止,REBOOTING重启中,STARTING启动中,STOPPING停止中,EXPIRED已过期,TERMINATING退还中,TERMINATED已退还)", max_length=50 ,default='RUNNING')
    zone = models.CharField(u"实例所属地域", max_length=50)
    instance_charge_type = models.CharField(u"实例计费模式", max_length=50)
    private_ip_addresses = models.CharField(u"内网ip", max_length=50)
    public_ip_addresses = models.CharField(u"外网ip", max_length=50)
    image_id = models.CharField(u"镜像id", max_length=50)
    os_name = models.CharField(u"操作系统名称", max_length=50)
    system_disk_type = models.CharField(u"系统盘类型", max_length=50)
    system_disk_size = models.CharField(u"系统盘尺寸", max_length=50)
    renew_flag = models.CharField(u"自动续费标识", max_length=50)
    internet_max_bandwidth_out = models.CharField(u"实例网络带宽上限", max_length=50)
    internet_charge_type = models.CharField(u"实例网络计费类型", max_length=50)
    created_time = models.DateTimeField(u"实例创建时间", default=timezone.now)
    expired_time = models.DateTimeField(u"实例到期时间", default=timezone.now)
    # 自定义表名称
    class Meta:
        db_table = 'qcloud_instance_info'

    objects = QcloudInstanceInfo_Manager()

"""
阿里云实例model管理
"""
class aliyunInstanceInfo_Manager(models.Manager):
    def findAllInstanceIds(self):
        queryStr = 'SELECT qii.instance_id FROM aliyun_instance_info qii '
        print queryStr
        cursor = connection.cursor()
        cursor.execute(queryStr)
        column_names = [d[0] for d in cursor.description]
        return [Row(zip(column_names, row)) for row in cursor]
    def findAllInstances(self):
        queryStr = "SELECT id,instance_id AS instanceId,instance_name AS instanceName,inner_ip_address AS inner_ip_address,instance_type AS instanceType,cpu,memory,`status`,zone,instance_charge_type AS instanceChargeType,image_id AS imageId,internet_max_bandwidth_out AS internetMaxBandwidthOut,instance_charge_type AS instanceChargeType,date_format(created_time, '%Y-%m-%d %H:%i:%s') AS createdTime,date_format(expired_time, '%Y-%m-%d %H:%i:%s') AS expiredTime FROM aliyun_instance_info"
        print queryStr
        cursor = connection.cursor()
        cursor.execute(queryStr)
        column_names = [d[0] for d in cursor.description]
        return [Row(zip(column_names, row)) for row in cursor]

"""
 "Instances": {
    "Instance": [
      {
        "CreationTime": "2015-07-27T07:08Z",
        "DeviceAvailable": true,
        "EipAddress": {},
        "ExpiredTime": "2011-09-08T16:00Z",
        "HostName": "iZ94t3s0jxkZ",
        "ImageId": "centos6u5_64_20G_aliaegis_20150130.vhd",
        "InnerIpAddress": {
          "IpAddress": [
            "10.170.106.80"
          ]
        },
        "InstanceChargeType": "PostPaid",
        "InstanceId": "i-94t3s0jxk",
        "InstanceName": "dd\u6027\u80fd\u6d4b\u8bd5",
        "InstanceNetworkType": "classic",
        "InstanceType": "ecs.s2.large",
        "InternetChargeType": "PayByTraffic",
        "InternetMaxBandwidthIn": -1,
        "InternetMaxBandwidthOut": 1,
        "IoOptimized": false,
        "OperationLocks": {
          "LockReason": []
        },
        "PublicIpAddress": {
          "IpAddress": [
            "120.25.13.106"
          ]
        },
        "RegionId": "cn-shenzhen",
        "SecurityGroupIds": {
          "SecurityGroupId": [
            "sg-94kd0cyg0"
          ]
        },
        "SerialNumber": "51d1353b-22bf-4567-a176-8b3e12e43135",
        "Status": "Running",
        "VpcAttributes": {
          "PrivateIpAddress": {
            "IpAddress": []
          }
        },
        "ZoneId": "cn-shenzhen-a"
      }
    ]
  },
  "PageNumber": 1,
  "PageSize": 10,
  "RequestId": "14A07460-EBE7-47CA-9757-12CC4761D47A",
  "TotalCount": 1
"""
class aliyunInstanceInfo (models.Model):
    instance_id = models.CharField(u"实例id", max_length=50 ,unique= True)
    instance_name = models.CharField(u"实例名称", max_length=50)
    description = models.CharField(u"实例描述",max_length=50)
    image_id = models.CharField(u"镜像id", max_length=50)
    region_id= models.CharField(u"实例所属地域ID",max_length=50)
    zone = models.CharField(u"实例所属地域", max_length=50)
    cpu = models.IntegerField(u"cpu")
    memory = models.IntegerField(u"内存")
    instance_type = models.CharField(u"实例类型", max_length=50)
    instance_type_family = models.CharField(u"实例规格族",max_length=50)
    hostname=models.CharField(u"实例机器名称",max_length=50)
    serial_number = models.CharField(u"实例机器的序列号",max_length=50)
    status = models.CharField(u"实例状态(PENDING准备中,RUNNING运行中,STOPPED已停止,REBOOTING重启中,STARTING启动中,STOPPING停止中,EXPIRED已过期,TERMINATING退还中,TERMINATED已退还)", max_length=50 ,default='RUNNING')
    security_group_ids = models.CharField(u"实例所属安全组的集合",max_length=200)
    public_ip_address= models.CharField(u"实例的公网 IP 地址",max_length=200)
    internet_max_bandwidth_in = models.CharField(u"实例网络带宽下限", max_length=50)
    internet_max_bandwidth_out = models.CharField(u"实例网络带宽上限", max_length=50)
    internet_charge_type = models.CharField(u"实例网络计费类型", max_length=50)
    created_time = models.DateTimeField(u"实例创建时间", default=timezone.now)
    vpc_attributes = models.CharField(u"专有网络属性",max_length=50)
    eip_address = models.CharField(u"弹性公网 IP 绑定信息",max_length=50)
    inner_ip_address=models.CharField(u"innerip",max_length=50)
    instance_network_type=models.CharField(u"实例实例网络类型。取值范围：Classic Vpc",max_length=50)
    operation_locks = models.CharField(u"锁定列表",max_length=200)
    instance_charge_type = models.CharField(u"实例计费模式PrePaid：预付费，即包年包月 PostPaid：后付费，即按量付费", max_length=50)
    spot_strategy=models.CharField(u"后付费实例的竞价策略 ",max_length=200)
    device_available = models.CharField(u"实例是否还可以挂载磁盘",max_length=50)
    deployment_setId = models.CharField(u"部署集 ID",max_length=50)
    network_interfaces = models.CharField(u"实例包含的弹性网卡集合",max_length=200)
    io_optimized = models.CharField(u"是否是 I/O 优化型实例",max_length=50)
    expired_time = models.DateTimeField(u"实例到期时间", default=timezone.now)
    key_pair_name = models.CharField(u"密钥对名称",max_length=200)

    # 自定义表名称
    class Meta:
        db_table = 'aliyun_instance_info'

    objects = aliyunInstanceInfo_Manager()


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)