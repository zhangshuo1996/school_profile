
let tree_data = undefined;
// get_and_show_team_tree();
/**
 * 获取  展示 某一学院下的团队树图数据
 *
 */
function get_and_show_team_tree() {

    $.ajax({
        type: "get",
        url: "/school/profile/get_team_member_info",
        data: {"school": school, "institution": institution},
        dataType: "json",
        success: function (json_data) {
            institution_relation_chart.clear();
            tree_data = json_data["data"];
            tree_data = control_node_status(tree_data);

            show_team_tree();
        }
    })
}

/**
 *
 */
function show_team_tree() {
    let tree_option = set_tree_option(tree_data);
    institution_relation_chart.showLoading();
    setTimeout(institution_relation_chart.setOption(tree_option), 500);
    institution_relation_chart.hideLoading();
}

/**
 * 控制节点打开和收缩
 */
function control_node_status(data) {
    data.collapsed = null;
    let children = data.children;
    for(let i = 0; i < children.length; i++){
        if(i == 0){
            children[i].collapsed = null;
        }else{
            children[i].collapsed = true;
        }
    }
    return data;
}



function set_tree_option(data) {
    let option = {
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
        },
        series:[
            {
                type: 'tree',
                id: 0,
                name: 'tree1',
                data: [data],

                top: '10%',
                left: '8%',
                bottom: '22%',
                right: '20%',

                symbolSize: 7,

                edgeShape: 'polyline',
                edgeForkPosition: '63%',
                initialTreeDepth: 3,

                lineStyle: {
                    width: 2
                },

                label: {
                    backgroundColor: '#fff',
                    position: 'left',
                    verticalAlign: 'middle',
                    align: 'right'
                },

                leaves: {
                    label: {
                        position: 'right',
                        verticalAlign: 'middle',
                        align: 'left'
                    }
                },

                expandAndCollapse: true,
                animationDuration: 550,
                animationDurationUpdate: 750
            }
        ]
    };
    option.series.data = [data];
    return option;
}

/**
 * 树图点击事件, 节点伸缩
 */
institution_relation_chart.on("click", function (params) {
    let depth = params.data.depth;
    if(depth == undefined || depth == 0 || depth == 2){
        return;
    }
    let team_name = params.data.name;
    let children = tree_data.children;
    for(let i = 0; i < children.length; i++){
        if(children[i]["name"] == team_name){
            children[i].collapsed = null;
        }else{
            children[i].collapsed = true;
        }
    }
    let data = set_tree_option(tree_data);
    institution_relation_chart.clear();
    institution_relation_chart.setOption(data);

});

/**
 * 关系图与树图切换事件
 */
$("#relation_graph").on("click", function () {
    institution_relation_chart.clear();
    institution_relation_chart.showLoading();
    show_community_relation();
});

$("#tree_graph").on("click", function () {
    institution_relation_chart.clear();
    if(tree_data == undefined){
        get_and_show_team_tree();
    }else{
        show_team_tree();
    }
});





