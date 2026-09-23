import os
import sys
import imageio_ffmpeg
from yt_dlp import YoutubeDL
from colorama import init, Fore, Style

# เริ่มการทำงานของ Colorama
init(autoreset=True)

def clear_screen():
    """เคลียร์หน้าจอ Terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ffmpeg_path():
    """ดึง Path ของ ffmpeg.exe อัตโนมัติ"""
    return imageio_ffmpeg.get_ffmpeg_exe()

def print_banner():
    """แสดงแบนเนอร์ส่วนหัว"""
    print(Fore.CYAN + Style.BRIGHT + "=" * 55)
    print(Fore.YELLOW + Style.BRIGHT + "      🎬 YOUTUBE DOWNLOADER & MP3 CONVERTER (4K) ")
    print(Fore.YELLOW + Style.BRIGHT + "                Made by : Apologym_ ")
    print(Fore.CYAN + Style.BRIGHT + "=" * 55)

def check_back_or_exit(user_input):
    """ตรวจสอบว่าผู้ใช้ต้องการย้อนกลับหรือออกจากโปรแกรมหรือไม่"""
    clean_input = user_input.strip().lower()
    if clean_input in ['b', 'back']:
        return "back"
    if clean_input in ['e', 'exit']:
        return "exit"
    return None

def select_mode():
    """ขั้นตอนที่ 1: เลือกโหมดวิดีโอหรือเสียง"""
    while True:
        clear_screen()
        print_banner()
        print(Fore.WHITE + " [1] 📹 ดาวน์โหลดวิดีโอ (Video - MP4)")
        print(Fore.WHITE + " [2] 🎵 ดาวน์โหลดเฉพาะเสียง (Audio - MP3)")
        print(Fore.RED + " [e] ❌ ออกจากโปรแกรม")
        print(Fore.CYAN + "-" * 55)
        
        choice = input(Fore.GREEN + "👉 เลือกรูปแบบที่ต้องการ (1/2 หรือ e): " + Style.RESET_ALL).strip()
        
        status = check_back_or_exit(choice)
        if status == "exit":
            return "exit", None
            
        if choice in ["1", "2"]:
            return choice, None
        
        print(Fore.RED + "\n⚠️ ตัวเลือกไม่ถูกต้อง กรุณาเลือกใหม่...")
        input("กด Enter เพื่อลองอีกครั้ง...")

def select_quality(mode):
    """ขั้นตอนที่ 2: เลือกคุณภาพความชัด"""
    while True:
        clear_screen()
        print_banner()
        
        if mode == "1":
            print(Fore.YELLOW + "🎬 [โหมดวิดีโอ MP4] เลือกความละเอียด:")
            print(" [1] 4K (2160p)")
            print(" [2] 2K (1440p)")
            print(" [3] Full HD (1080p)")
            print(" [4] HD (720p)")
        else:
            print(Fore.YELLOW + "🎵 [โหมดเสียง MP3] เลือกคุณภาพเสียง:")
            print(" [1] สูงสุด (320 kbps)")
            print(" [2] ปานกลาง (192 kbps)")
            print(" [3] ประหยัดพื้นที่ (128 kbps)")
            
        print(Fore.CYAN + "-" * 55)
        print(Fore.YELLOW + " [b] ↩️ ย้อนกลับไปเลือกโหมด")
        print(Fore.RED + " [e] ❌ ออกจากโปรแกรม")
        print(Fore.CYAN + "-" * 55)
        
        choice = input(Fore.GREEN + "👉 เลือกระดับคุณภาพ (b ย้อนกลับ / e ออก): " + Style.RESET_ALL).strip()
        
        status = check_back_or_exit(choice)
        if status == "back":
            return "back", None
        if status == "exit":
            return "exit", None

        if mode == "1" and choice in ["1", "2", "3", "4"]:
            quality_map = {"1": "2160", "2": "1440", "3": "1080", "4": "720"}
            return "ok", quality_map[choice]
        elif mode == "2" and choice in ["1", "2", "3"]:
            quality_map = {"1": "320", "2": "192", "3": "128"}
            return "ok", quality_map[choice]

        print(Fore.RED + "\n⚠️ ตัวเลือกไม่ถูกต้อง กรุณาเลือกใหม่...")
        input("กด Enter เพื่อลองอีกครั้ง...")

def input_urls():
    """ขั้นตอนที่ 3: รับลิงก์ YouTube"""
    while True:
        clear_screen()
        print_banner()
        print(Fore.YELLOW + "📌 วางลิงก์ YouTube ที่ต้องการดาวน์โหลด")
        print(Fore.WHITE + "   (วางได้หลายลิงก์พร้อมกัน โดยเว้นวรรค หรือคั่นด้วย ,)")
        print(Fore.CYAN + "-" * 55)
        print(Fore.YELLOW + " [b] ↩️ ย้อนกลับไปเลือกความชัด")
        print(Fore.RED + " [e] ❌ ออกจากโปรแกรม")
        print(Fore.CYAN + "-" * 55)
        
        raw_input = input(Fore.GREEN + "👉 วางลิงก์ที่นี่: " + Style.RESET_ALL).strip()
        
        status = check_back_or_exit(raw_input)
        if status == "back":
            return "back", None
        if status == "exit":
            return "exit", None

        if raw_input:
            # แยกลิงก์และลบตัวซ้ำ
            raw_urls = [url.strip() for url in raw_input.replace(",", " ").split() if url.strip()]
            urls = list(dict.fromkeys(raw_urls))
            return "ok", urls

        print(Fore.RED + "\n⚠️ ไม่พบลิงก์ กรุณาวางลิงก์อย่างน้อย 1 ลิงก์...")
        input("กด Enter เพื่อลองอีกครั้ง...")

def get_yt_options(mode, quality, ffmpeg_path):
    # กำหนดให้โฟลเดอร์ downloads อยู่ในโฟลเดอร์เดียวกับไฟล์สคริปต์เสมอ
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(base_dir, "downloads")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'restrictfilenames': False, # ตั้งเป็น True หากต้องการให้ชื่อไฟล์ไม่มีเว้นวรรค/สัญลักษณ์พิเศษ
        'ffmpeg_location': ffmpeg_path,
        'quiet': False,             # เปิด Log ไว้ชั่วคราวเพื่อตรวจสอบความผิดพลาด
        'no_warnings': False,
        'progress_hooks': [
            lambda d: sys.stdout.write(
                f"\r  {Fore.MAGENTA}└─ กำลังโหลด: {Fore.YELLOW}{d.get('_percent_str', '')} "
                f"{Fore.BLUE}(ความเร็ว {d.get('_speed_str', '')} | เหลืออีก {d.get('_eta_str', '')}){Style.RESET_ALL}   "
            ) if d['status'] == 'downloading' else None
        ],
    }

    if mode == "1":
        ydl_opts.update({
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'merge_output_format': 'mp4',
        })
    else:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
        })

    return ydl_opts

def main():
    while True:
        # Step 1: เลือกโหมด
        mode, _ = select_mode()
        if mode == "exit":
            print(Fore.YELLOW + "\n👋 ขอบคุณที่ใช้งาน ปิดโปรแกรมเรียบร้อยครับ")
            break

        # Step 2: เลือกความชัด
        status, quality = select_quality(mode)
        if status == "exit":
            print(Fore.YELLOW + "\n👋 ขอบคุณที่ใช้งาน ปิดโปรแกรมเรียบร้อยครับ")
            break
        if status == "back":
            continue # วนกลับไป Step 1

        # Step 3: กรอกลิงก์
        status, urls = input_urls()
        if status == "exit":
            print(Fore.YELLOW + "\n👋 ขอบคุณที่ใช้งาน ปิดโปรแกรมเรียบร้อยครับ")
            break
        if status == "back":
            continue # วนกลับไป Step 2 (เนื่องจากยังอยู่ในลูปหลัก)

        # Step 4: เริ่มดาวน์โหลด
        clear_screen()
        print_banner()
        ffmpeg_path = get_ffmpeg_path()
        
        ydl_opts = get_yt_options(mode, quality, ffmpeg_path)

        print(Fore.CYAN + f"\n🚀 เริ่มดาวน์โหลดทั้งหมด {len(urls)} รายการ...\n")

        with YoutubeDL(ydl_opts) as ydl:
            for index, url in enumerate(urls, 1):
                print(Fore.WHITE + Style.BRIGHT + f"[{index}/{len(urls)}] 🔗 {url}")
                try:
                    ydl.download([url])
                    print(Fore.GREEN + Style.BRIGHT + "\n  ✅ สำเร็จเรียบร้อย!\n")
                except Exception as e:
                    print(Fore.RED + f"\n  ❌ เกิดข้อผิดพลาด: {e}\n")

        print(Fore.GREEN + Style.BRIGHT + "🎉 ทำรายการครบถ้วนแล้ว! ไฟล์ถูกเซฟไว้ในโฟลเดอร์ 'downloads'")
        
        print(Fore.CYAN + "\n" + "=" * 55)
        again = input(Fore.YELLOW + "👉 ต้องการดาวน์โหลดต่อหรือไม่? (y/n): " + Style.RESET_ALL).strip().lower()
        if again != 'y':
            print(Fore.YELLOW + "\n👋 ขอบคุณที่ใช้งานครับ!")
            break

if __name__ == "__main__":
    main()
