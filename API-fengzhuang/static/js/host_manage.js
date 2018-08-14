/**
 * Created by heidsoft on 2017/6/16.
 * @description vcenter配置操作模块
 */


//vcenter 管理插件
var VCenterManage = (function ($,toastr) {
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

            var VCenterManageRecord = $(tableId).DataTable({
                paging: true, //隐藏分页
                ordering: false, //关闭排序
                info: false, //隐藏左下角分页信息
                searching: false, //关闭搜索
                pageLength : 5, //每页显示几条数据
                lengthChange: false, //不允许用户改变表格每页显示的记录数
                language: language, //汉化
                ajax: {
                    url: site_url+'vmware/api/getVcenterHostList',
                },
                columns: [
                    {
                        data: "name",
                        title:"主机名称"
                    },
                    {
                        data: "api_version",
                        title:"API版本"
                    },
                    {
                        data: "build",
                        title:"构建时间"
                    },
                    {
                        data: "full_name",
                        title:"全称"
                    },
                    {
                        data: "instance_uuid",
                        title:"uuid"
                    },
                    {
                        data: "locale_version",
                        title:"本地版本"
                    },
                    {
                        data: "vendor",
                        title:"厂商"
                    },
                    {
                        data: "version",
                        title:"版本"
                    },
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
        }
    }
})($,window.toastr);

//扩展到jquery
//$.fn.extend(VCenterManage);
//扩展函数

function open_host_side(){
    var sideContent = $('#host_side');
    sideContent.removeClass('hidden');
    getComputedStyle(document.querySelector('body')).display;
    sideContent.find('#close').addClass('open');
    sideContent.find('.shield-edit').addClass('open');
    sideContent.find('#shield-detail').removeClass('hidden');

    $('article.shield-content').css('overflow', 'hidden');
}

function close_host_side(){
    var sideContent = $('#host_side');
    sideContent.find('.shield-edit').removeClass('open').children('#shield-detail').addClass('hidden');
    sideContent.find('#close').removeClass('open');
    setTimeout(function(){
        sideContent.addClass('hidden');
        $('article.shield-content').css('overflow', 'auto');
    }, 300);

}

function make_single_graphs(){

    /*
    cpu.usage.maximum
    cpu.usage.minimum
    cpu.ready.summation
    cpu.capacity.contention.average

    mem.usage.minimum
    mem.usage.maximum

    disk.usage.minimum
    disk.usage.maximum

    net.usage.minimum
    net.usage.maximum
    */
    make_contain_graph($("#cpu_usage_maximum"),'cpu.usage.maximum','CPU最大利用率');
    make_contain_graph($("#cpu_usage_minimum"),'cpu.usage.minimum','CPU最小利用率');

    make_contain_graph($("#mem_usage_minimum"),'mem.usage.minimum','内存最小利用率');
    make_contain_graph($("#mem_usage_maximum"),'mem.usage.maximum','内存最大利用率');

    make_contain_graph($("#disk_usage_maximum"),'disk.usage.maximum','磁盘最大利用率');
    make_contain_graph($("#disk_usage_minimum"),'disk.usage.minimum','磁盘最小利用率');

    make_contain_graph($("#net_usage_minimum"),'net.usage.minimum','网络流量最小利用率');
    make_contain_graph($("#net_usage_maximum"),'net.usage.maximum','网络流量最大利用率');
    // $(".single-contain").each(function(){
    //
    // });
}

function make_contain_graph(contain, _type,_type_cn_name){
    var chart_div = contain.find(".line-chart");
    var host_id = chart_div.attr("data-host_id");
    if (!host_id){
        host_id = hosts_view.checked_host_index_table.id;
    }


    var params = {
        hostId: host_id,
        hostName: hosts_view.checked_host_index_table.name,
        metricName:_type,
        intervalId:86400,
        maxSample:86400,
        startTime:'',
        endTime:''
    };

    chart_div.html('<img class="graph-loading" alt="loadding" src="'+static_url+'img/hourglass_36.gif" style="margin-top: 75px;margin-left:45%;">');

    $.get(site_url+'vmware/api/getHostMonitorInfos', params, function(res){
        chart_div.html("");
        var chart_data ={
            series: [],
            x_axis: {
                "minRange": 1000,
                "type": "datetime"
            },
            chart_type: "spline",
            unit: "%",

        }
        if(res.result){

            var monitor_data = res.content.data;
            var x_axis_list_data = [];
            var series_info = {};
            var data_array =[];
            for (var i = 0; i <  monitor_data.length ; i++) {
                x_axis_list_data[i] = moment(monitor_data[i].unix_time).format('YYYY-MM-DD HH:mm:ss');
                var data_object=[];
                series_info[monitor_data[i].unix_time] = monitor_data[i].value;
                data_object[0] = monitor_data[i].unix_time*1000;
                data_object[1] = monitor_data[i].value;
                data_array[i] = data_object;
            }
            var serie_object = {
                x_axis_list:x_axis_list_data,
                data:data_array,
                name:_type_cn_name,
                type:"spline",
            }
            chart_data.series[0] = serie_object;
            Hchart.spline(chart_data, chart_div[0], series_info);
        }else{
            var error_tips_html = '<div class="chart-error">' +
                '<span class="error-mark">' +
                '<i class="fa fa-exclamation"></i>' +
                '</span><span class="error-text">'+
                res.message + '</span></div>';
            //chart_div.html(error_tips_html);
            chart_div.html(res.message);
        }
    }, 'json');
}


//基于vue实例,使用单向数据绑定
var hosts_view = new Vue({
    el: '#host_side',
    data: {
        checked_host_index_table:{},//选择主机
    },
    created:function () {

    },
    methods: {

    },
    watch: {
        'checked_host_index_table.length': {
            handler: function(newVal,oldVal) {
                if (this.checked_host_index_table.name !=='' ){
                    make_single_graphs();
                }
            },
            deep: true,
        },
    }

});



$(document).ready(function(){

    VCenterManage.init('#host_manage_record');

    $('#host_manage_record').on( 'click', 'tr:gt(0)', function () {
        var currentHost = VCenterManage.vmTable.row( this ).data();
        hosts_view.checked_host_index_table=currentHost;
        open_host_side();
    });

    $("#host_side").find("#cancel").click(function(){
        close_host_side();
    });


    $('#close, #sideContent').on('click', function(event){
        if($(event.target).attr('data-type') == 'close') {
            close_host_side();
        }
    });

})




