from dotenv import load_dotenv
import os
from auto_gomnet import AutoGomNet

load_dotenv()

USUARIO = os.getenv('USUARIO')
SENHA = os.getenv('SENHA')

auto = AutoGomNet(USUARIO, SENHA)

msg = '''
Digite 1 para anexar as entregas de trabalho
Digite 2 para anexar autorizações de cavas
Digite qualquer coisa para sair
'''

escolha = int(input(msg))

cont_anexados = 0

if escolha == 1:
    cont_anexados = auto.anexar_entregas()
elif escolha == 2:
    cont_anexados = auto.anexar_atorizacoes_cavas()
else:
    print('Encerrando programa!')
    exit()

print(f'PROCESSO CONCLUÍDO COM SUCESSO COM {cont_anexados} DOCUMENTOS ANEXADOS!')
print()
