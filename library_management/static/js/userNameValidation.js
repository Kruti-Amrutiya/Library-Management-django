$("#id_username").change(function () {
    var username = $(this).val();
    $.ajax({
    method: 'GET',
    url: '/validate_username/',
    data: {
        'username': username
    },
    dataType: 'json',
    success: function (data) {
        if (data.is_taken) {
        alert("A user with this username already exists.");
        }
    }
    });
});
