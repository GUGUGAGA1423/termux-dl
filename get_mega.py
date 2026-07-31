#!/usr/bin/env python3
import os
import re
import html
import subprocess
import cloudscraper
import urllib.parse

print("=" * 60)
print("  🎬 AnimeSalt Master Downloader (Auto-Folder Enabled)")
print("=" * 60)

# Base download directory setup
BASE_ANIME_DIR = os.path.expanduser("~/storage/downloads/Anime")
if not os.path.exists(BASE_ANIME_DIR):
    BASE_ANIME_DIR = os.getcwd()

user_input = input("\n🔍 Enter Title (or paste full Series/Movie URL): ").strip()
scraper = cloudscraper.create_scraper()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

target_url = ""

# 1. SEARCH OR DIRECT URL HANDLER
if user_input.startswith("http://") or user_input.startswith("https://"):
    target_url = user_input
else:
    search_query = urllib.parse.quote_plus(user_input)
    search_url = f"https://animesalt.link/?s={search_query}"

    print(f"\n🔄 Searching AnimeSalt for: '{user_input}'...")
    s_res = scraper.get(search_url, headers=headers)

    found_items = re.findall(r'href=["\'](https?://animesalt\.link\/(?:series|movies)\/[^"\']+|\/(?:series|movies)\/[^"\']+)["\']', s_res.text)

    unique_urls = []
    for item_link in found_items:
        full_url = f"https://animesalt.link{item_link}" if item_link.startswith("/") else item_link
        full_url = full_url.rstrip('/') + '/'
        if full_url not in unique_urls:
            unique_urls.append(full_url)

    if not unique_urls:
        alt_search_url = f"https://animesalt.link/search/{search_query}/"
        s_res = scraper.get(alt_search_url, headers=headers)
        found_items = re.findall(r'href=["\'](https?://animesalt\.link\/(?:series|movies)\/[^"\']+|\/(?:series|movies)\/[^"\']+)["\']', s_res.text)
        for item_link in found_items:
            full_url = f"https://animesalt.link{item_link}" if item_link.startswith("/") else item_link
            full_url = full_url.rstrip('/') + '/'
            if full_url not in unique_urls:
                unique_urls.append(full_url)

    if not unique_urls:
        print("❌ No series or movies found. Try pasting a direct link.")
        exit(1)

    print(f"\n✅ Found {len(unique_urls)} result(s):\n")
    for idx, u in enumerate(unique_urls, 1):
        tag = "🎬 Movie " if "/movies/" in u else "📺 Series"
        slug = u.rstrip('/').split('/')[-1]
        clean_title = slug.replace('-', ' ').title()
        print(f"  [{idx}] [{tag}] {clean_title}")

    choice = input("\n👉 Select number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(unique_urls):
        target_url = unique_urls[int(choice) - 1]
    else:
        print("❌ Invalid selection.")
        exit(1)

# 2. CREATE TARGET SUBFOLDER
anime_slug = target_url.rstrip('/').split('?')[0].rstrip('/').split('/')[-1]
folder_name = anime_slug.replace('-', ' ').title()
output_folder = os.path.join(BASE_ANIME_DIR, folder_name)
os.makedirs(output_folder, exist_ok=True)
print(f"\n📂 Files will be saved in: {output_folder}")

# 3. DETERMINE WORKFLOW (SERIES vs MOVIE)
selected_pages = []

if "/series/" in target_url:
    print(f"\n🔄 Scraping episode list...")
    res = scraper.get(target_url, headers=headers)
    if res.status_code != 200:
        print(f"❌ Failed to load series page. Status: {res.status_code}")
        exit(1)

    series_slug = anime_slug

    found_links = set(re.findall(r'href=["\'](\/episode\/[^"\']+)["\']', res.text))
    found_links.update(re.findall(r'https?://animesalt\.link(\/episode\/[^"\'\s<>]+)', res.text))

    raw_urls = set()
    for ep in found_links:
        full_ep = f"https://animesalt.link{ep}" if ep.startswith("/") else ep
        raw_urls.add(full_ep)

    season_tabs = re.findall(r'[Ss]eason\s*(\d+)\s*[^1-9]*?1-(\d+)', res.text)

    generated_urls = set()
    if season_tabs:
        for s_str, ep_count_str in season_tabs:
            s_num = int(s_str)
            ep_count = int(ep_count_str)
            for e_num in range(1, ep_count + 1):
                generated_urls.add(f"https://animesalt.link/episode/{series_slug}-{s_num}x{e_num}/")
    else:
        max_s = 1
        for ep_url in raw_urls:
            slug = ep_url.rstrip('/').split('/')[-1]
            m = re.search(r'(\d+)x(\d+)', slug)
            if m:
                max_s = max(max_s, int(m.group(1)))

        for s in range(1, max_s + 1):
            for e in range(1, 13):
                generated_urls.add(f"https://animesalt.link/episode/{series_slug}-{s}x{e}/")

    all_urls = raw_urls.union(generated_urls)

    parsed_episodes = []
    for ep_url in all_urls:
        slug = ep_url.rstrip('/').split('/')[-1]
        match = re.search(r'(\d+)x(\d+)', slug)
        if match:
            s_num = int(match.group(1))
            e_num = int(match.group(2))
        else:
            s_num, e_num = 99, 99
        parsed_episodes.append({
            'url': ep_url,
            'slug': slug,
            'season': s_num,
            'episode': e_num
        })

    unique_episodes = {}
    for item in parsed_episodes:
        key = (item['season'], item['episode'])
        if key not in unique_episodes:
            unique_episodes[key] = item

    parsed_episodes = sorted(unique_episodes.values(), key=lambda x: (x['season'], x['episode']))

    if not parsed_episodes:
        print("❌ Couldn't find any episode links.")
        exit(1)

    print(f"\n✅ Found {len(parsed_episodes)} episode(s):\n")
    for idx, item in enumerate(parsed_episodes, 1):
        print(f"  [{idx}] S{item['season']:02d}E{item['episode']:02d} ({item['slug']})")

    print("\nSelection Options:")
    print("  • Type 'all' to download everything")
    print("  • Type 's1' for Season 1 only")
    print("  • Type 's2' for Season 2 only")
    print("  • Type a range like '1-12'")
    print("  • Type specific numbers like '1,3,5'")

    choice = input("\n👉 Which episodes do you want to download? ").strip().lower()

    if choice == 'all':
        selected_pages = [x['url'] for x in parsed_episodes]
    elif choice.startswith('s') and choice[1:].isdigit():
        target_s = int(choice[1:])
        selected_pages = [x['url'] for x in parsed_episodes if x['season'] == target_s]
    elif '-' in choice:
        try:
            start, end = map(int, choice.split('-'))
            selected_pages = [parsed_episodes[i]['url'] for i in range(start-1, end)]
        except Exception:
            print("❌ Invalid range.")
            exit(1)
    else:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',') if x.strip().isdigit()]
            selected_pages = [parsed_episodes[i]['url'] for i in indices if 0 <= i < len(parsed_episodes)]
        except Exception:
            print("❌ Invalid selection.")
            exit(1)

