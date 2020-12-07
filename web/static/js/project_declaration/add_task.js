// $("#upload-file").on("change", function (e) {
//     if ($("#upload-file").val()) {
//         $("#form-upload-file").submit();
//     }
// });


/**
 * 用户点击添加任务的加号，弹出模态框
 */
$("#add_task").on("click", function () {
    let today = new Date();
    let year = today.getFullYear();
    let month = today.getMonth() + 1;
    month = month < 10 ? '0'+month : month;
    let day = today.getDate() < 10 ? '0'+today.getDate() : today.getDate();
    let time_str = year.toString() + "-" + month.toString() + "-" + day.toString();
    // 填充开始结束时间
    $("#add_task_start").val(time_str);
    $("#add_task_end").val(time_str);
    $("add_task_modal").modal();
});


/**
 * 用户新增任务
 * by zhang， 获取模态框中的数据，发送给后端相应的路由
 */
$("#add_task_button").on("click", function () {
    let add_task_name = $("#add_task_name").val();
    if(add_task_name.trim()==""){
        toggle_alert(false,"任务名不能为空");
        return false;
    }

    let data =new FormData();
    data.append("ep_id", ep_id);
    data.append("distribute_project_id", distribute_project_id);
    data.append("project_id", project_id);
    data.append("add_task_name", $("#add_task_name").val());
    data.append("add_task_executor", $("#add_task_executor").val());
    data.append("add_task_start", $("#add_task_start").val());
    data.append("add_task_end", $("#add_task_end").val());
    data.append("add_task_file", document.getElementById("upload_task_file").files[0]);
    data.append("add_task_default", $("#add_task_default").is(":checked"));

    add_task(data);
});


/**
 * 用户新增任务ajax请求
 * by zhang
 */
function add_task(data){
    $.ajax({
        type: "post",
        url: "/project_declaration/ajax/add_task",
        data: data,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (json_data) {
            if(json_data.error){
                toggle_alert(false, "新增失败");
                return false;
            }
            get_distribute_task();
            toggle_alert(true, "新增成功");
            $("#add_task_modal").modal("hide");
        }
    })
}

get_distribute_task();
