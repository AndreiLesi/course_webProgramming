import random
from . import util

def randomEntry(request):
    randomEntry = random.choice(util.list_entries())
    return {'randomEntry': randomEntry}