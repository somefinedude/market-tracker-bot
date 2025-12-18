#!/usr/bin/env python3
"""
Facebook Group Image Scraper - Click-based approach
Clicks on images to open photo viewer and extracts full resolution.
Scrolls through feed to get more images.
Organizes into folders: 1/, 2/, 3/ with post.txt and images
"""

import os
import re
import time
import json
import random
import logging
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "group_url": "https://www.facebook.com/groups/2181129945608119",
    "output_dir": "church_data",
    "max_posts": 500,
    "scroll_pause": 3,
    "no_new_images_limit": 5,
}

# ============================================================================
# Logging Setup
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# Helper Functions
# ============================================================================

def download_image(url: str, save_path: str) -> bool:
    """Download an image from URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://www.facebook.com/',
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        if len(response.content) < 5000:
            logger.warning(f"Image too small ({len(response.content)} bytes)")
            return False

        with open(save_path, 'wb') as f:
            f.write(response.content)

        logger.info(f"Downloaded: {len(response.content):,} bytes")
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

def save_progress(data: dict, filepath: str) -> None:
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_progress(filepath: str) -> dict:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {"processed_urls": [], "post_count": 0, "processed_texts": []}

# ============================================================================
# Main Scraper Class
# ============================================================================

class FacebookGroupScraper:
    def __init__(self):
        self.output_dir = CONFIG["output_dir"]
        self.driver = None
        self.post_counter = 0
        self.processed_urls = set()
        self.processed_texts = set()  # Track post text to avoid duplicates
        self.progress_file = os.path.join(self.output_dir, "progress.json")

    def setup_browser(self) -> None:
        logger.info("Setting up browser...")
        options = Options()

        profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "firefox_profile")
        os.makedirs(profile_dir, exist_ok=True)
        options.add_argument("-profile")
        options.add_argument(profile_dir)

        self.driver = webdriver.Firefox(options=options)
        self.driver.set_window_size(1920, 1080)
        logger.info("Browser ready")

    def close_browser(self) -> None:
        if self.driver:
            self.driver.quit()

    def login_to_facebook(self) -> None:
        logger.info("Logging in...")
        self.driver.get("https://www.facebook.com/login")
        time.sleep(3)

        try:
            # TODO: Enter your Facebook credentials here
            self.driver.find_element(By.ID, "email").send_keys("YOUR_EMAIL@example.com")
            time.sleep(0.5)
            self.driver.find_element(By.ID, "pass").send_keys("YOUR_PASSWORD")
            time.sleep(0.5)
            self.driver.find_element(By.NAME, "login").click()
            time.sleep(8)
            logger.info("Logged in")
        except Exception as e:
            logger.error(f"Login error: {e}")

    def navigate_to_group(self) -> None:
        logger.info(f"Navigating to {CONFIG['group_url']}")
        self.driver.get(CONFIG['group_url'])
        time.sleep(5)

        if 'Log in' in self.driver.page_source and 'Create new account' in self.driver.page_source:
            self.login_to_facebook()
            self.driver.get(CONFIG['group_url'])
            time.sleep(5)

        logger.info("Group page loaded")

    def get_scroll_position(self) -> int:
        """Get current scroll position to restore after closing viewer."""
        return self.driver.execute_script("return window.pageYOffset")

    def set_scroll_position(self, pos: int) -> None:
        """Restore scroll position after closing viewer."""
        self.driver.execute_script(f"window.scrollTo(0, {pos})")
        time.sleep(0.5)

    def get_full_res_from_viewer(self) -> str:
        """Get the full resolution image URL from the photo viewer."""
        time.sleep(2)

        selectors = [
            'img[data-visualcompletion="media-vc-image"]',
            'div[role="dialog"] img[src*="scontent"]',
            'img[src*="scontent"]',
        ]

        best_url = None
        best_size = 0

        for selector in selectors:
            try:
                images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images:
                    src = img.get_attribute('src')
                    if not src or 'scontent' not in src:
                        continue
                    if any(x in src for x in ['p50x50', 's50x50', 'p32x32', 's32x32', 'c0.0.40']):
                        continue

                    try:
                        width = self.driver.execute_script("return arguments[0].naturalWidth", img)
                        height = self.driver.execute_script("return arguments[0].naturalHeight", img)
                        size = (width or 0) * (height or 0)
                    except:
                        size = len(src)

                    if size > best_size:
                        best_size = size
                        best_url = src.replace('&amp;', '&')
            except:
                continue

        return best_url

    def close_photo_viewer(self) -> None:
        """Close the photo viewer by pressing Escape key."""
        try:
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1.5)
        except:
            pass

    def debug_log(self, msg: str) -> None:
        """Write debug message to local debug.txt file."""
        with open("debug.txt", "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} - {msg}\n")

    def get_post_text_from_feed(self, img) -> str:
        """Get post text from the article containing this image (before clicking)."""
        try:
            # Find the parent article element
            article = img.find_element(By.XPATH, './ancestor::div[@role="article"]')
            if article:
                # Get text from the article
                text = article.text[:200]  # First 200 chars for comparison
                # Clean it up - remove common UI text
                for skip in ['Like', 'Comment', 'Share', 'See more', 'All reactions']:
                    text = text.replace(skip, '')
                return text.strip()[:100]  # Use first 100 chars as signature
        except:
            pass
        return ""

    def find_clickable_images(self) -> list:
        """Find all large images that can be clicked."""
        all_images = self.driver.find_elements(By.CSS_SELECTOR, 'img[src*="scontent"]')
        self.debug_log(f"=== find_clickable_images: found {len(all_images)} total scontent images ===")

        clickable = []
        skipped_processed = 0
        skipped_small = 0
        skipped_profile = 0

        for img in all_images:
            try:
                src = img.get_attribute('src') or ''
                # Check by URL base (ignores CDN tokens that change)
                src_base = self.get_url_base(src)
                if src in self.processed_urls or self.is_url_processed(src):
                    skipped_processed += 1
                    continue
                if any(x in src for x in ['p50x50', 's50x50', 'p32x32', 's32x32', 'c0.0.40', 'p36x36']):
                    skipped_profile += 1
                    continue

                width = self.driver.execute_script("return arguments[0].offsetWidth", img)
                height = self.driver.execute_script("return arguments[0].offsetHeight", img)

                if width and height and width > 100 and height > 100:
                    clickable.append((img, src))
                else:
                    skipped_small += 1
            except:
                continue

        self.debug_log(f"  Clickable: {len(clickable)}, Skipped: processed={skipped_processed}, profile={skipped_profile}, small={skipped_small}")
        return clickable

    def get_post_text_from_viewer(self) -> str:
        """Try to extract post text/caption from the photo viewer."""
        try:
            # Various selectors for post caption in photo viewer
            text_selectors = [
                # Caption area in photo viewer
                'div[role="dialog"] div[data-ad-preview="message"] span',
                'div[role="dialog"] div[data-ad-comet-preview="message"] span',
                # Text near the photo
                'div[role="dialog"] span[dir="auto"]',
                'div[data-pagelet*="PhotoViewer"] span[dir="auto"]',
                # Comment/caption section
                'div[role="dialog"] div[dir="auto"]',
            ]

            best_text = ""
            for sel in text_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                    for e in elements:
                        text = e.text.strip()
                        # Skip short text, UI elements, and generic phrases
                        if len(text) < 15:
                            continue
                        if any(skip in text.lower() for skip in [
                            'like', 'comment', 'share', 'photo', 'see more',
                            'write a comment', 'press enter', 'this photo'
                        ]):
                            continue
                        # Keep the longest meaningful text
                        if len(text) > len(best_text):
                            best_text = text
                except:
                    continue

            return best_text[:1000] if best_text else ""
        except:
            pass
        return ""

    def click_next_image(self) -> bool:
        """Try to click right arrow to go to next image in the post. Returns True if successful."""
        try:
            # Try various selectors for the right/next arrow
            next_selectors = [
                'div[aria-label="Next"]',
                'div[aria-label="Next photo"]',
                'div[data-visualcompletion="ignore-dynamic"] div[aria-label="Next"]',
                'div[role="button"][aria-label="Next"]',
            ]
            for sel in next_selectors:
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if next_btn.is_displayed():
                        next_btn.click()
                        time.sleep(2)  # Wait for next image to load
                        return True
                except:
                    continue
            return False
        except:
            return False

    def get_url_base(self, url: str) -> str:
        """Get base part of URL (filename) to identify same image with different tokens."""
        if not url:
            return ""
        # Extract the filename part (e.g., "594089807_10236077481951802_2205837158738637292_n.jpg")
        match = re.search(r'/([^/]+_n\.(jpg|png|jpeg))', url, re.IGNORECASE)
        if match:
            return match.group(1)
        return url[:100]  # Fallback to first 100 chars

    def is_url_processed(self, url: str) -> bool:
        """Check if URL (or its base) is already processed."""
        if url in self.processed_urls:
            return True
        # Also check by base filename (handles different token variants)
        url_base = self.get_url_base(url)
        for processed in self.processed_urls:
            if url_base and url_base == self.get_url_base(processed):
                return True
        return False

    def process_image(self, img, src) -> bool:
        """Click image, get ALL images in post using right arrow, download to post folder."""
        try:
            self.debug_log(f"=== START process_image ===")
            self.debug_log(f"Thumbnail src (first 80 chars): {src[:80]}")

            # Save scroll position before clicking
            scroll_pos = self.get_scroll_position()
            self.debug_log(f"Scroll position: {scroll_pos}")

            # Scroll into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
            time.sleep(1)

            # Check post text BEFORE clicking - skip if already seen
            post_text_sig = self.get_post_text_from_feed(img)
            self.debug_log(f"Post text signature: '{post_text_sig[:50] if post_text_sig else 'EMPTY'}'")
            self.debug_log(f"Already in processed_texts? {post_text_sig in self.processed_texts if post_text_sig else 'N/A'}")

            if post_text_sig and post_text_sig in self.processed_texts:
                logger.info(f"Already processed this post (by text), skipping...")
                self.debug_log(f"SKIP: text already processed")
                self.processed_urls.add(src)
                return False

            # Check if thumbnail already processed
            already_processed = src in self.processed_urls or self.is_url_processed(src)
            self.debug_log(f"Thumbnail in processed_urls? {already_processed}")

            if already_processed:
                self.debug_log(f"SKIP: thumbnail already processed, not clicking")
                return False

            # Mark thumbnail as processed
            self.processed_urls.add(src)

            # Click to open viewer
            self.debug_log(f"Clicking image to open viewer...")
            try:
                img.click()
            except ElementClickInterceptedException:
                self.debug_log(f"Click intercepted, using JS click")
                self.driver.execute_script("arguments[0].click();", img)

            time.sleep(2)

            # Get first image URL to check if viewer opened
            full_res_url = self.get_full_res_from_viewer()
            self.debug_log(f"Full res URL from viewer: {full_res_url[:80] if full_res_url else 'NONE'}")

            if not full_res_url:
                logger.info("Could not get image from viewer, closing...")
                self.debug_log(f"FAIL: No full res URL, closing viewer")
                self.close_photo_viewer()
                time.sleep(1)
                self.driver.execute_script("window.scrollBy(0, 600)")
                return False

            # EARLY EXIT: If first full-res image already processed, skip entire post
            if self.is_url_processed(full_res_url):
                logger.info("First image already processed, skipping entire post")
                self.debug_log(f"EARLY SKIP: first full-res already in processed_urls")

                # Add the full-res URL we just found (helps skip same post)
                self.processed_urls.add(full_res_url)

                # Try to mark ALL visible images in current viewport as processed
                # This helps skip multi-image posts faster
                try:
                    visible_images = self.driver.find_elements(By.CSS_SELECTOR, 'img[src*="scontent"]')
                    marked = 0
                    for vi in visible_images[:30]:  # Limit to avoid too many
                        try:
                            vi_src = vi.get_attribute('src')
                            if vi_src and 'scontent' in vi_src:
                                self.processed_urls.add(vi_src)
                                marked += 1
                        except:
                            continue
                    self.debug_log(f"Marked {marked} visible images as processed")
                except Exception as e:
                    self.debug_log(f"Error marking images: {e}")

                self.close_photo_viewer()
                time.sleep(1)
                # Scroll down MORE to get past this multi-image post
                self.driver.execute_script("window.scrollBy(0, 1500)")
                return False

            # Navigate through ALL images in this post using right arrow
            self.debug_log(f"Starting right-arrow navigation...")
            all_urls_in_post = []
            seen_urls = set()
            consecutive_duplicates = 0
            nav_count = 0

            while True:
                current_url = self.get_full_res_from_viewer()
                nav_count += 1

                if current_url:
                    url_base = self.get_url_base(current_url)
                    self.debug_log(f"Nav {nav_count}: url_base={url_base[:40] if url_base else 'NONE'}")

                    # Check if we've seen this exact URL in THIS post (looped back to start)
                    if url_base in seen_urls:
                        consecutive_duplicates += 1
                        self.debug_log(f"  -> Already seen in this post, consec_dups={consecutive_duplicates}")
                        if consecutive_duplicates >= 2:
                            logger.info("Looped back to start, done with this post")
                            self.debug_log(f"LOOP DETECTED: breaking")
                            break
                    else:
                        consecutive_duplicates = 0
                        seen_urls.add(url_base)
                        all_urls_in_post.append(current_url)
                        self.debug_log(f"  -> Added to list, total={len(all_urls_in_post)}")

                # Try to go to next image
                clicked_next = self.click_next_image()
                self.debug_log(f"click_next_image returned: {clicked_next}")
                if not clicked_next:
                    logger.info("No more images (right arrow failed)")
                    self.debug_log(f"RIGHT ARROW FAILED: breaking")
                    break

                # Safety limit
                if len(all_urls_in_post) > 50:
                    self.debug_log(f"SAFETY LIMIT: 50 images, breaking")
                    break

            # Now check which URLs are NEW (not already processed globally)
            self.debug_log(f"Checking {len(all_urls_in_post)} URLs against processed_urls ({len(self.processed_urls)} total)")
            new_urls = []
            for url in all_urls_in_post:
                is_processed = self.is_url_processed(url)
                self.debug_log(f"  URL {self.get_url_base(url)[:30]}: processed={is_processed}")
                if not is_processed:
                    new_urls.append(url)

            if not new_urls:
                logger.info(f"All {len(all_urls_in_post)} images already processed, skipping post")
                self.debug_log(f"SKIP: all {len(all_urls_in_post)} images already processed")
                self.close_photo_viewer()
                time.sleep(1)
                self.driver.execute_script("window.scrollBy(0, 600)")
                self.debug_log(f"Scrolled down 600px after skip")
                return False

            logger.info(f"Found {len(new_urls)} new images out of {len(all_urls_in_post)} total")

            # Create post folder and download new images
            self.post_counter += 1
            post_dir = os.path.join(self.output_dir, str(self.post_counter))
            os.makedirs(post_dir, exist_ok=True)

            # Get post text
            post_text = self.get_post_text_from_viewer()

            # Save post text
            with open(os.path.join(post_dir, "post.txt"), 'w', encoding='utf-8') as f:
                f.write(post_text if post_text else f"Image from Facebook group post #{self.post_counter}")

            # Download all NEW images
            images_downloaded = 0
            for i, url in enumerate(new_urls, 1):
                image_path = os.path.join(post_dir, f"image_{i}.jpg")
                if download_image(url, image_path):
                    logger.info(f"Saved post #{self.post_counter} image {i}")
                    self.processed_urls.add(url)
                    images_downloaded += 1

            if images_downloaded > 0:
                logger.info(f"Post #{self.post_counter}: saved {images_downloaded} images total")

                # Mark this post text as processed
                if post_text_sig:
                    self.processed_texts.add(post_text_sig)

                # Save progress every 5 posts
                if self.post_counter % 5 == 0:
                    save_progress({
                        "processed_urls": list(self.processed_urls),
                        "post_count": self.post_counter,
                        "processed_texts": list(self.processed_texts)
                    }, self.progress_file)

                # Close viewer and scroll DOWN to next content
                self.close_photo_viewer()
                time.sleep(1)
                self.driver.execute_script("window.scrollBy(0, 600)")
                return True
            else:
                # No images downloaded, remove empty folder
                import shutil
                shutil.rmtree(post_dir, ignore_errors=True)
                self.post_counter -= 1

            # Close viewer and scroll DOWN
            self.close_photo_viewer()
            time.sleep(1)
            self.driver.execute_script("window.scrollBy(0, 600)")
            return False

        except StaleElementReferenceException:
            return False
        except Exception as e:
            logger.error(f"Error: {e}")
            self.close_photo_viewer()
            return False

    def scrape(self) -> None:
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            # Load previous progress
            progress = load_progress(self.progress_file)
            self.processed_urls = set(progress.get("processed_urls", []))
            self.processed_texts = set(progress.get("processed_texts", []))
            self.post_counter = progress.get("post_count", 0)
            logger.info(f"Resuming from post #{self.post_counter + 1}, {len(self.processed_urls)} URLs, {len(self.processed_texts)} texts processed")

            self.setup_browser()
            self.navigate_to_group()

            # Initial scroll to load content
            for _ in range(3):
                self.driver.execute_script("window.scrollBy(0, 500)")
                time.sleep(2)

            no_new_count = 0
            last_post_count = self.post_counter

            while self.post_counter < CONFIG["max_posts"]:
                # Find clickable images
                clickable = self.find_clickable_images()
                logger.info(f"Found {len(clickable)} new images to process")

                if not clickable:
                    no_new_count += 1
                    logger.info(f"No new images (attempt {no_new_count}/{CONFIG['no_new_images_limit']})")

                    if no_new_count >= CONFIG["no_new_images_limit"]:
                        logger.info("No new images after multiple scrolls. Stopping.")
                        break

                    # Scroll down
                    self.driver.execute_script("window.scrollBy(0, 800)")
                    time.sleep(CONFIG["scroll_pause"])
                    continue

                no_new_count = 0

                # Process each image
                for img, src in clickable:
                    if self.post_counter >= CONFIG["max_posts"]:
                        break

                    self.process_image(img, src)
                    time.sleep(random.uniform(1, 2))

                # Check if we made progress
                if self.post_counter == last_post_count:
                    # Scroll to get more content
                    self.driver.execute_script("window.scrollBy(0, 800)")
                    time.sleep(CONFIG["scroll_pause"])

                last_post_count = self.post_counter

            # Final save
            save_progress({
                "processed_urls": list(self.processed_urls),
                "processed_texts": list(self.processed_texts),
                "post_count": self.post_counter
            }, self.progress_file)

            logger.info(f"Done! Saved {self.post_counter} posts to {self.output_dir}/")

        except Exception as e:
            logger.error(f"Scraping error: {e}")
            raise
        finally:
            self.close_browser()

# ============================================================================
# Entry Point
# ============================================================================

def main():
    print("""
    ============================================
    Facebook Group Image Scraper (Click-based)
    ============================================
    - Clicks images to open photo viewer
    - Extracts full resolution images
    - Saves to folders: 1/, 2/, 3/ etc.
    - Each folder has post.txt + image_1.jpg
    - Scrolls to load more content
    - Saves progress for resume capability

    Press Ctrl+C to stop at any time.
    ============================================
    """)

    scraper = FacebookGroupScraper()
    scraper.scrape()

if __name__ == "__main__":
    main()


# ============================================================================
# NOTES: What worked vs what didn't
# ============================================================================
#
# WHAT WORKED:
# ------------
# 1. Click-based approach - clicking images opens Facebook's photo viewer
#    which shows full resolution images. This was the key breakthrough.
#
# 2. Getting naturalWidth/naturalHeight from the viewer to find the largest
#    image (the full-res one, not thumbnails).
#
# 3. Filtering out profile pictures by checking URL patterns like 'p50x50',
#    's32x32', 'c0.0.40' etc.
#
# 4. Filtering by display size (offsetWidth/offsetHeight > 100) to only
#    click on actual post images, not tiny profile pics.
#
# 5. Using Escape key to close the photo viewer.
#
# 6. Saving/restoring scroll position so we don't lose our place after
#    closing the viewer.
#
# WHAT DIDN'T WORK:
# -----------------
# 1. Extracting image URLs directly from post HTML - the URLs in the DOM
#    are for thumbnails, not full resolution. Facebook lazy-loads images.
#
# 2. Looking for '_n.jpg' pattern in post HTML - while these URLs exist,
#    they're not in img src attributes, they're in JSON/data attributes.
#
# 3. Using div[role="article"] to find posts - this catches both original
#    posts AND comments that appear in the feed. Comments only have small
#    profile pics (32x32), not actual post photos.
#
# 4. Trying to scroll within the post element to find images - Facebook's
#    virtual scrolling means elements get recycled as you scroll.
#
# 5. Extracting from outerHTML - the image URLs in the raw HTML are often
#    placeholder/thumbnail URLs, not the full resolution ones.
#
# KEY INSIGHT:
# ------------
# The only reliable way to get full-res images from Facebook is to simulate
# what a user does: click on the image to open the photo viewer, then grab
# the URL of the large image that's displayed there.
#
# Facebook serves different image sizes through their CDN using URL params.
# The photo viewer loads the largest available version.
# ============================================================================
