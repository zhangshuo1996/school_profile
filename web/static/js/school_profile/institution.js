let team_bar_chart = getEChartsObject("team_bar");
let institution_relation_chart = getEChartsObject("institution-relation");
let team_id_dict = {}; // 序号： team_id
let data = undefined;  // 后端传过来的关系原始数据
let expert_id = undefined;
let show_type = 1;  // show_type == 1：社区关系图， == 2 联系图
let teacher_id_name_dict;
let team_id_info_dict;
let team_id_color_dict = {};  // 团队对应的颜色字典
let leader_id_list = []; // 排序后的核心成员 id 列表
let team_id;
let graph_data; // 用于显示团队社区的数据
let COLOR_LIST = [
    "#636363", "#969696", "#bdbdbd",
    "#756bb1", "#9e9ac8",
    "#a1d99b", "#74c476", "#31a354",
    "#fdd0a2", "#fdae6b", "#fd8d3c", "#e6550d",
    "#9ecae1", "#6baed6", "#2c7be5",
];
show_community_relation();


/**
 * 复选框选择
 */
// $(".visit_status").on("click", function () {
//     if(expert_id === undefined){
//         return ;
//     }
//     // 清除所有的复选框
//     let check_box_arr = $(".visit_status");
//     for(let i = 0; i < check_box_arr.length; i++){
//         let check_box = $(check_box_arr[i]);
//         check_box.prop("checked", false);
//     }
//     // 渲染点击的复选框
//     let visit_status = $(this).val();
//     $(this).prop("checked", true);
//     // 更新后端的数据TODO:
//     $.ajax({
//         type: "get",
//         url: "/school/profile/update_node_visit_status",
//         data: {"teacher_id": expert_id, "visit_status": visit_status},
//         dataType: "json",
//         success: function () {
//             // 重新渲染联系图
//             data = undefined;
//             // show_link_relation();
//         }
//     })
// });


/**
 * 点击显示社区关系图
 */
// $("#institution-graph").on("click", function () {
//     show_type = 1;
//     $("#visit_status_card").attr("class", "d-none");
//     institution_relation_chart.clear();
//     show_community_relation();
// });



/**
 * 显示社区关系图
 */
function show_community_relation() {
    if(data === undefined){ // 如果关系数据未定义，请求关系数据
        get_institution_relation(1);
    }else{  // 如果关系数据已定义，直接使用
        let graph_data = convert_graph_data(data, 1);
        reloadGraph(graph_data, "force", 1);
    }
}


/**
 * 获取学院内部的关系数据
 */
function get_institution_relation() {
    // institution_relation_chart.showLoading();
    $.ajax({
        type: "get",
        url: "/school/profile/get_institution_relation",
        data: {"school": school, "institution": institution},
        dataType: "json",
        success: function (json_data) {
            data = json_data;
            graph_data = convert_graph_data(json_data);
            let team_info = construct_team_info(json_data);
            teacher_id_name_dict = team_info.teacher_id_name_dict;
            team_id_info_dict = team_info.team_id_info_dict;
            show_team_bar();
            // reloadGraph("force");
            show_team_patent_project_data();
            return true;
        }
    })
}

/**
 * 根据从图数据库中获取的数据 构造 团队的成员数量 和 成果数量数据
 */
function construct_team_info(json_data) {
    let nodes = json_data["nodes"];
    let teacher_id_name_dict = {};
    let team_id_info_dict = {};
    for(let i = 0; i < nodes.length; i++){
        let node = nodes[i];
        teacher_id_name_dict[node["id"]] = node["name"];
        if(team_id_info_dict.hasOwnProperty(node["team"])){
            team_id_info_dict[node["team"]]["patent"] += node["patent"];
            team_id_info_dict[node["team"]]["member_num"] += 1;
        }else{
            team_id_info_dict[node["team"]] = {
                "patent": node["patent"],
                "member_num": 1,
            }
        }
    }
    return {
        "teacher_id_name_dict": teacher_id_name_dict,
        "team_id_info_dict": team_id_info_dict
    }
}

/**
 * 显示学院团队 成员数量 与 成果数量 柱状图（竖着的）
 * @param sort_type : string
 * member_num 按成员数量排序， patent_num 按成果数量排序
 *
 */
