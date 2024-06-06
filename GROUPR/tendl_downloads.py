import subprocess

# Define a function to download a file using subprocess
def download_file(url, destination):
    subprocess.run(['wget', url, '-O', destination])
    return destination

# Define a function to download the .tendl file given specific user inputs to for element and atomic number
def tendl_download(element, Z, filetype, save_path = None):
    # Ensure that Z is properly formatted
    if type(Z) is not str:
        Z = str(Z)
    if len(Z) < 3:
        zero_repeater = 3 - len(Z)
        Z = '0' * zero_repeater + Z

    # Define general URL format for files in the TENDL database
    tendl_gen_url = 'https://tendl.web.psi.ch/tendl_2017/neutron_file/'

    # Construct the filetype-specific URl for the data file
    if filetype == 'endf' or filetype == 'ENDF':
        # Construct the URL of the ENDF file to be downloaded
        download_url = tendl_gen_url + f'{element}/{element}{Z}/lib/endf/n-{element}{Z}.tendl'

        # Define a save path for the ENDF file if there is not one already specified
        if save_path is None:
            #save_path = f'tendl_2017_{element}{Z}_{filetype}.endf'
            save_path = 'tape20'

    elif filetype == 'pendf' or filetype == 'PENDF':
        # Construct the URL of the PENDF file to be downloaded
        download_url = tendl_gen_url + f'{element}/{element}{Z}/lib/endf/n-{element}{Z}.pendf'

        # Define a save path for the PENDF file if there is not one already specified
        if save_path is None:
            #save_path = f'tendl_2017_{element}{Z}_{filetype}.pendf'
            save_path = 'tape21'

    # Extract file
    save_path = download_file(download_url, save_path)

    return save_path

# Call function by user CLI input
#element = input('Select element: ')
#Z = input('Select atomic number, Z = ')
#endf_path = tendl_download(element, Z, 'endf')
#try:
#    pendf_path = tendl_download(element, Z, 'pendf')
    print(f'ENDF file can be found at {endf_path}')
    print(f'PENDF file can be found at {pendf_path}')
#except:
    # Need to figure out somewhere in the function how to
    # register a "ERROR 404: Not Found" message.
    # Probably in the download_file function
    # Resolve later
    print(f'ENDF file can be found at {endf_path}')
    print('No PENDF file found')