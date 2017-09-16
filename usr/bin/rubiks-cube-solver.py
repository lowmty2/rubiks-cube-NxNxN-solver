#!/usr/bin/env python2

"""
Solve any size rubiks cube:
- For 2x2x2 and 3x3x3 just solve it
- For 4x4x4 and larger, reduce to 3x3x3 and then solve

This is a work in progress
"""

from rubikscubennnsolver import ImplementThis, SolveError, StuckInALoop
from rubikscubennnsolver.LookupTable import NoSteps
from rubikscubennnsolver.RubiksCube222 import RubiksCube222
from rubikscubennnsolver.RubiksCube333 import RubiksCube333
from rubikscubennnsolver.RubiksCube444 import RubiksCube444
from rubikscubennnsolver.RubiksCube555 import RubiksCube555
from rubikscubennnsolver.RubiksCube666 import RubiksCube666
from rubikscubennnsolver.RubiksCube777 import RubiksCube777
from rubikscubennnsolver.RubiksCubeNNN import RubiksCubeNNNEven, RubiksCubeNNNOdd
from rubikscubennnsolver.rotate_xxx import rotate_444
from math import sqrt
from time import sleep
import argparse
import logging
import os
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)16s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING))

parser = argparse.ArgumentParser()
parser.add_argument('--print-steps', default=False, action='store_true')
parser.add_argument('--debug', default=False, action='store_true')
parser.add_argument('--test', default=False, action='store_true')
parser.add_argument('--best', default=False, action='store_true')
parser.add_argument('--tsai', default=False, action='store_true', help='Use the tsai solver, 4x4x4 only')
parser.add_argument('--ev3', default=False, action='store_true', help='EV3 is only 300Mhz...use some CPU saving tricks')
parser.add_argument('--colormap', default=None, type=str, help='Colors for sides U, L, etc')
parser.add_argument('--order', type=str, default='URFDLB', help='order of sides in --state, default kociemba URFDLB')
parser.add_argument('--state', type=str, help='Cube state',

# 2x2x2
#    default='DLRRFULLDUBFDURDBFBRBLFU')
#    default='UUUURRRRFFFFDDDDLLLLBBBB')

# 3x3x3
#    default='RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU')
#    default='UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB') # solved

# 4x4x4
#    default='FUULURFFRLRBDDDULUDFLFBBFUURRRUBLBLBDLUBDBULDDRDFLFBBRDBFDBLRBLDULUFFRLRDLDBBRLRUFFRUBFDUDFRLFRU')
    default='DRFDFRUFDURDDLLUFLDLLBLULFBUUFRBLBFLLUDDUFRBURBBRBDLLDURFFBBRUFUFDRFURBUDLDBDUFFBUDRRLDRBLFBRRLB') # xyzzy test cube
#    default='RRRRRRRLRRRLRRRFLBBFBBBBBBBBRBBBUUUUUDDDUDDDDDDULLLFLLLRLLLRLFFLBFFBLFFFLFFFBFFFDDDDUUUUUUUUUDDD')
#    default='DUFFRDLRDLBUDLBULLBLFFUBURFFURFURDUBUDLLFDLRFDLRRRDBBBDDUFULLBFFBBBBLBBRFFUDFFUDDDLLDRRBRRUURRLU') # edges take 27 steps (used to take 46 steps)
#    default='LFBDUFLDBUBBFDFBLDLFRDFRRURFDFDLULUDLBLUUDRDUDUBBFFRBDFRRRRRRRLFBLLRDLDFBUBLFBLRLURUUBLBDUFUUFBD')
#    default='DFBRULBFFUDFDRULURDUUFLLRFLFDLRRFBRFUDUFLRBDBDULRBLBBBFDUFUBUFBDLLLRURDBDBDDBBLUFDRFFULRURRRBLDL') # takes a lot of moves
#    default='UUUUUUUUUUUUUUUURRRRRRRRRRRRRRRRFFFFFFFFFFFFFFFFDDDDDDDDDDDDDDDDLLLLLLLLLLLLLLLLBBBBBBBBBBBBBBBB') # solved