function show_team_bar(sort_type="member_num") {
    let team_info = sort_member_info();
    let leader_id_list = team_info.leader_id_list;
    let vertical_bar_option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        transitionDuration:0,//echart防止tooltip的抖动
    },
    legend: {
        data: ['专利数量'],
        show: false
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            position: "top",
            type: 'value'
        }
    ],
    yAxis: [
        {
            type: 'category',
            axisTick: {
                show: false
            },
            data: []
        }
    ],
    series: [
        {
            name: '专利数量',
            type: 'bar',
            itemStyle: {
                normal: {
                    color: function (params) {
                        let dataIndex =  params.dataIndex;
                        let color = COLOR_LIST[dataIndex % COLOR_LIST.length];
                        let team_id = leader_id_list[dataIndex];

                        team_id_color_dict[team_id] = color;
                        return color;
                    }
                },
            },
            stack: '总量',
            label: {
                show: true
            },
            barWidth: 15,
            data: [320, 302, 341, 374, 390, 450, 420]
        },
    ]
};
    vertical_bar_option.yAxis[0].data = team_info.leader_name_list;
    vertical_bar_option.series[0].data = team_info.patent_list;
    // vertical_bar_option.series[1].data = team_info.member_num_list;

    console.log(vertical_bar_option);
    team_bar_chart.setOption(vertical_bar_option);
}

/**
 * 对学院中的团队 成员数量和成果数量两种方式排序
 * @param sort_type : string
 * member_num 按成员数量排序， patent_num 按成果数量排序
 */
function sort_member_info(sort_type="patent"){
    let sort_team_id_list = Object.keys(team_id_info_dict).sort(function(a,b){ return team_id_info_dict[a][sort_type]-team_id_info_dict[b][sort_type]; });
    // let leader_id_list = []; //  团队核心成员列表
    let leader_name_list = []; //  团队核心成员列表
    let patent_list = []; // 团队成果数量列表
    let member_num_list = []; // 团队人员数量列表
    for(let i in sort_team_id_list){
        let team_id = sort_team_id_list[i];
        if(teacher_id_name_dict[team_id] === undefined)
            continue;
        leader_name_list.push(teacher_id_name_dict[team_id] + "团队");
        leader_id_list.push(team_id);
        patent_list.push(team_id_info_dict[team_id]["patent"]);
        member_num_list.push(team_id_info_dict[team_id]["member_num"]);
    }
    team_id = leader_id_list[leader_id_list.length-1];
    return {
        "leader_id_list": leader_id_list,
        "leader_name_list": leader_name_list,
        "patent_list": patent_list,
        "member_num_list": member_num_list
    };
}


/**
 * 转换关系图数据
 */
