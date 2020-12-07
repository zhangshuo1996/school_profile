COLOR_LIST = ["#2c7be5", "#6baed6", "#9ecae1", "#c6dbef",
    "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2",
    "#31a354", "#74c476", "#a1d99b", "#c7e9c0",
    "#756bb1", "#9e9ac8", "#bcbddc", "#dadaeb",
    "#636363", "#969696", "#bdbdbd", "#d9d9d9"];


barOption = {
    title: {
        left: "center",
        show: true
    },
    legend: {
        type: "scroll",
        data: [],
        left: "center",
        itemGap: 20,
        bottom: 10
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    yAxis: {
        type: 'category',
        data: [],
        axisTick: {
            alignWithLabel: true
        },
        axisLabel: {
           interval:0,
           rotate:20
        }
    },
    xAxis: {
        type: 'value',
        minInterval: 1
    },
    itemStyle: {
        barBorderRadius: 20,
    },
    series: [{data: []}],
    color: COLOR_LIST,
};


emptyBarOption = {
    title: {
        left: "center",
        show: true
    },
    legend: {
        type: "scroll",
        data: [],
        left: "center",
        itemGap: 20,
        bottom: 10
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    xAxis: {
        type: 'category',
        data: [],
        axisTick: {
            alignWithLabel: true
        }
    },
    yAxis: {
        type: 'value'
    },
    itemStyle: {
        barBorderRadius: 20,
    },
    series: [],
    color: COLOR_LIST,
};


lineOption = {
    title: {
        left: "center",
        show: true
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        type: "scroll",
        data: [],
        left: "center",
        itemGap: 20,
        bottom: 10
    },
    xAxis: {
        type: 'category',
        data: [],
        boundaryGap: false,
        axisTick: {
            alignWithLabel: true
        }
    },
    yAxis: {
        type: 'value'
    },
    itemStyle: {
        barBorderRadius: 5,
    },
    series: [],
    color: COLOR_LIST,
};


//饼图 option
pieOption = {
    tooltip: {
        trigger: 'item',
        formatter: '{b} : {c} ({d}%)',
        show: true,
        transitionDuration:0,//echart防止tooltip的抖动
    },
    legend: {
        type: "scroll",
        bottom: 10,
        data: []
    },
    color: COLOR_LIST,
    series: [
        {
            name: "",
            type: 'pie',
            // radius: '50%',
            radius: ['60%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                //formatter: '{b} : {c} ({d}%)',
                //position: 'center'
            },
            emphasis: {
                label: {
                    fontWeight: 'bold'
                }
            },
            data: []
        }
    ]
};


agentRankOption = {
    baseOption: {
        backgroundColor: '#fff', //背景颜色
        timeline: {
            data: [],//data: years
            axisType: 'category',
            autoPlay: false,
            playInterval: 1500, //播放速度

            left: '5%',
            right: '5%',
            bottom: '0%',
            width: '90%',
            label: {
                normal: {
                    textStyle: {
                        color: '#333',
                    }
                },
                emphasis: {
                    textStyle: {
                        color: '#000'
                    }
                }
            },
            symbolSize: 10,
            lineStyle: {
                color: '#fd8d3c'
            },
            checkpointStyle: {
                borderColor: '#e6550d',
                borderWidth: 2
            },
            controlStyle: {
                showNextBtn: true,
                showPrevBtn: true,
                normal: {
                    color: '#ff8800',
                    borderColor: '#ff8800'
                },
                emphasis: {
                    color: 'red',
                    borderColor: 'red'
                }
            },

        },

        tooltip: {
            'trigger': 'axis'
        },
        // calculable: true,
        grid: {
            left: '15%',
            // right: '150px',
            bottom: '60px',
            // top: '0%',
            containLabel: true
        },
        label: {
            normal: {
                textStyle: {
                    color: 'red'
                }
            }
        },
        yAxis: [{
            offset: '37',
            type: 'category',
            interval: 50,
            //inverse: ture,//图表倒叙或者正序排版
            data: [],

            axisLabel: {
                //rotate:45,
                show: false,
                textStyle: {
                    fontSize: 12,
                }, //rotate:45,
                interval: 50
            },
            axisLine: {
                lineStyle: {
                    color: '#000' //Y轴颜色
                },
            },
            splitLine: {
                show: false,
                lineStyle: {
                    color: '#333'
                }
            },

        }],
        xAxis: [{
            type: 'value',
            minInterval: 1,
            nameTextStyle: {
                color: '#888'
            },
            axisLine: {
                lineStyle: {
                    color: '#333' //X轴颜色
                }
            },
            axisLabel: {
                formatter: '{value}'
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#e3ebf6'
                }
            },
        }],
        legend: {
            show: true,
            data: ["活动", "项目"],
            selectedMode:false,//取消图例上的点击事件
        },
        series: [{
            name: '项目',
            type: 'bar',
            label: {
                normal: {
                    show: true,
                    position: 'right', //数值显示在右侧
                    // formatter: '{c}',
                    formatter: '',
                    color: "#333",
                }
            },
            color: "#2c7be5",
            barWidth: 10,
        },
            {
                name: '活动',
                type: 'bar',
                markLine: {
                    label: {
                        normal: {
                            show: false
                        }
                    },
                    lineStyle: {
                        normal: {
                            color: 'red',
                            width: 3
                        }
                    },
                },
                label: {
                    normal: {
                        show: true,
                        fontSize: 12, //标签国家字体大小
                        position: 'left', //数值显示在右侧
                        color: "#333",
                        formatter: function (p) {
                            return p.name;
                        }
                    }
                },
                barWidth: 10,
                color: "#6baed6",
            }
        ],
    },
    color: COLOR_LIST,
    options: []
};


//堆叠图
pile_option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
    },
    legend: {
        data: []
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            boundaryGap: false,
            data: ['', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: []
};



function set_pile_option(chart, option, data = {}) {
    if (!chart) {
        return false;
    }
    if (data.legend && option.legend) {
        option.legend.data = data.legend;
    }
    if (data.series && option.series) {
        option.series = data.series;
    }
    chart.clear();
    chart.hideLoading();
    chart.setOption(option);
}


function set_option(chart, option, data = {}) {
    if (!chart) {
        return false;
    }
    if (data.title && option.title) {
        option.title.text = data.title;
    }
    if (data.legend && option.legend) {
        option.legend.data = data.legend;
    }
    if (data.xAxis && option.xAxis) {
        option.xAxis.data = data.xAxis;
    }
    if (data.yAxis && option.yAxis) {
        option.yAxis.name = data.yAxis;
    }

    option.series = data.series;
    debugger;
    chart.clear();
    chart.hideLoading();
    chart.setOption(option);
}


function set_pie_option(chart, option, data = {}) {
    if (!chart) {
        return false;
    }
    if (data.legend && option.legend) {
        option.legend.data = data.legend;
    }

    if (data.seriesName && option.series) {
        option.series[0].name = data.seriesName;
    }
    option.series[0].data = data.series;
    if (data.color) {
        option.color = data.color;
    }
    chart.clear();
    chart.hideLoading();
    chart.setOption(option);
}


function setECharts_W_H(id) {
    let elem = document.getElementById(id);
    if (elem) {
        elem.style.width = elem.parentElement.clientWidth + "px";
        elem.style.height = elem.parentElement.clientHeight + "px";
        return elem;
    }
    return undefined;
}


function getEChartsObject(id) {
    let elem = setECharts_W_H(id);
    if (elem) {
        return echarts.init(elem);
    }
    return undefined;
}


/**
 * 设置并加载雷达图
 * @param dimension
 * @param data
 * @param chart
 * @param teacher_name
 */
function set_radar_option(dimension, data, chart, teacher_name="点击右图节点查看科研水平评估") {
    $("#radar_graph_header").html(teacher_name + "团队科研水平评估");
    let option = {
        title: {
            // text: '多雷达图'
        },
        tooltip: {
            // trigger: 'axis',
            show: true,
            transitionDuration: 0,//echart防止tooltip的抖动
        },
        legend: {
            left: 'center',
            // backgroundColor: '#ccc',
            data: ['分布']
        },
        radar: [
            {},
            {
                indicator: dimension,
                radius: 90,
                center: ['50%', '51%'],
                splitArea: {
                    areaStyle: {
                        color: ['rgba(255, 255, 255, 0)'],
                        shadowColor: 'rgba(0, 0, 0, 0.3)',
                        shadowBlur: 10
                    }
                },
            }
        ],
        series: [
            {
                type: 'radar',
                radarIndex: 1,
                areaStyle: {},
                data: [
                    {
                        value: data,
                        name: '某主食手机',
                        itemStyle: { // 单个拐点标志的样式设置。
                            normal: {
                                borderColor: 'rgba(0,0,255,1)',
                                // 拐点的描边颜色。[ default: '#000' ]
                                borderWidth: 3,
                                // 拐点的描边宽度，默认不描边。[ default: 0 ]
                            }
                        },
                        lineStyle: { // 单项线条样式。
                            normal: {
                                opacity: 0.5 // 图形透明度
                            }
                        },
                        areaStyle: { // 单项区域填充样式
                            normal: {
                                color: '#2c7be5' // 填充的颜色。[ default: "#000" ]
                            }
                        }
                    }
                ],
                tooltip: {
                    trigger: 'axis',
                    backgroundColor: '#0D1B42',  //鼠标移动到图上面时，显示的背景颜色
                    padding:15,     //定义内边距
                    formatter: function(params) { //自定义函数修改折线图给数据加单位
                       console.log(params)
                        var str = '';//声明一个变量用来存储数据
                        str += '<div>'+ params[0].name +'</div>';   //显示日期的函数
                        for(var i=0; i<params.length; i++) {  //图显示的数据较多时需要循环数据，这样才可以成功的给多条数据添加单位
                            str += '<div style="color:'+params[i].color+'"><span>'+ params[i].seriesName +'</span> : <span>'+ (params[i].data ? params[i].data+'%' : '暂无') +'</span></div>';
                        }
                        return str;
                    }
                },
            }
        ]
    };
    chart.clear();
    chart.hideLoading();
    chart.setOption(option);
}