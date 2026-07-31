# termux-dl
# 🎬 AnimeSalt-DL

A fast, lightweight batch downloader and search CLI tool for **AnimeSalt**, designed for **Termux** and **Linux**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-green)

---

## ✨ Features

* 🔍 **Built-in Search**: Search series or movies directly from your terminal—no URLs needed.
* 📂 **Automatic Organization**: Automatically creates clean show folders (`Anime/Series Name/...`) for all downloads.
* 🎬 **Full Movie & Series Support**: Seamlessly parses both multi-season series and standalone anime movies.
* ⚡ **Flexible Selection**: Pick entire shows (`all`), specific seasons (`s1`, `s2`), ranges (`1-12`), or specific episodes (`1,3,5`).
* 🖥️ **Quality Picker**: Choose between 480p, 720p, and 1080p.
* 📥 **Fast Downloads**: Uses `megadl` for maximum speed.

---

## 🚀 One-Line Installation (Termux)

Open **Termux** and run this single command:

```bash
curl -sL [https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/animesalt-dl/main/install.sh](https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/animesalt-dl/main/install.sh) | bash
```

> **Note:** Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username!

---

## 📖 How to Use

Once installed, simply type `anime` anywhere in your terminal:

```bash
anime
```

### Example Walkthrough
1. Enter `my dress up darling` or `your name`.
2. Select your show/movie from the search results.
3. Choose your desired season or episode range (e.g. `s1`, `1-12`, or `all`).
4. Select quality (`1` for 480p, `2` for 720p, `3` for 1080p).
5. Sit back! Files will download straight into `~/storage/downloads/Anime/Show Name/`.

---

## ⚙️ Prerequisites

If installing manually without the script, make sure you have:
* `python3`
* `megatools` (for `megadl`)
* `cloudscraper` (`pip install cloudscraper`)
