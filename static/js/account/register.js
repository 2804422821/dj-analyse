;var register = function () {

    var handle_form = function () {
        $("#registerform").validate({
            errorClass: "text-danger",
            rules: {
                username: {
                    required: true,
                    rangelength: [4, 20],
                    remote: {
                        type: "POST",
                        url: "/account/is_name_not_exists",
                        data: {
                            username: function () {
                                return $("#username").val();
                            }
                        }
                    }
                },
                email: {
                    required: true,
                    email: true,
                    remote: {
                        type: "POST",
                        url: "/account/is_email_not_exists",
                        data: {
                            email: function () {
                                return $("#email").val();
                            }
                        }
                    }
                },
                password: {
                    required: true,
                    rangelength: [6, 24]
                },
                password_confirm: {
                    required: true,
                    rangelength: [6, 24],
                    equalTo: "#password"
                }
            },
            messages: {
                username: {
                    required: '用户名不能为空',
                    rangelength: '用户名长度必须在4～20之间',
                    remote: "该用户名已经存在"
                },
                email: {
                    required: '邮箱不能为空',
                    email: '邮箱格式不正确',
                    remote: "该邮箱已经存在"
                },
                password: {
                    required: '密码不能为空',
                    rangelength: '密码长度必须在6～24之间',
                },
                password_confirm: {
                    required: '密码不能为空',
                    rangelength: '密码长度必须在6～24之间',
                    equalTo: '两次输入的密码不一致'
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

    return {
        init: function () {
            handle_form();
        }
    };
}();

$(document).ready(function () {
    register.init();
});

