var current_page = 0;

$(document).ready(function(){
    var namespace = '/parse';
    var socket = io('http://' + document.domain + ':' + location.port + namespace);
    InitButtonPageTask();
    InitDatetimePicker();
    InitSocketUpdateState(socket);
    InitButtonNewTasks();
    GetPageNext();
});

function InitDatetimePicker() {
    var div = $('.JS-datetime');
    div.datetimepicker({
        format: 'YYYY-MM-DDTHH:mm:ssZ' //ISO 8601
    });
}

function InitButtonNewTasks() {
    var button = $('.JS-new-task');
    button.click(function () {
        var url = $(this).attr('data-action'),
            data = $('.JS-form').serialize();
        $.ajax({
            url: url,
            data: data,
            type: 'post',
            success: function (html) {
                $('.JS-tasks').prepend(html);
            },
            error: function (response) {
                alert(response.responseText);
            }
        });
    })
}

function InitSocketUpdateState(socket) {
    socket.on('update_state', function (response) {
        $('#' + response.task_id).replaceWith(response.html);
    })
}

function InitButtonPageTask() {
    var button = $('.JS-page-task');
    button.click(function () {
        GetPageNext();
    });
}


function GetPageNext() {
    var button = $('.JS-page-task');
    var url = button.attr('data-action');
    $.ajax({
        url: url + '/' + current_page,
        type: 'post',
        success: function (json) {
            $('.JS-tasks').prepend(json['html']);
            if (json['has_next']) {
               current_page += 1;
            }
            else {
                button.addClass('disabled');
                button.off('click');
            }
        }
    });
}
