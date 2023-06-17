import os
import re

newNames = {
    'L1P1': 'Foundations of Physics 1 paper 1',
    'L2P1': 'Foundations of Physics 2A',
    'L2P2': 'Foundations of Physics 2B',
    'L2P3': 'Mathematical Methods in Physics',
    'L2P4': 'Stars and Galaxies',
    'L2P5': 'Theoretical Physics 2',
    'L3P1': 'Foundations of Physics 3A',
    'L3P2': 'Foundations of Physics 3B',
    'L3P3': 'Planets and Cosmology 3',
    'L3P4': 'Theoretical Physics 3',
    'L3P6': 'Modern Atomic and Optical Physics 3',
    'L4P1': 'Atoms, Lasers and Qubits',
    'L4P2': 'Advanced Theoretical Physics',
    'L4P3': 'Advanced Condensed Matter Physics',
    'L4P4': 'Advanced Astrophysics',
    'L4P5': 'Particle Theory',
    'L4P6': 'Theoretical Astrophysics'
}

def rename_files(location):
    files = os.listdir(location)
    pattern = re.compile(r'^(L\dP\d)([A-Z])(Q\d).*\.tex$')

    for file in files:
        match = pattern.match(file)
        if match:
            prefix = match.group(1)
            q_number = match.group(3)

            new_prefix = newNames.get(prefix)
            if new_prefix:
                new_file = f"{new_prefix}~{q_number}.tex"
                os.rename(os.path.join(location, file), os.path.join(location, new_file))
                print(f"Renamed {file} to {new_file}")
            else:
                print(f"No match found in the dictionary for {prefix}")
        else:
            print(f"File {file} does not match the pattern")

if __name__ == "__main__":
    rename_files('2017-papers-raw')
    rename_files('2018-papers-raw')
    rename_files('2019-papers-raw')
    rename_files('2020-papers-raw')
