"""
main.py - Punto de entrada de la aplicacion pjecz-lira-cli-typer.

Uso:
    python main.py watch [OPTIONS]
"""

from pathlib import Path

import typer

from pjecz_lira_cli_typer.videos_watcher import watch_videos

app = typer.Typer(help="Herramienta CLI para copiar videos nuevos a la unidad G.")


@app.command()
def watch(
    source: Path = typer.Option(
        Path.home() / "Videos",
        "--source",
        "-s",
        help="Directorio de origen a vigilar.",
        show_default=True,
    ),
    dest_drive: str = typer.Option(
        "G:\\",
        "--dest",
        "-d",
        help="Unidad o directorio destino donde se copian los videos.",
        show_default=True,
    ),
    wait: int = typer.Option(
        60,
        "--wait",
        "-w",
        help="Segundos que debe pasar sin modificaciones antes de copiar el archivo.",
        show_default=True,
    ),
    poll: int = typer.Option(
        10,
        "--poll",
        "-p",
        help="Intervalo en segundos para revisar archivos pendientes.",
        show_default=True,
    ),
):
    """Vigila el directorio Videos y copia archivos nuevos hacia la unidad destino."""
    watch_videos(
        source_dir=source,
        dest_drive=dest_drive,
        wait_seconds=wait,
        poll_interval=poll,
    )


if __name__ == "__main__":
    app()
