#!/data/data/com.termux/files/usr/bin/bash

echo "=========================================="
echo "  🚀 Installing AnimeSalt-DL for Termux"
echo "=========================================="

# 1. Update and install packages
echo "📦 Installing system dependencies..."
pkg update -y && pkg install -y python megatools curl git

# 2. Install python dependencies
echo "🐍 Installing Python libraries..."
pip install cloudscraper

# 3. Download the Python script to internal storage
mkdir -p ~/.animesalt-dl
curl -sL https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/animesalt-dl/main/animesalt_dl.py -o ~/.animesalt-dl/animesalt_dl.py

# 4. Create executable binary wrapper
cat << 'EOF' > $PREFIX/bin/anime
#!/data/data/com.termux/files/usr/bin/bash
python3 ~/.animesalt-dl/animesalt_dl.py "$@"
EOF

chmod +x $PREFIX/bin/anime

echo "=========================================="
echo "✅ Installation Complete!"
echo "👉 Just type 'anime' to start downloading."
echo "=========================================="
