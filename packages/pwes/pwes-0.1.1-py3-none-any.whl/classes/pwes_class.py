#%%
import json
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
#display all columns
pd.set_option('display.max_columns', None)

from Bio.PDB import PDBParser
p = PDBParser(QUIET=True)

import shutil


from scipy.spatial.distance import euclidean
import scipy.cluster.hierarchy as sch


from pwes.plotting.plotting import plot_PWES_fn, plot_elbow_fn
from pwes.mapping.map_to_pymol import map_to_pymol


class PWES_for_protein:
    def __init__(self, pdb_name, pdb_path, data_path, output_dir="./figures", output_suffix = '', data_sep = ",", input_df=None):
                # define attributes relating to naming and pdb file
        self.pdb_name = pdb_name
        self.pdb_path = pdb_path      
        
        self.suffix = output_suffix
        
        
        
        
        assert data_path is not None or input_df is not None, "Either data_path or input_df must be provided"
        
        self.data_path = data_path

        if type(input_df) is pd.DataFrame:
            self.df = input_df
        else:
        
            self.data_sep = data_sep
            self.df = self.get_df()
        
        protein_names = self.df["gene"].unique()
        self.protein_name = "_".join(protein_names)
        
        
        # except:
        #     raise Exception("PDB file not found")
        
        if not self.pdb_path[-4:] == ".pdb":
            self.pdb_location = f"{self.pdb_path}/{self.pdb_name}.pdb"
        else:
            self.pdb_location = self.pdb_path
        try:
            print(self.pdb_location)
            self.structure = self.get_structure()
        except:
            raise Exception("PDB file not found")
        
        
        self.output_dir = os.path.join(output_dir, self.protein_name, self.suffix)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.PWES_array, self.dij_array, self.xij_array, self.df, self.linkage_matrix = self.calc_PWES_pwij()
        
        self.dict_of_scores = {}
        
        



    def get_structure(self):
        
        p = PDBParser(QUIET=True)
        structure = p.get_structure(self.protein_name, self.pdb_location)
        # copy structure to f"figures/{self.protein_name}/{self.treatment}/{self.pdb_name}/"
        #shutil.copy(f"{self.pdb_path}/{self.pdb_name}.pdb", f"figures/{self.protein_name1}_{self.protein_name2}/{self.treatment}/{self.pdb_name}/")
        return structure


    def get_df(self):
        df = pd.read_csv(self.data_path, sep=self.data_sep)
        return df


    def calc_PWES_pwij(self):
        
        df = self.df.copy()
        
        #get unique "chain" values
        chains = df["chain"].unique()
        
        collection_df = []
        
        chain_dict = {}
        
        for chain in chains:
            
            
            df_chain = df[df["chain"] == chain]
            df_chain = df_chain[df_chain["resnum"].str.len() >0]
            gene = df_chain["gene"].unique()[0]
            chain_dict[gene] = chain
            # get residues in pdb
            residues_in_pdb = self.structure[0][chain].get_residues()
            
            resnum_in_pdb = [res.get_id()[1] for res in residues_in_pdb if res.get_id()[0] == " "]
            
            df_chain["resnum"] = df_chain["resnum"].str.split(";")
            
            df_chain = df_chain[df_chain["resnum"].apply(lambda x: len(x) > 0)]
            
            # remove rows if any res_num is not in the pdb
            
            df_chain = df_chain[df_chain["resnum"].apply(lambda x: all([int(res_num) in resnum_in_pdb for res_num in x]))]
            
            # add to collection_df
            collection_df.append(df_chain)
            print(df_chain.shape)
            
        df = pd.concat(collection_df, ignore_index=True)
        print(df.shape)
        
        df = df.reset_index(drop=True)
        df["guide_idx"] = df.index
        
        num_rows = df.shape[0]
        #print(num_rows)
        xij_array = np.zeros((num_rows, num_rows))
        dij_array = np.zeros((num_rows, num_rows))
        PWES_array = np.zeros((num_rows, num_rows))
        for i, rowi in df.iterrows():
            guidei_atoms_coordinates = []
            gene1 = rowi["gene"]
            for res_num in set(rowi["resnum"]):
                    res = self.structure[0][chain_dict[gene1]][int(res_num)]
                    for atom in res:
                        guidei_atoms_coordinates.append(atom.get_coord())
            
            # turn into numpy array
            guidei_atoms_coordinates = np.array(guidei_atoms_coordinates)
            #calculate centroid
            c1 = np.mean(guidei_atoms_coordinates, axis=0)
            c1 = c1.flatten()
            for j, rowj in df.iterrows():
                gene2 = rowj["gene"]
                if i == j:
                    continue
                
                guidej_atoms_coordinates = []
                for res_num in set(rowj["resnum"]):
                    res = self.structure[0][chain_dict[gene2]][int(res_num)]
                    for atom in res:
                        guidej_atoms_coordinates.append(atom.get_coord())
        
                # turn into numpy array
                guidej_atoms_coordinates = np.array(guidej_atoms_coordinates)
                #calculate centroid
                c2 = np.mean(guidej_atoms_coordinates, axis=0)
                # make 1d
                c2 = c2.flatten()
                
                # calculate the euclidean distance between the centroids
                try:
                    dij_array[i,j] = euclidean(c1, c2)
                except:
                    print(rowi["resnum"], rowj["resnum"], c1.shape, c2.shape, i, j, c1, c2)
                    break
                # calculate the xij
                xij_array[i,j] = rowi["log_fold_change"] + rowj["log_fold_change"]

        #calculate mean and std of xij
        xij_mean = np.mean(xij_array)
        xij_std = np.std(xij_array)
    
        t = 16
        #calculate pwij
        for i in range(num_rows):
            for j in range(num_rows):
                pwij = np.tanh((xij_array[i,j] - xij_mean)/xij_std)*np.exp(-((dij_array[i,j]**2)/(2*t**2)))
                PWES_array[i, j] = pwij
        np.fill_diagonal(PWES_array, 0)
        
        print(dij_array.shape, xij_array.shape, PWES_array.shape, df.shape)

        linkage_matrix = sch.linkage(PWES_array, method="ward", metric="euclidean")
        
        return PWES_array, dij_array, xij_array, df, linkage_matrix



    def plot_PWES(self, threshold, n_simulations=5000):
        
        try:
            dict_of_clusters, wcss, pvalues = plot_PWES_fn(self.df, self.PWES_array, self.protein_name, self.linkage_matrix, self.dict_of_scores, self.output_dir, self.suffix, threshold, n_simulations)
        except TypeError:
            return None
        self.dict_of_scores[len(dict_of_clusters)] = {"clusters": dict_of_clusters, "wcss": wcss, "pvalues": pvalues}
        
        map_to_pymol(self.pdb_location, dict_of_clusters, len(dict_of_clusters), self.output_dir, self.protein_name)
        
        return None

    
    
    def plot_elbow(self):
        plot_elbow_fn(self.dict_of_scores, self.output_dir, self.protein_name, self.suffix)
    


    def perform_for_all_thresholds(self, n_simulations=5000):
        
        if os.path.exists(f"figures/{self.protein_name}/{self.suffix}/{self.pdb_name}/WCSS_vs_Clusters.pdf"):
            print(f"Already performed for {self.protein_name} {self.suffix} {self.pdb_name}")
            return None
        
        thresholds = list(np.linspace(4, 30, 3))
        for threshold in thresholds:
            
            self.plot_PWES(threshold, n_simulations)
            
        
        with open(f"{self.output_dir}/scores.json", "w") as f:
            json.dump(self.dict_of_scores, f)
        
        
        ##### plotting 
        
        self.plot_elbow(self.dict_of_scores, self.output_dir, self.protein_name, self.suffix)
        
        return None


# %%
