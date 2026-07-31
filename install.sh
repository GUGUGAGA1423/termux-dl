#!/data/data/com.termux/files/usr/bin/bash

echo "=========================================="
echo "  🚀 Installing termux-dl"
echo "=========================================="

# 1. Request storage permissions if not granted
if [ ! -d "$HOME/storage" ]; then
    echo "📱 Requesting storage permission..."
    termux-setup-storage
fi

# 2. Update and install packages
echo "📦 Installing system dependencies..."
pkg update -y && pkg install -y python megatools curl git

# 3. Install python dependencies
echo "🐍 Installing Python libraries..."
pip install cloudscraper

# 4. Download the Python script to internal storage
mkdir -p ~/.termux-dl
curl -sL https://raw.githubusercontent.com/GUGUGAGA1423/termux-dl/main/get_mega.py -o ~/.termux-dl/get_mega.py

# 5. Create executable binary wrapper
cat << 'EOF' > $PREFIX/bin/anime
#!/data/data/com.termux/files/usr/bin/bash
python3 ~/.termux-dl/get_mega.py "$@"
EOF

chmod +x $PREFIX/bin/anime

echo "=========================================="
echo "✅ Installation Complete!"
echo "👉 Just type 'anime' to start downloading."
echo "=========================================="