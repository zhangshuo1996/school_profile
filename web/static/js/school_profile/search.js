/*
搜索点击事件监听
 */
$("#submit_button").on("click", function () {
    let input_key = $("#input_key").val();
    if(input_key != ""){
        // 显示加载圆圈
        $("#load_cycle").attr("class", "");
    }
});

function search(){
    var input_key = document.getElementById("input_key2").value;
    console.log(input_key);
    console.log("0----");
    $.ajax({
        url: '/get_input',
        data: {"input_key": input_key},
        type: "POST",
        dataType: "json",
        success: function(data){
            console.log(data["data"]);
            fill(data);
        }
    });
}

/*

*/
function fill(data){
    fill_str = "";
    for(i = 0; i < data.length; i++){
        tmp_str = "<p>" + data[i]["basic_info"]["school"] + "</p>" +
                "<p>" + data[i]["basic_info"]["institution"] + "</p>" +
                "<p>" + data[i]["basic_info"]["name"] + "</p>" +
                "<p>" + data[i]["achieve_nums"] + "</p>" +"<br>";
        fill_str += tmp_str;
    }
    document.getElementById("fill").innerHTML = fill_str;
    console.log("success");
}
