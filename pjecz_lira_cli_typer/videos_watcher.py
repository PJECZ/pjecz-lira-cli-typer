"""
videos_watcher.py - Observador del directorio Videos.

- Vigila el directorio Videos en busca de archivos nuevos o modificados.
- Cuando un archivo lleva más de un minuto sin ser modificado, lo copia
hacia la unidad G manteniendo la misma ruta relativa.
"""

import shutil
import time
from pathlib import Path

from watchdog.events import FileCreatedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer


class VideosEventHandler(FileSystemEventHandler):
    """Manejador de eventos del sistema de archivos para el directorio Videos."""

    def __init__(self, source_dir: Path, dest_drive: str, wait_seconds: int = 60):
        super().__init__()
        self.source_dir = source_dir.resolve()
        self.dest_drive = dest_drive
        self.wait_seconds = wait_seconds
        # Diccionario: ruta_archivo -> timestamp de ultima modificacion detectada
        self._pending: dict[Path, float] = {}

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        file_path = Path(str(event.src_path)).resolve()
        self._pending[file_path] = time.time()

    def on_modified(self, event: FileModifiedEvent) -> None:
        if event.is_directory:
            return
        file_path = Path(str(event.src_path)).resolve()
        self._pending[file_path] = time.time()

    def process_pending(self) -> None:
        """Revisa los archivos pendientes y copia los que ya cumplieron el tiempo de espera."""
        now = time.time()
        ready = [fp for fp, ts in self._pending.items() if now - ts >= self.wait_seconds]
        for file_path in ready:
            del self._pending[file_path]
            if not file_path.exists():
                continue
            try:
                relative = file_path.relative_to(self.source_dir)
            except ValueError:
                continue
            dest_path = Path(self.dest_drive) / relative
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(file_path), str(dest_path))
            print(f"[OK] Copiado: {file_path} -> {dest_path}")


def watch_videos(
    source_dir: Path,
    dest_drive: str,
    wait_seconds: int,
    poll_interval: int,
) -> None:
    """Inicia el observador del directorio Videos."""
    if not source_dir.exists():
        raise FileNotFoundError(f"El directorio de origen no existe: {source_dir}")

    print(f"Observando: {source_dir}")
    print(f"Destino:    {dest_drive}")
    print(f"Espera:     {wait_seconds} segundos antes de copiar")
    print("Presiona Ctrl+C para detener.\n")

    handler = VideosEventHandler(source_dir, dest_drive, wait_seconds)
    observer = Observer()
    observer.schedule(handler, str(source_dir), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(poll_interval)
            handler.process_pending()
    except KeyboardInterrupt:
        print("\nDeteniendo observador...")
    finally:
        observer.stop()
        observer.join()
        print("Observador detenido.")
