;var edit = function () {
    var config = undefined;

    var handle_submit_form = function () {
        $("#add_form").validate({
            errorClass: "text-danger",
            rules: {
                name: {
                    remote: {
                        type: "POST",
                        url: "/analyse/field/name_not_exists/" + config.app_id,
                        data: {
                            name: function () {
                                return $("#id_name").val();
                            },
                            exclude: function () {
                                return config.field_id
                            }
                        }
                    }
                },
                bind_key: {
                    remote: {
                        type: "POST",
                        url: "/analyse/field/key_not_exists/" + config.app_id,
                        data: {
                            name: function () {
                                return $("#id_bind_key").val();
                            },
                            exclude: function () {
                                return config.field_id
                            }
                        }
                    }
                }
            },
            messages: {
                name: {
                    required: '名称不能为空',
                    max: '名称不能超过1000个字符',
                    remote: "字段名已经存在"
                },
                bind_key: {
                    max: '名称不能超过20个字符',
                    remote: "绑定名已经存在"
                }
            },
            success: function (label) {
                label.remove();
            },
            errorPlacement: function (error, element) {
                error.insertAfter(element);
            }
        })


        // 触发校验，不然需要点击两次提交按钮
        $('#id_name').blur();
        $('#id_bind_key').blur();
    }

    return {
        init: function (option) {
            config = {
                app_id: undefined,
                field_id: undefined
            };
            config = $.extend({}, config, option);
            handle_submit_form();
        }
    };
}();

