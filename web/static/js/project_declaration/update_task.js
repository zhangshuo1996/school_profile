/**
 * 更新某项任务的开始时间以及结束时间
 * by zhang
 */
function update_task_start_end(task, start, end){
    $.ajax({
        type: "post",
        url: "/project_declaration/ajax/update_task_start_end",
        data: {"task_id": task["id"], "start": start, "end": end},
        dataType: "json",
        success: function (json_data) {
            if(json_data.error){
                toggle_alert(false, "获取失败");
                return false;
            }
            // toggle_alert(true, "起止时间更新成功");
        }
    })
}


/**
 * 更新某项任务的进度
 * by zhang
 */
function update_task_progress(task, progress){
    $.ajax({
        type: "post",
        url: "/project_declaration/ajax/update_task_progress",
        data: {"task_id": task["id"], "progress": progress, "distribute_project_id": distribute_project_id},
        dataType: "json",
        success: function (json_data) {
            if(json_data.error){
                return false;
            }
        }
    })
}


/**
 * 用户点击弹出更新模态框
 * by zhang
 */
$("#task-distribute-list").on("click", ".text-truncate", function (e) {
    if(can_write == false){
        // 没有写权限时不触发， 直接返回
        return;
    }
    //填充更新模态框
    $("#update_task_id").val($(this).data("id"));
    $("#update_task_name").val($(this).data("name"));
    $("#update_executor").val($(this).data("executor"));
    $("#update_start").val($(this).data("start"));
    $("#update_end").attr("min", $(this).data("start")).val($(this).data("end"));
    $("#update_task_status").val($(this).data("status"));
    let file_id = $(this).data("fid");
    // if(file_id == undefined){ // 该任务没有对应的文件
    //
    // }else{ //该任务有对应的文件，隐藏模态框中的上传部分
    //
    // }
    $("#template-list-modal").modal();
});


/**
 * 用户确认更新提交
 * by zhang
 */
$("#update_submit").on("click", function () {
    let task_id = $("#update_task_id").val();
    let task_name = $("#update_task_name").val();
    let executor = $("#update_executor").val();
    let start = $("#update_start").val();
    let end = $("#update_end").val();
    let task_status = $("#update_task_status").val();
    let update_default = $("#update-default").is(":checked");

    let data =new FormData();
    data.append("task_id", task_id);
    data.append("task_name", task_name);
    data.append("executor", executor);
    data.append("start", start);
    data.append("end", end);
    data.append("default", update_default);
    data.append("project_id", project_id);
    data.append("task_status", task_status);
    data.append("update_task_file", document.getElementById("update_task_file").files[0]);

    $.ajax({
        type: "post",
        url: "/project_declaration/ajax/update_task",
        data: data,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (json_data) {
            if(json_data.error){
                toggle_alert(false, "获取失败");
                return false;
            }
            toggle_alert(true, "更新成功");
            // 重新获取并显示任务的分配情况
            get_distribute_task();
            $("#template-list-modal").modal("hide");
        }
    })
});


/**
 * 用户确认删除某一任务
 * by zhang
 */
$("#delete_submit").on("click", function () {
    let task_id = $("#update_task_id").val();
    $.ajax({
        type: "post",
        url: "/project_declaration/ajax/delete_task",
        data: {"task_id": task_id},
        dataType: "json",
        success: function (json_data) {
            if(json_data.error){
                toggle_alert(false, "获取失败");
                return false;
            }
            toggle_alert(true, "更新成功");
            // 重新获取并显示任务的分配情况
            get_distribute_task();
            $("#template-list-modal").modal("hide");
        }
    })
});
