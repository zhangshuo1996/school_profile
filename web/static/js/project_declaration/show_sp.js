let filtrate_page_width;
$(document).ready(function () {

    filtrate_page_width = (document.body.clientWidth) / 4;
    filtrate_page_width = filtrate_page_width > 500 ? filtrate_page_width : 500;
    document.getElementById("show_service_provider").style.width = filtrate_page_width + "px";
    hide_show_sp(filtrate_page_width);
});

$("#arrow").on("click", function (e) {
    if ($(this).hasClass("show")) {
        hide_show_sp(filtrate_page_width);
    } else {
        no_hide_show_sp();
    }
});

/*
显示增加服务型模态框
 */
$("#arrow2").on("click", function () {
    get_all_sp_category();
});


/*
增加服务商的提交按钮
 */
$("#add_sp_submit").on("click", function () {
    let sp_name = $("#sp_name").val();
    let sp_category_id = $("#sp_category").val();
    let charger_name = $("#charger_name").val();
    let telephone = $("#telephone").val();

    let data = {
        "sp_name": sp_name,
        "category_id": sp_category_id,
        "charger": charger_name,
        "telephone": telephone
    };
    add_sp(data);
});

$("#show_sp_info_table").on("click", ".delete-sp", function () {
    let sp_id = $(this).data("id");
    $.ajax({
        type: "get",
        url: "/project_declaration/ajax/delete_sp",
        data: {"sp_id": sp_id},
        dataType: "json",
        success: function (json_data) {
            get_all_sp_info();
            // $("#add_sp_modal").modal("hide");
            toggle_alert(true, "删除成功");
            hide_show_sp(filtrate_page_width);
        }
    })
})

function add_sp(data) {
    $.ajax({
        type: "get",
        url: "/project_declaration/ajax/add_sp",
        data: data,
        dataType: "json",
        success: function (json_data) {
             $("#add_sp_modal").modal("hide");
             toggle_alert(true, "新增成功");
             hide_show_sp(filtrate_page_width);
        }
    })
}


/*
获取 显示所有的服务商类型
 */
function get_all_sp_category() {
     $.ajax({
        type: "get",
        url: "/project_declaration/ajax/get_all_sp_category",
        dataType: "json",
        success: function (json_data) {
            let sp_category_list = json_data.data;
            fill_sp_category(sp_category_list);
        }
    })
}

/*
填充服务商类型下拉框
 */
function fill_sp_category(sp_category_list) {
    let html = [];
    for(let i=0; i < sp_category_list.length; i++){
        let row_data = `
            <option value="${sp_category_list[i]["id"]}">${sp_category_list[i]["name"]}</option>
        `;
        html.push(row_data);
    }
    let inner_html = html.join("");
    $("#sp_category").html(inner_html);
    $("#add_sp_modal").modal();

}

// function hide_filtrate_page(filtrate_page_width) {
function hide_show_sp(filtrate_page_width) {
    $("#arrow").removeClass("show");
    $("#arrow").attr("style", "font-size: 20px");
    document.getElementById("show_service_provider").style.right = `-${filtrate_page_width}px`;
}

function no_hide_show_sp() {
    $("#arrow").addClass("show");
    $("#arrow").attr("style", "color: #0000ee; font-size: 25px");
    document.getElementById("show_service_provider").style.right = 0;
    //获取并显示所有的服务商信息
    get_all_sp_info();
}


/*
获取所有的服务商信息
 */
function get_all_sp_info() {
    $.ajax({
        type: "get",
        url: "/project_declaration/ajax/get_sp_info",
        data: {"distribute_project_id": distribute_project_id},
        dataType: "json",
        success: function (json_data) {
            let ep_list = json_data.data;
            fill_sps(ep_list);
        }
    })
}

/*
填充服务商信息
 */
function fill_sps(sp_list) {
    let html = [];
    for(let i=0; i < sp_list.length; i++){
        let row_data = `
            <tr>
                <td>${sp_list[i]["name"]}</td>
                <td>${sp_list[i]["charger"]}</td>
                <td>${sp_list[i]["telephone"]}</td>
                <td title="删除"><span class="fe fe-delete delete-sp" data-id="${sp_list[i]["sp_id"]}"></span> </td>
            </tr>
        `;
        html.push(row_data);
    }
    let innerString = html.join("");
    $("#show_sp_info_table").html(innerString);
}