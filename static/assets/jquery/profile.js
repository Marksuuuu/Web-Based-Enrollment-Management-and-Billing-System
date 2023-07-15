$('document').ready(function() {
    $('#resendVerification').click(function(){
        var dataName = $('.layout-page').attr('data-name');
        console.log("🚀 ~ file: profile.js:5 ~ $ ~ dataName:", dataName)
        var formData = new FormData();
        formData.append('dataName', dataName);

        resendVerification(formData)
    })

    })
    function resendVerification(data) {
        $.ajax({
          url: '/resend-verification',
          type: 'POST',
          data: data, 
          contentType: false,
          processData: false,
          success: function(data) {
            console.log("🚀 ~ file: profile.js:11 ~ resendVerification ~ data:", data)
            if (data.error) {
              // Handle error response
              displayToast(data.error, 'bg-danger');
            } else {
              // Verification email resent successfully
              displayToast(data.message, 'bg-success');
            }
          },
          error: function(xhr, status, error) {
            // Handle error
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