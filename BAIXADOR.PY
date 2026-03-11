import yt_dlp
import datetime
from tkinter import Tk, filedialog

def ja_baixado(url):
    try:
        with open("historico_downloads.txt", "r", encoding="utf-8") as f:
            for linha in f:
                if url in linha:
                    return True
    except FileNotFoundError:
        return False
    return False
def progresso(d):
    if d['status'] == 'downloading':
        print(f"\rBaixando... {d['_percent_str']}", end="")
    elif d['status'] == 'finished':
        print("\nDownload finalizado, processando arquivo...")
while True:
    url = input("Cole o link do vídeo ou playlist: ")
    if ja_baixado(url):
        repetir = input("Esse vídeo já foi baixado antes. Baixar novamente? (s/n): ").lower()
        if repetir != "s":
            print("Download cancelado.")
            continue
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if "entries" in info:
        titulo = info.get("title", "Playlist")
    else:
        titulo = info.get("title", "Video")
    with open("historico_downloads.txt", "a", encoding="utf-8") as f:
        f.write(f"{data} | {titulo} | {url}\n")
    root = Tk()
    root.withdraw()
    if "entries" in info:
        total_videos = len(info["entries"])
        print(f"\nPlaylist detectada com {total_videos} vídeos.")
        quantidade = input("Quantos vídeos deseja baixar? (ou ENTER para todos): ")
        if quantidade.strip() == "":
            limite = None
        else:
            limite = int(quantidade)
        pasta = filedialog.askdirectory(title="Escolha a pasta para salvar a playlist")
        if not pasta:
            print("Download cancelado.")
            continue
        opcoes = {
            "outtmpl": f"{pasta}/%(title)s.%(ext)s",
            "progress_hooks": [progresso],
            "ignoreerrors": True
        }
        if limite:
            opcoes["playlistend"] = limite
    else:
        titulo = info["title"]
        arquivo = filedialog.asksaveasfilename(
            title="Salvar vídeo como",
            initialfile=titulo + ".mp4",
            defaultextension=".mp4",
            filetypes=[("Vídeo MP4", "*.mp4"), ("Todos os arquivos", "*.*")]
        )
        if not arquivo:
            print("Download cancelado.")
            continue
        opcoes = {
            "outtmpl": arquivo,
            "progress_hooks": [progresso],
            "ignoreerrors": True
        }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])
    print("\nDownload concluído!")
    continuar = input("Deseja baixar outro vídeo? (s/n): ").lower()
    if continuar != "s":
        print("Programa encerrado.")
        break          
