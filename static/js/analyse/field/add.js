;var add = function () {
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
    }

    return {
        init: function (option) {
            config = {
                app_id: undefined
            };
            config = $.extend({}, config, option);
            handle_submit_form();
        }
    };
}();