# 5x5x5
#    default='RFFFUDUDURBFULULFDBLRLDUFDBLUBBBDDURLRDRFRUDDBFUFLFURRLDFRRRUBFUUDUFLLBLBBULDDRRUFUUUBUDFFDRFLRBBLRFDLLUUBBRFRFRLLBFRLBRRFRBDLLDDFBLRDLFBBBLBLBDUUFDDD')
#    https://www.speedsolving.com/forum/threads/arnauds-5x5x5-edge-pairing-method-examples.1447/
#    default='LDFRDDUUUUFUUUBLUUUFLDFDRFDDFBBRRRULRRRBFRRRURFRFDUBDRUBFFFUBFFFUUFFFRLDLRFDLBDDLDDDRDDDDUDDDDUULDLFBFLFFULLLRFLLLRLLLLRRBLBBRBULULBBBRUBBBRBBBBULBRFB')
#    default='UDLFDLDDLUFDUBRLBDLFLRBFRBLBBFUDURDULRRBRLFUURBUFLUBDUDRURRRBUFUFFFRUFFLDUURURFFULFFRLFDBRRFRDDBRFBBLBRDFBBBBUDDLLLDBUULUDULDLDDLBRRLRLUBBFFBDLFBDDLFR')
#    default='UUUUUUUUUUUUUUUUUUUUUUUUURRRRRRRRRRRRRRRRRRRRRRRRRFFFFFFFFFFFFFFFFFFFFFFFFFDDDDDDDDDDDDDDDDDDDDDDDDDLLLLLLLLLLLLLLLLLLLLLLLLLBBBBBBBBBBBBBBBBBBBBBBBBB') # solved
#    default='DFFURRULDLDLURLBDDRRBFRURFBFBFRBDLBBFRBLRFBRBBFLULDLBLULLFRUBUFLDFFLDULDDLUURRDRFBRLULUDRBDUUUBBRFFDBDFURDBBDDRULBUDRDLLLBDRFDLRDLLFDBBUFBRURFFUFFUUFU') # step10 takes 9s
#    default='URUBFUUFRDFFUUFLRDBLLBDDDLUULRDLDUBDLRBBLFLBRBFUUBBRBFFUDLFLLBFUFUDRLBFUBBURRLLRUFRDUFFDFRFUBRBBDRFRFLLFURLLFBRBLUDRDDRRDRRFDUDLFLDLUUDUDBRBBBRBDDLDFL') # step10 takes 45s, step30 takes 14s
#    default='RFUBLFUBRULLUDDRLRLLFFFLUBDBLBFFUFLFURBFFLDDLFFBBRLUUDRRDLLLRDFFLBBLFURUBULBRLBDRUURDRRDFURDBUUBBFBUDRUBURBRBDLFLBDFBDULLDBBDDDRRFURLDUDUBRDFRFFDFDRLU') # step10 takes 50s

# 6x6x6
#    default='FBDDDFFUDRFBBLFLLURLDLLUFBLRFDUFLBLLFBFLRRBBFDRRDUBUFRBUBRDLUBFDRLBBRLRUFLBRBDUDFFFDBLUDBBLRDFUUDLBBBRRDRUDLBLDFRUDLLFFUUBFBUUFDLRUDUDBRRBBUFFDRRRDBULRRURULFDBRRULDDRUUULBLLFDFRRFDURFFLDUUBRUFDRFUBLDFULFBFDDUDLBLLRBL')
#    default='UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB') # solved
#    defult='xxxxxxxDRRLxxLDDBxxLUUDxxFRDUxxxxxxxxxxxxxxBBLBxxURFUxxDRBDxxDFDLxxxxxxxxxxxxxxULLRxxUFLLxxBLFRxxBBRDxxxxxxxxxxxxxxLFBRxxBUUFxxFDDFxxURUFxxxxxxxxxxxxxxRFDLxxURFUxxUBBFxxRULDxxxxxxxxxxxxxxBBLFxxFLLRxxDRBBxxFDRUxxxxxxx') # good step20 IDA test

# 7x7x7
#    default='DBDBDDFBDDLUBDLFRFRBRLLDUFFDUFRBRDFDRUFDFDRDBDBULDBDBDBUFBUFFFULLFLDURRBBRRBRLFUUUDUURBRDUUURFFFLRFLRLDLBUFRLDLDFLLFBDFUFRFFUUUFURDRFULBRFURRBUDDRBDLLRLDLLDLUURFRFBUBURBRUDBDDLRBULBULUBDBBUDRBLFFBLRBURRUFULBRLFDUFDDBULBRLBUFULUDDLLDFRDRDBBFBUBBFLFFRRUFFRLRRDRULLLFRLFULBLLBBBLDFDBRBFDULLULRFDBR')

