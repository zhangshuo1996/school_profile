/**
 * 显示高校画像入口的旭日图
 */
let COLOR_LIST = [
    ["#3333FF", "#3333FF", "#3333FF", "#3333FF"],
    ["#FF3300", "#e6550d", "#fd8d3c", "#fd8d3c"],
    ["#31a354", "#74c476", "#a1d99b", "#31a354"],
    ["#990000", "#660000", "#990033", "#660033"],
    ["#696969", "#696969", "#808080", "#333333"],
    ["#006400", "#228B22", "#556B2F", "#9ACD32"],
    ["#660099", "#9933CC", "#CC66FF", "#660066"],
];
let province__area_patent_num;
let province__city_school;
let city__patent_num;
let school__patent_num;
let rise_sun_graph = getEChartsObject("rise_sun_graph");

get_province_school_patent_num();

function get_province_school_patent_num(){
    $.ajax({
        type: "get",
        url: "/school/profile/get_province_school_patent_num",
        data: {},
        dataType: "json",
        success: function (json_data) {
            province__city_school = json_data.province__city_school;
            province__area_patent_num = json_data.province__area_patent_num;
            city__patent_num = json_data.city__patent_num;
            school__patent_num = json_data.school__patent_num;
            let option_data = format_data(province__city_school);
            option_data.sort(compare);
            option.series.data = option_data;
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
        let level1_color = province__area_patent_num[province]["area_code"]-1;
        // let level2_color = randomNum(1, 4);
        let level2_color = 0;
        debugger;
        let temp1 = {
            name : province,
            itemStyle: {
                color: COLOR_LIST[level1_color][level2_color],
            },
            children: [],
        };
        let province_info = data[province];
        for(let city in province_info){
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
            // 高校按专利数量排序
            temp2.children.sort(function (x, y) {
                let value_x = x.value;
                let value_y = y.value;
                if(value_x > value_y){
                    return 1;
                }else{
                    return -1;
                }
            });
            temp1.children.push(temp2);
        }
        // 城市按专利数量排序
        temp1.children.sort(function (x, y) {
            let city_x = x.name;
            let city_y = y.name;
            if(city__patent_num[city_x] > city__patent_num[city_y]){
                return 1;
            }else{
                return -1;
            }
        });
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
        center: ['50%', "45%"],
        sort: null,
        levels: [
        {// 最内层

        }, { // 省级
        r0: '15%', // 内半径
        r: '45%', // 本身半径
        itemStyle: {
            borderWidth: 2
        },
        label: {
            // rotate: 'tangential' // 标签旋转
            align: "right",
            color: "#000000",
        }
        }, { // 市级
            r0: '45%',
            r: '70%',
            label: {
                fontStyle: 'normal',
                fontSize: 12,
                align: 'right',
                color: "#000000",
            }
        }, { // 高校
            r0: '70%',
            r: '72%',
            label: {
                position: 'outside',
                fontSize: 12,
                padding: 3,
                silent: false,
                color: "#000000",
                fontFamily: "HeiTi",
                fontWeight: "bold",
                // textBorderColor: "rgba(16, 15, 15, 1)",
                // textBorderColor: "#000000",
                // textBorderWidth: 3
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


/**
 * 对显示的大区 及高校排序
 */
function compare(x, y){
    let province_x = x["name"];
    let province_y = y["name"];
    let area_code_x = province__area_patent_num[province_x]["area_code"];
    let area_code_y = province__area_patent_num[province_y]["area_code"];

    let patent_num_x = province__area_patent_num[province_x]["patent_num"];
    let patent_num_y = province__area_patent_num[province_y]["patent_num"];
    if(area_code_x ==area_code_y){
        return patent_num_x > patent_num_y ? 1 : -1;
    }else if(area_code_x < area_code_y){
        return 1;
    }else{
        return -1;
    }
}

rise_sun_graph.on("click", function (params) {
    let school = params.data.name;
    if(school.indexOf("大学") > 0 || school.indexOf("研究") > 0){
        window.location.href = "/school/profile/index/" + school;
    }else{
        return;
    }
});
