/**
 * 显示高校画像入口的旭日图
 */
let COLOR_LIST = [[	"#0000FF", "#2c7be5", "#6baed6", "#00BFFF"],
                ["#e6550d", "#fd8d3c", "#fdae6b", "#e6550d"],
                ["#31a354", "#74c476", "#a1d99b", "#31a354"],
                ["#756bb1", "#9e9ac8", "#6A5ACD", "#9932CC"],
                ["#636363", "#969696", "#bdbdbd", "#000000"]];

let rise_sun_graph = getEChartsObject("rise_sun_graph");

get_province_school_patent_num();

function get_province_school_patent_num(){
    $.ajax({
        type: "get",
        url: "/school/profile/get_province_school_patent_num",
        data: {},
        dataType: "json",
        success: function (json_data) {
            let data = json_data.data;
            let option_data = format_data(data);
            option.series.data = option_data;
            debugger;
            rise_sun_graph.setOption(option);

        }
    })
}

/**
 * 将原始数据： {
                "江苏省" : {
                        "南京市" : {
                            "南大"： 1111，
                            "东大"： 2222，
                            。。。
                        }，
                        。。。
                }，
                。。。。
            }
    转换成 ： [{
            name: 'Flora',
            itemStyle: {
                color: '#da0d68'
            },
            children: [{
                name: 'Black Tea',
                value: 1,
                itemStyle: {
                    color: '#975e6d'
                }
            },...],
            }...
            ]
 * @param data
 */
function format_data(data){
    let option_data = [];
    debugger;
    for(let province in data){
        let level1_color = randomNum(0, 4);
        let temp1 = {
            name : province,
            itemStyle: {
                color: COLOR_LIST[level1_color][0],
            },
            children: [],
        };
        let province_info = data[province];
        for(let city in province_info){
            let level2_color = randomNum(0, 3);
            let temp2 = {
                name: city,
                itemStyle: {
                        color: COLOR_LIST[level1_color][level2_color],
                    },
                children: []
                };
            let city_info = province_info[city];
            for(let school in city_info){
                temp2.children.push({
                    name: school,
                    itemStyle: {
                        color: COLOR_LIST[level1_color][level2_color],
                    },
                    value: city_info[school]
                })
            }
            temp1.children.push(temp2);
        }
        option_data.push(temp1);
    }
    return option_data;
}

let data = [];

let option = {
    title: {
        text: '全国高校专利分布',
        subtext: '',
        textStyle: {
            fontSize: 18,
            align: 'center'
        },
        subtextStyle: {
            align: 'center'
        },
        sublink: ''
    },
    series: {
        type: 'sunburst',
        highlightPolicy: 'ancestor',
        data: data,
        radius: [0, '95%'],
        sort: null,
        levels: [
        {

        }, { // 省级
        r0: '15%', // 内半径
        r: '45%', // 本身半径
        itemStyle: {
            borderWidth: 2
        },
        label: {
            // rotate: 'tangential' // 标签旋转
            align: "right"
        }
        }, { // 市级
            r0: '45%',
            r: '70%',
            label: {
                fontStyle: 'normal',
                fontSize: 12,
                align: 'right'
            }
        }, { // 高校
            r0: '70%',
            r: '72%',
            label: {
                position: 'outside',
                fontSize: 12,
                padding: 3,
                silent: false,
                // textBorderColor: "rgba(16, 15, 15, 1)",
                textBorderWidth: 3.5
            },
            itemStyle: {
                borderWidth: 3
            }
        }]
    }
};

//生成从minNum到maxNum的随机数
function randomNum(minNum,maxNum){
    switch(arguments.length){
        case 1:
            return parseInt(Math.random()*minNum+1,10);
        break;
        case 2:
            return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);
        break;
            default:
                return 0;
            break;
    }
}

rise_sun_graph.on("click", function (params) {
    let school = params.data.name;
    debugger;
    if(school.indexOf("大学") > 0 || school.indexOf("研究") > 0){
        window.location.href = "/school/profile/index/" + school;
    }else{
        return;
    }
});
