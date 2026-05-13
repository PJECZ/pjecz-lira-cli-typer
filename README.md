# pjecz-lira-cli-typer
Interfaz de línea de comandos (CLI) para cargar archivos a la Plataforma Lira. Hecho con Typer.

## Instalación en Windows

Para crear un ejecutable que se ejecute sin abrir la consola, ve a la carpeta del proyecto y ejecuta:

```bash
pyinstaller --onefile --noconsole main.py
```

El ejecutable generado se creará en `carpeta_del_proyecto\dist\main.exe`

### Preparación

Debes tener instalado:

- Python 3.14
- uv - Manejador de paquetes para Python
- GDrive - Aplicación de sincronización con Google Drive

### Instalar _script_ como servicio en windows

1. Abre el `Programador de tareas` de Windows
2. Presiona sobre el menú derecho la opción `Crear tarea básica...`
3. Añade un nombre ejem: "syncFolder" y una descripción: "Programa para sincronizar folder de videos con GDrive"
4. **Desencadenar**: Al iniciarse el equipo
5. **Acción**: Iniciar un programa
6. **Programa o script**: Aquí busca la ruta del ejecutable que se generó esta en: `C:\...\carpeta_del_proyecto\dist\main.exe`
7. **Agregar argumentos (opcional)**: Añade los siguiente parámetros: `--source c:\carpeta-origen --dest c:\carpeta-destino`
8. Ahora selecciona la tarea, da clic derecho sobre ella y selecciona ejecutar. Copia un archivo en el directorio `c:\carpeta-origen` y revisa después de un minuto el directorio `c:\carpeta-destino` para comprobar si funciona.

Listo! con esto debería mantenerse en ejecución el programa y copiar los archivos del directorio origen al destino.