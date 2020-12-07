let data = transport.data;
let sorted_patent_id_list = data["sorted_patent_id_list"];
let patent_id_authors_dict = data["patent_id_authors_dict"];
let patent_id_text_dict = data["patent_id_text_dict"];
let patent_id_team_id_list = data["patent_id_team_id_list"];
let patent_id_projects_dict = data["patent_id_projects_dict"];
let teacher_base_info = data["teacher_base_info"];

let old_input_key = transport.input_key;
let team_radar_chart = getEChartsObject('team-radar');
let index=0; // 搜索结果显示第几页
let patent_id = sorted_patent_id_list[index];

let team_relation_chart_obj = document.getElementById("team-relation-chart");
let team_relationship_chart = echarts.init(team_relation_chart_obj);

insert_search_outcome();


$(document).ready(function() {
    // $(".show_content ul li").next("ul").hide();
    $(".show_content ul li").click(function() {
        $(this).next("ul").toggle();
    });
    fill_input();
});

/*
填充搜索框中的搜索内容
 */
function fill_input(){
    $("#input_key").val(old_input_key);
}

/**
 * 鼠标悬浮时左右箭头变大
 */
$(".move-page").mouseover(function () {
    $(this).attr("style", "font-size: 3rem");
});
$(".move-page").mouseleave(function () {
    $(this).attr("style", "font-size: 2rem");
});


/**
 * 鼠标点击下载界面
 */
$("#search_outcome").on("click", "#download_page", function () {
   download_page();
});

let result;
function download_page(){
    $("#fill_data").val(index);
    let sub = document.getElementById('submit_download');
    sub.click();
}


/**
 *鼠标点击箭头时更换页面
 */
$("#next_page").on("click", function () {
    let cur_index = index;
    index = cur_index + 1;
    if(index >= sorted_patent_id_list.length-1){
        //"已经是最后一个团队"
        return ;
    }
    patent_id = sorted_patent_id_list[index];
    team_id = patent_id_team_id_list[patent_id];
    let teacher_id = patent_id_authors_dict[patent_id][0];
    insert_search_outcome();
     // 更新雷达图
    get_team_dimension_info(team_id);
    // 更新关系图
    getTeamRelation(team_id);
    show_index();
});


$("#last_page").on("click", function () {
    let cur_index = index;
    index = cur_index - 1;
    if(index < 0){
        //"已经是最后一个团队"
        return ;
    }
    let teacher_id = patent_id_authors_dict[patent_id][0];
    patent_id = sorted_patent_id_list[index];
    team_id = patent_id_team_id_list[patent_id];
    insert_search_outcome();
     // 更新雷达图
    get_team_dimension_info(team_id);
    // 更新关系图
    getTeamRelation(team_id);
    show_index();
});

/**
 *
 */
function insert_search_outcome() {
    let cur_patent_id = sorted_patent_id_list[index];
    let author_id_list = patent_id_authors_dict[cur_patent_id];
    let teacher_id = patent_id_authors_dict[patent_id][0];

    let team_id = patent_id_team_id_list[cur_patent_id];
    let school = teacher_base_info[teacher_id]["school"];
    let institution = teacher_base_info[teacher_id]["institution"];
    let lab = teacher_base_info[teacher_id]["lab"];
    let patent_name = patent_id_text_dict[cur_patent_id]["patent_name"];
    let patent_text = patent_id_text_dict[cur_patent_id]["patent_text"];
    let project_list = patent_id_projects_dict[cur_patent_id];
    let project_length = 6;
    if(project_list.length < 6){
        project_length = project_list.length;
    }

    let html = [];
    let row_data = `
        <div class="card">
                <div class="card-header">
                    <div class="card-header-title">
                    `;

    row_data += `
    
                    <span class="expert"><span class="fe fe-users" style="font-size: 2rem"></span>
    `;
    for(let j = 0; j < author_id_list.length; j++){
        if(j > 2){
            break;
        }
        let teacher_id = author_id_list[j];
        let teacher_name = teacher_base_info[teacher_id]["name"];
        row_data += `<span class="expert" style="margin: 1px; padding: 1px" data-id="${team_id}" data-institution="${institution}">${teacher_name}</span></span>`
    }
    row_data += `
        </div> <span class="institution"><span class="fe fe-home"></span> ${school}</span>
    `;

    if(institution !== "" && institution != null){
        row_data += `<span class="institution">- ${institution}</span>`;
    }
    if(lab !== "" && lab != null){
        row_data += `<span class="fe fe-box" style="margin-left: 1px; margin-right: 1px"></span><span> ${lab}</span>`;
    }

    row_data += `
        </div>
                <div class="card-body" style="">
                    <div class="row" style="">
                        <div class="col-md-12 show_content">
                            <ul style="list-style-type: none;">
                                <li><span class="fe fe-align-center"></span><a href="###">专利成果</a> <span class="badge badge-pill badge-primary">1</span></li>
                                    <span class="fe fe-bookmark" style="padding-left: 15px; line-height: 20px;">${patent_name}</span><br>
                                    <span class="fe fe-book-open" style="padding-left: 15px; line-height: 20px;">${patent_text}</span>
                            </ul>
                            <ul style="list-style-type: none;">
                                <li ><span class="fe fe-align-center"></span><a href="###">相关项目</a> <span class="badge badge-pill badge-success">${project_length}</span></li>
                                <ul>
    `;
    for(let j = 0; j < project_list.length; j++){
        if(j > 5){
            break;
        }
        row_data += `<li style="line-height: 20px;">${project_list[j]}</li>`;
    }
    row_data += `
                
                                
                                </ul>
                            </ul>
                        </div>
                    </div>
                    <div class="similar-patent"></div>
                </div>
            </div>
    
    `;

    html.push(row_data);

    let innerHtml = html.join("");
    $("#search_outcome").html(innerHtml);

    // 显示搜索结果中第一个团队的雷达图与关系图
    get_team_dimension_info(team_id);
    getTeamRelation(team_id);
    show_index();
}


