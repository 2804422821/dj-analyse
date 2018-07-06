;var add = function () {

    var handle_submit_form = function () {
        $("#add_form").validate({
            errorClass: "text-danger",
            rules: {
                name: {
                    // required: true,
                    // max: 50,
                    remote: {
                        type: "POST",
                        url: "/analyse/app/not_exists",
                        data: {
                            name: function () {
                                return $("#id_name").val();
                            }
                        }
                    }
                }
                // description: {
                //     max: 150
                // }
            },
            messages: {
                name: {
                    required: '名称不能为空',
                    max: '名称不能超过50个字符',
                    remote: "应用名已经存在"
                },
                description: {
                    max: '描述不能超过150个字符'
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
            handle_submit_form();
        }
    };
}();

$(document).ready(function () {
    add.init();
});

