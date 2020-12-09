
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


