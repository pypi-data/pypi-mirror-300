import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import scipy.cluster.hierarchy as sch



def plot_PWES_fn(tiling_df, PWES_array, protein_name, linkage_matrix, dict_of_scores, output_directory, suffix, threshold, n_simulations):
    

    """
    this method plots the clustermap and boxplot for the PWES method and saves the figures in the output directory
    input:
    tiling_df: pandas DataFrame
    PWES_array: numpy array
    protein_name: str
    linkage_matrix: numpy array
    dict_of_scores: dict
    output_directory: str
    suffix: str
    threshold: float
    
    output:
    dict_of_clusters: dict
    wcss: list
    
    
    """

    
    clusters = sch.fcluster(linkage_matrix, t=threshold, criterion='distance')
    n_clusters = len(np.unique(clusters))
    
    #check if n_clusters is in dict_of_scores
    if n_clusters in dict_of_scores or n_clusters > 35:
        return None
    
    
    # create the directory if it does not exist
    output_directory = os.path.join(output_directory, str(n_clusters))
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    
    
    tiling_df['cluster'] = clusters

    chain_ids = tiling_df["chain"].unique()
    
    dict_of_clusters = {}
    for i, _ in enumerate(tiling_df["cluster"].unique()):
        cluster_df = tiling_df[tiling_df["cluster"] == i+1]
        
        cluster_dict = {}
        for chain in chain_ids:
            cluster_dict[chain] = []
            for resnum in cluster_df[cluster_df["chain"] == chain]["resnum"]:
                cluster_dict[chain].extend(resnum)
            cluster_dict[chain] = "+".join(map(str, set(cluster_dict[chain])))
        dict_of_clusters[f"{i+1}"]= cluster_dict
        
    
    with open(os.path.join(output_directory,"clusters.json"), "w") as outfile:
        json.dump(dict_of_clusters, outfile)
        
        
        
        
    # plot Dendrogram with threshold
    
    # Plot the dendrogram
    plt.figure(figsize=(10, 5))
    dendrogram = sch.dendrogram(linkage_matrix, color_threshold=threshold)
    # plot the threshold
    plt.axhline(y=threshold, color='r', linestyle='--')
    plt.savefig(os.path.join(output_directory,f"{protein_name}_dendrogram_{n_clusters}.pdf"))
    plt.close()
    
    
    
    wcss = []
    for i in np.unique(clusters):
        wcss.append(np.sum((PWES_array[clusters == i] - np.mean(PWES_array[clusters == i]))**2))
    wcss = np.sum(wcss)
    
    
    
    # Convert cluster assignments to valid RGBA colors
    # You can use a colormap to map cluster numbers to colors

    cmap = sns.color_palette("Set1", n_colors=len(np.unique(clusters)))
    cluster_colors = sns.color_palette(cmap, len(np.unique(clusters)))
    colors = [cluster_colors[i - 1] for i in clusters]


    clusters_sorted = np.argsort(clusters)
    clusters_sorted = clusters[clusters_sorted]
    #index for changes in clusters
    cluster_changes = np.where(clusters_sorted[:-1] != clusters_sorted[1:])[0]
    # add 1 to the index to get the correct position
    cluster_changes = cluster_changes + 1
    # Visualize the clusters using a clustermap
    g= sns.clustermap(PWES_array,
                    method="ward",
                    metric="euclidean",
                    cmap="coolwarm",
                    #cbar_pos=(0.05, 0.85, 0.05, 0.18),
                    vmin=-1, vmax=1,
                    cbar_kws={"ticks": [-1, 0, 1]},
                    row_linkage=linkage_matrix,
                    col_linkage=linkage_matrix,
                    row_colors=colors,
                    col_colors=colors,
                    #dendrogram_ratio=(0.25,0)
                    )

    #Remove x and y ticks and corresponding text
    g.ax_heatmap.set_xticks([])
    g.ax_heatmap.set_yticks([])
    g.ax_heatmap.set_xticklabels([])
    g.ax_heatmap.set_yticklabels([])
    # set x and y labels
    g.ax_heatmap.set_xlabel(f"{len(tiling_df)} Guides")

    plt.title(f"Gene: {protein_name}\nNumber of Clusters: {n_clusters}\n Distance Threshold: {threshold}")

    

    # Add horizontal lines to the clustermap to indicate cluster changes
    for i in cluster_changes:
        g.ax_heatmap.axhline(y=i, color='k', linestyle='-', linewidth=0.5)
        g.ax_heatmap.axvline(x=i, color='k', linestyle='-', linewidth=0.5)

    # save the figure
    #plt.tight_layout()
    # save figure as svg
    # add white space around the figure
    plt.savefig(os.path.join(output_directory,f"{protein_name}_clustermap_{n_clusters}.pdf"), bbox_inches="tight")
    
    plt.close()


    cluster_count = tiling_df['cluster'].value_counts()
    
    #output the cluster count to a csv file
    cluster_count.to_csv(os.path.join(output_directory,f"{protein_name}_cluster_count_{n_clusters}.csv"))
    
    tiling_df['cluster_count'] = tiling_df['cluster'].map(cluster_count)
    
    
    # Create a color palette based on the number of unique clusters
    palette = sns.color_palette("viridis", n_colors=cluster_count.nunique())

    # Plot the boxplot with the specified color palette
    ax = sns.violinplot(x="cluster", y="log_fold_change", hue="cluster_count", data=tiling_df, palette=palette, legend=False, linewidth=1)
    
    
    
    # if more than 20 clusters, only show every other x-tick
    
    if n_clusters > 20:
        for ind, label in enumerate(ax.get_xticklabels()):
            if ind % 2 == 0:
                label.set_visible(True)
            else:
                label.set_visible(False)
    else:
        for ind, label in enumerate(ax.get_xticklabels()):
            label.set_visible(True)
    

    # Create a color bar with the correct range
    color_bar = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(vmin=0, vmax=max(cluster_count)))


    # Add the color bar to the plot
    cbar = plt.colorbar(color_bar, ax=ax)
    cbar.set_label('Number of Entries in Cluster')
    # x-axis label
    plt.ylabel('Cluster')
    # y-axis label
    plt.xlabel('LFC')

    plt.title(f"Gene: {protein_name}\nNumber of Clusters: {len(np.unique(clusters))}\n Distance Threshold: {threshold}")
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory,f"{protein_name}_boxplot_{n_clusters}.pdf"), bbox_inches="tight")
    plt.close()
    
    pvalues = simulate_pwes(clusters, PWES_array, threshold, protein_name, output_directory, PWES_array, PWES_array, suffix, n_simulations)
    
    return dict_of_clusters, wcss, pvalues



