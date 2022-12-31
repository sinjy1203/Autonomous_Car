from pathlib import Path
import shutil

data_dir = Path('./data/raw_chess')
if data_dir.exists():
    shutil.rmtree(data_dir)