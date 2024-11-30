import os
import shutil

import src.app as app

def main():
    refresh_dir('public')
    copy_static_to_public()

    app.run()

def copy_static_to_public() -> None:
    if not os.path.exists('static'):
        raise FileNotFoundError('static directory not found')
    if not os.path.exists('public'):
        os.mkdir('public')
    
    def copy(src, dest):
        if os.path.isdir(src):
            if not os.path.exists(dest):
                print(f'Creating {dest}')
                os.mkdir(dest)
            for file in os.listdir(src):
                copy(os.path.join(src, file), os.path.join(dest, file))
        else:
            print(f'Copying {src} to {dest}')
            shutil.copy(src, dest)

    copy('static', 'public')
    
def refresh_dir(dir: str) -> None:
    if os.path.exists(dir):
        print(f'Clearing {dir}')
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if os.path.isdir(path):
                refresh_dir(path)
            else:
                print(f'Removing {path}')
                os.remove(path)
    else:
        print(f'Creating {dir}')
        os.mkdir(dir)

main()