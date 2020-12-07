var industry_myChart = echarts.init(document.getElementById("industry_statistic"));

function get_industry_info() {
    $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/get_industry_info",
        dataType: "json",
        success: function (response) {
            if(response.status == true){
                set_industry_graph(response.industry_list, response.industry_count);
            }
        },
        error: function(){
            console.log("error")
        }
    });
}

function set_industry_graph(industry_list, industry_count){
    option = {
    color: ['#3398DB'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: ''        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            data: industry_list,
            axisTick: {
                alignWithLabel: true
            },
            axisLabel: {
               interval:0,
               rotate:40
            }
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [
        {
            name: '企业数量',
            type: 'bar',
            barWidth: '40%',
            data: industry_count
        }
    ]
};
    industry_myChart.setOption(option, true);
}

get_industry_info()
