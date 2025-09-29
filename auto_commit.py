# auto_commit.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# Configuración
REPO_PATH = os.path.dirname(os.path.abspath(__file__))  # Carpeta raíz del proyecto
COMMIT_MESSAGE_TEMPLATE = "🛠️ Auto-commit: cambios detectados en ARGOTH"

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Ignorar cambios en .git y en el propio script
        if ".git" in event.src_path or "auto_commit.py" in event.src_path:
            return
        print(f"📌 Cambio detectado en: {event.src_path}")
        try:
            # Añadir cambios
            subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
            # Commit
            subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE_TEMPLATE], cwd=REPO_PATH, check=True)
            print("✅ Commit automático realizado.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error haciendo commit: {e}")

def main():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=REPO_PATH, recursive=True)
    observer.start()
    print("🚀 Auto-commit activo. Observando cambios en ARGOTH...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()