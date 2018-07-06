;var edit = function () {

    var handle_submit_form = function () {
        $("#add_form").validate({
            errorClass: "text-danger",
            messages: {
                name: {
                    required: '名称不能为空',
                    max: '名称不能超过50个字符'
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
    edit.init();
});

