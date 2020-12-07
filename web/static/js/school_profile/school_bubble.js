// let school_industry_level_compare_bubble_chart = getEChartsObject("school_industry_level_compare_bubble");
//
// let industry_list = [];
// let institution_list = ['Saturday', 'Friday', 'Thursday',
//         'Wednesday', 'Tuesday', 'Monday', 'Sunday', 'Sunday', 'Sunday'];
// let bubble_option = {};
// let max_patent_num = 500;
// let color_list = [
//     "#2c7be5", "#6baed6", "#9ecae1",
//     "#e6550d", "#fdae6b",  "#fdd0a2",
//     "#31a354", "#74c476", "#a1d99b",
//     "#bdbdbd",
// ];
//
//
// let bubble_data = [];
//
// get_industry_num_by_level();
//
//
// function get_industry_num_by_level(){
//     $.ajax({
//         type: "get",
//         url: "/school/profile/get_institution_industry_patent_num",
//         data: {"school": school},
//         dataType: "json",
//         success: function (json_data) {
//             max_patent_num = json_data["max_num"];
//             institution_list = json_data["institution_list"];
//             industry_list = json_data["industry_list"];
//             bubble_data = json_data["result"];
//             bubble_data = bubble_data.map(function (item) {
//                 return [item[1], item[0], item[2], item[3], item[4]];
//             });
//             set_bubble_option();
//             school_industry_level_compare_bubble_chart.setOption(bubble_option);
//         }
//     })
// }
//
//
// function set_bubble_option(){
//    bubble_option = {
//         title: {
//             text: '',
//             link: 'https://github.com/pissang/echarts-next/graphs/punch-card'
//         },
//         legend: {
//             data: ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D'],
//             color:["#2c7be5", "#6baed6", "#9ecae1",
//                     "#e6550d", "#fdae6b",  "#fdd0a2",
//                     "#31a354", "#74c476", "#a1d99b"],
//             // left: 'left',
//             show: true
//         },
//         tooltip: {
//             position: 'top',
//             formatter: function (params) {
//                 return institution_list[params.value[1]] + " \n "  + industry_list[params.value[0]] + '\n' + params.value[4];
//             }
//         },
//         grid: {
//             left: 'left',  // 设置边距
//             top: '3%',
//             bottom: 10,
//             right: 100,
//             containLabel: true
//         },
//         xAxis: {
//             position: 'top',
//             type: 'category',
//             data: industry_list,
//             // boundaryGap: false,
//             splitLine: {
//                 show: false,  // 是否显示间隔线
//                 lineStyle: {
//                     color: '#999',
//                     // type: 'dashed'
//                 }
//             },
//             axisLine: {
//                 show: true
//             },
//             axisLabel: {
//                interval:1,  // 设置坐标轴文字旋转
//                rotate:-10
//             }
//         },
//         yAxis: {
//             type: 'category',
//             data: institution_list,
//             axisLine: {
//                 show: true
//             },
//             axisLabel: {
//                interval: 0,
//                rotate:10
//             }
//         },
//         series: [{
//             name: 'Punch Card',
//             type: 'scatter',
//             symbolSize: function (val) {
//                 return convert_data(val[2]);
//             },
//             data: bubble_data,
//             itemStyle: {
//                 color: function (val) { //  点的颜色实现
//                     let level = val["data"][3];
//                     return color_list[level-1];
//                 }
//             },
//             // animationDelay: function (idx) {  // 实现动画效果
//             //     return idx * 5;
//             // }
//         }],
//         // dataZoom: [{  // 设置滑动条
//         //     yAxisIndex: 0,
//         //     show: true,//是否显示滑动条，不影响使用
//         //     type: 'slider', // 这个 dataZoom 组件是 slider 型 dataZoom 组件
//         //     startValue: 0, // 从头开始。
//         //     endValue: 3  // 一次性展示6个。
//         // }]
//     };
// }
//
// /**
//  * 将专利数量转化为点的大小
//  */
// function convert_data(patent_num) {
//     if(patent_num === 0){
//         return 0;
//     }
//     if(patent_num > max_patent_num / 2){
//         return 30;
//     }else if(patent_num > max_patent_num / 4){
//         return 22
//     }else if(patent_num > max_patent_num / 8){
//         return 16
//     }else if(patent_num > max_patent_num / 16){
//         return 12
//     }else if(patent_num > max_patent_num / 24){
//         return 8
//     }else if(patent_num > max_patent_num / 32){
//         return 5
//     }else if(patent_num > max_patent_num / 48){
//         return 3
//     }else if(patent_num > max_patent_num / 64){
//         return 2
//     }else{
//         return 1;
//     }
// }
//
// /**
//  * 气泡图点击事件, 跳转至学院画像
//  */
// school_industry_level_compare_bubble_chart.on("click", function (params) {
//     let index = params.value[0];
//     let institution = institution_list[institution_list.length - 1 - index];
//     debugger;
//     // window.location.href = "/school/profile/institution_profile/" + school + "/" + institution;
// });
//
//
//
//
//
