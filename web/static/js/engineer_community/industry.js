// 全局变量
var SCHOOL_NAME= "";
var INSTITUTION_NAME = "";
var INDUSTRY_NAME = "";
var DATA = {};
let team_id_dict = {};
let map = {};
/**
 * 根据行业名称，获取行业内的社交关系
 * @param {String} industry
 */
function getIndustryGraphDate(industry){
    myChart.showLoading();
    $.ajax({
        type: "get",
        url: "/engineer_community/get_industry_graph_data",
        data: {"industry":industry,  "relation": true},
        dataType: "json",
        success: function (json_data) {
            // console.log(response);
            let graph_data = convert_graph_data(json_data);
            reloadGraph(graph_data);
        },
        error: function () {
            toggle_alert(false, "", "服务器连接失败,请稍后再试");
            myChart.hideLoading();
        }
    });
}

//echarts 对象
let myChart = echarts.init(document.getElementById('container'));

//关系图属性
let graphOption = {
    tooltip: {
        formatter: function (params) {
            if (params.dataType == "node") {

                //设置提示框的内容和格式 节点和边都显示name属性
                if(params.data.is_agent == 1){
                        return `<strong>节点属性</strong><hr>姓名：${params.data.label}`;
                }else{
                    return `<strong>节点属性</strong><hr>姓名：${params.data.label}<br>所属企业：${params.data.ep_name}`;
                }
            }
            // else{
            //     if(params.data.visited){
            //         return  `<strong>关系属性</strong><hr>拜访次数：${params.data.visited}次<br>参与活动：${params.data.activity}`;
            //     }
            //     return `
            //     专利合作：${params.data.patent}次<br>`;
            // }
        }
    },

    // 图例
    legend: [
    ],
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

            // 当鼠标移动到节点上，突出显示节点以及节点的边和邻接节点
            focusNodeAdjacency:true,
            // 是否启用图例 hover(悬停) 时的联动高亮。
            legendHoverLink : true,

            label: {
                normal: {
                    position: 'inside',
                    show : true,

                    //回调函数，显示用户名
                    formatter: function(params){
                        return params.data.label;
                    }
                }
            },
            force: {
                repulsion : [20,100],//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                gravity : 0.03,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                edgeLength :[100,300],//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
                layoutAnimation : true
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

let selected = {};

myChart.on('legendselectchanged', function (obj) {
        let select  = obj.selected;
        if(select == null) return;
        let selectName = obj.name;
        $('#community_id').val(map[selectName]);
        for(let key in selected){
            if(key==selectName){
                selected[key] = true;
            }else{
                selected[key] = false;
            }
        }
        // 按社区推荐
        //teacherRecommend(obj.name);
        // 按行业推荐
        //teacherRecommendForIndustry(industry);
        graphOption.legend.selected = selected;
        myChart.setOption(graphOption)
    }
);

function teacherRecommend(communityName) {
    console.log(communityName);
    console.log(map);
    let communityId = map[communityName];
    console.log(communityId);
        $.ajax({
        type: "get",
        url: "/engineer_community/get_teacher_info",
        data: {"community_id":communityId},
        dataType: "json",
        success: function (json_data) {
            console.log(json_data);
            fillTeacherRecommend(json_data);
        },
        error: function () {
            toggle_alert(false, "", "服务器连接失败,请稍后再试");
        }
    });
}


function teacherRecommendForIndustry(industry) {
    console.log(industry);
        $.ajax({
        type: "get",
        url: "/engineer_community/get_teacher_info_for_industry",
        data: {"industry":industry},
        dataType: "json",
        success: function (json_data) {
            console.log(json_data);
            fillTeacherRecommend(json_data);
        },
        error: function () {
            toggle_alert(false, "", "服务器连接失败,请稍后再试");
        }
    });
}
function fillTeacherRecommend(data) {
    let html = [];
    if(data.length == 0){
        let row_str = `<h3 class="card-title">
                            <span class="text-primary">
                                       &nbsp;  &nbsp;暂无学者推荐
                            </span>
                       </h3>`;
        html.push(row_str)
    }else{
        let index = 0;
        for(let i=0; i <data.length; i++){
            index++;
            if(index > 10) break;
            let row_str = `
                            <h3 class="card-title">
                                    <span class="text-primary">
                                           &nbsp;  &nbsp;  ${i+1}.${data[i]["teacher_name"]} &nbsp; ${data[i]["title"]}
                                    </span>
                            </h3>
                                <small>&nbsp;  &nbsp; &nbsp;
                                    <span class="text">
                                         ${data[i]["school"]}&nbsp; ${data[i]["institution"]}
                                    </span>
                                </small>
                            <br> <br>
            `
            html.push(row_str)
        }
    }
    let inner_str = html.join("");
    $("#recommend").html(inner_str);
}

function reloadGraph(data){
    if(!"nodes" in data) return;
    let links = data.links;
    // console.log(nodes.length, links.length, cates.length);
    graphOption.series[0].data = data.nodes;
    graphOption.series[0].links = links;

    let categories = [];
    console.log(data.community);
    // if ("community" in data){
    for (let i = 0; i < data.community; i++) {
        let name = data.core_node[String(i)]+"团队";
        categories[i] = {
            name: name
        };
        if(i == 0){
            selected[name] = true;
            //按社区推荐
            //teacherRecommend(name)
        }else{
            selected[name] = false;
        }
        teacherRecommendForIndustry(industry)
    }

    graphOption.series[0].categories = categories;
    graphOption.legend = {
        data: categories.map(function (a) {
            return a.name;
        }),
        selected: selected
    };
    myChart.setOption(graphOption);
    myChart.hideLoading();
}

//添加点击跳转事件
myChart.on('click', function (params) {
    //仅限节点类型
    if (params.dataType == 'node' && params.data.name != "0"){
        //页面
        //window.open('/scholar/detail/'+params.data.name);
        console.log(params.data);
    }
});

/*
转换关系图数据
 */
function convert_graph_data(data) {
    // console.log(data);
    let temp_links = data.links;
    let temp_nodes = data.nodes;
    let links = [];
    let nodes = [];
    let team_set = new Set();
    let have_push_links_set = new Set();
    for(let i = 0; i < temp_links.length; i++){
        let source = String(temp_links[i]["source"]);
        let target = String(temp_links[i]["target"]);
        let s1 = source + "--" + target;
        let s2 = target + "--" + source;
        let patent_num = temp_links[i]["value"];
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
            patent:patent_num,
            project:0,
        });
    }
    let id_set = new Set();
    for(let i = 0; i < temp_nodes.length; i++){
        if(id_set.has(temp_nodes[i]["id"])){
            continue;
        }
        id_set.add(temp_nodes[i]["id"]);
        if(temp_nodes[i]["is_agent"] == 1){
          nodes.push({
                name: String(temp_nodes[i]["id"]),
                label: temp_nodes[i]["name"],
                ep_name: temp_nodes[i]["ep_name"],
                category: temp_nodes[i]["community"],
                draggable: true,
                symbolSize: 26,
                is_agent: 1,
                itemStyle: {
                    "normal": {
                        "borderColor": 'yellow',
                        "borderWidth": 3,
                        "shadowBlur": 6,
                        "shadowColor": 'rgba(0, 0, 0, 0.3)'
                    }
                }
            });
        }else{
            nodes.push({
                name: String(temp_nodes[i]["id"]),
                label: temp_nodes[i]["name"],
                ep_name: temp_nodes[i]["ep_name"],
                category: temp_nodes[i]["community"],
                draggable: true,
                symbolSize: 26
            });
        }

        team_set.add(String(temp_nodes[i]["community"]));
    }
    console.log(team_set);
    let team_map = {};
    let index = 0;
    let hash_team_set = new Set();
    for(let team_id of team_set){
        let team_leader = get_team_principle(team_id, temp_nodes);
        if(team_leader !== undefined){
            hash_team_set.add(team_id);
            team_map[index] = team_leader;
            team_id_dict[team_id] = index++;
        }
    }
    console.log(hash_team_set);
    //解决社区中中心点不在社区中的不好办法，把这些节点去掉
    for(let i=0; i<nodes.length; i++){
        if(!hash_team_set.has(String(nodes[i]["category"]))){
            nodes.splice(i, 1);
            i--;
        }
    }
    for(let i = 0; i < nodes.length; i++){
        let team_id = nodes[i]["category"];
        nodes[i]["team_id"] = team_id;
        nodes[i]["category"] = team_id_dict[team_id];
    }
    // console.log(index);
    // console.log(team_map);
    // console.log(links);
    // console.log(nodes);
    // console.log(team_set);
    return {
        community: index,
        core_node: team_map,
        links: links,
        nodes: nodes,
        team_set: team_set
    };
}


/**
 * 根据 team_id 获取这个团队的首脑人物
 * @param team_id
 * @param nodes
 * @returns {string|*}
 */
function get_team_principle(team_id, nodes) {
    for(let i = 0; i < nodes.length; i++){
        if(team_id == nodes[i]["id"]){
            let key = nodes[i]["name"]+"团队";
            map[key] = nodes[i]["id"];
            return nodes[i]["name"];
        }
    }
    return undefined;
}

//点击行业进行切换
$(".industry-selecting").on('click', function (e) {
    industry = $(this).text().trim();
    console.log(industry);
    getIndustryGraphDate(industry)
});

//下载excel
$('#namelist').click(function (){
    //获取当前选中的区县
    let community_name = "";
    for(let key in selected){
        if(selected[key] == true){
            community_name = key;
        }
    }
    let community_id =  map[community_name];
    //let date = new Date();
    let url = `${DOWNLOAD_NAMELIST_URL}?community_id=${community_id}`;
    window.open(url);
});

//页面加载完成
let industry="其他仪器仪表制造业";

getIndustryGraphDate(industry);
