function handleLogin(event) {
    event.preventDefault(); 
    console.log(document.getElementById("username").value);
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
  
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.href = "/detect";
      } else {
        alert(data.error);
      }
    });
  }
  