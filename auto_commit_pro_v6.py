# auto_commit_pro_v6_final.py - Auto Commit PRO ARGOTH v6 Final
# ===============================================================
# Detecta cambios automáticamente y hace commits con formato profesional
# Incluye emojis según fase detectada, agrupación de cambios y compatibilidad VS Code

import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# ===============================
# CONFIGURACIÓN
# ===============================
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
GROUP_INTERVAL = 5  # segundos para agrupar cambios
WATCH_EXTENSIONS = (".py", ".csv")
IGNORE_FOLDERS = [".venv", "__pycache__", ".git"]

PHASE_MAPPING = {
    "strategy": ["strategy.py"],
    "build": ["utils_", "main.py"],
    "config": ["config.py", "settings.py"],
    "test": ["test_", "tests/"],
    "run": ["auto_commit_", "execute_", "loop_"],
    "security": ["security_", "risk_"],
    "infra": ["db_", "backend_", "infra_"],
    "improve": ["refactor", "optimize", "clean"]
}

PHASE_EMOJIS = {
    "build": "🏗️",
    "config": "⚙️",
    "strategy": "📊",
    "test": "🔬",
    "run": "🚀",
    "security": "🛡️",
    "infra": "📦",
    "improve": "✨"
}

DEFAULT_SECTION = "ARGOTH"
DEFAULT_ACTION = "Actualización automática"

# ===============================
# VARIABLES GLOBALES
# ===============================
changed_files = set()
last_change_time = 0

# ===============================
# FUNCIONES
# ===============================
def detect_phase(file_path):
    fname = os.path.basename(file_path).lower()
    for phase, keys in PHASE_MAPPING.items():
        if any(k in fname for k in keys):
            return phase
    return "strategy"

def replace_emoji_tags(msg: str) -> str:
    replacements = {
        ":bar_chart:": "📊",
        ":rocket:": "🚀",
        ":test_tube:": "🔬",
        ":shield:": "🛡️",
        ":gear:": "⚙️",
        ":package:": "📦",
        ":sparkles:": "✨",
        ":building_construction:": "🏗️"
    }
    for tag, emoji in replacements.items():
        msg = msg.replace(tag, emoji)
    return msg

def commit_changes(files):
    if not files:
        return
    try:
        phases_used = set()
        for f in files:
            subprocess.run(["git", "add", f], cwd=REPO_PATH, check=True)
            phases_used.add(detect_phase(f))
        phase = next(iter(phases_used))
        emoji = PHASE_EMOJIS.get(phase, "")
        file_list = ", ".join([os.path.basename(f) for f in files])
        commit_msg = f"{emoji} [{DEFAULT_SECTION}]: {DEFAULT_ACTION} ({file_list})"
        commit_msg = replace_emoji_tags(commit_msg)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_PATH, check=True)
        print(f"✅ Auto commit v6: {commit_msg}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al hacer commit: {e}")

def schedule_commit(file_path):
    global last_change_time
    if any(ignored in file_path for ignored in IGNORE_FOLDERS):
        return
    if not file_path.endswith(WATCH_EXTENSIONS):
        return
    changed_files.add(file_path)
    last_change_time = time.time()

# ===============================
# HANDLER WATCHDOG
# ===============================
class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        schedule_commit(event.src_path)

# ===============================
# EJECUCIÓN PRINCIPAL
# ===============================
def main():
    observer = Observer()
    event_handler = WatcherHandler()
    observer.schedule(event_handler, REPO_PATH, recursive=True)
    observer.start()
    print("🚀 Auto Commit PRO v6 Final iniciado... observando cambios en el repo")

    try:
        while True:
            time.sleep(1)
            if changed_files and (time.time() - last_change_time) >= GROUP_INTERVAL:
                commit_changes(list(changed_files))
                changed_files.clear()
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 Auto Commit PRO v6 Final detenido por usuario")
    observer.join()

if __name__ == "__main__":
    main()
    

    