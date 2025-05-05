import os
import re
from datetime import datetime

def encontrar_backup_mais_recente(pasta='backup'):
    padrao = re.compile(r'backup_flask_(\d{8}_\d{6})\.zip')
    mais_recente = None
    timestamp_recente = None

    for arquivo in os.listdir(pasta):
        match = padrao.match(arquivo)
        if match:
            timestamp_str = match.group(1)
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            if not timestamp_recente or timestamp > timestamp_recente:
                timestamp_recente = timestamp
                mais_recente = arquivo

    if mais_recente:
        caminho_completo = os.path.join(pasta, mais_recente)
        print(f'Backup mais recente: {caminho_completo}')
        return caminho_completo
    else:
        print('Nenhum backup encontrado.')
        return None
