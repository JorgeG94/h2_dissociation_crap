import os
import numpy as np

# Bond distances
distances = np.arange(0.55, 6.01, 0.1)

# Templates
template_fci = """!   File created by MacMolPlt 7.7.3
 $CONTRL SCFTYP=mcscf RUNTYP=ENERGY MAXIT=200 MULT=1 $END
 $contrl ispher=1 $end
 $contrl cityp=aldet $end
 $SYSTEM mwords=1000 $END
 $BASIS GBASIS=ccq $END
 $det  ncore=0 nact=2 nels=2 nstate=2 $end
 $cidet  ncore=0 nact=2 nels=2 nstate=2 $end
 $SCF DIRSCF=.TRUE. $END
 $DATA
Title
C1
H 1.0 0.0 0.0 0.0
H 1.0 {x:.2f} 0.0 0.0
 $END
"""

template_cc = """!   File created by MacMolPlt 7.7.3
 $CONTRL SCFTYP=rhf RUNTYP=ENERGY MAXIT=200 MULT=1 $END
 $contrl ispher=1 $end
 $contrl cctyp=ccsd(t) $end
 $SYSTEM mwords=1000 $END
 $BASIS GBASIS=ccq $END
 $SCF DIRSCF=.TRUE. $END
 $DATA
Title
C1
H 1.0 0.0 0.0 0.0
H 1.0 {x:.2f} 0.0 0.0
 $END
"""

template_dft = """!   File created by MacMolPlt 7.7.3
 $CONTRL SCFTYP=rhf RUNTYP=ENERGY MAXIT=200 MULT=1 $END
 $contrl ispher=1 $end
 $contrl dfttyp=uselibxc $end
 $libxc functional={functional} $end
 $dft dc=.true. idcver=3 $end
 $SYSTEM mwords=1000 $END
 $BASIS GBASIS=ccq $END
 $SCF DIRSCF=.TRUE. $END
 $DATA
Title
C1
H 1.0 0.0 0.0 0.0
H 1.0 {x:.2f} 0.0 0.0
 $END
"""

# DFT functionals
dft_functionals = ["B3LYPV5", "PBE0", "M06-2X", "PBE0-DH", "SCAN0-DH", "TPSS0-DH", "B2-PLYP"]

# Create FCI inputs
fci_dir = "fcih2_inputs"
os.makedirs(fci_dir, exist_ok=True)
for r in distances:
    with open(os.path.join(fci_dir, f"h2_r_{r:.2f}.inp"), "w") as f:
        f.write(template_fci.format(x=r))

# Create CCSD(T) inputs
cc_dir = "ccsdt_inputs"
os.makedirs(cc_dir, exist_ok=True)
for r in distances:
    with open(os.path.join(cc_dir, f"h2_r_{r:.2f}.inp"), "w") as f:
        f.write(template_cc.format(x=r))

# Create DFT inputs for each functional
for func in dft_functionals:
    dft_dir = f"dft_{func.lower().replace('-', '_')}_inputs"
    os.makedirs(dft_dir, exist_ok=True)
    for r in distances:
        with open(os.path.join(dft_dir, f"h2_r_{r:.2f}.inp"), "w") as f:
            f.write(template_dft.format(x=r, functional=func))

print("All input files generated!")

