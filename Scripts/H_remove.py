
import pymol
from pymol import cmd, stored


cmd.select("trimmed", "not hydro")
cmd.save("4j4l_temp.pdb", "trimmed")
