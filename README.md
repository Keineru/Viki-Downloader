# Viki-Downloader
Viki Downloader descarga subtitulos y videos de episodios de Viki en srt y mp4 respectivamente.

Uso: vikidownloader.py url [-s] [--lang IDIOMA] [--v]
    
    positional arguments:
      url                   URL del video de Viki
    optional arguments:
      -h, --help            Muestra este mensaje y la aplicación cierra
      -s, --subs            Muestra todos los subtitulos disponibles
      --lang LANG           Codigo ISO del idioma
      -v, --video           Descarga el video

    Ejemplo:
    python vikidownloader.py http://www.viki.com/videos/1105299v-w-episode-1 --lang en -v
