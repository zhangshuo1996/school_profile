// import Chart from "./chart.js";
// console.log("school.js");
// var school = transport.school;
// var dataset = [
//         {"x": "计算机学院", "y": 2019, "r": 56},
//         {"x": "计算机学院", "y": 2018, "r": 45},
//         {"x": "计算机学院", "y": 2017, "r": 49},
//         {"x": "计算机学院", "y": 2016, "r": 51},
//         {"x": "计算机学院", "y": 2015, "r": 59},
//         {"x": "软件学院", "y": 2019, "r": 23},
//         {"x": "软件学院", "y": 2018, "r": 21},
//         {"x": "软件学院", "y": 2017, "r": 15},
//         {"x": "软件学院", "y": 2016, "r": 30},
//         {"x": "软件学院", "y": 2015, "r": 26},
//         {"x": "机械学院", "y": 2019, "r": 56},
//         {"x": "机械学院", "y": 2018, "r": 45},
//         {"x": "机械学院", "y": 2017, "r": 49},
//         {"x": "机械学院", "y": 2016, "r": 51},
//         {"x": "机械学院", "y": 2015, "r": 59},
//         {"x": "信息学院", "y": 2019, "r": 56},
//         {"x": "信息学院", "y": 2018, "r": 45},
//         {"x": "信息学院", "y": 2017, "r": 49},
//         {"x": "信息学院", "y": 2016, "r": 51},
//         {"x": "信息学院", "y": 2015, "r": 59},
//         {"x": "建筑学院", "y": 2019, "r": 56},
//         {"x": "建筑学院", "y": 2018, "r": 45},
//         {"x": "建筑学院", "y": 2017, "r": 49},
//         {"x": "建筑学院", "y": 2016, "r": 51},
//         {"x": "建筑学院", "y": 2015, "r": 59},
//         {"x": "自动化学院", "y": 2019, "r": 56},
//         {"x": "自动化学院", "y": 2018, "r": 45},
//         {"x": "自动化学院", "y": 2017, "r": 49},
//         {"x": "自动化学院", "y": 2016, "r": 51},
//         {"x": "自动化学院", "y": 2015, "r": 59},
//         {"x": "汽车学院", "y": 2019, "r": 56},
//         {"x": "汽车学院", "y": 2018, "r": 45},
//         {"x": "汽车学院", "y": 2017, "r": 49},
//         {"x": "汽车学院", "y": 2016, "r": 51},
//         {"x": "汽车学院", "y": 2015, "r": 59},
//         {"x": "材料学院", "y": 2019, "r": 56},
//         {"x": "材料学院", "y": 2018, "r": 45},
//         {"x": "材料学院", "y": 2017, "r": 49},
//         {"x": "材料学院", "y": 2016, "r": 51},
//         {"x": "材料学院", "y": 2015, "r": 59},
//         {"x": "地质学院", "y": 2019, "r": 56},
//         {"x": "地质学院", "y": 2018, "r": 45},
//         {"x": "地质学院", "y": 2017, "r": 49},
//         {"x": "地质学院", "y": 2016, "r": 51},
//         {"x": "地质学院", "y": 2015, "r": 59},
//         {"x": "物理学院", "y": 2019, "r": 56},
//         {"x": "物理学院", "y": 2018, "r": 5},
//         {"x": "物理学院", "y": 2017, "r": 9},
//         {"x": "物理学院", "y": 2016, "r": 5},
//         {"x": "物理学院", "y": 2015, "r": 9},
// ]; // 给定的数据
// var institution_list = [];
// var year_list = [];
// var color_list = ["","","","","","","","","","","","","","","","","","","","",""];
// get_institution_year();
//
//     console.log(institution_list);
//     console.log(year_list);
//     console.log(dataset);
//     console.log("-------1");
//     /* ----------------------------配置参数------------------------  */
//     const chart = new Chart();
//     const config = {
//         margins: {top: 20, left: 40, bottom: 40, right: 0},
//         textColor: 'black', // 文本颜色
//         gridColor: 'black', // 坐标颜色
//         ShowGridX: [10, 20, 30, 40, 50, 60, 70 ,80, 90, 100],
//         ShowGridY: [10, 20, 30, 40, 50, 60, 70 ,80, 90, 100],
//         title: school + '各学院成果分布图',
//         pointMaxSize: 20,
//         hoverColor: 'white',
//         animateDuration: 100,
//         pointCenterColor: 'white', // 气泡中心颜色
// //        pointEdgeColor: chart._colors(0)
//         pointEdgeColor: 'grey'  // 气泡边缘颜色
//     }
//
//     chart.margins(config.margins);
//
//     /* ----------------------------尺度转换------------------------  */
//
//     chart.scaleX = d3.scaleBand()
//                         .domain(institution_list)
//                         .range([0, chart.getBodyWidth() - 150 ])
//
//     chart.scaleY = d3.scaleBand()
// //                    .domain([0, Math.ceil(d3.max(data, (d) => d.y)/10)*10])
//                     .domain(year_list)
//                     .range([chart.getBodyHeight() , 40]);
//
//     chart.scaleSize = d3.scaleLinear()
//                         .domain([0, d3.max(dataset, (d) => d.r)])
//                         .range([0, config.pointMaxSize]);
//
//
//     /* ----------------------------渲染数据点------------------------  */
//     chart.renderPoints = function(){
//         let points = chart.body().selectAll('.point')
//                     .data(dataset);
//             console.log("!!@@")
//             console.log(points)
//             points.data(dataset)
//                     .enter()
//                     .append('circle')
//                     .classed('point', true)
//                 .merge(points)
//                     .attr('cx', (d) => chart.scaleX(d.x) + chart.getBodyWidth() / (institution_list.length+1) / 2)
//                     .attr('cy', (d) => chart.scaleY(d.y) + chart.getBodyHeight() / (year_list.length + 1) / 2)
//                     .attr('r', 0)
//                     .attr('fill', 'url(#bubble-fill)')
//                     .transition().duration(config.animateDuration)
//                     .attr('r', (d) => chart.scaleSize(d.r));
//
//             points.exit()
//                     .remove();
//     }
//
//    /* ----------------------------定义颜色径向渐变------------------------  */
//     chart.defRadialGrad = function(){
//         const radialGrad = chart.svg()
//
//                                 .append('defs')
//                                 .append('radialGradient')
//                                 .attr('id', 'bubble-fill')
//                                 .attr('cx', 0.4)
//                                 .attr('cy', 0.4);
//
//
//               radialGrad.append('stop')
//                         .attr('offset', '0%')
//                         .attr('stop-color', config.pointCenterColor);
//
//               radialGrad.append('stop')
//                         .attr('offset', '100%')
//                         .attr('stop-color', config.pointEdgeColor);
//
//     }
//
//     /* ----------------------------渲染坐标轴------------------------  */
//     chart.renderX = function(){  //渲染X轴
//         chart.svg()
//                 .insert('g','.body')
//                 .attr('transform', 'translate(' + chart.bodyX() + ',' + (chart.bodyY() + chart.getBodyHeight()) + ')')
//                 .attr('class', 'xAxis')
//                 .call(d3.axisBottom(chart.scaleX));
//     }
//
//     chart.renderY = function(){ //渲染Y轴
//         chart.svg()
//                 .insert('g','.body')
//                 .attr('transform', 'translate(' + chart.bodyX() + ',' + chart.bodyY() + ')')
//                 .attr('class', 'yAxis')
//                 .call(d3.axisLeft(chart.scaleY));
//     }
//
//     chart.renderAxis = function(){
//         chart.renderX();
//         chart.renderY();
//     }
//
//     console.log("-------5");
//     /* ----------------------------渲染文本标签------------------------  */
//     chart.renderText = function(){
//         d3.select('.xAxis').append('text')
//                             .attr('class', 'axisText')
//                             .attr('x', chart.getBodyWidth())
//                             .attr('y', 0)
//                             .attr('fill', config.textColor)
//                             .attr('dy', 30)
//                             .text('X');
//
//         d3.select('.yAxis').append('text')
//                             .attr('class', 'axisText')
//                             .attr('x', 0)
//                             .attr('y', 0)
//                             .attr('fill', config.textColor)
//                             .attr('dx', '-30')
//                             .attr('dy', '10')
//                             .text('Y');
//     }
//
//     /* ----------------------------渲染网格线------------------------  */
//     chart.renderGrid = function(){
//         d3.selectAll('.yAxis .tick')
//             .each(function(d, i){
//                 if (config.ShowGridY.indexOf(d) > -1){
//                     d3.select(this).append('line')
//                         .attr('class','grid')
//                         .attr('stroke', config.gridColor)
//                         .attr('x1', 0)
//                         .attr('y1', 0)
//                         .attr('x2', chart.getBodyWidth())
//                         .attr('y2', 0);
//                 }
//             });
//
//         d3.selectAll('.xAxis .tick')  //
//             .each(function(d, i){
//                 console.log("______________", d);
//                 if (config.ShowGridX.indexOf(d) > -1){
//                     d3.select(this).append('line')
//                         .attr('class','grid')
//                         .attr('stroke', config.gridColor)
//                         .attr('x1', 0)
//                         .attr('y1', 0)
//                         .attr('x2', 0)
//                         .attr('y2', -chart.getBodyHeight());
//                 }
//             });
//     }
//
//     /* ----------------------------渲染图标题------------------------  */
//     chart.renderTitle = function(){
//         chart.svg()
//                 .append('text')
//                 .classed('title', true)
//                 .attr('x', chart.width()/2)
//                 .attr('y', 0)
//                 .attr('dy', '2em')
//                 .text(config.title)
//                 .attr('fill', config.textColor)
//                 .attr('text-anchor', 'middle')
//                 .attr('stroke', config.textColor);
//
//     }
//
//     /* ----------------------------绑定鼠标交互事件------------------------  */
//     chart.addMouseOn = function(){
//         //防抖函数
//         function debounce(fn, time){
//             let timeId = null;
//             return function(){
//                 const context = this;
//                 const event = d3.event;
//                 timeId && clearTimeout(timeId)
//                 timeId = setTimeout(function(){
//                     d3.event = event;
//                     fn.apply(context, arguments);
//                 }, time);
//             }
//         }
//
//         d3.selectAll('.point')
//             .on('mouseover', function(d){
//                 const e = d3.event;
//                 const position = d3.mouse(chart.svg().node());
//                 e.target.style.cursor = 'hand'
//
//                 d3.select(e.target)
//                     .attr('r', chart.scaleSize(d.r) + 5);
//
//                 chart.svg()
//                     .append('text')
//                     .classed('tip', true)
//                     .attr('x', position[0]+5)
//                     .attr('y', position[1])
//                     .attr('fill', config.textColor)
//                     .text( d.x + ' ' + d.y + '年专利数量：' + d.r + "件");
//             })
//             .on('mouseleave', function(d){
//                 const e = d3.event;
//
//                 d3.select(e.target)
//                     .attr('r', chart.scaleSize(d.r));
//
//                 d3.select('.tip').remove();
//             })
//             .on('mousemove', debounce(function(){
//                     const position = d3.mouse(chart.svg().node());
//                     d3.select('.tip')
//                     .attr('x', position[0]+5)
//                     .attr('y', position[1]-5);
//                 }, 6)
//             );
//     }
//
//     chart.render = function(){
//
//         chart.renderAxis();
//
// //        chart.renderText();
//
// //        chart.renderGrid();
//
//         chart.defRadialGrad();
//
//         chart.renderPoints();
//
//         chart.addMouseOn();
//
//         chart.renderTitle();
//
//         console.log("-------10");
//     }
//
//     chart.renderChart();
//
// /*
// 从给定的数据中获取学校列表和年份列表
// */
// function get_institution_year(){
//     for(var i = 0; i < dataset.length; i++){
//             var institution = dataset[i].x;
//             var year = dataset[i].y;
//             if(institution_list.indexOf(institution) == -1){
//                 institution_list.push(institution);
//             }
//             if(year_list.indexOf(year) == -1){
//                 year_list.push(year);
//             }
//         }
// }
//
// var expand = document.getElementById("expand");
// var oA = expand.getElementsByTagName("a");
// var onOff = true;
// var old = "";
// console.log(oA);
// oA[0].onclick = function move(){
//     console.log(onOff);
//     if(onOff){
//         onOff = false;
//         old = expand.innerHTML; //原始文档
//         expand.innerHTML = expand.innerHTML.substring(0, 120) + "...<a href=\"javascript:;\"> 》 展开 </a>";
//         oA = expand.getElementsByTagName('a');
//         oA[0].onclick = move;
//     }else{
//         onOff = true;
//         expand.innerHTML = old;
//         oA = expand.getElementsByTagName('a');
//         oA[0].onclick = move;
//     }
// }
//
