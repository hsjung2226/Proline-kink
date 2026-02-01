import pymol
from pymol import cmd, stored

iter_num = sys.argv[1]
iter_num = int(iter_num)


cmd.select("trimmed", "not hydro")
cmd.save("4j4l_round%s_0_2.pdb"%(iter_num), "trimmed")


