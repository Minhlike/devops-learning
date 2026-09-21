#!/bin/bash
set -euxo pipefail

dnf install -y nginx

cat > /usr/share/nginx/html/index.html <<'EOF'
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AWS S23</title>
</head>
<body>
  <h1>Hello from AWS EC2</h1>
  <p>DevOps Learning - Session 23</p>
</body>
</html>
EOF

systemctl enable --now nginx