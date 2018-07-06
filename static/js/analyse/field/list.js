;var list = function () {
    var sourceId = undefined,
        newIndex = undefined;

    var handle_list = function () {
        $("#sortable").sortable({
            start: function (event, ui) {
                list.sourceId = parseInt(ui.item.attr('fid'));

                var width = ui.helper.width();
                width = (width - 70) / 4
                var tds = ui.helper.children()
                for (var i = 0; i < tds.length - 1; i++) {
                    $(tds[i]).width(width);
                }
            },
            update: function (event, ui) {
                list.newIndex = ui.item.index();
                updateFieldSortIndex(list.sourceId, list.newIndex);
                clearObject();
            },
            stop: function (event, ui) {
                clearObject();
            }
        });
        $("#sortable").disableSelection();
    }

    var clearObject = function () {
        list.sourceId = undefined;
        list.newIndex = undefined;
    }

    var updateFieldSortIndex = function (fieldId, newIndex) {
        var action = '/analyse/field/change_index/' + fieldId + '/' + (newIndex + 1);
        $.post(action, null, function (result) {
            console.log(result);
            if (result == "false") {
                alert("更新失败");
                window.location = window.location;
            }
        });
    }

    return {
        init: function () {
            handle_list();
        }
    };
}();

$(document).ready(function () {
    list.init();
});