function convert_graph_data(data) {
    let temp_links = data.links;
    let temp_nodes = data.nodes;
    let links = [];
    let nodes = [];
    let team_set = new Set();
    for(let i = 0; i < temp_nodes.length; i++){
        team_set.add(temp_nodes[i]["team"]);
    }
    let have_push_links_set = new Set();
    for(let i = 0; i < temp_links.length; i++){
        let source = String(temp_links[i]["source"]);
        let target = String(temp_links[i]["target"]);
        let s1 = source + "--" + target;
        let s2 = target + "--" + source;
        if(have_push_links_set.has(s1) || have_push_links_set.has(s2)){
            continue;
        }else{
            have_push_links_set.add(s1);
            have_push_links_set.add(s2);
        }
        links.push({
            source: source,
            target: target,
            paper:0,
            patent:0,
            project:0,
        });
    }
    let name_set = new Set();
    let normal_style = {};

    for(let i = 0; i < temp_nodes.length; i++){
        if(name_set.has(temp_nodes[i]["name"])) {
            continue;
        }
        if(!team_set.has(temp_nodes[i]["team"])){
            continue;
        }
        name_set.add(temp_nodes[i]["name"]);
        let category = undefined;
        if(show_type === 1){
            nodes.push({
                name: String(temp_nodes[i]["id"]),
                school: school,
                institution: temp_nodes[i]["institution"],
                label: temp_nodes[i]["name"],
                category: temp_nodes[i]["team"],
                patent: temp_nodes[i]["patent"],
                visit_status: temp_nodes[i]["visit_status"],
                draggable: true,
                symbolSize: get_node_size(temp_nodes[i]["patent"]),
                itemStyle: {
                    // normal: normal_style,
                }
            });
        }else{
            let visit_status = temp_nodes[i]["visit_status"];
            let visit_status_color = {0: '#2c7be5', 1: '#e6550d', 2: '#31a354', 3: '#756bb1', 4: '#636363'};
            category = visit_status;
            normal_style = {
                color: visit_status_color[visit_status],
            };
            nodes.push({
                name: String(temp_nodes[i]["id"]),
                school: school,
                institution: temp_nodes[i]["institution"],
                label: temp_nodes[i]["name"],
                category: category,
                patent: temp_nodes[i]["patent"],
                visit_status: temp_nodes[i]["visit_status"],
                draggable: true,
                symbolSize: get_node_size(temp_nodes[i]["patent"]),
                itemStyle: {
                    normal: normal_style,
                }
            });

        }
        // team_set.add(String(temp_nodes[i]["team"]));
    }
    let team_map = {};
    let index = 0;
    for(let team_id of team_set){
        let team_leader = get_team_principle(team_id, temp_nodes);
        if(team_leader === undefined){
            continue;
        }
        team_map[index] = team_leader;
        team_id_dict[team_id] = index++;
    }
    for(let i = 0; i < nodes.length; i++){
        let team_id = nodes[i]["category"];
        nodes[i]["team_id"] = team_id;
        nodes[i]["category"] = team_id_dict[team_id];
    }
    let return_nodes = [];
    if(show_type === 1){
        // 过滤掉nodes中category为undefined的
        for(let i = 0; i < nodes.length; i++){
            if(nodes[i].category !== undefined){
                return_nodes.push(nodes[i]);
            }
        }
    }else{
        return_nodes = nodes;
    }
    return {
        community: index,
        core_node: team_map,
        links: links,
        nodes: return_nodes,
        team_set: team_set
    };
}


//关系图属性
let graphOption = {
    tooltip: {
        formatter: function (params) {
            if (params.dataType === "node") {
                let shcool = params.data.school === undefined? school: params.data.school,
                    institution = params.data.institution === undefined? INSTITUTION_NAME: params.data.institution;
                //设置提示框的内容和格式 节点和边都显示name属性
                return `<strong>节点属性</strong><hr>姓名：${params.data.label}<br>所属学校：${shcool}<br>所属学院：${institution} <br> ${params.data.team_id}`;
            }
            else{
                return ""
            }

        },
        transitionDuration:0,//echart防止tooltip的抖动
    },
    // 图例
    legend: [],
    animation: true,
    series : [
        {
            type: 'graph',
            layout: 'force',
            data: [],
            links: [],
            categories: [],
            // // 边的长度范围
            // edgeLength: [10, 50],
            //是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            roam: true,
            // 默认缩放比例
            zoom: 0.8,
            // 当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            focusNodeAdjacency:false,
            // 是否启用图例 hover(悬停) 时的联动高亮。
            legendHoverLink : true,
            circular: {
                rotateLabel: true
            },
            // force: {
            //     repulsion: 100,
            // },

            label: {

                normal: {
                    show : true,
                    color: "#2c7be5",
                    borderWidth: 2,
                    fontSize: 15,
                    position: 'insideBottomRight',
                    //回调函数，显示用户名
                    formatter: function(params){
                        //TODO: 关系图与列表联动
                        if(params.data.team_id == team_id){
                            return params.data.label;
                        }else{
                            return "";
                        }
                    }
                }
            },
            force: {
                repulsion : [20,100],//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                gravity : 0.05,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                edgeLength :[20,100],//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
                layoutAnimation : true
            },
            itemStyle:{
                borderColor: '#fff',
                borderWidth: 1,
                shadowBlur: 10,
                shadowColor: 'rgba(10, 10, 10, 0.3)',
                normal: {
                    color: function (params) {
                        let team_id = params.data.team_id;
                        let color = team_id_color_dict[team_id];
                        return color;
                    }
                }
            },
            lineStyle: {
                show : true,
                color: 'target',//决定边的颜色是与起点相同还是与终点相同
                curveness: 0.1//边的曲度，支持从 0 到 1 的值，值越大曲度越大。
            }
        }
    ]
};


