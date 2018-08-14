//vcenter 管理插件
var AliyunManage = (function ($,toastr) {
    return {
        //初始化虚拟机表格对象
        vmTable:null,
        //被选择记录ID
        selectedRows:[],
        //初始化虚拟机表格
        init:function (tableId) {

            var language = {
                search: '搜索：',
                lengthMenu: "每页显示 _MENU_ 记录",
                zeroRecords: "没找到相应的数据！",
                info: "分页 _PAGE_ / _PAGES_",
                infoEmpty: "暂无数据！",
                infoFiltered: "(从 _MAX_ 条数据中搜索)",
                paginate: {
                    first: '<<',
                    last: '>>',
                    previous: '上一页',
                    next: '下一页',
                }
            }

            var AliyunManageRecord = $(tableId).DataTable({
                paging: true, //隐藏分页
                ordering: false, //关闭排序
                info: false, //隐藏左下角分页信息
                searching: false, //关闭搜索
                pageLength : 5, //每页显示几条数据
                lengthChange: false, //不允许用户改变表格每页显示的记录数
                language: language, //汉化
                ajax: {
                    url: site_url+'aliyun/api/getAliyunVmList',
                },
                columns: [
                    {
                        data: "instanceName",
                        title:"实例名称"
                    },
                    {
                        data: "instanceType",
                        title:"实例类型"
                    },
                    {
                        data: "cpu",
                        title:"CPU"
                    },
                    {
                        data: "memory",
                        title:"内存"
                    },
                    {
                        data: "status",
                        title:"状态"
                    },
                    {
                        data: "zone",
                        title:"区域"
                    },
                    {
                        data: "instanceChargeType",
                        title:"实例计费类型"
                    },
                    {
                        data: "inner_ip_address",
                        title:"内网IP"
                    },
                ],
            });

            this.vmTable = AliyunManageRecord;

            //设置button
            new $.fn.dataTable.Buttons( AliyunManageRecord, {
                buttons: [
                    {
                        extend: 'copyHtml5',
                        text: '拷贝表格'
                    },
                    {
                        extend: 'excelHtml5',
                        text: '导出Excel'
                    },
                    {
                        extend: 'pdfHtml5',
                        text: '导出PDF'
                    },
                    {
                        extend: 'csvHtml5',
                        bom: "utf-8",
                        text: '导出CSV'
                    },
                ],
            } );

            //将button放置到底部
            var tableContainer = AliyunManageRecord.buttons().container();
            tableContainer.appendTo(
                AliyunManageRecord.table().container()
            );

            return AliyunManageRecord;
        }
    }
})($,window.toastr);

//扩展到jquery
//$.fn.extend(QcloudManage);
//扩展函数


$(document).ready(function(){

    AliyunManage.init('#aliyun_manage_record');

})