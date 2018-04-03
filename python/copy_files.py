# copy files listed in text file
import os
from shutil import copyfile

filen = r"C:\Users\sefremov\WorkFolder\Lab\test_dir\test_list.txt"
file = open(filen, "r")

items = []
for line in file:
    items.append(line.strip())
    
for s in sorted(items):
    print(s)

file.close()

foldern = r"\\lcheng41-desk1\Users\lcheng41\Documents\share\FromIngrid\Ingrids_Test_Clips"
#foldern = r"\\lcheng41-desk1\Users\lcheng41\Documents\share\ToBo"
#foldern = r"C:\Users\sefremov\WorkFolder\Lab\test_dir"
dst_foldern = r"C:\Users\sefremov\WorkFolder\Lab\test_dir\output"

if not os.path.exists(dst_foldern):
    os.makedirs(dst_foldern)
    
found = 0    

dirs = [f for f in os.listdir(foldern) if not os.path.isfile(os.path.join(foldern, f))]
for f in dirs:
   source_folder = os.path.join(foldern, f)
   files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
   for name in items:
       stream = name + ".av1"
       gsf = name + ".gsf"
       if (stream in files) and (gsf in files):
           src = os.path.join(source_folder, stream)
           print("[" + str(found) + "]: " + stream + " --- Copying...")
           copyfile(src, os.path.join(dst_foldern, stream))
           src = os.path.join(source_folder, gsf)
           print("[" + str(found) + "]: " + gsf + " --- Copying...")
           copyfile(src, os.path.join(dst_foldern, gsf))
           found += 1
           if found == 34:
               break
   if found == 34:
       break
