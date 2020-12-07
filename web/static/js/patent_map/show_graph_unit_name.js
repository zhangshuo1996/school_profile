let category = $('#unit').attr('data-category');
let unit_name = $('#unit').text();

ajaxGetCommunities(category, unit_name);
//节点点击事件
graphChart.on('click', function (params){
    if (params.dataType != 'node')
        return ;
    //获取类别
    let class_ = params.value[1];
    //有效值判断
    if (category.length == 0 || isNaN(parseInt(class_))){
        toggle_alert(false, '数据出错，请稍后重试');
        return ;
    }
    //TODO: 待删除
    //构造链接
    /*
    let param = `category=${category}&unit_name=${unit_name}&class_=${class_}`;
    let url = COMMUNITY_DETAIL_URL + '?' + param;
    window.location.href = url;
     */
});
