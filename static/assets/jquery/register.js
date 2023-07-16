$(document).ready(function () {
    $('#registerBtn').click(function (e) {
        e.preventDefault();

        register()

    });

    function register() {
        var username = $('#username').val();
        var firstname = $('#firstname').val();
        var middlename = $('#middlename').val();
        var lastname = $('#lastname').val();
        var email = $('#email').val();
        var password = $('#password').val();
        var repeat_password = $('#repeatPassword').val();

        if (username == '', firstname == '', middlename == '', lastname == '', email == '', password == '', repeat_password == '') {
            Swal.fire({icon: 'warning', title: 'Please fill in all the required fields.', showConfirmButton: true});
            return;
        }

        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (! emailRegex.test(email)) {
            Swal.fire({icon: 'warning', title: 'Please enter a valid email address.', showConfirmButton: true});
            return;
        }

        if (password != repeat_password) {
            Swal.fire({icon: 'warning', title: 'Please check your password.', showConfirmButton: true});
            return;
        }

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
        beforeSend: function () {
            $('#waitMeDiv').waitMe({
                effect: 'rotateplane',
                text: '',
                bg: 'rgba(255, 255, 255, 0.7)',
                color: '#5f61e6',
                maxSize: '',
                waitTime: -1,
                textPos: 'vertical',
                fontSize: '',
                source: ''
            });
        },
        success: function (response) {
            if (response.msg == 1) {
                Swal.fire({icon: 'success', title: 'Register Success', text: 'Now Please Check your email for verification link to activate', showConfirmButton: true});
                resetAll()
            } else if (response.error) {
                Swal.fire({icon: 'error', title: 'Register Error', text: response.error, showConfirmButton: true});
            }
            $('#waitMeDiv').waitMe("hide");
        },
        error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 0) {
                alert('No internet connection.')
            } else if (jqXHR.status === 404) {
                alert('Requested page not found [404].')
            } else if (jqXHR.status === 500) {
                alert('Internal Server Error [500].')
            } else if (textStatus === 'parsererror') {
                alert('Requested JSON parsing failed.')
            } else if (textStatus === 'timeout') {
                alert('Time out error.')
            } else if (textStatus === 'abort') {
                alert('Ajax request aborted.')
            } else {
                alert('Uncaught Error: ' + errorThrown)
            }
        }
    }).done(function () {
        $('#waitMeDiv').waitMe("hide");
    })
}

function resetAll() {
    $('#username').val('')
    $('#firstname').val('')
    $('#middlename').val('')
    $('#lastname').val('')
    $('#email').val()
    $('#password').val('')
    $('#personRepeatPassword').val('')
    $('#repeatPassword').val('');
}
