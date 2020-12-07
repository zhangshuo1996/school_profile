graphChart = echarts.init(document.getElementById('rules'));
comparisonChart = echarts.init(document.getElementById('patent_comparison'));
//暂存legend的数据
LEGEND = [];

//柱状图
function get_patent_comparison(data){
    let option = {
        legend: {
            data: [],
            type: 'scroll',
            orient: 'vertical',
            left: '3%',
            show: false
        },
        color: COLOR_LIST,
        //left影响柱状图的位置
        grid: {left: '40%', top: '0%', width: '70%', height: '100%'},
        xAxis: {type: 'value', show: false},
        yAxis: {type: 'category', show: true},
        tooltip: {
            formatter: get_graph_tooltip
        },
        series : []
    };
    //柱状图
    let style = {
        normal: {
            label: {
                show: true,
                position: 'inside',
            },
            color: get_bar_color
        }
    };
    let barData = [];
    let yAxis = [];
    for (let class_ in data.community){
        let community = data.community[class_];
        barData.push(community.patent_count);
        yAxis.push(community.title);
    }
    yAxis.reverse();
    barData.reverse();
    option.yAxis.data = yAxis;
    option.series.push({
        type: 'bar',
        itemStyle: style,
        data: barData,
        barWidth: '50%',
    });
    return option;
}
/**
 * 获取tooltip
 * @param params
 */
function get_graph_tooltip(params){
    //hover 柱状图
    if (params.seriesType == 'bar'){
        return `${params.name} : ${params.value}`;
    }
    //力导向图 hover 点
    if (params.dataType != 'node')
        return ;
    let index = params.data.category;
    let option = graphChart.getOption();
    let legend = option.legend[0];
    return legend.data[index].name;
}
//为柱状图赋予添加legend的功能
comparisonChart.on('click', function (params){
    //点击了柱状图 会 选中/隐藏节点
    if (params.seriesType == 'bar'){
        graphChart.dispatchAction({
            type: 'legendToggleSelect',
            batch: [{name: params.name}]
        });
        comparisonChart.dispatchAction({
            type: 'legendToggleSelect',
            batch: []
        })
    }
});
//柱状图的颜色
function get_bar_color(params){
    let length = LEGEND.length;
    let option = graphChart.getOption();
    let selected = option.legend[0].selected;
    //更换柱状图的颜色
    for (let key in selected){
        //当前未选中
        if (!selected[key] && key == params.name)
            return '#CCCCCC';
    }
    let index = length - params.dataIndex % length - 1;
    //console.log(index, params.name);
    return COLOR_LIST[index];
}

function get_graph_option(data){
    let option = {
        legend: {
            data: [],
            type: 'scroll',
            orient: 'vertical',
            left: '3%',
            show: false
        },
        color: COLOR_LIST,
        tooltip: {
            formatter: get_graph_tooltip
        },
        series : [
            //力导向图
            {
                name: 'Graph',
                type: 'graph',
                layout: 'force',
                data: [],
                links: [],
                edgeSymbol: ['none', 'arrow'],
                roam: true,
                zoom: 0.8,
                left: 'left',
                label: {
                    position: 'inside',
                    show: false,
                },
                force: {
                    repulsion: 50,
                    edgeLength: [10, 50]
                }
            },
        ]
    };
    LEGEND = [];
    //添加节点和链接
    let nodes = [], legend = [];
    let links = data.links;
    let minSupport = Number.MAX_VALUE, maxSupport = Number.MIN_VALUE;
    for (let i = 0;i < data.nodes.length; i++){
        let datum = data.nodes[i];
        let class_ = datum['class'];
        let community = data.community[class_];
        let class_title = community.title;
        //是否选中
        if (legend.length == 0 || legend[legend.length-1].name != class_title){
            legend.push({name: class_title});
            LEGEND.push(class_title);
            //legend_selected[class_title] = (legend.length < 10)? true: false;
        }
        //value:[support, class_]
        nodes.push({name: datum.name, category: legend.length-1, value: [datum.support, class_]});
        if (minSupport > datum.support)
            minSupport = datum.support;
        if (maxSupport < datum.support)
            maxSupport = datum.support;
    }
    //遍历长度
    /*
    for (let i = 0;i < links.length; i++){
        let link = links[i];
        link.value = (code_count_mapping[link.source] + code_count_mapping[link.target])/2;
    }
     */
    //[10, 20]
    for (let i = 0;i < nodes.length; i++){
        nodes[i].symbolSize = (nodes[i].value[0] - minSupport) / (maxSupport - minSupport) * 10 + 10;
    }
    option.legend.data = legend;
    //option.legend.selected = legend_selected;
    option.series[0].categories = legend;
    option.series[0].data = nodes;
    option.series[0].links = links;
    return option;
}

/**
 * ajax获取单位<unit_name>的IPC群组
 * @param category: school | district
 * @param unit_name 单位名称，比如东南大学
 */
function ajaxGetCommunities(category, unit_name){
    graphChart.showLoading();
    comparisonChart.showLoading();
    $.ajax({
        type: "get",
        url: IPC_COMMUNITIES_URL,
        data: {category: category, unit_name: unit_name},
        dataType: "json",
        success: function (json_data) {
            if (json_data['error']) {
                toggle_alert(false, '获取数据失败');
                return false;
            }
            //共分类网络图
            graphChart.hideLoading();
            comparisonChart.hideLoading();
            graphChart.clear();
            let graphOption = get_graph_option(json_data.data);
            graphChart.setOption(graphOption);
            //柱状图
            comparisonChart.hideLoading();
            comparisonChart.clear();
            let comparisonOption = get_patent_comparison(json_data.data);
            comparisonChart.setOption(comparisonOption);
        }
    });
}
