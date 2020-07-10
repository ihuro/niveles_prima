"""Check Fibertel Prima levels
"""
import requests
import tabulate
from bs4 import BeautifulSoup
from colorama import (
    init,
    Fore,
    Style
)
from loguru import logger
from loguru._defaults import LOGURU_SUCCESS_NO


URL = 'http://provisioning.fibertel.com.ar/asp/nivelesPrima.asp'

# Colors
BAD = Fore.RED
FINE = Fore.GREEN
WARNING = Fore.YELLOW

TEXTS = {
    BAD: 'INCORRECT',
    FINE: 'CORRECT',
    WARNING: 'WARNING'
}

# Tags Limits
NO_LIMITS = (None, None)
COLORS = {
    'tx': {
        (35, 47): FINE,
        NO_LIMITS: BAD
    },
    'rx': {
        (-7, 7): FINE,
        (-15, 15): WARNING,
        NO_LIMITS: BAD
    }
}


def between(value, limits):
    """Cehck if the value is between the limits
    """
    bottom, top = limits
    return (limits == NO_LIMITS) or (bottom <= value <= top)


def get_status(value, tag):
    """Check the value for an specific tag to see its status
    """
    if tag in COLORS:
        colors = COLORS[tag]
        for limits, color in colors.items():
            if between(value, limits):
                return color
        return BAD


@logger.catch
def get_niveles(url=URL):
    """Get niveles prima from the required URL and parse the HTML response
    """
    niveles = requests.get(url)
    niveles_parsed = BeautifulSoup(niveles.content, features='html.parser')

    data = []
    for td in niveles_parsed.find_all('td', class_='etiqueta'):
        status_text = ''
        tag = td.text.lower()
        value = td.find_next_sibling('td').text
        if tag in COLORS:
            level = float(value.split(' ')[0].replace(',', '.'))
            status = get_status(level, tag)
            status_text = f"{status}{Style.BRIGHT}{TEXTS[status]}{Style.RESET_ALL}"
            logger.success(f"{tag}: {value}")
        data.append((tag.title(), value, status_text))

    return data


def print_tabulate(niveles, table_format="fancy_grid"):
    """Print result using tabulate
    """
    if niveles:
        tabla_niveles = tabulate.tabulate(
            niveles,
            headers=(f"{Style.BRIGHT}TAG", f"Value", f"State{Style.RESET_ALL}"),
            tablefmt=table_format,
            colalign=("left", "left", "center")
        )
        print(tabla_niveles)


def success_or_less(record):
    """Function to filter logger messages higher thant success
    """
    return record["level"].no <= LOGURU_SUCCESS_NO


def configure_logger():
    """Configure loguru
    """
    # Clear defaults
    logger.remove()

    # Log exceptions
    logger.add(
        "niveles_prima_trace.log",
        rotation="10MB",
        compression="gz",
        backtrace=True,
        diagnose=True,
        level="ERROR"
    )

    # Log success values (to keep trace of TX and RX)
    logger.add(
        "niveles_prima.log",
        rotation="1MB",
        compression="gz",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="SUCCESS",
        filter=success_or_less
    )


if __name__ == '__main__':
    configure_logger()
    niveles = get_niveles()
    print_tabulate(niveles)
