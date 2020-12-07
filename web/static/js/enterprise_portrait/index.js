// 移除搜索记录
$(".btn-delete").on("click", function() {
        let id = $(this).attr("data-id");
        let data = {"history_id": id};
        let tr =  $(this).parents("tr");
        $.ajax({
            type: "get",
            url: "/data_mining/enterprise_portrait/delete_history",
            data: data,
            dataType: "json",
            success:function(json_data){
                if(json_data.status){
                    tr.remove();
                }
            },
            error: function (error) {
            }
        });
});