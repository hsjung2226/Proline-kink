import pymol
from pymol import cmd, stored

iter_loop = int(sys.argv[1])
iter_resi = int(sys.argv[2]) 
FN = sys.argv[3]

print(iter_loop, "\n")
print(iter_resi, "\n")
print(FN, "\n")
cmd.load("4j4l_round%s.pdb"%(iter_loop - 1))
cmd.select("target", "%s and resi 1-%s"%(FN, iter_resi))
cmd.align("target", "4j4l_round%s"%(iter_loop - 1))
cmd.save("4j4l_round%s_0.pdb"%(iter_loop), FN)

