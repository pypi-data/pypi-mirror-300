 ###########################################################################################################################
#                                       Nomenclature of A1:w:N1 waterbridges                                              #
###########################################################################################################################
# This will work for the 'A1-w-B1_Base.txt' file, i.e. on those water bridges formed by one amino acid and one ribonucleotide.
# However, this code can be modified easily for other higher-order water bridges.
# Importing the required modules.
import math

to_update = {':A': ':rA', ':U': ':rU',':G': ':rG',':C': ':rC',}


# User-defined function to convert PDB record of a water molecule from HBPLUS format (B0026-HOH) 
# to original PDB format (HOH B 26).  
def convert_water_to_pdb(W_id):
    W_id_a = W_id[0]
    W_id_b = W_id[1:5]
    W_id = W_id_a + str(int(W_id_b))
    
    W_id = list(W_id)
    while len(W_id) <5:
        W_id.insert(1, ' ')
    W_id = ''.join(W_id)
    w_pdb = 'O   HOH ' + W_id
    return w_pdb

# User-defined function to convert PDB record of nucleotide to HBPLUS format to original PDB format.  
def convert_nt_to_pdb(idd):
    id_a = idd[0]
    id_b = idd[1:5]
    id_c = idd[8]
    id_atom = idd[10:13]
    chainresi = id_a + str(int(id_b))
    chainresi = list(chainresi)
    while len(chainresi) <5:
        chainresi.insert(1, ' ')
    chainresi.insert(0, ' ' )
    chainresi.insert(0, id_c)
    chainresi.insert(0, id_atom)
    while len(chainresi) <11:
        chainresi.insert(1, ' ')
    nt_pdb = ''.join(chainresi)
    return nt_pdb

# User-defined function to decide interacting edge of nucleotide.
def decision(nt1, nt2, hoh):
    global nt1_xyz, nt2_xyz, hoh_xyz 
    for cords in cord_data:
        if hoh in cords and 'HETATM' in cords: 
            hoh_xyz = [float(cords[31:38].strip()), float(cords[39:46].strip()), float(cords[47:55].strip())]
        if nt1 in cords and 'ATOM' in cords: 
            nt1_xyz = [float(cords[31:38].strip()), float(cords[39:46].strip()), float(cords[47:55].strip())]
        if nt2 in cords and 'ATOM' in cords: 
            nt2_xyz = [float(cords[31:38].strip()), float(cords[39:46].strip()), float(cords[47:55].strip())]
    if (math.dist(hoh_xyz, nt1_xyz)) < (math.dist(hoh_xyz, nt2_xyz)): near_atom = nt1[0:3].strip()
    else: near_atom = nt2[0:3].strip()
    return near_atom

# List of nucleotides and amino acids.
NT = ['-  A', '-  U', '-  G', '-  C']
AA = ['-GLY', '-ALA', '-SER', '-THR', '-CYS', '-VAL', '-LEU', '-ILE', '-MET', '-PRO', '-PHE', '-TYR', '-TRP', '-ASP', '-GLU', '-ASN', '-GLN', '-HIS', '-LYS', '-ARG']

# Combination of atoms to decide interacting portion of amino acid
MC = ['O  ', 'N  ', 'OXT', ['N  ', 'O  '], ['N  ', 'OXT'], ['O  ', 'OXT'], ['N  ', 'O  ', 'OXT']] # Main chain

# Combination of atoms to decide interacting portion of amino acid
WC_edge = [['N1 ', 'N6 '],  ['N1 ', 'N2 '], ['N1 ', 'O6 '],  ['N3 ', 'N4 '], ['N3 ', 'O2 '], ['N3 ', 'O4 ']] # Watson-Crick edge
HG_edge = [['N6 ', 'N7 '],  ['N7 ', 'O6 ']] # Hoogsteen edge
SG_edge = [['N3 ', 'N9 '], ['N3 ', 'O2\''], ['N1 ', 'O2 '], ['N2 ', 'N3 '], ['O2 ', 'O2\''], ['O2\'', 'O3\'']] # Sugar edge


