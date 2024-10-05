import subprocess
import re

def chep():
    """
    Ejecuta el comando 'systemctl status chep' y extrae el puerto SSH remoto.
    
    La función ejecuta 'sudo systemctl status chep', busca el puerto SSH utilizando
    una expresión regular, y devuelve el puerto si es encontrado.
    
    Returns:
        str: El puerto SSH encontrado, o un mensaje de error si no se encuentra el puerto.
    """
    result = subprocess.run(['sudo', 'systemctl', 'status', 'chep'], stdout=subprocess.PIPE, text=True)
    output = result.stdout

    match = re.search(r'ssh -N -R (\d+):localhost:22', output)
    if match:
        ssh_port = match.group(1)
        return ssh_port
    else:
        return "No se encontró el puerto SSH"
