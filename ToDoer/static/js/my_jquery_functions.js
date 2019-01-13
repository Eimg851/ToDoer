//Deletes a task via an ajax post request
function deleteTask(timestamp) {
    var url = "/deleteTask";
    var time = timestamp;
    var csrf = $("#delete_icons").attr('csrf-token');
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            timestamp: time,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#board").html(data);
        }
    });
};

//Sets values of the editModal and opens the modal view
function editModal(task, timestamp, due) {
    $('.modal-body #editTaskTitle').val(task);
    $('.modal-body #editTaskDue').val(due);
    $('.modal-body #taskTimestamp').val(timestamp);
    $('#editTaskModal').modal('show');
};

//Sets values of the shareModal and opens the modal view
function shareModal(task, timestamp, due) {
    $('.modal-body #shareTaskTitle').val(task);
    $('.modal-body #shareTaskDue').val(due);
    $('.modal-body #taskTimestamp').val(timestamp);
    $('#shareTaskModal').modal('show');
};

//Sets values of the shareListModal and opens the modal view
function shareListModal(task, timestamp, due) {
    $('#shareTaskModal').modal('show');

};

//Posts the email address of the share recipient to the django app
$(document).on("submit", "#shareListForm", function(e) {
    $('#shareTaskModal').modal('hide');
    var recipient = $('#shareUser').val();
    var csrf = $("#shareTaskForm").attr("csrf-token");
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            recipient: recipient,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#board").html(data);
        }
    });
    e.preventDefault();
});


//Updates the task information via an ajax post request
$(document).on("submit", "#editTaskForm", function(e) {
    $('#editTaskModal').modal('hide');
    var url = "/editTask"
    var task = $('#editTaskTitle').val();
    var due = $('#editTaskDue').val();
    var timestamp = $('#taskTimestamp').val();
    var csrf = $("#editTaskForm").attr("csrf-token");
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            task: task,
            due: due,
            timestamp: timestamp,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#board").html(data);
        }
    });
    e.preventDefault();
});

//Posts the email address of the share recipient to the django app
$(document).on("submit", "#shareTaskForm", function(e) {
    $('#shareTaskModal').modal('hide');
    var url = "/shareTask"
    var task = $('#shareTaskTitle').val();
    var due = $('#shareTaskDue').val();
    var timestamp = $('#taskTimestamp').val();
    var recipient = $('#shareUser').val();
    var csrf = $("#shareTaskForm").attr("csrf-token");
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            task: task,
            due: due,
            timestamp: timestamp,
            recipient: recipient,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#board").html(data);
        }
    });
    e.preventDefault();
});


//Marks a task a complete
function markAsDone(timestamp) {
    if ($('#checkbox').is(':checked')) {
        var url = "/markAsDone";
        var time = timestamp;
        var csrf = $("#checkbox").attr('csrf-token');
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                timestamp: time,
                csrfmiddlewaretoken: csrf,
                status: "done"
            },
            success: function(data) {
                $("#board").html(data);
            }
        });
    }
}

//Marks a task as incomplete
function markAsNotDone(timestamp) {
    var csrf = $("#undo_icons").attr('csrf-token');
    var url = "/markAsDone";
    var time = timestamp;
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            timestamp: time,
            csrfmiddlewaretoken: csrf,
            status: "todo"
        },
        success: function(data) {
            $("#board").html(data);
        }
    });
}

//Sets the values of the settingsModal and opens the modal view
function settingsModal(fname, sname, email) {
    $('.modal-body #settingsFName').val(fname);
    $('.modal-body #settingsSName').val(sname);
    $('.modal-body #settingsEmail').val(email);
    $('#settingsModal').modal('show');

};

//Posts the values of the settings form to the django app to be updated
$(document).on("submit", "#settingsForm", function(e) {
    $('#settingsModal').modal('hide');
    var fname = $('#settingsFName').val();
    var sname = $('#settingsSName').val();
    var email = $('#settingsEmail').val();
    var csrf = $("#settingsForm").attr("csrf-token");
    $.ajax({
        type: 'POST',
        url: "/settings",
        data: {
            fname: fname,
            sname: sname,
            email: email,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#userOptions").html(data);
        }
    });
    e.preventDefault();
});
