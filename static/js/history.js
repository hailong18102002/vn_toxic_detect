document.addEventListener('DOMContentLoaded', function() {
  // Xử lý nút quay lại
  document.getElementById('back-button').addEventListener('click', function() {
      window.location.href = '/detect';
  });

  // Xử lý nút đăng xuất
  document.querySelector('.logout-btn').addEventListener('click', function() {
      // Thêm logic đăng xuất ở đây
      alert('Đăng xuất thành công!');
      window.location.href = '/'; // Ví dụ: chuyển hướng đến trang đăng nhập
  });

  // Xử lý nút "Xem thêm"
  document.querySelectorAll('.view-more').forEach(function(link) {
      link.addEventListener('click', function(e) {
          e.preventDefault();
          alert('Nội dung rất dài vượt quá 50 ký tự nên sẽ được rút gọn để hiển thị.');
      });
  });
});