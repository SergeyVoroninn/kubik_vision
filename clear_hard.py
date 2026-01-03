import os
names_of_files = ['phase1x24_prun','move_twist','move_slice_sorted','move_flip','move_corners','fs24_sym','fs24_rep','fs24_classidx','cornerprun','conj_twist']
for f in names_of_files:
    if os.path.exists(f):
        os.remove(f)