#!/bin/bash
set -euxo pipefail

dnf install -y nginx

HOST="$(hostname)"

cat > /usr/share/nginx/html/index.html <<EOF
<!DOCTYPE html>
<html>
<body>
<h1>S26 - AWS Load Balancing Lab</h1>
<p>Response from: ${HOST}</p>
</body>
</html>
EOF

echo "healthy" > /usr/share/nginx/html/health

systemctl enable nginx
systemctl start nginx