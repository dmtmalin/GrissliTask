$(document).ready(function(){
    var namespace = '/parse';
    var socket = io('http://' + document.domain + ':' + location.port + namespace);

    InitDatetimePicker();
    InitButtonNewTasks();
    InitSocketUpdateState(socket);
});


function InitDatetimePicker() {
    var div = $('.JS-datetime');
    div.datetimepicker({
        format: 'YYYY-MM-DDTHH:mm:ssZ' //ISO 8601
    });
}

function InitButtonNewTasks() {
    var button = $('.JS-new-tasks');
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