function handleSignup(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("Đăng ký thành công! Vui lòng đăng nhập.");
        window.location.href = "/";
      } else {
        alert(data.error);
      }
    });
  }