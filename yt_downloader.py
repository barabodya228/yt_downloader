import subprocess
from tqdm import tqdm

def get_format_list(url):
    command = [
        'yt-dlp',
        '--cookies-from-browser', 'firefox',
        '--list-formats',
        url
    ]
    subprocess.run(command)

def download_video(url, format_id, mode, format_choice='mp4'):
    # Автоматически добавляем аудио, если выбран только видео формат
    if mode == '1':  # аудио+видео
        if format_id.isdigit():
            quality = f"{format_id}+bestaudio"
        else:
            quality = format_id
    elif mode == '2':  # только видео
        quality = format_id
    elif mode == '3':  # только аудио
        quality = format_id
    else:
        quality = 'best'

    command = [
        'yt-dlp',
        '--cookies-from-browser', 'firefox',
        '--format', quality,
        '--merge-output-format', format_choice,
        '--no-playlist',
        '--progress',
        '--quiet',  # Для уменьшения вывода
        url
    ]

    print("\nЗапуск yt-dlp с передачей куков напрямую из Firefox...")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

    # Прогресс-бар
    for line in tqdm(process.stdout, desc="Скачивание видео", unit="byte"):
        if 'Downloading' in line:
            # Извлекаем прогресс из вывода
            pass  # Можно добавить дополнительные действия для точного отслеживания прогресса.

    process.stdout.close()
    process.wait()

def main():
    url = input("Вставь ссылку на видео: ").strip()

    show_formats = input("Показать доступные форматы? (y/N): ").strip().lower()
    if show_formats == 'y':
        get_format_list(url)

    print("Выберите режим загрузки:")
    print("1 — аудио+видео")
    print("2 — только видео")
    print("3 — только аудио")
    mode = input("Ваш выбор [1]: ").strip() or '1'

    if mode == '1':
        format_id = input("Введите ID видеоформата (например: 137), либо 'best': ").strip() or 'best'
    elif mode == '2':
        format_id = input("Введите ID видеоформата (например: 137), либо 'bestvideo': ").strip() or 'bestvideo'
    elif mode == '3':
        format_id = input("Введите ID аудиоформата (например: 140), либо 'bestaudio': ").strip() or 'bestaudio'
    else:
        format_id = 'best'

    format_choice = input("Выберите конечный контейнер (mp4/webm, по умолчанию 'mp4'): ").strip() or 'mp4'

    download_video(url, format_id, mode, format_choice)

if __name__ == '__main__':
    main()
