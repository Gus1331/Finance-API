from apscheduler.schedulers.background import BackgroundScheduler
from controllers.awesomeapi_controller import leitura
import time

def configurar_agendamento():
    scheduler = BackgroundScheduler()
    scheduler.add_job(leitura, 'interval', seconds=86400)

    scheduler.start()