let scatterChart = echarts.init(document.getElementById("scatter"));
let last_unselected = null;

scatterOption= {
    title: {
        text: "第五代通信技术（5G）"
    },
    grid: {
        left: '0',
        right: '0',
        bottom: '10px',
        top: "10px",
        width: "100%",
        height: "100%",
    },
    tooltip: {},
    legend: {
        orient: 'horizontal',
        //right: 10
    },
    xAxis: [{
        show: false
    }],
    yAxis: [{
        show: false
    }],
    dataZoom: [{
        type: 'inside'
    },{
        type: 'inside',
        orient: 'vertical',
    }],
    animation: false,
    series: []
};
scatterChart.showLoading();

$.ajax({
        type: "get",
        url: "/ajax/technology/get_data",
        dataType: "json",
        success: function (array) {
            scatterChart.hideLoading();
            //按簇划分
            for (let i = 0; i < array.length; i++){
                //console.log(array[i]);
                scatterOption.series.push({
                    name: '簇' + i,
                    type: 'scatter',
                    data: array[i],
                    dimensions: ['x', 'y'],
                    symbolSize: 6,
                    large: true,
                    itemStyle: {
                        opacity: 1
                    }
                })
            }
            scatterChart.setOption(scatterOption);
        },
        error: function (error) {
            scatterChart.hideLoading();
        }
});
//showLogistic('5G', '');

//重写图例选中函数
scatterChart.on('legendselectchanged', function (obj) {
    // 所有 selected Object 里面 true 代表 selected， false 代表 unselected
    let selected = obj.selected;
    if (selected == null)
        return ;
    let legends = [];
    let option = scatterChart.getOption();
    let index = 0;
    //当前“选中”的索引
    let selected_index = '';
    let is_reversed = false;
    //再点一次表示反选
    if (last_unselected && !selected[last_unselected]){
        is_reversed = true;
        last_unselected = null;
    }
    //遍历，设置opacity
    for(let name in selected) {
        if (!selected.hasOwnProperty(name)) {
            continue;
        }
        let opacity = 1;
        if (selected[name]) {
            opacity = is_reversed ? 1: 0.2;
        }
        else{
            opacity = 1;
            legends.push({name: name});
            if (!is_reversed){
                selected_index = index;
                last_unselected = name;
            }
        }
        option.series[index].itemStyle.opacity = opacity;
        index++;
    }
    //把之前取消选中的，再次反选回来
    scatterChart.setOption(option);
    scatterChart.dispatchAction({
        type: 'legendToggleSelect',
        batch: legends
    });
    //console.log(selected_index);
    //showLogistic('5G', selected_index);
});

/**
 * 展示S曲线
 * @param tech_name 技术名称
 * @param idx 索引 可以是'' 或者是int
 */
function showLogistic(tech_name, idx) {
    barChart.showLoading();
    $.ajax({
        type: "get",
        url: "/ajax/technology/calc_tech/" + tech_name + '/' + idx,
        dataType: "json",
        success: function (json_data) {
            barChart.hideLoading();
            setBarOption(barChart, json_data);
        },
        error: function (error) {
            barChart.hideLoading();
        }
    });
}