# 10x10x10
#    default='ULBDLDBUFRBBBBBLBFFFDFRFBBDDFDFRFFLDLDLURRBUDRRBFLUDFRLBDURULRUUDBBBUBRURRRLDLRFFUFFFURRFBLLRRFLFUDBDRRDFULLLURFBFUUBDBBDBFLFDFUUFDUBRLUFDBLRFLUDUFBFDULDFRUBLBBBUBRRDBDDDDFURFLRDBRRLLRFUFLRDFDUULRRDULFDUDRFLBFRLDUDBDFLDBDUFULULLLBUUFDFFDBBBRBRLFLUFLFUFFRLLLFLBUDRRFDDUDLFLBRDULFLBLLULFLDLUULBUDRDFLUDDLLRBLUBBRFRRLDRDUUFLDDFUFLBDBBLBURBBRRRFUBLBRBRUBFFDBBBBLBUFBLURBLDRFLFBUDDFFRFFRLBDBDUURBUFBDFFFLFBDLDUFFBRDLBRLRLBFRUUUULRRBDBRRFDLLRRUUBDBDBFDLRDDBRUUUUUBLLURBDFUFLLRDBLRRBBLBDDBBFUDUDLDLUFDDDUURBFUFRRBLLURDDRURRURLBLDRFRUFBDRULUFFDUDLBBUURFDUDBLRRUDFRLLDULFUBFDLURFBFULFLRRRRRFDDDLFDDRUFRRLBLUBU')

# 14x14x14
#    default='FBDRLBLRRURRLDRBDLBURDFDDDRBLBBFBRDLLFDUBLFRLDFUUBFRDBFBBBULFRLBUFLBDDDLLDRBFLLBBLFBFFDFBFDDFRRRBDRRBRBDUFDRLRUDLDFDDURFLBUBBUUDLBRRDUDRDBBBLDBRBBBUFLBLRUURBDDLDRLUFFBLFRLDFBRFLDLBULFFBRLDBDDFLLRFLUBFDFBRLRLFDBLBURLBLFRFBLLDULUDURLBUUULLRRLUBDDLURLLRFURFRFRBDDUBLDFBLUDRLRDRRBLFUFRDUFFRULBLRBBRUFDBUBBBBLDBRBLDDRRFDDBFFUUBRBLFUBBRFUURBFDRLURLRBFUUFUBRUDRBDFBBFURFLFFDRDFUFFULFLUBDFUFFDLRRFRUDUDLBBBDLLLDUFUDRFDBLRRFFLRUFDRFURDLRRDRDLFBRLRLULRFBDLFDRLFRDDFLLDBFBUBBRLLDLFURFRFULUBLUBFLFFBFDFBDUUBURUUUBFUBDLLFLUUUFDUDLUUULDLLUDDBUFRDRULRLLULRULFBLUDFURFLFUBDLLFLFUBUUBBUFLUDUBRDBLFFUUUFDRLRULUDDRLRBLRUUFBRRRRULBDLFBFLDLRDFUBLUBRDDFUULFLDLUBFURRURUBDFFFDLRFFLBRFRDRUDUULURULLDFRBUDRDLFUFULDBLUBFRFBURDLLUUFDURLRDBLFFRFDBFURLFUBLUUUFFRULUBURRURFDDBFUFRBURBBDRFUDDFDLRUURFBBDBDRLUBRRBFDFRDFDLRDUFFUBRRBDBBLDLFDUDDRLFRRRBUUUBRFUFBUFFBRRDRDDBBDRUULDRFRFBUFLFFBLRBFLLLRUDFDRUDLDRLFRLUFLUBRDUFDDLLUDDRBUBBBDRDBBFRBDDRRLRRUUBBUDUDBLDBDFLFRFUBFLFDBBLRLULDBRFBRRLUUURDFFFDBLDUDBRFDDFFUBLUUURBBULFUFUDFBRDLLFURBULULBUDLUFFBDRBRRDBUUULFDURRDFDDLUDBDRBFBUFLULURUFDRFRFBBFBBBDRLBLUDLDRDLLDRRLLDLFBRBRLDUFBDDUDBLDFRFBBBDRDRDDLDRULFFLLFLBLDFLURLBUDFBDLRBLFDFLUDDFUBUBLURBBBLFRLFLBDDBURFFBFRRL')

