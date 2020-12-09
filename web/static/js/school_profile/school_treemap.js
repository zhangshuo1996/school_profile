let school_industry_level_compare_bubble_chart = getEChartsObject("school_industry_level_compare_bubble");

let institution_info_dict = {};


get_industry_num_by_level();


function get_industry_num_by_level(){
    $.ajax({
        type: "get",
        url: "/school/profile/get_institution_industry_patent_num2",
        data: {"school": school},
        dataType: "json",
        success: function (json_data) {
            institution_list = json_data["institution_list"];
            institution_info_dict = json_data["institution_info_dict"];
            result = json_data["result"];
            set_bubble_option(result);

        }
    })
}

function getLevelOption() {
        return [
            {
                itemStyle: {
                    borderWidth: 0,
                    gapWidth: 5
                },
            },
            {
                // upperLabel: {
                //     show: true,
                //     fontStyle: 'normal',
                //     color: "#000",
                //     position: "insideTopLeft",
                //     fontSize: 14,
                //     formatter: function (params) {
                //     }
                // },
                itemStyle: {
                    gapWidth: 1
                }
            },
            {
                colorSaturation: [0.35, 0.5],
                itemStyle: {
                    gapWidth: 1,
                    borderColorSaturation: 0.6
                }
            }
        ];
    }

function set_bubble_option(diskData){

    let formatUtil = echarts.format;

    let option = {

        title: {
            text: '学院-行业分布',
            left: 'center',
            show: false
        },
        legend:{
            show: true,
            data: institution_list,
        },

        tooltip: {
            formatter: function (info) {
                let value = info.value;
                let treePathInfo = info.treePathInfo;
                let treePath = [];

                for (let i = 1; i < treePathInfo.length; i++) {
                    treePath.push(treePathInfo[i].name);
                }
                return [
                    '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('\\')) + '</div>',
                    ' ' + value + ' ',
                ].join('');
            },
            transitionDuration:0,//echart防止tooltip的抖动

        },

        series: [
            {
                name: '学院-行业分布',
                type: 'treemap',
                visibleMin: 300,
                label: {
                    show: true,
                    formatter: ' {b}',
                    color: "rgba(13, 0, 0, 1)",
                    // fontWeight: "lighter",
                    fontSize: 15,
                    textBorderColor: "transparent",
                    textBorderWidth: 1,
                },
                itemStyle: {
                    borderColor: '#fff'
                },
                levels: getLevelOption(),
                data: diskData
            }
        ]
    };
    school_industry_level_compare_bubble_chart.setOption(option);
}

/**
 * 气泡图点击事件, 跳转至学院画像
 */
school_industry_level_compare_bubble_chart.on("click", function (params) {
    let institution = params.data.category;
    window.location.href = "/school/profile/institution_profile/" + school + "/" + institution;
});



