import pymol
from pymol import cmd, stored
import sys


iter_loop = int(sys.argv[1])
iter_residue = int(sys.argv[2])
rotate_num = int(sys.argv[3])


interval = 25

for num in range(rotate_num + iter_residue + 2, rotate_num + interval) :
    cmd.set_dihedral("%d/c"%(num), "%d/n"%(num+1), "%d/ca"%(num+1), "%d/c"%(num + 1), -160)
    cmd.set_dihedral("%d/n"%(num), "%d/ca"%(num), "%d/c"%(num), "%d/n"%(num + 1), 160)


cmd.load("4j4l_round%s.pdb"%(iter_loop - 1))
cmd.select("target", "4j4l_round%s_%s_1 and resi 1-%s"%(iter_loop, iter_residue, rotate_num))
cmd.align("target", "4j4l_round%s"%(iter_loop - 1))
cmd.save("4j4l_round%s_%s.pdb"%(iter_loop, iter_residue + 1), "4j4l_round%s_%s_1"%(iter_loop, iter_residue))


