from apscheduler.schedulers.background import BackgroundScheduler
from controllers.awesomeapi_controller import leitura
import time

def configurar_agendamento(es):
    print('configurado')
    leitura(es)
    # scheduler = BackgroundScheduler()

    # scheduler.add_job(leitura , 'interval', seconds=24)

    # scheduler.start()