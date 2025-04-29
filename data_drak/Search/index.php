<?php
// Search/index.php

// Lấy tham số từ URL
$q     = isset($_GET['q']) ? trim($_GET['q']) : '';
$type  = isset($_GET['type']) ? trim($_GET['type']) : 'auto';

// Đơn giản hiển thị lại (sau này bạn thay bằng logic query hoặc gọi API)
?>
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Kết quả Tra cứu</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body class="p-4">
  <h1 class="mb-4">Kết quả Tra cứu Mã số thuế</h1>

  <div class="card mb-4">
    <div class="card-body">
      <h5 class="card-title">Từ khóa: <strong><?= htmlspecialchars($q) ?></strong></h5>
      <p class="card-text">Loại tìm kiếm: <strong><?= htmlspecialchars($type) ?></strong></p>
    </div>
  </div>

  <!-- Ở đây bạn sẽ hiển thị kết quả thực tế -->
  <p>Đây là nơi hiển thị danh sách công ty tìm được.</p>

</body>
</html>