def simulate_pwes(clusters, PWES_array, threshold, protein_name, output_directory, xij_array, dij_array, suffix, n_simulations):
    
    result_array = PWES_array
    xij_array = xij_array
    dij_array = dij_array
    gene = protein_name
    experiment = suffix
    
    
    t = 16
    unique_clusters = np.unique(clusters)
    xij_mean = np.mean(xij_array)
    xij_std = np.std(xij_array)
    residue_range = np.arange(0, dij_array.shape[0])

    def pwes(xij, dij, xij_mean, xij_std, t):
        return np.tanh((xij - xij_mean) / xij_std) * np.exp(-((dij**2) / (2*(t**2))))

    sim_types = ["residues", "scores"]
    p_value_matrix = np.zeros((len(unique_clusters), len(sim_types)))
    # Calculate the number of rows and columns needed for the subplots
    num_rows = len(unique_clusters)
    num_cols = len(sim_types)

    # Create the figure with appropriate spacing between subplots, setting the height to the number of clusters
    plt.figure(figsize=(10, num_rows), layout='constrained')  # Adjust figure width as needed

    # Big figure title
    plt.suptitle(f"Gene: {gene}, Experiment: {experiment}, Number of Clusters: {len(unique_clusters)}, Threshold: {threshold}", fontsize=16)
    
    
    for sim_type_idx, sim_type in enumerate(sim_types):
        for cluster_idx, cluster in enumerate(unique_clusters):
            cluster_indices = np.where(clusters == cluster)[0]
            cluster_result_array = result_array[cluster_indices, :][:, cluster_indices]
            sim_sum_array = np.zeros(n_simulations)

            all_rand_res = np.random.choice(residue_range, (n_simulations, 1, cluster_result_array.shape[0]), replace=True)
            cluster_xij_array = xij_array[cluster_indices, :][:, cluster_indices]
            cluster_dij_array = dij_array[cluster_indices, :][:, cluster_indices]
            for sim in range(n_simulations):
                sim_indices = np.ix_(all_rand_res[sim, 0], all_rand_res[sim, 0])
                if sim_type == "residues":
                    
                    simulated_pwes = pwes(cluster_xij_array, dij_array[sim_indices], xij_mean, xij_std, t)
                                        

                elif sim_type == "scores":
                    simulated_pwes = pwes(xij_array[sim_indices], cluster_dij_array, xij_mean, xij_std, t)

                np.fill_diagonal(simulated_pwes, 0)  # To exclude diagonal elements
                sim_sum_array[sim] = np.sum(np.abs(simulated_pwes))

            obs_sum = np.sum(np.abs(pwes(xij_array[cluster_indices, :][:, cluster_indices],
                                    dij_array[cluster_indices, :][:, cluster_indices], 
                                    xij_mean, xij_std, t)))

            
            # calculate empirical p-value
            if sim_type == "residues":
                p_value = (np.sum(sim_sum_array >= obs_sum) +1)/ (n_simulations+1)
                
            if sim_type == "scores":
                p_value = np.min([(np.sum(sim_sum_array >= obs_sum) +1)/ (n_simulations+1), (np.sum(sim_sum_array <= obs_sum) +1) / (n_simulations +1)])

            p_value_matrix[cluster_idx, sim_type_idx] = p_value

            # Plot histogram with adjusted subplot dimensions
            plt.subplot(num_rows, num_cols, cluster_idx * num_cols + sim_type_idx + 1)
            plt.hist(sim_sum_array, bins=50)
            plt.axvline(obs_sum, color='r')
            
            #sim type title
            if sim_type == "residues":
                plt.title(f"Fixed lfc: Cluster {cluster}, p-value: {p_value:.1e}, Observed sum: {obs_sum:.2f}", fontsize=9)
            if sim_type == "scores":
                plt.title(f"Fixed distances: Cluster {cluster}, p-value: {p_value:.1e}, Observed sum: {obs_sum:.2f}", fontsize=9)

    #plt.subplots_adjust(wspace=0.4, hspace=2)  # Adjust the space between subplots (optional)
    plt.savefig(f"{output_directory}/{gene}_simulated_pwes_{len(unique_clusters)}_clusters_{threshold}.pdf")

    plt.close()
    #convert p_value_matrix to list
    p_value_matrix = p_value_matrix.tolist()
    
    return p_value_matrix


def plot_elbow_fn(dict_of_scores, output_directory, protein_name, suffix):
    """
    this method plots the elbow plot for the PWES method and saves the figure in the output directory
    input:
    dict_of_scores: dict
    output_directory: str
    protein_name: str
    suffix: str
    
    output:
    None
    """
    # plot the elbow plot
    wcsses = []
    keys = list(dict_of_scores.keys())
    #sort the keys
    keys.sort()
    for i in keys:
        wcsses.append(dict_of_scores[i]["wcss"])
        
    plt.figure(figsize=(10, 5))
    plt.plot(keys, list(wcsses), linestyle='-', marker='o')
    plt.xlabel("Number of Clusters")
    plt.ylabel("WCSS")
    plt.title(f"Elbow Plot for {protein_name}")
    plt.savefig(f"{output_directory}/{protein_name}_elbow_plot_{suffix}.pdf")
    plt.close()
    
    return None