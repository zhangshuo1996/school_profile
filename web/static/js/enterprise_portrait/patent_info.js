var dom = document.getElementById("container");

var myChart = echarts.init(dom);
var app = {};
option = null;


$(document).ready(function(){
     myChart.showLoading({
    　　text : '加载中',
    　　effect : 'whirling'
    });
   $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/get_patent_by_first_ipc",
        dataType: "json",
        success: function (json_data) {
            if (json_data['status']) {
                setOption(json_data['ipc_list'], json_data['ipc_count']);
            }

        },
        error: function (error) {
        }
    });
});


function second_ipc(){
    myChart.showLoading({
        　　text : '加载中',
        　　effect : 'whirling'
        });
    $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/get_patent_by_second_ipc",
        dataType: "json",
        success: function (json_data) {
            if (json_data['status']) {
                setOption(json_data['ipc_list'], json_data['ipc_count']);
            }

        },
        error: function (error) {
        }
    });
}


function third_ipc(){
    myChart.showLoading({
        　　text : '加载中',
        　　effect : 'whirling'
        });
    $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/get_patent_by_third_ipc",
        dataType: "json",
        success: function (json_data) {
            if (json_data['status']) {
                setOption(json_data['ipc_list'], json_data['ipc_count']);
            }
        },
        error: function (error) {
        }
    });
}


function setOption(data1, data2) {
    var dom = document.getElementById("container");
    var myChart = echarts.init(dom);
    option = {
        color: ['#3398DB'],
        tooltip: {
            trigger: 'axis',
            position:function(p){
                //其中p为当前鼠标的横纵坐标位置  调整位置基本满足要求 换行效果很丑 不适合
                if(p[0] < 750){
                    return [p[0], p[1] - 50];
                }
                return [p[0]-400, p[1] - 50];

            },
            formatter: function (params) {
                console.log(params)
                var res=''
                for(var i=0; i<Math.ceil(params[0].name.length/30);i++){
                    res+='<p>'+params[0].name.substring(i*10, i*10+40)+'</p>'
                }
                for(var i=0;i<params.length;i++){
                    console.log(params[i].seriesName+':'+params[i].data);
                    res+='<p>'+params[i].seriesName+':'+params[i].data+'</p>'
                }
                return res;
            },
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow',   // 默认为直线，可选为：'line' | 'shadow'
                axis: 'auto'
            },
            textStyle: {   // 提示框内容的样式
              align:"left"
            }
        },
        grid: {
            left: '5%',
            right: '5%',
            bottom: '30%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: data1,
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    interval:0,
                    formatter: function(name){
            　　　　    return name.slice(0, name.indexOf(":"));
            　　      }
                },
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '专利数量',
                type: 'bar',
                barWidth: '40%',
                data: data2
            }
        ]
    };
    ;
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
    myChart.hideLoading();
}
