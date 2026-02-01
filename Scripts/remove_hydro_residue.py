import pymol
from pymol import cmd, stored


iter_loop = int(sys.argv[1])
iter_residue = int(sys.argv[2])

cmd.bond("1/ca", "1/cb")
cmd.unbond("1/ca","2/ca")

cmd.select("trimmed", "not hydro")
cmd.save("4j4l_round%s_%s_1.pdb"%(iter_loop, iter_residue ), "trimmed")