# Read previously generated file containing water bridges.
file = open('A1-w-N1.txt', 'r')
data = file.readlines()
for lines in data:
    AA_info = [] # List of amino acids.
    NT_info = [] # List of nucleotides.
    if 'pdb' in lines: 
        print(lines)
        # Reading PDB files to extract coordinates of atoms.
        cord_file = open(lines.split('.')[0].split(' ')[2] + '.ent')
        cord_data = cord_file.readlines()
        print(lines.strip(), file=open('classified_A1-w-N1_waterbridges.txt', "a"))
    if 'pdb' not in lines and 'HOH' in lines:
        # Determine whether the water bridge is cyclic or acyclic.
        if "NIL" in lines: z5 = ''
        else: z5 = 'cyc-'
        # Extracting amino acids and nucleotides.
        x = lines.split('[')[0]
        for i in range(21, len(x), 23):
            y = lines[i:i+8] 
            y1 = y[:4]
            y2 = y[5:]
            if y1 in NT: 
                z1 = y1[3:].strip()
                NT_info.append(y) 
            else: 
                z3 = y1.split('-')[1].strip()
                AA_info.append(y)
        print(AA_info, NT_info)
        
        # Deciding the interacting edge of nucleotide
        # Case 1: When 2 atoms of a nucleotide are forming hydrogen bonds with water.
        if len(NT_info) ==2:
            nt_atom = []
            for nt in NT_info:
                nt1 = nt[:4]
                nt2 = nt[5:]
                nt_atom.append(nt2)
            nt_atom.sort()
            if nt_atom in WC_edge: z2 = '(WC)'
            if nt_atom in HG_edge: z2 = '(HG)'
            if nt_atom in SG_edge: z2 = '(SG)'
        
        # Case 2: When only 1 atom of nucleotide is forming a hydrogen bond with water.
        if len(NT_info) ==1:
            xx = x.split(' --- ')
            for n in xx:
                print(n)
                
                if 'HOH' in n: 
                    w_pdb =  convert_water_to_pdb(n)
                    print(w_pdb)
                    
                if '-  A' in n:
                    if ' N6 ' in n:
                        new_n_h = n.replace('N6', 'C5')
                        new_n_w = n.replace('N6', 'N1')
                        nt_pdb_h = convert_nt_to_pdb(new_n_h)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_h, nt_pdb_w, w_pdb)
                        if nearest_atom == 'C5': z2 = '(HG)'
                        else: z2 = '(WC)'
                    elif ' N7 ' in n: z2 = '(HG)'
                    elif ' N1 ' in n: z2 = '(WC)'
                    elif ' N3 ' in n: z2 = '(SG)'
                    elif ' N9 ' in n: z2 = '(SG)'
                    elif ' O2\' ' in n: z2 = '(SG)'
                    
                        
                elif '-  G' in n:
                    if ' O6 ' in n:
                        new_n_h = n.replace('O6', 'C5')
                        new_n_w = n.replace('O6', 'N1')
                        nt_pdb_h = convert_nt_to_pdb(new_n_h)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_h, nt_pdb_w, w_pdb) #nt_pdb_h will decide edge
                        if nearest_atom == 'C5': z2 = '(HG)'
                        else: z2 = '(WC)'
                    elif ' N2 ' in n:
                        new_n_s = n.replace('N2', 'N3')
                        new_n_w = n.replace('N2', 'N1')
                        nt_pdb_s = convert_nt_to_pdb(new_n_s)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_s, nt_pdb_w, w_pdb) #nt_pdb_s will decide edge
                        if nearest_atom == 'N3': z2 = '(SG)'
                        else: z2 = '(WC)'
                    elif ' N7 ' in n: z2 = '(HG)'
                    elif ' N1 ' in n: z2 = '(WC)'
                    elif ' N3 ' in n: z2 = '(SG)'
                    elif ' N9 ' in n: z2 = '(SG)'
                    elif ' O2\' ' in n: z2 = '(SG)'
                
                elif '-  U' in n: 
                    if ' O4 ' in n:
                        new_n_h = n.replace('O4', 'C5')
                        new_n_w = n.replace('O4', 'N3')
                        nt_pdb_h = convert_nt_to_pdb(new_n_h)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_h, nt_pdb_w, w_pdb) #nt_pdb_s will decide edge
                        if nearest_atom == 'C5': z2 = '(HG)'
                        else: z2 = '(WC)' 
                    elif ' O2 ' in n:
                        new_n_s = n.replace('O2', 'N1')
                        new_n_w = n.replace('O2', 'N3')
                        nt_pdb_s = convert_nt_to_pdb(new_n_s)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_s, nt_pdb_w, w_pdb) #nt_pdb_s will decide edge
                        if nearest_atom == 'N1': z2 = '(SG)'
                        else: z2 = '(WC)' 
                    elif ' O2\' ' in n: z2 = '(SG)'
                    elif ' N1 ' in n: z2 = '(SG)'
                    elif ' N3 ' in n: z2 = '(WC)'
                        
                
                elif '-  C' in n:
                    if ' O2 ' in n:
                        new_n_s = n.replace('O2', 'N1')
                        new_n_w = n.replace('O2', 'N3')
                        nt_pdb_s = convert_nt_to_pdb(new_n_s)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_s, nt_pdb_w, w_pdb) #nt_pdb_s will decide edge
                        if nearest_atom == 'N1': z2 = '(SG)'
                        else: z2 = '(WC)' 
                
                    elif ' N4 ' in n:
                        new_n_h = n.replace('N4', 'C5')
                        new_n_w = n.replace('N4', 'N3')
                        nt_pdb_h = convert_nt_to_pdb(new_n_h)
                        nt_pdb_w = convert_nt_to_pdb(new_n_w)
                        nearest_atom = decision(nt_pdb_h, nt_pdb_w, w_pdb) #nt_pdb_s will decide edge
                        if nearest_atom == 'C5': z2 = '(HG)'
                        else: z2 = '(WC)' 
                    elif ' O2\' ' in n: z2 = '(SG)'
                    elif ' N1 ' in n: z2 = '(SG)'
                    elif ' N3 ' in n: z2 = '(WC)'
        
        # Deciding interacting portion of amino acid.
        if len(AA_info) == 3:
            at_atom = []
            j = 0
            for at in AA_info:
                at1 = at[:4]
                at2 = at[5:]
                if at2 in MC: j += 1
                at_atom.append(at2)
            if j == 3: z4 = '(m)' 
            if j == 1: z4 = '(ms)'
            if j == 2: z4 = '(ms)'
            if j == 0: z4 = '(s)'

        if len(AA_info) == 2:
            at_atom = []
            j = 0
            for at in AA_info:
                at1 = at[:4]
                at2 = at[5:]
                if at2 in MC: j += 1
                at_atom.append(at2)
            if j == 2: z4 = '(m)' 
            if j == 1: z4 = '(ms)'
            if j == 0: z4 = '(s)'
        if len(AA_info) == 1:
            for at in AA_info:
                at2 = at[5:]
                if at2 in MC: z4 = '(m)'
                else: z4 = '(s)'
        name =  z5 + z3 + z4 + ':w:' + z1 + z2

        for char in to_update.keys():
            name = name.replace(char, to_update[char])
        interaction = lines.strip() + ' —> ' + name
        print(interaction )
        print(interaction.strip(), file=open('classified_A1-w-N1_waterbridges.txt', "a"))
