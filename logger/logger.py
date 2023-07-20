import logging

def logger():
    # Configura o nível básico do logging para DEBUG.
    # Isso significa que todas as mensagens de log de nível DEBUG ou superior serão rastreadas.
    logging.basicConfig(level=logging.DEBUG)
    
    # getLogger(__name__) fornece um logger específico para este módulo,
    # permitindo que diferentes módulos ou partes do código tenham loggers separados.
    logger = logging.getLogger(__name__)

    try:
        # Condição hipotética para ilustrar uma possível mensagem de erro.
        if logger is None:
            raise ValueError("O logger não foi inicializado corretamente")
    except ValueError as e:
        # Exibe a mensagem de erro.
        print(f"Ocorreu um erro: {e}")
    
    print("Inicializando logger...")
    
    return logger

# Aplicação do logger.
try:
    logger = logger()
    print("Logger inicializado com sucesso.")
except Exception as e:
    print(f"Ocorreu um erro ao inicializar o logger: {e}") 