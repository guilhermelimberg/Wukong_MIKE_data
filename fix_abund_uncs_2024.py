from astropy.io import ascii
import pandas as pd
import numpy as np
import re

# load ABUNDANCE data
abund_data = ascii.read("abund_data_v4.txt") # your file name here (.txt or something) and transform abund_data table into DataFrame
abund_data = pd.DataFrame(abund_data.as_array())

# load LINE data
line_data = ascii.read("line_data_v4.txt") # your file name here (.txt or something) and transform line_data table into DataFrame
line_data = pd.DataFrame(line_data.as_array())

# grab the unique names of all stars in the sample
all_stars = abund_data["star"].unique()

# a logica vai ser criar esse array com os novos valores de e_stat_w e dps adicionar no new_abund_data
e_stat_w_new = []

for STAR in all_stars: # aqui a gente vai fazer um loop nas ESTRELAS
	star_X = line_data[line_data["star"]==STAR] #all_stars[i]]
	species = abund_data["species"][abund_data["star"]==STAR].unique()
	#print(species)
	for x in species: # dps um outro loop nos ELEMENTOS que foram medidos em cada estrela
		avg_abund_w = abund_data["logeps_w"][(abund_data["star"]==STAR) & (abund_data["species"]==x)]  # this is the weighted mean abundance
		weights     = line_data["weight"][(line_data["star"]==STAR) & (line_data["species"]==x)] # get all the weigths
		abunds      = line_data["logeps"][(line_data["star"]==STAR) & (line_data["species"]==x)]# get all the abundances line by line 
		aux_product = []
		for w, a in zip(weights, abunds): # outro loop para calcular a parte dos pesos multiplicados pelas abunds (eq 6 from Ji+2020 Carinas1/2 paper)
			aux_value = w * (a - avg_abund_w)**2. 
			aux_product.append(float(aux_value))
		sig_stat_value = np.sqrt( (np.sum(aux_product))/(np.sum(weights)) + 1/(np.sum(weights)) ) # now we compute sigma_stat (e_stat_w_new) 
		e_stat_w_new.append(round(sig_stat_value,3))
		# if x == 13.0: print(sig_stat_value, "\n", e_stat_w_new)

# now I need to recalculate final abundance errors using this new e_stat_w_new

# now I will start a new abundance table with only what matters for the 'master' tables
# I will also add this "e_stat_w_new" array to the "new_abund_table" pandas.DataFrame as a column
new_abund_table = abund_data["star"]
new_abund_table = pd.DataFrame(new_abund_table) # begin new pands DataFrame with the "species" column just cause why not
new_abund_table.insert(1, "species", abund_data["species"])
new_abund_table.insert(2, "elem", abund_data["elem"].apply(lambda x: x.replace(' ', '')))
new_abund_table.insert(3, "N", abund_data["N"])
new_abund_table.insert(4, "ul", abund_data["ul"])
new_abund_table.insert(5, "e_stat_w_old", abund_data["e_stat_w"]) # THIS IS STILL THE WRONG VALUES OF e_stat_w

"""
df['Name'] = df['Name'].apply(lambda x: x.replace(' ', ''))
print(df)
"""

new_abund_table["e_stat_w_new"] = np.array(e_stat_w_new).tolist() # this are the new values! success! 

new_abund_table.insert(7, "e_Teff_w", abund_data["e_Teff_w"])
new_abund_table.insert(8, "e_logg_w", abund_data["e_logg_w"])
new_abund_table.insert(9, "e_vt_w", abund_data["e_vt_w"])
new_abund_table.insert(10, "e_MH_w", abund_data["e_MH_w"]) 
new_abund_table.insert(11, "[X/H]", abund_data["[X/H]"])
new_abund_table.insert(12, "e_XH_old", abund_data["e_XH"]) # esses valores aqui tbm estao ERRADOS (eq 10 from Ji+2020b, Carinas 1/2 paper)


# the equation for [X/H] abundance errors is equation 10 from Ji+2020b
# eq10 : sigma_[X/H] = np.sqrt( e_stat_w_new_X**2 + np.sum(delta_X_sp**2) )
# so I need to compute these sums of deltas for stellar params. happily, all we need is in the new_abund_table

# grab the unique names of all stars in the sample
all_stars = new_abund_table["star"].unique()

# a logica vai ser criar esse array com os novos valores de e_stat_w e dps adicionar no new_abund_data
e_xfe_all = []

