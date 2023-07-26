# O código acima define e implementa uma função logger. A função
# logger inicializa e configura um logger para este módulo.

# Primeiro, o nível básico do logging é configurado para DEBUG
# através da função logging.basicConfig(). Isso significa que
# todas as mensagens de log de nível DEBUG ou superior serão
# rastreadas.

# Em seguida, a função logging.getLogger(__name__) é chamada para
# fornecer um logger específico para este módulo. Isso permite que
# diferentes módulos ou partes do código tenham loggers separados.

# Uma condição hipotética é criada para ilustrar uma possível
# mensagem de erro. Se o logger for None, uma exceção ValueError
# é levantada com a mensagem "O logger não foi inicializado
# corretamente". Esta exceção é capturada em um bloco try/except,
# que imprime a mensagem de erro.

# A função logger é então chamada e a instância de logger
# retornada é atribuída à variável logger. Se a função logger
# lançar uma exceção, esta é capturada e sua mensagem é impressa.
import logging


def logger():
    """
    Função para inicializar e configurar o logger.

    Configura o nível de log para DEBUG, o que significa que
    todas as mensagens de log de nível DEBUG ou superior
    serão rastreadas.

    Retorna:
    - logger: Um logger específico para este módulo, permitindo
    que diferentes módulos ou partes do código tenham
    loggers separados.
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    return logger