/**
 * 重新加载关系图数据，把数据赋值给graphOption中的data
 * @param data 关系图数据
 */
function reloadGraph(layout="circular"){
    let data = graph_data;
    if(!"nodes" in data) return;
    let links = data.links;
    //  给目前选择的团队中的leader 节点加上外边距
    let process_nodes = [];
    for(let i = 0; i < data.nodes.length; i++){
        let node = data.nodes[i];
        if(node["name"] == team_id){
            node.itemStyle = {
                borderWidth: 2,
                borderColor: "#e6550d",
                shadowBlur: 5
            }
        }else{
            node.itemStyle = {};
        }
        process_nodes.push(node);
    }


    graphOption.series[0].data = process_nodes;
    graphOption.series[0].links = links;
    graphOption.series[0].layout = layout;
    institution_relation_chart.clear();
    institution_relation_chart.setOption(graphOption);
    institution_relation_chart.hideLoading();
}


/**
 * 根据专利的数量 返回专家节点的大小
 *
 */
function get_node_size(patent_num) {
    if(patent_num < 5){
        return 10;
    }
    if(patent_num < 10){
        return 15;
    }
    if(patent_num < 20){
        return 20;
    }
    if(patent_num < 30){
        return 25;
    }else{
        return 30;
    }
}


/**
 * 根据 team_id 获取这个团队的首脑人物
 * @param team_id
 * @param nodes
 * @returns {string|*}
 */
function get_team_principle(team_id, nodes) {
    for(let i = 0; i < nodes.length; i++){
        if(team_id === nodes[i]["id"]){
            return nodes[i]["name"];
        }
    }
    return undefined;
}


/**
 * 柱状图点击事件, 跳转至学院画像
 */
team_bar_chart.on("click", function (params) {
    let dataIndex = params.dataIndex;
    team_id = leader_id_list[dataIndex];
    reloadGraph("force");
    show_team_patent_project_data();
});


/**
 * 获取某一团队下的专利数据和项目数据，更新前端显示
 *
 */
function show_team_patent_project_data(expert_id=team_id) {

    $.ajax({
        type: "get",
        url: "/school/profile/get_teacher_patent_project_data",
        data: {"teacher_id": expert_id},
        dataType: "json",
        success: function (data) {
            let patent_info = data["patent_info"];
            let project_info = data["project_info"];
            show_select_team(expert_id); // 显示目前展示的是哪个团队
            show_patent_project_data(patent_info, project_info); // 显示当前团队的专利和项目信息
        }
    })
}


/**
 * 显示专利数据和项目数据
 *
 */
function show_patent_project_data(patent_info, project_info){
    let html_patents = [];
    for(let i = 0; i < patent_info.length; i++){
        html_patents.push(
            `<p class="overflow" title="${patent_info[i]["title"]}"><span class="fe fe-bookmark"></span> ${patent_info[i]["title"]}</p>`
        )
    }
    let html_string = html_patents.join("");
    html_string = html_string == "" ? "暂无该专家专利数据" : html_string;
    $("#team_patent").html(html_string);

    let html_projects = [];
    for(let i = 0; i < project_info.length; i++){
        html_projects.push(
            `<p class="overflow" title="${project_info[i]["name"]}"><span class="fe fe-bookmark"></span>  ${project_info[i]["name"]}</p>`
        )
    }
    html_string = html_projects.join("");
    html_string = html_string == "" ? "暂无该专家项目数据" : html_string;
    $("#team_project").html(html_string);

}

/**
 * 显示选择了那个团队
 *
 */
function show_select_team(expert_id=team_id) {
    let expert_name = teacher_id_name_dict[expert_id];
    $("#team_project_title").html(expert_name+" 主要项目");
    $("#team_patent_title").html(expert_name+" 主要专利");
}


/**
 * 关系图点击事件， 显示该专家的主要专利和主要项目
 */
institution_relation_chart.on("click", function (params) {
    expert_id = params.data.name;
    show_team_patent_project_data(expert_id);
});
