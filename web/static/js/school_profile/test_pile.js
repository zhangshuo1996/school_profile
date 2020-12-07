let pile_chart = getEChartsObject("institution-patent-bar");
let institution_list=data["institution_list"];
let industry_institution_list_dict = data["industry_institution_list_dict"];
function construct_series(pile_option) {
    let series = [];
    let industry_list = [];
    for(let key in industry_institution_list_dict){
        industry_list.push(key);
        series.push({
            name: key,
            type: 'bar',
            stack: '总量',
            barWidth: 20,
            barGap: "150%",
            label: {
                show: false,
                position: 'insideRight'
            },
            data: industry_institution_list_dict[key]
        })
    }
    pile_option.series = series;

    pile_option.legend.data = industry_list;
    pile_option.xAxis.data = institution_list;
    set_pile_option(pile_chart, pile_option);
}
let pile_option = {
    color: [
        '#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83',
        '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3', 'rgb(250, 235, 215, 1)',
        'rgb(127, 255, 212, 1)', 'rgb(240, 255, 255, 1)', 'rgb(0, 0, 0, 1)', 'rgb(255, 235, 205, 1)',
        'rgb(0, 0, 255, 1)', 'rgb(138, 43, 226, 1)', 'rgb(165, 42, 42, 1)', 'rgb(222, 184, 135, 1)',
        'rgb(95, 158, 160, 1)', 'rgb(127, 255, 0, 1)', 'rgb(210, 105, 30, 1)', 'rgb(255, 127, 80, 1)',
        'rgb(0, 0, 139, 1)', 'rgb(0, 139, 139, 1)', 'rgb(184, 134, 11, 1)', 'rgb(169, 169, 169, 1)',
        'rgb(233, 150, 122, 1)', 'rgb(143, 188, 143, 1)', 'rgb(72, 61, 139, 1)', 'rgb(47, 79, 79, 1)',
        'rgb(0, 191, 255, 1)', 'rgb(105, 105, 105, 1)', 'rgb(105, 105, 105, 1)', 'rgb(30, 144, 255, 1)',
        'rgb(240, 255, 240, 1)', 'rgb(255, 105, 180, 1)', 'rgb(205, 92, 92, 1)', 'rgb(75, 0, 130, 1)',
        'rgb(255, 255, 240, 1)', 'rgb(240, 230, 140, 1)', 'rgb(230, 230, 250, 1)', 'rgb(255, 240, 245, 1)',
        'rgb(224, 255, 255, 1)', 'rgb(250, 250, 210, 1)', 'rgb(211, 211, 211, 1)', 'rgb(144, 238, 144, 1)',
        'rgb(211, 211, 211, 1)', 'rgb(255, 182, 193, 1)', 'rgb(255, 160, 122, 1)', 'rgb(32, 178, 170, 1)',
        'rgb(135, 206, 250, 1)', 'rgb(119, 136, 153, 1)', 'rgb(119, 136, 153, 1)', 'rgb(176, 196, 222, 1)',
        'rgb(255, 255, 224, 1)', 'rgb(0, 255, 0, 1)', 'rgb(50, 205, 50, 1)', 'rgb(250, 240, 230, 1)',
        'rgb(186, 85, 211, 1)', 'rgb(147, 112, 219, 1)', 'rgb(60, 179, 113, 1)', 'rgb(123, 104, 238, 1)',
        'rgb(245, 255, 250, 1)', 'rgb(255, 228, 225, 1)', 'rgb(255, 228, 181, 1)', 'rgb(255, 222, 173, 1)',
        'rgb(0, 0, 128, 1)', 'rgb(253, 245, 230, 1)', 'rgb(128, 128, 0, 1)', 'rgb(107, 142, 35, 1)',
        'rgb(255, 165, 0, 1)', 'rgb(255, 69, 0, 1)', 'rgb(218, 112, 214, 1)', 'rgb(238, 232, 170, 1)',
        'rgb(152, 251, 152, 1)', 'rgb(175, 238, 238, 1)', 'rgb(219, 112, 147, 1)', 'rgb(255, 239, 213, 1)',
        'rgb(255, 218, 185, 1)', 'rgb(205, 133, 63, 1)', 'rgb(255, 192, 203, 1)', 'rgb(221, 160, 221, 1)',
        'rgb(65, 105, 225, 1)', 'rgb(139, 69, 19, 1)', 'rgb(250, 128, 114, 1)', 'rgb(244, 164, 96, 1)',
        'rgb(46, 139, 87, 1)', 'rgb(255, 245, 238, 1)', 'rgb(160, 82, 45, 1)', 'rgb(192, 192, 192, 1)',
        'rgb(135, 206, 235, 1)', 'rgb(106, 90, 205, 1)', 'rgb(112, 128, 144, 1)', 'rgb(112, 128, 144, 1)',
        'rgb(255, 250, 250, 1)',  'rgb(0, 255, 127, 1)', 'rgb(70, 130, 180, 1)', 'rgb(210, 180, 140, 1)',
        'rgb(0, 128, 128, 1)', 'rgb(216, 191, 216, 1)', 'rgb(255, 99, 71, 1)', 'rgb(64, 224, 208, 1)',
        'rgb(238, 130, 238, 1)', 'rgb(245, 222, 179, 1)', 'rgb(255, 255, 255, 1)', 'rgb(245, 245, 245, 1)',
        'rgb(255, 255, 0, 1)', 'rgb(154, 205, 50, 1)'
    ],
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        formatter: function (params) {
            let data = "";
            for(let i=params.length - 1; i >= 0; i--){
                if(params[i]["value"] == 0){
                    continue;
                }
                data += "  " + params[i]["seriesName"] + " " + params[i]["value"] + "<br>";
            }
            return data;
        }
    },
    legend: {
        type: "scroll",
        orient: 'vertical',
        x: "right",
        y: 'center',
        data: ['交通学院', '建筑学院', '自动化学院', '仪器学院', '计算机学院']
    },
    grid: {
        top: '10%',
        left: '5%',
        right: '20%',
        bottom: 1,
        containLabel: true
    },
    yAxis: {
        type: 'value'
    },
    xAxis: {
        type: 'category',
        data: ['建筑行业', '土木行业', '仪器行业', '计算机行业', '水利行业', '设备制造', '人工智能算法'],
        axisLabel: {
           interval:0,
           rotate:20
        },
    },
    series: [
        {
            name: '交通学院',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [320, 302, 301, 334, 390, 330, 320]
        },
        {
            name: '建筑学院',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
            name: '自动化学院',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
            name: '仪器学院',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [150, 212, 201, 154, 190, 330, 410]
        },
        {
            name: '计算机学院',
            type: 'bar',
            stack: '总量',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [820, 832, 901, 934, 1290, 1330, 1320]
        }
    ]
};
// construct_series(pile_option);
$("#industry_compare").on("click", function () {
    construct_series(pile_option);
});
