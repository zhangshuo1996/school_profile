let clock;
let nums = 60;
/*
用户点击获取验证码事件
 */
$("#get_verification_code").click(function (thisBtn) {
    let telephone = $("#telephone").val();
    let flag = isMobileNumber(telephone);
    if(!flag){
        return ;
    }
    $("#get_verification_code").attr("disabled", "true");
    //是否发送成功
    let data = {
        "telephone": telephone
    };
    get_verification_code(data);
});

/*
判断手机号是否合理
 */
function isMobileNumber(phone) {
    let flag = false;
    let message = "";
    let myreg = /^(((13[0-9]{1})|(14[0-9]{1})|(17[0-9]{1})|(15[0-3]{1})|(15[4-9]{1})|(18[0-9]{1})|(199))+\d{8})$/;
    if (phone == '') {
        message = "手机号码不能为空！";
    } else if (phone.length != 11) {
        message = "请输入11位手机号码！";
    } else if (!myreg.test(phone)) {
        message = "请输入有效的手机号码！";
    } else {
        flag = true;
    }
    if (message != "") {
        toggle_alert(false, message);
    }
    return flag;
}

/*
获取验证码倒计时时间函数
 */
function doLoop() {
    nums--;
    if(nums > 0){
        $("#get_verification_code").text(nums + '秒后重新获取');
    }else{
        clearInterval(clock);
        $("#get_verification_code").attr("disabled", "false");
        $("#get_verification_code").text("点击发送验证码");
        nums = 60;
    }
}


/*
获取验证码
 */
function get_verification_code(data) {
    $.ajax(
        {
            url: "/auth/get_verification_code",
            type: "POST",
            data: data,
            dataType: "json",
            success: function (json_data) {
                //验证码发送失败
                if(json_data.error){
                    toggle_alert(false, json_data.errorMsg);
                    $("#get_verification_code").attr("disabled", "false");
                    return false;
                }
                toggle_alert(true, "验证码已发送，请查收");
                $("#get_verification_code").text(nums + '秒后重新获取');
                clock = setInterval(doLoop, 1000);
            }
        }
    )
}

$(document).ready(function(){
    let type = $('#login_type').val();
    if (type == 'password')
        changeForm(0);
    else
        changeForm(1);
});


function changeForm(selectedIdx){
    //index:0 password index:1 code
    let forms = [['#password_type', '#password'], ['#code_type', '#verification_code']];
    //显示选中
    $(forms[selectedIdx][0]).addClass('active');
    $(forms[selectedIdx][1]).parent().parent().removeClass('d-none');
    //隐藏未选中的
    let unselected = selectedIdx == 0?1:0;
    $(forms[unselected][0]).removeClass('active');
    $(forms[unselected][1]).parent().parent().addClass('d-none');
    /*
    $('#code_type').addClass('active');
    $('#verification_code').parent().parent().removeClass('d-none');

    $('#password_type').removeClass('active');
    $('#password').parent().parent().addClass('d-none');
     */
}
//密码登录
$('#password_type').click(function (e){
    changeForm(0);
    //填充数据
    let $target = $(e.target);
    let type = $target.data("target");
    $('#login_type').val(type);
});
//验证码登录
$('#code_type').click(function (e){
    changeForm(1);
    //填充数据
    let $target = $(e.target);
    let type = $target.data("target");
    $('#login_type').val(type);
});

