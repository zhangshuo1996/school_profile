var school_data = [];
var input_school_list = [];

var $searchInput;
var setSelectedItem;
var selectedItem;

var all_school = [];

judge_project_id();

let csrf_token = "{{ csrf_token() }}";
//在确保请求不属于GET HEAD OPTIONS TRACE，并且发向站内，才设置csrf_token
$.ajaxSetup({
        beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
    }
});

$(document).ready(function () {
    $("#select_id").select2();
});


$(".form_datetime").datetimepicker({
    format: 'yyyy-mm-dd hh:ii',
    autoclose: true,
    language: 'zh-CN',
    todayHighlight: true,
    minuteStep: 10
});
$('#start_time').on('click', function () {
    $('#start_time').datetimepicker('show');
});
$('#end_time').on('click', function () {
    $('#end_time').datetimepicker('show');
});
/*
项目选择框变化  事件
*/
$("#project").change(function (e) {
    judge_project_id();
});


/*
判断项目是否为产学研项目，
    若是，则显示学校输入框
    若非，非不显示
 */
function judge_project_id() {
    let project_id = $("#project").val();
    if(project_id == "82"){
        show_school_select(true);
    }else{
        show_school_select(false);
    }
}


/*
显示学校选择框
 */
function show_school_select(is_showed) {
    if(is_showed){
        $("#school_select").removeClass("d-none");
        // 获取学校名单， 填充数据
        if(all_school.length == 0){
            all_school = get_all_school();

        }
    }else{
        $("#school_select").addClass("d-none");
    }
}

/*
获取所有的学校名单
 */
function get_all_school(){
    $.ajax({
        url: "/activity/get_all_school",
        dataType: "json",
        type: "get",
        success: function (json_data) {
            all_school = json_data.data;
            fill_school_select_data(all_school);
            return all_school;
        }
    })
}


/*
填充学校下拉框数据
 */
function fill_school_select_data(){
    let html = [`--请选择合作高校--`];
    for(let i = 0; i < all_school.length; i++){
        let row_data = `<option value="${all_school[i]["name"]}">${all_school[i]["name"]}</option>`;
        html.push(row_data);
    }
    let html_string = html.join("");
    $("#select_id").html(html_string);
}

$("#select").on("change", function () {
    let select_school = $("#select_id").val();
    add_school_tag(select_school);
});


/**
 * 手动添加tag
 * */
$("#determine-tag").on("click", function () {
    let tag = $("#search-text").val().trim();
    if (tag.length){
        add_school_tag(tag);
    }
    $("#search-text").val("");
});

function add_school_tag(name) {
    let html = `
        <label class="mr-2 position-relative school-tag">
            <span class="badge badge-success font-size-base">${name}</span>
            <span class="delete-tag cursor-pointer"><i class="fe fe-x-circle hover-danger"></i></span>
            <input type="hidden" name="input_school_list[]" value="${name}"/>
        </label>`;
    $("#show_school").append(html);
}

/**
 * 删除tag
 * */
$("#show_school").on("click", ".delete-tag", function () {
    $(this).parent(".school-tag").remove();
});


