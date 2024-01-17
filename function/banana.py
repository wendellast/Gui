
from datetime import datetime


now = datetime.now()
now.strftime("%d/%m/%Y %H:%M:%S")



def response_if(command):
    if command == 'que horas são':
        return f'Agora são: {now.strftime("%d/%m/%Y %H:%M:%S")}'
    else:
        return False
