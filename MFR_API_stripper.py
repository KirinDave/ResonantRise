from __future__ import print_function
import os
import shutil
import sys
import threading
import time
import zipfile
if sys.version_info[0] == '3':
    import builtins
else:
    builtins = __builtins__
import glob

class t:
    starttime = 0.0


class RepackError(Exception): pass

if len(sys.argv) < 2:
    raise RepackError("No jar file(s) provided")

if sys.argv[1] == '-h' or sys.argv[1] == "--help":
    print("Help:")
    print("repack.py jarfile <jarfile1 <jarfile2>>")
    print("Paths must be absolute, so either /dir/mod.jar or in the same directory.")
    sys.exit()

print("Warning!!")
print("This script does not check the zip files! Use at your own risk!")
input("Press enter to continue, or press Ctrl+C/D (Ctrl+Z enter on windows) to exit")

#print("Being evil and injecting stuff into builtins")
#print("Also being evil and THREADS")

def updatetime():
    time.sleep(0.1)
    t.starttime += 0.1

threading.Thread(target=updatetime).start()

# BUILTINS FIX
def nprint(*args, **kwargs):
    builtins.oprint("[{t}]".format(t=t.starttime), *args)
builtins.oprint = builtins.print
builtins.print = nprint
# END BUILTINS FIX

print("Builtins Fix injected")

# Main loop, run through all files


for jarf in sys.argv[1:]:
    if not os.path.exists("./unpack"):
        os.makedirs("./unpack")
    print("Loading jar file", jarf)
    exists = os.path.exists(jarf)
    if not exists:
        print("JARFILE {} DOES NOT EXIST, KILLING SELF".format(jarf))
        sys.exit(1)
    print("Reading ZIP")
    if not zipfile.is_zipfile(jarf):
        print("Jarfile", jarf, "is not a zip file. Skipping.")
        continue
    z = zipfile.ZipFile(jarf)

    # Check for MFR api files
    nl = z.namelist()
    #print(nl)
    for n in nl:
        if "powercrystals/minefactoryreloaded/api/rednet" in n:
            print("Detected api/rednet in zip")
            break
    else:
        z.close()
        continue

    # API files found
    # Unpack zip
    print("Dangerously unpacking zip into 'unpack' - still not checking zip file!")
    z.extractall("./unpack")

    # No need for the zip file anymore
    z.close()

    # Now create a new file to use
    z = zipfile.ZipFile("{jf}-patched.jar".format(jf=jarf.split('.jar')[0]), 'w')
    # Remove the api files
    print("Removing API files")
    try:
        shutil.rmtree("./unpack/powercrystals/minefactoryreloaded/api/rednet")
    except:
        print("Fatal error: Unable to remove files.")
        shutil.rmtree("./unpack")
        sys.exit(1)
    print("Re-packing zip file")

    for root, subdir, fs in os.walk("./unpack"):
        for f in fs:
            print("Repacking file", os.path.join(root, f))
            z.write(os.path.join(root, f))
    print("Finished. Closing zip file and removing unpack files.")
    z.close()
    shutil.rmtree('./unpack')