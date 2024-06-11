import ENDFtk
import gendf_tools as GENDFtk
import pandas as pd
import contextlib

# Main implementation
print('Input GENDF file or download from FENDL 3.2b')
usr_selection = input('For local input, type I. For download, type D. (I, D): ')
if usr_selection == 'I':
    gendf_path = input('Type in path of GENDF file: ')
    pKZA = GENDFtk.gendf_pkza_extract(gendf_path)
elif usr_selection == 'D':
    element = input('Select target element: ')
    A = input('Select mass number (A): ')
    gendf_path, pKZA = GENDFtk.gendf_download(element, A)

print(f"GENDF file path: {gendf_path}")
print(f"Parent KZA (pKZA): {pKZA}")

# Load MT table
# Data for MT table collected from 
# https://www.oecd-nea.org/dbdata/data/manual-endf/endf102_MT.pdf
mt_table = pd.read_csv('mt_table.csv')

# Read in data with ENDFtk
tape = ENDFtk.tree.Tape.from_file(gendf_path)
mat_ids = tape.material_numbers
mat = mat_ids[0]
xs_MF = 3
file = tape.material(mat).file(xs_MF)

# Extract MT values
MTs = []
for i in range(1000):
    with GENDFtk.suppress_output():
        try:
            file.section(i)
            MTs.append(i)
        except:
            continue

# Initialize lists
cross_sections_by_MT = []
emitted_particles_list = []
dKZAs = []

# Extract data for each MT
for MT in MTs:
    try:
        sigma_list = GENDFtk.extract_cross_sections(file, MT)
        if not sigma_list:
            continue
        dKZA, emitted_particles = GENDFtk.reaction_calculator(MT, mt_table, pKZA)
        if dKZA is None:
            continue
        cross_sections_by_MT.append(sigma_list)
        dKZAs.append(dKZA)
        emitted_particles_list.append(emitted_particles)
    except Exception as e:
        print(f"Error processing MT {MT}: {e}")
        continue

# Store data in a DataFrame
gendf_data = pd.DataFrame({
    'Parent KZA': [pKZA] * len(dKZAs),
    'Daughter KZA': dKZAs,
    'Emitted Particles': emitted_particles_list,
    'Cross Sections': cross_sections_by_MT
})

# Save to CSV
gendf_data.to_csv('gendf_data.csv', index=False)
print("Saved gendf_data.csv")
print(gendf_data.head())