else:
    selected_pages = [target_url]

# 4. QUALITY SELECTION
print("\n🎬 Select Video Quality:")
print("  [1] 480p")
print("  [2] 720p")
print("  [3] 1080p (Default)")
qual_input = input("👉 Choice (1-3, default=3): ").strip()
target_qual_idx = int(qual_input) if qual_input in ["1", "2", "3"] else 3

print(f"\n🚀 Starting download process for {len(selected_pages)} item(s)...\n" + "="*60)

# 5. DOWNLOAD EXECUTION INTO SUBFOLDER
for item_url in selected_pages:
    item_name = item_url.rstrip('/').split('?')[0].rstrip('/').split('/')[-1]
    print(f"\n📺 Processing: {item_name}")

    headers["Referer"] = item_url
    res = scraper.get(item_url, headers=headers)
    if res.status_code != 200:
        print(f"  ❌ Couldn't load page ({res.status_code}). Skipping...")
        continue

    rel_links = re.findall(r'href=["\'](\/\?trdownload=[^"\']+)["\']', res.text)
    if not rel_links:
        rel_links = re.findall(r'https?://animesalt\.link(\/\?trdownload=[^"\'\s<>]+)', res.text)

    clean_links = [html.unescape(l) for l in rel_links]
    links = list(set([f"https://animesalt.link{l}" if not l.startswith("http") else l for l in clean_links]))

    if not links:
        print("  ❌ No download links found on page. Skipping...")
        continue

    sorted_links = sorted(
        links, 
        key=lambda x: int(re.search(r'trdownload=(\d+)', x).group(1)) if re.search(r'trdownload=(\d+)', x) else 0
    )

    chosen_dl_url = sorted_links[min(target_qual_idx - 1, len(sorted_links) - 1)]

    try:
        r = scraper.get(chosen_dl_url, headers=headers, allow_redirects=False)
        mega_link = r.headers.get("Location")

        if not mega_link or "mega.nz" not in mega_link:
            r2 = scraper.get(chosen_dl_url, headers=headers, allow_redirects=True)
            if "mega.nz" in r2.url:
                mega_link = r2.url
            else:
                match = re.search(r'https?://mega\.nz/[^\s"\'<>]+', r2.text)
                if match:
                    mega_link = match.group(0)

        if mega_link and "mega.nz" in mega_link:
            print(f"  ✅ Mega Link: {mega_link}")
            print(f"  📥 Downloading to {folder_name}/...")
            subprocess.run(["megadl", mega_link], cwd=output_folder)
        else:
            print("  ❌ Could not resolve Mega link.")

    except Exception as e:
        print(f"  ❌ Download error: {e}")

print("\n🎉 Process finished!")
