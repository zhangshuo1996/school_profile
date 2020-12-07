let technicalFieldComparisonChart = getEChartsObject("chart-technical-field-comparison");
let teamGraphChart = getEChartsObject("chart-team-graph");
technicalFieldComparisonChart.showLoading();

let TeacherTeamOption = undefined, EngineerTeamOption = undefined;

//关系图属性
let graphOption = {
    tooltip: {},
    animation: true,
    color: ["#2c7be5", "#e6550d", "#31a354", "#756bb1", "#636363"],
    series: [
        {
            type: 'graph',
            layout: 'force',
            data: [],
            links: [],
            roam: true,
            focusNodeAdjacency: true,
            legendHoverLink: true,
            draggable: true,
            label: {
                normal: {
                    position: 'inside',
                    show: true,
                }
            },
            force: {
                repulsion: 100,//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                gravity: 0.05,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                edgeLength: [50, 100],//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] ,值越小则长度越长
                layoutAnimation: true
            },
            lineStyle: {
                show: true,
                color: 'target',//决定边的颜色是与起点相同还是与终点相同
                curveness: 0.1//边的曲度，支持从 0 到 1 的值，值越大曲度越大。
            }
        }
    ]
};

function getTechnicalFieldComparison() {
    $.ajax({
        type: "get",
        url: "/recommend/technicalFieldComparison",
        data: {"eid": ENGINEER_ID, "tid": TEACHER_ID, "team": TEAM},
        success: function (res) {
            if (res.success == false) {
                toggle_alert(false, res.message);
                return false;
            }
            let option = JSON.parse(JSON.stringify(pile_option));
            option.legend.data = [ENGINEER_TEAM, TEACHER_TEAM];
            option.xAxis[0].data = res.data.xAxis;
            option.xAxis[0].name = "类别";
            option.yAxis[0].name = "数量";
            option.series = [
                {
                    name: ENGINEER_TEAM,
                    type: "line",
                    areaStyle: {},
                    smooth: true,
                    data: res.data.eData,
                },
                {
                    name: TEACHER_TEAM,
                    type: "line",
                    areaStyle: {},
                    smooth: true,
                    data: res.data.tData,
                },
            ];
            option.color = ["#e6550d", "#2c7be5"];
            technicalFieldComparisonChart.setOption(option);
            technicalFieldComparisonChart.hideLoading();
        },
        error: function (error) {
            console.error(error);
        }
    });
}

function showTeamMembers(type = 0) {
    let option = type == 0 ? EngineerTeamOption : TeacherTeamOption;
    teamGraphChart.showLoading();
    if (option !== undefined) {
        teamGraphChart.setOption(option);
        teamGraphChart.hideLoading();
    } else {
        getTeamMembers();
    }

}

function getTeamMembers(type = 0) {
    $.ajax({
        type: "get",
        url: "/recommend/teamMembers",
        data: {"eid": ENGINEER_ID, "tid": TEACHER_ID},
        success: function (res) {
            TeacherTeamOption = JSON.parse(JSON.stringify(graphOption));
            EngineerTeamOption = JSON.parse(JSON.stringify(graphOption));

            EngineerTeamOption.series[0].links = res.engineer.links;
            TeacherTeamOption.series[0].data = res.teacher.nodes;
            TeacherTeamOption.series[0].links = res.teacher.links;

            let option  = type === 0? EngineerTeamOption:TeacherTeamOption;
            teamGraphChart.setOption(option);
            teamGraphChart.hideLoading();
        },
        error: function (error) {
            console.error(error);
        }
    });
}


function getLinkPath() {
    $.ajax({
        type: "get",
        url: "/link-path/path",
        // TODO
        data: {},
        success: function (res) {
            let LinkPathOption = JSON.parse(JSON.stringify(graphOption));
            LinkPathOption.series[0].data = res.data.nodes;
            LinkPathOption.series[0].links = res.data.links;
            LinkPathOption.series[0].symbolSize = 25;

            // teamGraphChart.setOption(TeacherTeamOption);
            // teamGraphChart.hideLoading();
        },
        error: function (error) {
            console.error(error);
        }
    });
}

getLinkPath()

getTechnicalFieldComparison();
getTeamMembers(0);