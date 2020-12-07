/**
 * 修改中介机构logo
 * */
$("#agent-avatar").on("change", function (e) {
    let avatar_url = getObjectURL(this.files[0]); //获取图片的路径，该路径不是图片在本地的路径
    updateAvatar("/user/update_agent_avatar", avatar_url);
});


//修改中介或者政府人员的头像
$("#avatar").on("change", function (e) {
    let avatar_url = getObjectURL(this.files[0]); //获取图片的路径，该路径不是图片在本地的路径
    updateAvatar("/user/update_avatar", avatar_url);
});


//建立可存取到file的url
function getObjectURL(file) {
    let url = null;
    if (window.createObjectURL != undefined) { // basic
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}


function updateAvatar(url, avatar_url){
    if (avatar_url) {
        $("#avatar-img-real").attr("src", avatar_url); //将图片路径存入src中，显示出图片
        $(".avatar .avatar-img.rounded-circle").attr("src", avatar_url);
        let avatar_file = new FormData();
        avatar_file.append('avatar', this.files[0]);
        $.ajax({
            url: url,
            type: "POST",
            data: avatar_file,
            processData: false,   // jQuery不要去处理发送的数据
            contentType: false,   // jQuery不要去设置Content-Type请求头
            dataType: "json",
            success: function (data) {
                if (data.error) {
                    toggle_alert(false, "头像上传失败");
                    return false;
                }
                toggle_alert(true, "上传成功");
            },
            error: function (error) {
                toggle_alert(false, "上传头像失败，请稍后再试");
            }
        });
    }
}

$("#set-superior").on("change", function (e) {
    let superior = $(this).val();
    $.ajax({
        type: "POST",
        url: "/gov_main/modify_superior",
        data: {"id": superior},
        dataType: "json",
        success: function (data) {
            toggle_alert(data.success, data.message);
        },
        error: function (e) {
            console.error(e);
            toggle_alert(false, "修改失败,请稍后再试");
        }
    });
});

$("#telephone").blur(function () {
    let telephone = $(this).val();
     if(/^1[34578]\d{9}$/.test(telephone)){
         $.ajax({
            type: "GET",
            url: "/admin/system/telephone_verify/",
            data: {"telephone": telephone},
            dataType: "json",
            success: function (data) {
                if (data.code==0){
                    $("#telephone_verify").css({'display':'','color':'#F00'})
                    $("#telephone_verify").html(data.data);
                }else{
                    $("#telephone_verify").css({'display':'','color':'green'})
                    $("#telephone_verify").html(data.data);
                }
            },
            error: function (e) {
                console.error(e);
            }
        });
     }else{
       $("#telephone_verify").css({'display':'','color':'#F00'})
       $("#telephone_verify").html("请输入正确的手机号")
     }

});
