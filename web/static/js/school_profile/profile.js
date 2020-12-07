
//--------------------------------------------------------------------- 饼图 ---------------------------------------------------------------------
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


//--------------------------------------------------------------------- 雷达图 ---------------------------------------------------------------------
let school_radar_chart = getEChartsObject("school-radar");

/**
 * 加载雷达图
 */
set_radar_option(
     [
                {text: '研究人员水平', max: 100},
                {text: '研究人员数量', max: 100},
                {text: '学校水平', max: 100},
                {text: '实验平台', max: 100},
                {text: '成果数量', max: 100},
            ],
    [10, 10, 10, 10, 10],
    school_radar_chart,
);



get_school_normalize_dimension_score();



/**
 * 获取学校归一化之后的各维度分数， 显示雷达图
 * @param school
 */
function get_school_normalize_dimension_score() {
    $.ajax({
        type: "get",
        url: "/school/profile/get_school_normalize_dimension_score",
        data: {"school": school},
        dataType: "json",
        success: function (json_data) {
            set_radar_option(
                 [
                            {text: '研究人员水平', max: 100},
                            {text: '研究人员数量', max: 100},
                            {text: '学校水平', max: 100},
                            {text: '实验平台', max: 100},
                            {text: '成果数量', max: 100},
                        ],
                [
                    json_data["researcher_level_score"],
                    json_data["researcher_num_score"],
                    json_data["school_level_score"],
                    json_data["lab_score"],
                    json_data["achieve_num"],
                ],
                school_radar_chart,
            );
        }
    })
}

//--------------------------------------------------------------------- 柱状图 ---------------------------------------------------------------------
// let institution_patent_chart = getEChartsObject("institution-patent-bar");


// get_institution_patent_num(school);

// let barOption = {
//     title: {
//         left: "center",
//         show: true
//     },
//     legend: {
//         type: "scroll",
//         data: [],
//         left: "center",
//         itemGap: 20,
//         bottom: 10
//     },
//     tooltip: {
//         trigger: 'axis',
//         axisPointer: {
//             type: 'shadow'
//         }
//     },
//     yAxis: {
//         type: 'value',
//         data: [],
//         axisTick: {
//             alignWithLabel: true
//         },
//
//     },
//     xAxis: {
//         type: 'category',
//         minInterval: 1,
//         axisLabel: {
//            interval:0,
//            rotate:20
//         }
//     },
//     itemStyle: {
//         barBorderRadius: 20,
//     },
//     series: [{data: []}],
//     color: COLOR_LIST,
// };

/*TODO: 待删除
获取各学院的专利数量, 显示柱状图
 */
function get_institution_patent_num(school){
    $.ajax({
        type: "get",
        url: "/school/profile/get_institution_patent_num",
        data: {"school": school},
        dataType: "json",
        success: function (json_data) {
            let patent_nums = json_data["series"];
            let institutions = json_data["institutions"];

            let split1 = institutions[2];
            let split2 = institutions[7];
            let value1 = patent_nums[0];
            let value2 = patent_nums[3];
            let value3 = patent_nums[8];

            let MyOption = {
                series : {
                    "data": patent_nums,
                    "type": "bar",
                    "barWidth": 10
                }
            };
            barOption.xAxis.data = institutions;
            barOption.grid = {
                 left: '20px',
                 right: '20px',
                bottom: '1%',
                containLabel: true
            };
            MyOption.series.markArea = {
                silent: true,
                data: [
                [{
                    yAxis:0,
                    itemStyle: {
                        color: "#74c476",
                    }
                }, {
                    xAxis: split1,
                    yAxis: value1
                }],
                [{
                    xAxis: split1,
                    yAxis:0,
                    itemStyle: {
                        color: "#a1d99b",
                    }
                }, {
                    xAxis: split2,
                    yAxis: value2
                }],
                [{
                    xAxis: split2,
                    yAxis:0,
                    itemStyle: {
                        color: "#c7e9c0",
                    }
                },{
                    yAxis:value3,
                }
                ],
                    ]
            };
            // set_option(institution_patent_chart, barOption, MyOption);
        }
    })
}


/**TODO: 待删除
 * 柱状图点击事件, 跳转至学院画像
 */
// institution_patent_chart.on("click", function (params) {
//     let institution = params.name;
//     window.location.href = "/school/profile/institution_profile/" + school + "/" + institution;
// });
