import random
import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
import constants
from constants import CODE


def code_generate():
    digits = '0123456789'

    return ''.join(random.choice(digits) for i in range(CODE))
