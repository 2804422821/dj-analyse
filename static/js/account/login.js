;var login = function () {

    var handle_login_form = function () {
        $("#loginform").validate({
            errorClass: "text-danger",
            rules: {
                account: {
                    required: true,
                },
                password: {
                    required: true,
                }
            },
            messages: {
                account: {
                    required: '用户名不能为空'
                },
                password: {
                    required: '密码不能为空'
                }
            },
            success: function (label) {
                label.remove();
            },
            errorPlacement: function (error, element) {
                error.insertAfter(element);
            }
        })
    }

    var handle_recover_form = function () {
        $("#recoverform").validate({
            errorClass: "text-danger",
            rules: {
                email: {
                    required: true,
                    email: true,
                    remote: {
                        type: "POST",
                        url: "/account/is_email_exists",
                        data: {
                            email: function () {
                                return $("#email").val();
                            }
                        }
                    }
                }
            },
            messages: {
                email: {
                    required: '邮箱不能为空',
                    email: '邮箱格式不正确',
                    remote: "该邮箱不存在"
                }
            },
            success: function (label) {
                label.remove();
            },
            errorPlacement: function (error, element) {
                error.insertAfter(element);
            }
        });

        $('#btnsend').click(function () {
            if ($('#recoverform').valid()) {
                submit_send();
            }
        })
    }

    var submit_send = function () {
        var options = {
            url: '/account/find_password',
            type: 'post',
            success: function () {
                alert('密码已经发送到了您的邮箱！');
            }
        };

        $('#recoverform').ajaxSubmit(options);
    }

    return {
        init: function () {
            handle_login_form();
            handle_recover_form();
        }
    };
}();

$(document).ready(function () {
    login.init();
});

