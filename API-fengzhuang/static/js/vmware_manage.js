/**
 * Created by heidsoft on 2017/6/16.
 * @description vcenter配置操作模块
 */



//vcenter 管理插件
var VCenterManage = (function ($,toastr) {
    // progressbar
    var progressbarShow;
    return {
        //初始化虚拟机表格对象
        vmTable:null,
        //被选择记录ID
        selectedRows:[],
        //初始化虚拟机表格
        init:function (tableId,op) {

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

            var VCenterManageRecord = $(tableId).DataTable({
                destroy:true,
                paging: true, //隐藏分页
                ordering: false, //关闭排序
                info: false, //隐藏左下角分页信息
                searching: false, //关闭搜索
                pageLength : 5, //每页显示几条数据
                lengthChange: false, //不允许用户改变表格每页显示的记录数
                language: language, //汉化
                sLoadingRecords:true,

                ajax: {
                    url: site_url+'vmware/api/getVcenterVirtualMachineList',
                    data:{
                       opVal: op ,
                       typeVal: function () { return $(type).val();},
                       account: function () {return $(user_account).val();}
                    }
                },
                'columnDefs': [
                    {
                        'targets': 0,
                        'className': 'dt-head-center dt-body-center',
                        'checkboxes': {
                            'selectRow': true
                        }
                    }
                ],
                // select: {
                //     style:    'os',
                //     selector: 'td:first-child'
                // },
                //多选
                'select': {
                    'style': 'multi'
                },
                columns: [
                    {
                        data: "id",
                    },
                    {
                        title : '名称',
                        data: "name",
                    },
                    {
                        title : '内存(MB)',
                        data: "memorySizeMB",
                    },
                    {
                        title : 'CPU个数',
                        data: "numCpu",
                    },
                    {
                        title : '最大CPU使用',
                        data: "maxCpuUsage",
                    },
                    {
                        title : '最大内存使用',
                        data: "maxMemoryUsage",
                    },
                    {
                        title : '是否为模板',
                        data: "template",
                        render: function ( data, type, row ) {
                            if(data === false){
                                return "不是模板";
                            }else{
                                return "是模板";
                            }

                        },
                    },
                    {
                        title : '系统类型',
                        data: "guest_fullname",
                    },
                    {
                        title : '运行状态',
                        data: "power_state",
                        render: function ( data, type, row ) {

                            if(data === 'poweredOn'){
                                return "运行";
                            }else if(data === 'poweredOff'){
                                return "关机";
                            }else if(data === 'suspended'){
                                return "挂起" ;
                            }

                        },
                    },
                    {
                        title : '总体状态',
                        data: "overallStatus",
                        render: function ( data, type, row ) {
                            if(data === 'green'){
                                return "正常";
                            }else if (data === 'yellow'){
                                return "警告";
                            }else if (data === 'red'){
                                return "严重";
                            }
                            else{
                                return data;
                            }
                        },
                    },
                    {
                        title : 'IP',
                        data: "ipaddress",
                    }
                    //
                    // {
                    //     title : '操作',
                    //     data: "id",
                    //     render: function ( data, type, row ) {
                    //         var opHTML='<a class="king-btn king-info" onclick="VCenterManage.lookup('+data+')">查看详情</a>';
                    //         return opHTML;
                    //     },
                    // },
                ],
            });


            this.vmTable = VCenterManageRecord;

            //设置button
            new $.fn.dataTable.Buttons( VCenterManageRecord, {
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
            var tableContainer = VCenterManageRecord.buttons().container();
            tableContainer.appendTo(
                VCenterManageRecord.table().container()
            );

            return VCenterManageRecord;
        },
        //操作动作前置条件
        beforeAction:function(){
            var rows_selected = this.vmTable.column(0).checkboxes.selected();
            if(typeof rows_selected === 'undefined' || rows_selected.length === 0){
                toastr.warning("请选择虚拟机资源");
                setTimeout(function(){
                    progressbarShow.remove();
                },300);
                return false
            }
            var rowIds = this.selectedRows =[];
            $.each(rows_selected, function(index, rowId){
                rowIds.push(rowId);
            });
            this.selectedRows = rowIds;
            return true
        },

        //创建虚拟机
        create:function () {
            //toastr.warning("这是高级功能，蓝鲸社区版暂不支持该功能,如果需要请联系OneOaaS");

            //return
            console.log(123);
            $.ajax({
                url: site_url+'vmware/api/create',
                type: 'post',
                dataType:'json',
                data: {
                    "vmId":this.selectedRows,
                },
                success: function (data) {
                    toastr.success(data.message);
                }
            });
            $('#createVmWizard').modal('show');
        },
        //克隆虚拟机
        clone:function () {
            VCenterManage.progressbarModal();
            if(!this.beforeAction()){
                return
            }
            if(this.selectedRows.length>1){
                toastr.warning("蓝鲸版克隆操作只支持选择一台虚拟机");
                progressbarShow.remove();
                return
            }
            $('#cloneVmWizard').modal('show');
            progressbarShow.remove();

        },
        //执行克隆
        executeClone:function () {
            var cloneVmName = $("#cloneVmName").val();
            var select_datacenter = $("#select_datacenter .select2_box").select2("val");
            var select_cluster = $("#select_cluster .select2_box").select2("val");
            var select_datastore = $("#select_datastore .select2_box").select2("val");
            $.ajax({
                url: site_url+'vmware/api/clone',
                type: 'post',
                dataType:'json',
                data: {
                    "vmId":this.selectedRows[0],
                    "vmName":cloneVmName,
                    "vmDatacenter":select_datacenter,
                    "vmCluster":select_cluster,
                    "vmDatastore":select_datastore,
                },
                success: function (data) {
                    $('#cloneVmWizard').modal('hide');
                    toastr.success(data.message);
                    VCenterManage.vmTable.ajax.reload( null, false );

                }
            });
        },
        //关闭虚拟机
        poweroff: function (data) {
            VCenterManage.progressbarModal();
            if(!this.beforeAction()){
                return
            }

            if(this.selectedRows.length>1){
                toastr.warning("蓝鲸版关机操作只支持一台虚拟机");
                progressbarShow.remove();
                return
            }

            // var progressTimer,
            //     progressbar = $( "#progressbar" ),
            //     progressLabel = $( ".progress-label" ),
            //     dialogButtons = [{
            //         text: "Cancel Download",
            //         click: closeDownload
            //     }],
            //     dialog = $( "#dialog" ).dialog({
            //         autoOpen: false,
            //         closeOnEscape: false,
            //         resizable: false,
            //         buttons: dialogButtons,
            //         open: function() {
            //             progressTimer = setTimeout( progress, 2000 );
            //         },
            //         beforeClose: function() {
            //             downloadButton.button( "option", {
            //                 disabled: false,
            //                 label: "Start Download"
            //             });
            //         }
            //     }),
            //     downloadButton = $( "#downloadButton" )
            //         .button()
            //         .on( "click", function() {
            //             $( this ).button( "option", {
            //                 disabled: true,
            //                 label: "Downloading..."
            //             });
            //             dialog.dialog( "open" );
            //         });
            //
            // progressbar.progressbar({
            //     value: false,
            //     change: function() {
            //         progressLabel.text( "Current Progress: " + progressbar.progressbar( "value" ) + "%" );
            //     },
            //     complete: function() {
            //         progressLabel.text( "Complete!" );
            //         dialog.dialog( "option", "buttons", [{
            //             text: "Close",
            //             click: closeDownload
            //         }]);
            //         $(".ui-dialog button").last().trigger( "focus" );
            //     }
            // });
            //
            // function progress() {
            //     var val = progressbar.progressbar( "value" ) || 0;
            //
            //     progressbar.progressbar( "value", val + Math.floor( Math.random() * 3 ) );
            //
            //     if ( val <= 99 ) {
            //         progressTimer = setTimeout( progress, 50 );
            //     }
            // }
            //
            // function closeDownload() {
            //     clearTimeout( progressTimer );
            //     dialog
            //         .dialog( "option", "buttons", dialogButtons )
            //         .dialog( "close" );
            //     progressbar.progressbar( "value", false );
            //     progressLabel
            //         .text( "Starting download..." );
            //     downloadButton.trigger( "focus" );
            // }


            $.ajax({
                url: site_url+'vmware/api/poweroff',
                type: 'post',
                dataType: 'json',
                data: {
                    "vmId":this.selectedRows[0],
                },
                success: function (data) {
                    progressbarShow.remove();
                    toastr.success(data.message);
                    //重新刷新表格数据
                    VCenterManage.vmTable.ajax.reload( null, false );
                }
            });
        },
        //开启虚拟机
        start: function (data) {
            VCenterManage.progressbarModal();
            if(!this.beforeAction()){
                return
            }
            if(this.selectedRows.length>1){
                toastr.warning("蓝鲸版开机操作只支持一台虚拟机");
                progressbarShow.remove();
                return
            }
            $.ajax({
                url: site_url+'vmware/api/start',
                type: 'post',
                dataType: 'json',
                data: {
                    "vmId":this.selectedRows[0],
                },
                success: function (data) {
                    progressbarShow.remove();
                    toastr.success(data.message);
                    VCenterManage.vmTable.ajax.reload( null, false );
                },
                error:function () {
                    progressbarShow.remove();
               }
            });
        },
        //重启虚拟机
        reboot: function (data) {
            VCenterManage.progressbarModal();
            if(!this.beforeAction()){
                return
            }
            if(this.selectedRows.length>1){
                toastr.warning("蓝鲸版重启操作只支持一台虚拟机");
                progressbarShow.remove();
                return
            }
            $.ajax({
                url: site_url+'vmware/api/reboot',
                type: 'post',
                dataType: 'json',
                data: {
                    "vmId":this.selectedRows[0],
                },
                success: function (data) {
                    progressbarShow.remove();
                    toastr.success(data.message);
                    VCenterManage.vmTable.ajax.reload( null, false );
                },
                error:function () {
                    progressbarShow.remove();
               }
            });
        },
        //销毁虚拟机
        destroy: function (data) {
            VCenterManage.progressbarModal();
            if(!this.beforeAction()){
                return
            }
            if(this.selectedRows.length>1){
                toastr.warning("蓝鲸版销毁操作只支持一台虚拟机");
                progressbarShow.remove();
                return
            }
            var vmwareDestroy = dialog({
                width: 260,
                title: '提示',
                content: '确认销毁？',
                okValue: '确定',
                ok: function() {
                    $.ajax({
                        url: site_url+'vmware/api/destroy',
                        type: 'post',
                        dataType: 'json',
                        data: {
                            "vmId":VCenterManage.selectedRows[0],
                        },
                        success: function (data) {
                            progressbarShow.remove();
                            toastr.success(data.message);
                            VCenterManage.vmTable.ajax.reload( null, false );
                        },
                        error:function () {
                            progressbarShow.remove();
                        }
                    });
                },
                cancelValue: '取消',
                cancel: function() {
                    progressbarShow.remove();
                },
                onshow: function() {},
            });
            vmwareDestroy.show();
        },
        snapshot:function () {

            if(!this.beforeAction()){
                return
            }
            if(this.selectedRows.length>1){
                toastr.warning("蓝鲸版克隆操作只支持选择一台虚拟机");
                return
            }


            $('#snapshotVmWizard').modal('show');



        },
        executeSnapshot:function () {
            var snapshotName = $("#snapshotName").val();
            var snapshotDesc = $("#snapshotDesc").val();
            $.ajax({
                url: site_url+'vmware/api/createVMSnapshot',
                type: 'post',
                dataType: 'json',
                data: {
                    "vmId":this.selectedRows[0],
                    "name":snapshotName,
                    "description":snapshotDesc,
                },
                success: function (data) {
                    $('#snapshotVmWizard').modal('hide');
                    if(data.result){
                        toastr.success(data.message);
                    }else{
                        toastr.error(data.message);
                    }
                }
            });
        },
        lookup: function (data) {
            console.log("查看详情1"+data);
        },
        //同步虚拟机
        async: function (data) {
            if(!this.beforeAction()){
                return
            }
            $.ajax({
                url: site_url+'vmware/api/asyncDemo',
                type: 'post',
                dataType: 'json',
                data: {
                    "id":this.selectedRows[0],
                },
                success: function (data) {
                    toastr.success(data.message);
                    VCenterManage.vmTable.ajax.reload( null, false );
                }
            });
        },
        //webssh控制台
        webssh:function () {
            VCenterManage.progressbarModal();
            window.location.href = site_url + "vmware/webssh/manage";
            //toastr.warning("这是高级功能，蓝鲸社区版暂不支持该功能,如果需要请联系OneOaaS");
            return
        },
        RDP:function () {
            toastr.warning("这是高级功能，蓝鲸社区版暂不支持该功能,如果需要请联系OneOaaS");
            return
        },
        // progressbarModal
        progressbarModal:function(){
            progressbarShow=dialog({
                cancel: false,
                padding: 0,
                width:500,
                content:'<div id="progressbar"></div>'
            });
            $( "#progressbar" ).progressbar({
                value: false
            });
            progressbarShow.showModal();
        },

    }
})($,window.toastr);

//扩展到jquery
//$.fn.extend(VCenterManage);

function open_vm_side(){
    var sideContent = $('#vm_side');
    sideContent.removeClass('hidden');
    getComputedStyle(document.querySelector('body')).display;
    sideContent.find('#close').addClass('open');
    sideContent.find('.shield-edit').addClass('open');
    sideContent.find('#shield-detail').removeClass('hidden');

    $('article.shield-content').css('overflow', 'hidden');
}

function close_vm_side(){
    var sideContent = $('#vm_side');
    sideContent.find('.shield-edit').removeClass('open').children('#shield-detail').addClass('hidden');
    sideContent.find('#close').removeClass('open');
    setTimeout(function(){
        sideContent.addClass('hidden');
        $('article.shield-content').css('overflow', 'auto');
    }, 300);

}


$(document).ready(function(){

    $("#ccAppList .select2_box").select2({
        ajax: {
            url: site_url+"vmware/api/getAppList",
            cache: false,
            //对返回的数据进行处理
            results: function(data){
                return data;
            }
        }
    })

    $("#select_datacenter .select2_box").select2({
        ajax: {
            url: site_url+"vmware/api/getAllDatacenter",
            cache: false,
            //对返回的数据进行处理
            results: function(data){
                return data;
            }
        }
    })

    $("#select_cluster .select2_box").select2({
        ajax: {
            url: site_url+"vmware/api/getAllCluster",
            cache: false,
            //对返回的数据进行处理
            results: function(data){
                return data;
            }
        }
    })

    $("#select_datastore .select2_box").select2({
        ajax: {
            url: site_url+"vmware/api/getAllDatastore",
            cache: false,
            //对返回的数据进行处理
            results: function(data){
                console.log(data);
                return data;
            }
        }
    })


    $('#createVmWizard').bootstrapWizard(
        {
            tabClass: 'nav nav-pills',
            onNext: function(tab, navigation, index) {
                console.log("onNext:"+index);
                console.log(navigation);
                console.log(tab);
                if(index==4){
                    //$('#rootwizard').bootstrapWizard('display', $('#stepid').val());
                }
            },
            onPrevious:function(tab, navigation, index) {
                console.log("onPrevious"+index);
                console.log("onPrevious"+index);
            }
        }
    );

    $('#rootwizard .finish').click(function() {
        alert('Finished!, Starting over!');
        //$('#rootwizard').find("a[href*='tab1']").trigger('click');
    });

    VCenterManage.init('#vcenter_manage_record',0);
    $("#ssearchBtn").on('click',function() {
        VCenterManage.init('#vcenter_manage_record',1);
    });
    $("#vm_side").find("#cancel").click(function(){
        close_vm_side();
    });
    //关闭侧边栏
    $('#close, #sideContent').on('click', function(event){
        if($(event.target).attr('data-type') == 'close') {
            close_vm_side();
        }
    });

    //表格行选中事件
    // VCenterManage.vmTable.on( 'select', function ( e, dt, type, indexes ) {
    //     if ( type === 'row' ) {
    //         var data = VCenterManage.vmTable.rows( indexes ).data().pluck( 'id' );
    //     }
    // } );

    // $('#vcenter_manage_record').on( 'click', 'tr', function () {
    //
    //     // if ( $(this).hasClass('selected') ) {
    //     //     $(this).removeClass('selected');
    //     // } else {
    //     //     VCenterManage.vmTable.$('tr.selected').removeClass('selected');
    //     //     $(this).addClass('selected');
    //     // }
    //
    //     var currentVm = VCenterManage.vmTable.row( this ).data();
    //
    //     //基于vue实例,使用单向数据绑定
    //     vm_view = new Vue({
    //         el: '#vm_side',
    //         data: {
    //             disk_data:[],//磁盘数据
    //             network_data:[],//网卡数据
    //             snapshot_data:[], //快照数据,
    //             vminfo:{}
    //         },
    //         created:function () {
    //             var _self=this;
    //             $.ajax({
    //                 url: site_url+'vmware/api/getVMSnapshotList',
    //                 type: 'get',
    //                 dataType:'json',
    //                 data: {
    //                     "vmId":currentVm.id,
    //                 },
    //                 success: function (data) {
    //                     console.log(data);
    //                     var tmp = [{"id":1,"name":"vm-snaphost01","time":"2017-07-21","description":"调试jvm快照","is_enabled":true},
    //                         {"id":2,"name":"vm-snaphost02","time":"2017-07-21","description":"调试jvm快照","is_enabled":true},
    //                         {"id":3,"name":"vm-snaphost03","time":"2017-07-21","description":"调试jvm快照","is_enabled":true}]
    //                     _self.snapshot_data = tmp;
    //                     console.log(_self.snapshot_data);
    //                     _self.vminfo = currentVm;
    //                 }
    //             });
    //         },
    //         mounted: function () {
    //
    //         },
    //         watch: {
    //
    //         },
    //         methods: {
    //
    //         }
    //     });
    //
    //     open_vm_side();
    //
    //
    // } );

})