# 15x15x15
#    default='RLURLURBDDULFUUURFLRBLURUBFDBULFLUBBFLDUFBDRFRBRUDFULFRUFLUDFRLFDFLLFDBULURRLBFBUURDULFDFBLRRRLFULLFFFDUULRRRUUUUFDBLDDFFLRDLLUURUBBULUFFURBRRLBBUUBBFDRRBRBRLUDLUDRBFBFULLRRBBFBFRDDDLDDDFRFUFLURUFLBDLUBRLDFRRDBDBFLFUDFLDFFURLFULLDDRURRDLRFLDFLULUUDDRFDRBLRBRBFUFDBDUUDBRRBDFBLBLRBBLBFLLDUBFFFFBDDRLBBBRFDFFUBBDURFLUUDDDRDDLDBRLBULLFLFBRBRBLUDDLRDRDUDFLFRUFLDLBLURDDDRUFDLBRDRLFBDBLDRFBFFBURULUDRRBRDFRFFLULLUBRDRRRDUFRBLFULUBBUFFBRBBFRLFDRRDBLDFRDRDDRLRUULBDURDURFDDLFDUUDBFLBDUFBULFRRDUDUBFBUDBBFUDFUUDLUDDRFDDDFRRRBUDRBFBBULLUFBLRLFLLBRRRRUBDRFLFDFDBLRFLURULULFFBUUUUFDBBLDLUBBRUBBBRBFLULLBLUUULLUBFFDULDFFBFFFUFFDUDRFBUFLDDLURFLRFLRFBUUBLRFDDRULUUUFFRDDBLRDULFURUDDBDLBBUUBFURFRFBRLBUULBLDDDBUBRFFULLUDFFDLDFUBLLBLDFFDDLBDUFUFFLBBBUBULDDFBRRFFLDUDDFRBLRRDDUDLBDBLURBUDBRRLUBBDRFBUFRDRDRBBDULBUFFDRBBDFBUULFFRLLDURRRDFFUUFULDULURLDLUUUDLBBUDLDRFBDBBDLUFBRRFDFLLDLFDBRBBRFUDDDBURDRBUBRUBDUBLDLLDLURLDFDBRUBDLDFRRRBRLULFRFLDRLBUBRUBLFBFDFFLFRFDFLBRULLRBLDRBBFURRRDUUULLULLDLBLBBDFBUUUBRRUFFBRUDBFRDFDLFLFFRFFFFRULDFFDFRUBBBRURBUFLBDFBBBBBRRRLFLFBDRRUFLURDDLRRBRLLFURRURBRFLLLFFURBFULFRFFBLDUUUUBDDUFFDRBRLDDFRBULDDDFFRURUFLDRFLDFBLRUFFUBBDFFDBLLDBDUBDLDLUDFBFLRULRRBDBLRBLDLUURRLLRULDBLBLLRRFDDRBBRBUBDDULDRFBFBBFLUFBLUULDDFDBRLLUBUBBDFBBLBBUBLULDRUDBLRULDUDLUFRRDLLUDDBUFLFLBUFUURFDRDLBURLLRRRULRBFFRRBRFBUBRBUUFRLRDRDLBBRFLLLDDBRFUFRBULFLFDRDDRRDBF')

args = parser.parse_args()

if args.debug:
    log.setLevel(logging.DEBUG)

if args.test:
    cube = RubiksCube444(solved_4x4x4, args.colormap, avoid_pll=True, use_tsai=args.tsai)
    cube.test()
    sys.exit(0)

