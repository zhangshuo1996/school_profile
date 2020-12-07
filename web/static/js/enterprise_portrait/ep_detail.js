var myChart_engineer_graph = echarts.init(document.getElementById('engineer_graph'));
var myChart_ep_research_ability_graph = echarts.init(document.getElementById('ep_research_ability_graph'));
var categories = [];
var role_with_portrait = $("#role_with_portrait").val();
if(role_with_portrait != 0){
    myChart_engineer_graph.on('click', function (param) {
    var ep_name = document.getElementById("ep_name").innerText;
    var engineer_name = param.data.name;
    var engineer_id = param.data.value;
    var visited_status = param.data.category
    $("#ep_name_modal").val(ep_name);
    $("#engineer_name_modal").val(engineer_name);
    $("#engineer_id_modal").val(engineer_id);
    var radios = document.getElementsByName("options_radio");
	   for(var i=0; i<radios.length; i++) {
           radios[i].checked = false;
           if (radios[i].value == visited_status) {
               radios[i].checked = true;
           }
       }
    $("#myModal").modal();
    });
    var categories = [{name:"未联系过"},{name:"已联系过"},{name:"提供技术需求"},{name:"参加活动"},{name:"签订合同"}];
}


function get_engineer_count(ep_id) {
    $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/get_engineer_count",
        data: {"ep_id" : ep_id},
        dataType: "json",
        success: function (response) {
            if(response.status == true){
                setOption_engineer(response.engineer_nodes, response.links, role_with_portrait);
                setOption_ep_research_ability_graph(response.research_score);
            }
        },
        error: function(){
            console.log("error")
        }
    });
}


function setOption_ep_research_ability_graph(data){
    option = {
        tooltip: {
        trigger: 'axis'
    },
        radar: [
            {
                indicator: [
                    {text: '注册资金', max: 100},
                    {text: '工程师数量', max: 100},
                    {text: '政策申报', max: 100},
                    {text: '科技成果', max: 100}
                ],
                center: ['50%', '50%'],
                radius: 150
            },
        ],

        series: [
        {
            type: 'radar',
            tooltip: {
                trigger: 'item'
            },
            areaStyle: {},
            data: [
                {
                    value: data,
                    name: ep_name,
                }
            ],

        },
        {
            type: 'radar',
            radarIndex: 1,
            areaStyle: {},
            data: [
            ]
        }
    ]
};
    myChart_ep_research_ability_graph.setOption(option);
}


function setOption_engineer(engineer_nodes, links, role_with_portrait){

    option = {
    // 提示框的配置
        tooltip: {
            formatter: function (x) {
                return x.data.des;
            }
        },
        legend: [{
            // selectedMode: 'single',
            data: categories.map(function (a) {
            return a.name;
            })
        }],
        color: ['#2c7be5','#e6550d', '#31a354', '#756bb1', '#636363'],
        // 工具箱
        toolbox: {
            // 显示工具箱
            show: true,
            feature: {
                mark: {
                    show: true
                },
            }
        },
        series: [{
            type: 'graph', // 类型:关系图
            layout: 'force', //图的布局，类型为力导图
            symbolSize: 40, // 调整节点的大小
            roam: true, // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移,可以设置成 'scale' 或者 'move'。设置成 true 为都开启
            // edgeSymbol: ['circle', 'arrow'],
            itemStyle: {
                // normal: {
        	    // 	// （1） 直接写一个颜色，这样的结果是所有节点都是同一个颜色
        		//  	color: '#2c7be5',
        	    // }
            },
            edgeSymbolSize: [2, 10],
            edgeLabel: {
                normal: {
                    textStyle: {
                        fontSize: 14
                    }
                }
            },
            nodeStyle : {
                color: '#ffcd7e',
            },
            force: {
                repulsion: 700,
                edgeLength: 200
            },
            draggable: true,
            lineStyle: {
                normal: {
                    width: 2,
                    color: '#000000',
                },
                type: 'curve',
                legendHoverLink : true
            },
            edgeLabel: {
                normal: {
                    show: true,
                    formatter: function (x) {
                        return x.data.name;
                    }
                }
            },
            label: {
                normal: {
                    show: true,
                    textStyle: {}
                }
            },
            // 数据
            data: engineer_nodes,
            links: links,
            categories: categories,
        }]
    };
    if(role_with_portrait==0){
        option.legend=[];
        option.color=["#2c7be5"];
    }
    myChart_engineer_graph.setOption(option);
}


var ep_id = document.getElementById("ep_id").innerText;
var ep_name = document.getElementById("ep_name").innerText;
get_engineer_count(ep_id);
$("#reload_graph").on("click", function() {
    var engineer_id = $("#engineer_id_modal").val();
    var visited_status = $('input[name="options_radio"]:checked').val();
    let data = {
        "engineer_id" : engineer_id,
        "visited_status" : visited_status
    }
    $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/update_engineer_visited_status",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response.status == true){
                $("#myModal").modal('hide');
                var ep_id = document.getElementById("ep_id").innerText;
                get_engineer_count(ep_id);
            }
        },
        error: function(){
            console.log("error")
        }
    })
})
