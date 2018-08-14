$(document).ready(function() {

    var promise = $.ajax({
        url: site_url+'overview/getAnalysisDataRequest',
        type: 'post',
        dataType:'json',
        data: {},
    });

    promise.then(handleData,handleError);

    function handleData(data) {
        $('#memory_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series: [{
                name: '内存分布',
                type: 'pie',
                data: data.memroy
            }]
        });


        $('#cpu_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series: [{
                name: 'CPU分布',
                type: 'pie',
                data: data.cpu
            }]
        });

        $('#storage_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series:[{
                name: '存储分布',
                type: 'pie',
                data: data.storage
            }]

        });

        $('#flow_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series:[{
                name: 'CPU-Core分布',
                type: 'pie',
                data: data.cpuCores
            }]
        });
    }
    function handleError(error) {
        //处理错误
        // console.log(error);
        $('#memory_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series: [{
                name: '内存分布',
                type: 'pie',
                data: []
            }]
        });


        $('#cpu_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series: [{
                name: 'CPU分布',
                type: 'pie',
                data: []
            }]
        });

        $('#storage_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series:[{
                name: '存储分布',
                type: 'pie',
                data: []
            }]

        });

        $('#flow_analysis').kendoChart({
            legend:{
                position : "bottom"
            },
            theme : 'bootstrap',
            seriesDefaults: {
                labels: {
                    template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                    position: "outsideEnd",
                    visible: true,
                    background: "transparent"
                }
            },
            series:[{
                name: '虚拟机分布',
                type: 'pie',
                data: []
            }]
        });
    }

});
