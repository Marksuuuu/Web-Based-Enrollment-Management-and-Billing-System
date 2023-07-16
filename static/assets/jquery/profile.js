$('document').ready(function () {
    $('#resendVerification').click(function () {
        var dataName = $('.layout-page').attr('data-name');
        console.log("🚀 ~ file: profile.js:5 ~ $ ~ dataName:", dataName)
        var formData = new FormData();
        formData.append('dataName', dataName);

        resendVerification(formData)
    })

    $('#deactivateAccountBtn').click(function () {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                checkIfchecked()
            }
        })

    })

})
function checkIfchecked() {
    if ($('#accountActivation').is(":checked")) {
        var dataID = $(".layout-container").data('id');
        var formData = new FormData();
        formData.append('dataID', dataID);

        makeAjaxRequest('/deactivate-account', formData)
    } else {
        console.log('unchecked')
    }
}

function makeAjaxRequest(url, data) {
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
        processData: false,
        contentType: false,
        success: function (param) {
            window.location.href = '/logout'; // Corrected line
        },
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

function resendVerification(data) {
    $.ajax({
        url: '/resend-verification',
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log("🚀 ~ file: profile.js:11 ~ resendVerification ~ data:", data)
            if (data.error) { // Handle error response
                displayToast(data.error, 'bg-danger');
            } else { // Verification email resent successfully
                displayToast(data.message, 'bg-success');
            }
        },
        error: function (xhr, status, error) { // Handle error
            console.error('Error:', error);
        }
    });
}

function displayToast(message, toastClass) {
    var toastDiv = $('<div class="bs-toast toast fade show ' + toastClass + '" role="alert" aria-live="assertive" aria-atomic="true"></div>');
    var toastHeader = $('<div class="toast-header"></div>');
    var icon = $('<i class="bx bx-user-x me-2"></i>');
    var closeButton = $('<button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>');
    var toastBody = $('<div class="toast-body"></div>').text(message);

    toastHeader.append(icon);
    toastHeader.append('<div class="me-auto fw-semibold">Verify First!</div>');
    toastHeader.append(closeButton);

    toastDiv.append(toastHeader);
    toastDiv.append(toastBody);

    $('#verification-toast').append(toastDiv);
}
