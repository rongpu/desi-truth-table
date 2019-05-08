import glob
import subprocess

filelist = glob.glob('decals-*')

for filename in filelist:
    filename_new = 'ls-' + filename[7:]
    print(filename_new)
    subprocess.run(['mv', filename, filename_new])
