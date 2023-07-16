$('document').ready(function () {
    $('#senddResetLink').click(function () {
        sendForgotPassword()

    })
});

function sendForgotPassword() {
    var email = $('#email').val();
    var formData = new FormData();

    formData.append('email', email)

    makeAjaxRequest('/forgot-password', formData)
}


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
        success: function (msg) {
            if (msg.msg == 1) {
                Swal.fire({
                    icon: 'success',
                    title: 'Password Reset Email Sent',
                    text: 'Please Check your email',
                    showConfirmButton: true,
                });
            } else if (msg.msg == 2) {
                Swal.fire({
                    icon: 'error',
                    title: 'Email Not Found',
                    text: 'Email not found make sure you have a valid email address and if not Please register your account',
                    showConfirmButton: true,
                });
            }
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
