# Wukong_MIKE_data
All information regarding stars from the Wukong stellar stream from spectroscopy with MIKE/Magellan.

abund_data: final abundances + errors for each star ([smhr](https://github.com/andycasey/smhr)/[LESSPayne](https://github.com/alexji/LESSPayne) format)

line_data: line-by-line abundances + errors for each star

reduced_spectra: yes, the MIKE spectra reduced

Wukong_ALL_MIKEsample.csv: a file with almost all relevant information for the Wukong stars coming from Gaia, spectroscopic surveys (H3 or APOGEE), and our own analysis. 

wuk_master_abund_table.csv: all abundance information for all stars obtained through our analysis in a more comprehensible way and easy to deal with than smhr/LESSPayne standard. A code to generate this kinds of tables from smhr/LESSPayne outputs is available at [this repo](https://github.com/guilhermelimberg/abund-tables).

Na_NLTE_corrections.csv: line-by-line NLTE corrections to the sodium abundances from [Lind+2011](https://ui.adsabs.harvard.edu/abs/2011A%26A...528A.103L/abstract).

Most columns in these tables are fairly self-explanatory. However, if you want to use this data and need to make be sure regarding any quantities, contact me at guilherme.limberg @ usp.br

IMPORTANT UPDATE early 2024: during refereeing process, an issue was indentified in my calculation of weighted statistical uncertainties for abundances, which, in turn, propagated into final uncertainties being underestimated. This was particularly affecting those abundances with few lines measured and large systematics (mainly Al and N). Although this did not change our qualitative conclusions, we fixed this issue. You should NEVER use files in this repository with suffix "_old_", although I keep them here for history. You should always use files with suffix "_fix_" and/or "_2024_". The "_line_data_" file was unchanged.
