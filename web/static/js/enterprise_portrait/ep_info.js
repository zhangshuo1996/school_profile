 $("#sort").change(function() {
     var vs = $('#sort  option:selected').val();
     var ep_id_list = $("#ep_id_list").val();
     var pa_id_list = $("#pa_id_list").val();
     let data = {"vs":vs, "ep_id_list": ep_id_list, "pa_id_list": pa_id_list};
     $.ajax({
        type: "get",
        url: "/data_mining/enterprise_portrait/sort_ep",
        data: data,
        dataType: "json",
        success: function (response) {

            if(response.status == true){
                $("#ep_base_info").html("");
                let html = [];
                for(let i = 0; i < response.ep_info.length; i++){
                    let row_data = `<div class="row">
                    <div class="col-sm-8 offset-sm-2" id="search-results">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="card-title">
                                    <span class="text-primary">
                                        <a href="/get_ep_detail/${response.ep_info[i]['id']}/${response.ep_info[i]['name']}/${response.ep_info[i]['pa_id']}"}>
                                            ${response.ep_info[i]["name"]}
                                        </a>
                                    </span>
                                </h3>
                                <small>注册资金：
                                    <span class="text">
                                         ${response.ep_info[i]["registered_capital"]}万元&nbsp;&nbsp;&nbsp;&nbsp;
                                    </span>
                                </small>
                                <small>成立时间：
                                    <span class="text">
                                         ${response.ep_info[i]["entablish_date"]}&nbsp;&nbsp;&nbsp;&nbsp;
                                    </span>
                                </small>
                                <small>电话：
                                    <span class="text">
                                         ${response.ep_info[i]["telephone"]}
                                    </span>
                                </small>
                                <br>
                                <small>相关工程师：
                                    <span class="text">
                                         ${response.ep_info[i]["engineers"]}
                                    </span>
                                </small>

                            </div>
                        </div>
                    </div>
                    </div>
                    `;
                html.push(row_data);
                }
                let html_string = html.join("");
                $("#ep_base_info").html(html_string);
            }
        },
        error: function(){
            console.log("error")
        }
    });
 });