try:
    size = int(sqrt((len(args.state) / 6)))

    if size == 2:
        cube = RubiksCube222(args.state, args.order, args.colormap, args.debug)
    elif size == 3:
        cube = RubiksCube333(args.state, args.order, args.colormap, args.debug)
    elif size == 4:
        cube = RubiksCube444(args.state, args.order, args.colormap, avoid_pll=True, debug=args.debug, use_tsai=args.tsai)
    elif size == 5:
        cube = RubiksCube555(args.state, args.order, args.colormap, args.debug)
    elif size == 6:
        cube = RubiksCube666(args.state, args.order, args.colormap, args.debug)
    elif size == 7:
        cube = RubiksCube777(args.state, args.order, args.colormap, args.debug)
    elif size % 2 == 0:
        cube = RubiksCubeNNNEven(args.state, args.order, args.colormap, args.debug)
    else:
        cube = RubiksCubeNNNOdd(args.state, args.order, args.colormap, args.debug)

    cube.ev3 = args.ev3
    cube.best = args.best

    # Uncomment to produce a cube from alg.cubing.net
    # https://alg.cubing.net/?alg=R_Rw-_D_Uw_R2_Fw2_Uw2_F2_Uw_Fw_%2F%2F_stage_centres%0AU_L_Fw2_D2_L_Fw2_U_Rw2_U-_%2F%2F_3_dedges_%26%232b%3B_partial_centres%0AB_D-_B-_Uw2_L_U-_F_R_Fw2_%2F%2F_6_dedges_%26%232b%3B_centres%0ARw2_U_R-_U-_D-_L2_D_Rw2_%2F%2F_9_dedges%0AFw2_D-_F-_D_Fw2_%2F%2F_12_dedges%0AL2_U-_D_R2_L-_B2_D-_F_%2F%2F_Kociemba_phase_1%0AR2_F2_U2_R2_L2_F2_U-_R2_U-_L2_U2_R2_B2_%2F%2F_Kociemba_phase_2&puzzle=4x4x4&setup=(R1_Rw3_D1_Uw1_R2_Fw2_Uw2_F2_Uw1_Fw1_U1_L1_Fw2_D2_L1_Fw2_U1_Rw2_U3_B1_D3_B3_Uw2_L1_U3_F1_R1_Fw2_Rw2_U1_R3_U3_D3_L2_D1_Rw2_Fw2_D3_F3_D1_Fw2_L2_U3_D1_R2_L3_B2_D3_F1_R2_F2_U2_R2_L2_F2_U3_R2_U3_L2_U2_R2_B2_x-_z-)-&view=playback
    '''
    for step in "R1 Rw3 D1 Uw1 R2 Fw2 Uw2 F2 Uw1 Fw1 U1 L1 Fw2 D2 L1 Fw2 U1 Rw2 U3 B1 D3 B3 Uw2 L1 U3 F1 R1 Fw2 Rw2 U1 R3 U3 D3 L2 D1 Rw2 Fw2 D3 F3 D1 Fw2 L2 U3 D1 R2 L3 B2 D3 F1 R2 F2 U2 R2 L2 F2 U3 R2 U3 L2 U2 R2 B2".split():
        cube.rotate(step)

    kociemba_string = cube.get_kociemba_string(True)
    print(kociemba_string)
    cube.print_cube()
    sys.exit(0)
    '''

    #print(args.colormap)
    #print(args.state)
    #sys.exit(0)

    cube.print_cube()
    cube.www_header()
    cube.www_write_cube("Initial Cube")

    cube.solve()
    print("Final Cube")
    cube.print_cube()
    cube.print_solution()

    print("\n**********************************************************")
    print("See /tmp/solution.html for more detailed solve instruction")
    print("**********************************************************\n")

    # Now put the cube back in its initial state and verify the solution solves it
    solution = cube.solution

    if size == 2:
        cube = RubiksCube222(args.state, args.order, args.colormap)
    elif size == 3:
        cube = RubiksCube333(args.state, args.order, args.colormap)
    elif size == 4:
        cube = RubiksCube444(args.state, args.order, args.colormap, avoid_pll=True, use_tsai=args.tsai)
    elif size == 5:
        cube = RubiksCube555(args.state, args.order, args.colormap)
    elif size == 6:
        cube = RubiksCube666(args.state, args.order, args.colormap)
    elif size == 7:
        cube = RubiksCube777(args.state, args.order, args.colormap)
    elif size % 2 == 0:
        cube = RubiksCubeNNNEven(args.state, args.order, args.colormap, args.debug)
    else:
        cube = RubiksCubeNNNOdd(args.state, args.order, args.colormap, args.debug)

    len_steps = len(solution)

    for (i, step) in enumerate(solution):

        if args.print_steps:
            print("Phase     : %s" % cube.phase())
            print("Move %d/%d: %s" % (i+1, len_steps, step))

        cube.rotate(step)

        www_desc = "Phase: %s<br>\nCube After Move %d/%d: %s<br>\n" % (cube.phase(), i+1, len_steps, step)
        cube.www_write_cube(www_desc)

        if args.print_steps:
            cube.print_cube()
            print("\n\n\n\n")
            sleep(1)
            os.system('clear')

    cube.www_footer()

    if args.print_steps:
        cube.print_cube()

    if not cube.solved():
        kociemba_string = cube.get_kociemba_string(False)
        edge_swap_count = cube.get_edge_swap_count(edges_paired=True, orbit=None, debug=True)
        corner_swap_count = cube.get_corner_swap_count(debug=True)

        raise SolveError("cube should be solved but is not, edge parity %d, corner parity %d, kociemba %s" %
            (edge_swap_count, corner_swap_count, kociemba_string))

except (ImplementThis, SolveError, StuckInALoop, NoSteps, KeyError):
    cube.print_cube_layout()
    cube.print_cube()
    cube.print_solution()
    print(cube.get_kociemba_string(True))
    raise
