from invoke import task
import os
from datetime import datetime, timedelta
import zipfile
import shutil
from utils import encontrar_backup_mais_recente
import os
import re
from datetime import datetime

@task 
def backup(c, source='.', destination='backup', dias_max=7):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_backup_dir = os.path.join(destination, f'temp_{timestamp}')
    zip_filename = os.path.join(destination, f'backup_flask_{timestamp}.zip')
        
    os.makedirs(temp_backup_dir, exist_ok=True)
    incluir = ['app', 'template', 'src', 'task.py']

    for item in incluir:
        if os.path.exists(item):
            destino_item = os.path.join(temp_backup_dir, item)
            try:
                if os.path.isdir(item):
                    shutil.copytree(item, destino_item)
                else:
                    shutil.copy2(item, destino_item)
                print(f'Copiado: {item}')
            except Exception as e:
                print(f'Erro ao copiar {item}: {e}')
            
    # Compactando os arquivos
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, temp_backup_dir))
    
    print(f'\n Backup criado em: {zip_filename}')
    shutil.rmtree(temp_backup_dir)
    remover_antigos_backups(destination, dias_max)

def remover_antigos_backups(pasta_backup, dias_max):
    agora = datetime.now()
    limite = agora - timedelta(days=int(dias_max))

    for arquivo in os.listdir(pasta_backup):
        if arquivo.endswith(".zip"):
            caminho = os.path.join(pasta_backup, arquivo)
            mod_time = datetime.fromtimestamp(os.path.getmtime(caminho))
            if mod_time < limite:
                os.remove(caminho)
                print(f"Backup antigo removido: {arquivo}")

@task
def descompactar(c):
    caminho_zip = encontrar_backup_mais_recente()

    if caminho_zip:
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall('restaurado')
        print('Backup restaurado na pasta "restaurado"')    