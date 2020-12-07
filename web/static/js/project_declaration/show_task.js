/**
 * 根据分配的项目id，获取该项目下所有的任务
 * by zhang
 */
function get_distribute_task() {
    $.ajax({
        type: "get",
        url: "/project_declaration/ajax/get_distribute_task",
        data: {"distribute_project_id": distribute_project_id},
        dataType: "json",
        success: function (json_data) {
            if (json_data.error) {
                toggle_alert(false, "获取失败");
                return false;
            }
            let tasks = [];
            let data = json_data.data;
            for (let i = 0; i < data.length; i++) {
                tasks.push({
                    id: String(data[i]["task_id"]),
                    name: data[i]["task_name"],
                    start: data[i]["gmt_create"],
                    end: data[i]["gmt_deadline"],
                    progress: 100,
                    executor: data[i]["executor"],
                    status: data[i]["status"],
                    file_id: data[i]["file_id"]
                })
            }
            // 构造甘特图
            gantt = construct_gantt(tasks);
            gantt.change_view_mode(json_data.mode);
            // 显示甘特图左边栏的具体任务
            show_tasks(tasks);
        }
    })
}


/**
 * 显示甘特图左边栏的具体任务
 */
function show_tasks(tasks) {
    let html = [];
    for (let i = 0; i < tasks.length; i++) {
        let status = tasks[i]["status"];
        let show_type, show_status;
        if (status == 0) {
            show_type = "primary";
            show_status = "待分配"
        } else if (status == 1) {
            show_type = "secondary";
            show_status = "进行中"
        } else {
            show_type = "success";
            show_status = "已完成"
        }
        let download="";
        if(tasks[i]["file_id"] != undefined){
            download = `<a href="/file/download_file/${tasks[i]["file_id"]}" target="_blank">
                            <span class="fe fe-download"></span>
                        </a>`;
        }
        let row_data = `
            <div class="list-group-item p-0 d-flex">
                <span class="text-truncate cursor-pointer" data-id="${tasks[i]["id"]}" data-name="${tasks[i]["name"]}"
                    data-executor="${tasks[i]["executor"]}" data-start="${tasks[i]["start"]}"
                    data-end="${tasks[i]["end"]}" data-status="${tasks[i]["status"]}" data-fid="${tasks[i]["file_id"]}">
                    ${tasks[i]["name"]}
                </span>
                <span class="ml-auto pr-2 nowrap">
                    ${download}
                    <span class="badge badge-${show_type}">${show_status}</span>
                </span>
            </div>
        `;

        html.push(row_data);
    }
    if(html.length === 0){
        html.push("<p>暂无任务</p>");
    }
    $("#show_tasks").html(html.join(""));
}


/**
 * gantt 构造甘特图
 */
let gantt;

function construct_gantt(tasks) {
    let gantt = new Gantt("#gantt", tasks);
    return gantt;
}

/**
 * 添加修改时间的监听事件
 * */
$("#add_task_start").on("change", function (e) {
    $("#add_task_end").attr("min", $(this).val()).val($(this).val());
});

$("#update_start").on("change", function (e) {
    $("#update_end").attr("min", $(this).val()).val($(this).val());
});
