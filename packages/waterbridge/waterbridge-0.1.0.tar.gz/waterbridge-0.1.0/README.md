***********A python code for detecting water bridges in RNA–protein complexes***********
This code is written in python3. To run this code, go through the following steps:
1.	Place all three codes (‘1_Identification of water bridges.py’, ‘2_Topological classification of water bridges.py’, and ‘3_Nomenclature of A1-w-N1 waterbridges.py’) into a folder along with ‘.hb2’ files obtained from HBPLUS and respective PDB files.
   
2.	Double click ‘1_Identification of water bridges.py’, the code will run automatically and generate three text files:- 
        ‘waterbridges_ALL.txt’ – contains all identified water bridges.
 	    ‘waterbridges_Base.txt’ – contains all identified water bridges involving at least one ribonucleotide utilizing its nucleobase moiety to form hydrogen bonds with water.
        ‘waterbridges_RiboPhos.txt’ – contains all other identified water bridges involving only phosphate moiety or ribose moiety.

3.	For demonstration, we used ‘waterbridges_Base.txt’. Double click on ‘2_Topological classification of water bridges.py’, it will classify water bridges according to their topology and generate many test files, one for each topology (‘A1-w-N1_Base.txt’, ‘A1-w-B2_Base’)
  
4. Now, run ‘3_Nomenclature of A1-w-N1 waterbridges.py’, to assign a name to each base-mediated water bridge present in ‘waterbridges_Base.txt’. This will generate a file ‘classified_A1-w-B1_waterbridges’.

