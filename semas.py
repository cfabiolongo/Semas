from phidias.Main import *
from phidias.Types import *


def_vars('X', 'Y', 'Z', 'U', 'S')

from actions import *
# from onto_builder import *
from front_end import *


# instantiate the engine
PHIDIAS.run()
# run the engine shell
PHIDIAS.shell(globals())