for STAR in all_stars: # aqui a gente vai fazer um loop nas ESTRELAS
	star_X = new_abund_table[new_abund_table["star"]==STAR] #all_stars[i]]
	species = new_abund_table["species"][new_abund_table["star"]==STAR].unique()
	for x in species: # dps um outro loop nos ELEMENTOS que foram medidos em cada estrela (esse eh um jeito mto burro de fazer isso)
		e_stat_spec = float(star_X["e_stat_w_new"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_teff_spec = float(star_X["e_Teff_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_logg_spec = float(star_X["e_logg_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_vt_spec   = float(star_X["e_vt_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_mh_spec   = float(star_X["e_MH_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_xfe_spec  = np.sqrt( e_stat_spec**2. + e_teff_spec**2. + e_logg_spec**2. + e_vt_spec**2.  + e_mh_spec**2.)
		e_xfe_all.append(round(e_xfe_spec,3))

# agora, bora adicionar essa incerteza e_XFe final na tabela nova
new_abund_table["e_XH_new"] = np.array(e_xfe_all).tolist() # this are the new values! success! 
#new_abund_table[["elem", "N", "e_XFe_old", "e_XFe_new"]] ### USE THIS TO CHECK IF ALL IS GOOD



new_abund_table.insert(14, "[X/Fe]", abund_data["[X/Fe]"])
new_abund_table.insert(15, "e_XFe_old", abund_data["e_XFe"]) # esses valores aqui tbm estao ERRADOS (eq 10 from Ji+2020b, Carinas 1/2 paper)

# the equation for [X/Y] abundance errors is equation 10 from Ji+2020b
# eq10 : sigma_[X/Y] = np.sqrt( e_stat_w_new_X**2 + e_stat_w_new_Y**2 + np.sum( delta_X_sp - delta_Y_sp )**2 )
# so I need to compute these sums of deltas for stellar params. happily, all we need is in the new_abund_table

# grab the unique names of all stars in the sample
all_stars = new_abund_table["star"].unique()

# a logica vai ser criar esse array com os novos valores de e_stat_w e dps adicionar no new_abund_data
e_xfe_all = []

for STAR in all_stars: # aqui a gente vai fazer um loop nas ESTRELAS
	star_X = new_abund_table[new_abund_table["star"]==STAR] #all_stars[i]]
	species = new_abund_table["species"][new_abund_table["star"]==STAR].unique()
	for x in species: # dps um outro loop nos ELEMENTOS que foram medidos em cada estrela (esse eh um jeito mto burro de fazer isso)
		e_stat_spec = float(star_X["e_stat_w_new"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_stat_fe   = float(star_X["e_stat_w_new"][(star_X["star"]==STAR) & (star_X["species"]==26.0)]) # always Fe I
		e_teff_spec = float(star_X["e_Teff_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_teff_fe   = float(star_X["e_Teff_w"][(star_X["star"]==STAR) & (star_X["species"]==26.0)]) # always Fe I
		e_logg_spec = float(star_X["e_logg_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_logg_fe   = float(star_X["e_logg_w"][(star_X["star"]==STAR) & (star_X["species"]==26.0)]) # always Fe I
		e_vt_spec   = float(star_X["e_vt_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_vt_fe     = float(star_X["e_vt_w"][(star_X["star"]==STAR) & (star_X["species"]==26.0)]) # always Fe I
		e_mh_spec   = float(star_X["e_MH_w"][(star_X["star"]==STAR) & (star_X["species"]==x)])
		e_mh_fe     = float(star_X["e_MH_w"][(star_X["star"]==STAR) & (star_X["species"]==26.0)]) # always Fe I
		# if x == 13.0: print(e_stat_spec, "\n", e_stat_fe, "\n", e_teff_spec, "\n", e_teff_fe, "\n", e_logg_spec, "\n", e_logg_fe, "\n", e_vt_spec, "\n", e_vt_fe, "\n", e_mh_spec, "\n", e_mh_fe)
		if x == 26.0: e_xfe_spec = 0.0
		else: e_xfe_spec  = np.sqrt( e_stat_spec**2. + e_stat_fe**2. + (e_teff_spec - e_teff_fe)**2. + (e_logg_spec - e_logg_fe)**2. + (e_vt_spec - e_vt_fe)**2.  + (e_mh_spec - e_mh_fe)**2.)
		e_xfe_all.append(round(e_xfe_spec,3))

# agora, bora adicionar essa incerteza e_XFe final na tabela nova
new_abund_table["e_XFe_new"] = np.array(e_xfe_all).tolist() # this are the new values! success! 
#new_abund_table[["elem", "N", "e_XFe_old", "e_XFe_new"]] ### USE THIS TO CHECK IF ALL IS GOOD

# save everything
new_abund_table.to_csv("abund_data_v4_fix_uncs_2024.csv", index=False)