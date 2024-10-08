import pymol2
import os


def map_to_pymol(pdb_location, dict_of_clusters, n_clusters, output_dir, protein_name):
    
    with pymol2.PyMOL() as pymol:
        pymol.cmd.load(pdb_location)
        
        for cluster in dict_of_clusters:
            
                # Select residues from the specified chain
                chains = list(dict_of_clusters[cluster].keys())
                
                n_clusters = len(dict_of_clusters)
                
                for chain in chains:
                    if len(dict_of_clusters[cluster][chain]) == 0:
                        continue
                    else:
                        pymol.cmd.select(f"cluster_{cluster}_{chain}", f"resi {'+'.join(dict_of_clusters[cluster][chain].split('+'))} and chain {chain}")
                        pymol.cmd.color("red", f"cluster_{cluster}_{chain}")
                
                
            

        
        # Save the PyMOL session
        pymol.cmd.save(os.path.join(output_dir,f"{n_clusters}", f"{protein_name}_clusters_{n_clusters}.pse"))
    
    