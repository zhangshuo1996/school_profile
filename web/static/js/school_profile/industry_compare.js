let industry_compare_bar_chart = getEChartsObject("this_industry_main_school_bar");
let school_industry_pie_chart = getEChartsObject("school_industry_pie");

load_school_industry_pie();
/**
 * 加载学校下行业分布饼图
 */
function load_school_industry_pie() {
    $.ajax({
        type: "get",
        url: "/school/profile/get_school_industry",
        data: {"school": school},
        dataType: "json",
        success: function (data) {

            set_pie_option(school_industry_pie_chart, pieOption, data);
            dispatch_pie(data["series"], industry);
        }
    })
}

/**
 * 行业分布饼图点击事件
 */
school_industry_pie_chart.on("click", function (params) {
    let industry = params.name;
    window.location.href = "/school/profile/industry_compare/" + school + "/" + industry;
});


load_industry_institution();
/**
 * 加载某一行业下的学院对比柱状图
 */
function load_industry_institution(){
    let industry_compare_option = {
        title: {
            text: '',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            // data: ['专利数量']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            // boundaryGap: [0, 0.01]
        },
        yAxis: {
            type: 'category',
            data: []
        },
        series: [
            {
                // name: '专利数量',
                type: 'bar',
                itemStyle: {
                    emphasis: {
                            barBorderRadius: 30
                        },
                    normal: {
                        barBorderRadius:[10, 10, 10, 10],
                        color: function (params) {
                            return COLOR_LIST[params.dataIndex];
                        }
                    }
                },
                barWidth: 15,
                data: []
            },
        ]
    };


    industry_compare_option.yAxis.data = data["school_institution_list"];
    industry_compare_option.series[0].data = data["patent_num_list"];
    industry_compare_bar_chart.setOption(industry_compare_option);
}


/**
 * 加载后 饼图默认突出显示
 *
 */
function dispatch_pie(industry_arr, industry) {
    debugger;
    // 找到industry的下标
    let dataIndex = 0;
    for(let i = 0; i < industry_arr.length; i++){
        if(industry_arr[i]["name"] == industry){
            dataIndex = i;
            break;
        }
    }
    school_industry_pie_chart.dispatchAction({
        type: "highlight",
        seriesIndex: 0,
        dataIndex: dataIndex
    })
}