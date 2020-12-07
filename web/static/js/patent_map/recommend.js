let radarChart = getEChartsObject("radar");
//暂存数据
JSON_DATA = null;
//重新请求
function ajaxGetRecommendUnites(){
    //获取当前选中的区县
    let $unit = $('#unit');
    let category = $unit.attr('data-category');
    let unit_name = trim($unit.text());
    //获取选中的行业
    let class_list = $('#industry').val();
    //修改下载链接
    radarChart.showLoading();
    //请求数据
    $.ajax({
        type: "get",
        url: RECOMMEND_URL,
        data: {category: category, unit_name: unit_name, class_list: class_list},
        dataType: "json",
        success: function (json_data) {
            radarChart.hideLoading();
            if (!json_data.error){
                fillData(json_data);
                fillRadarGraph(json_data);
            }
            else{
                toggle_alert(false, json_data.msg);
            }
        }
    });
}

//下载excel
$('#download_excel').click(function (){
    //获取当前选中的区县
    let $unit = $('#unit');
    let category = $unit.attr('data-category');
    let unit_name = trim($unit.text());
    //获取选中的行业
    let class_list = $('#industry').val();
    let class_param = [];
    for (let index = 0;index < class_list.length; index++){
        let class_ = class_list[index];
        class_param.push(`class_list[]=${class_}`);
    }
    //let date = new Date();
    let url = `${DOWNLOAD_URL}?category=${category}&unit_name=${unit_name}&${class_param.join('&')}`;
    window.open(url);
});

$(document).ready(function (){
    ajaxGetRecommendUnites();
    //设置select2的宽度
    changeSelect2Width();
});

function fillData(json_data){
    let html = [];
    //数据出错
    if (json_data['error']) {
        html.push(`<span class="text-center text-muted">${json_data.msg}</span>`);
    }
    else {
        let data = json_data.data;
        for (let i = 0;i < data.length; i++){
            let datum = data[i];
            let institution = datum.institution;
            let comparison = institution.length == 0 ?'-': institution.join('; ');
            //let avatar_url = `${SCHOOL_AVATAR_URL}/school_name=${datum.name}`;
            let row = `
            <tr class="tr_callable" data-idx="${i}">
                <td>${i+1}</td>
                <td>
                    <img src="/static/school/${datum.name}.png" class="img-circle" alt="图标">
                    <span class="text-primary">${datum.name}</span>
                </td>
                <td>${comparison}</td>
                <td><span class="badge badge-primary justify-content-between">${datum.similarity}</span></td>
            </tr>`;
            html.push(row);
        }
    }
    let html_string = html.join("");
    $('#unit_recommend').html(html_string);
    //添加点击事件
    $('.tr_callable').click(function (event){
        //获取点击的 单位
        let $target = $(event.currentTarget);
        let idx = parseInt($target.attr('data-idx'));
        //设置option
        fillRadarGraph(JSON_DATA, idx);
    });

}

function fillRadarGraph(json_data, idx=null){
    let legend = [];
    let self_data = JSON.parse(JSON.stringify(json_data.self_data));
    legend.push(self_data.name);
    let indicator = JSON.parse(JSON.stringify(json_data.indicator));
    let series = [self_data];
    //以点击的单位的值为标准，进行移动
    if (idx != null){
        let name = json_data.data[idx].name;
        let value = json_data.data[idx].value.slice();
        legend.push(name);
        series.push({name: name, value: value});
        //函数
        function swap(data, i, j){
            if (i == j)
                return
            //debugger
            swapArray(value, i, j);
            swapArray(self_data.value, i, j);
            swapArray(indicator, i, j);
        }
        quickSort(value, 0, value.length-1, swap);
        /*
        //调换位置 非零在前，0在后
        let begin = 0, end = value.length - 1;
        while (begin < end){
            //找到第一个为0
            while (begin < end && value[begin] != 0)
                begin++;
            while (begin < end && value[end] == 0)
                end--;
            if (begin < end){
                swapArray(value, begin, end);
                swapArray(self_data.value, begin, end);
                swapArray(indicator, begin, end);
            }
        }
         */
    }
    let option = get_radar_option(legend, indicator, series);
    radarChart.clear();
    radarChart.setOption(option);
    JSON_DATA = json_data;
}

function get_radar_option(legend, indicator, series){
    let option = {
        title: {
            text: '雷达图',
            show: false
        },
        //TODO: 更好的展示专利比较
        tooltip: {
            formatter: '{b}'
        },
        legend: {
            data: legend,
        },
        radar: {
            name: {
                textStyle: {
                    color: '#fff',
                    backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5]
                },
                show: false
            },
            indicator: indicator,
        },
        series: [{
            name: '雷达图（专利对比）',
            type: 'radar',
             areaStyle: {opacity: 0.25},
            data: series
        }],
    };
    return option;
}

//动态改变select2的宽度
function changeSelect2Width(){
    let width = $('.select2-selection.select2-selection--multiple').width() / 3 - $('button.select2-selection__choice__remove').outerWidth() - 20;
    $('.select2-selection__choice__display').css('width', width);
}

