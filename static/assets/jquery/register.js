$(document).ready(function () {
    $('#registerBtn').click(function (e) {
        e.preventDefault();

        register()

    });

    function register() {
        var username = $('#username').val()
        var firstname = $('#firstname').val()
        var middlename = $('#middlename').val()
        var lastname = $('#lastname').val()
        var email = $('#email').val()
        var password = $('#password').val()
        var repeat_password = $('#personRepeatPassword').val()
        var fileInput = $('#profile')[0].files[0];

        var formData = new FormData()
        formData.append('fileInput', fileInput);
        formData.append('username', username);
        formData.append('firstname', firstname);
        formData.append('middlename', middlename);
        formData.append('lastname', lastname);
        formData.append('email', email);
        formData.append('password', password);

        makeAjaxRequest('/register', formData);
    }
})


function makeAjaxRequest(url, data) {
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
        processData: false,
        contentType: false,
        success: function (param) {},
        error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 0) {
                console.log('No internet connection.')
            } else if (jqXHR.status === 404) {
                console.log('Requested page not found [404].')
            } else if (jqXHR.status === 500) {
                console.log('Internal Server Error [500].')
            } else if (textStatus === 'parsererror') {
                console.log('Requested JSON parsing failed.')
            } else if (textStatus === 'timeout') {
                console.log('Time out error.')
            } else if (textStatus === 'abort') {
                console.log('Ajax request aborted.')
            } else {
                console.log('Uncaught Error: ' + errorThrown)
            }
        }
    });
}