/**
 * 获取该团队的内部关系数据，并重新加载关系图
 * by zhang
 */
function getTeamRelation(team_id){
    team_relationship_chart.showLoading();
    let leader_info = teacher_base_info[team_id];
    if(leader_info == undefined){
        team_relationship_chart.clear();
        $("#leader_name").html("成果著作人暂无团队");
        team_relationship_chart.hideLoading();
        debugger;
    }else{
        institution = leader_info["institution"];
        school = leader_info["school"];
        $.ajax({
            type: "get",
            url: "/school/search/getTeamRelation",
            data: {"school": school, "team_id": team_id, "institution": institution},
            dataType: "json",
            success: function (json_data) {
                if(json_data["success"]){
                    let graph_data = convert_graph_data(json_data);
                    let leader = json_data["leader"];
                    reloadGraph(graph_data);
                    $("#leader_name").html(leader + "团队内部合著关系");

                }else{
                    $("#leader_name").html("成果著作人暂无团队");
                    team_relationship_chart.hideLoading();
                }
            }
        })
    }
}


/**
 * 获取团队的各维度信息，用于更新雷达图
 */
function get_team_dimension_info(team_id) {

    let leader_info = teacher_base_info[team_id];
    if(leader_info == undefined) {
        team_radar_chart.clear();
        $("#radar_graph_header").html("成果著作人暂无团队");
        debugger;
    }else {
        $.ajax({
            type: "get",
            url: "/school/profile/get_team_dimension_info",
            data: {"team_id": team_id, "school": school},
            dataType: "json",
            success: function (json_data) {
                if (json_data["success"]){
                    // 更新雷达图
                    set_radar_option(
                         [
                                    {text: '研究人员水平', max: 100},
                                    {text: '研究人员数量', max: 100},
                                    {text: '学校水平', max: 100},
                                    {text: '实验平台', max: 100},
                                    {text: '成果数量', max: 100},
                                    {text: '项目数量', max: 100},
                                ],
                        [
                            json_data["researcher_level_score"],
                            json_data["researcher_num_score"],
                            json_data["school_level_score"],
                            json_data["lab_score"],
                            json_data["achieve_num"],
                            json_data["project_score"]
                        ],
                            team_radar_chart,
                    );
                    let leader = json_data["leader"];
                    $("#radar_graph_header").html(leader + "团队科研水平评估");
                }else{
                    $("#radar_graph_header").html("成果著作人暂无团队");
                }
            }
        })
    }
}

function show_index() {
    let row_arr = [];
    for(let i=0; i < sorted_patent_id_list.length-1; i++){
        let read_index = i + 1;
        if(index === i){
            row_arr.push(`<li class="page-item active"><a class="page-link" href="#">${read_index}</a></li>`)
        }else{
            row_arr.push(`<li class="page-item"><a class="page-link" href="#">${read_index}</a></li>`)
        }
    }
    let html_string = row_arr.join("");
    $("#show_index").html(html_string);

}