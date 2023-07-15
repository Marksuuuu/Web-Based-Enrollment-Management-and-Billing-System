function submitForm(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const data = {
      username: username,
      password: password
    };
    fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(response => {
      if (response.ok) {
        window.location.href = '/index?success=true';
      } else {
        response.json().then(data => {
          alert(data.error);
        });
      }
    }).catch(error => {
      alert('An error occurred: ' + error);
    });
  }