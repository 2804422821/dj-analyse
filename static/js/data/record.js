;var record = function () {
    var config = undefined,
        datatable = undefined;

    var handle_record_table = function () {
        datatable = $('#list').DataTable({
            paging: false,
            searching: false,
            info: false,
            "lengthMenu": [[20, 30, 50], [20, 30, 50]],
            "pageLength": 20,
            "bSortClasses": false,
            "bSort": false,
            "serverSide": true,//服务器模式，这个给值了，才会传分页等等参数
            "ajax": {
                "url": 'Form/GetJobItems',
                'type': "POST",
                "data": function (data) {
                    return data;
                }
            }
        });

        // Ajax call finished
        datatable.on('xhr.dt', function () {

        });
    }

    return {
        init: function (option) {
            config = {
                app_id: undefined
            };
            config = $.extend({}, config, option);
            handle_record_table();
        }
    };
}();

$(document).ready(function () {
    // 不弹出错误信息
    $.fn.dataTable.ext.errMode = 'none'
    record.init();
});
