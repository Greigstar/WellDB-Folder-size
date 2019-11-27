import locale
import os
import sys
#folder = r'D:\Python\Sub_Appl_Data\WellDB'
folder = r'G:\Sub_Appl_Data\WellDB\MR'
Folder_of_interest=['00.Original_Vendor_Data','01.Well_Planning','02.Drilling_and_Completion','03.Directional_Surveys','04.Mud_Logs','05.LWD_Log_data','06.Wireline_Log_Data','07.Borehole_Seismic','08.Formation_Pressure_Data','09.Well_Test_Data','10.Fluid_Data','11.Core_Data','12.Geology_Data_and_Evaluations','13.Petrophysical_Data_Evaluations','14.Final_Well_Report_and_Completion_Log','15.Production_Logs','16.Production','99.Miscellaneous']
locale.setlocale(locale.LC_ALL, "")

#File=open(r'D:\Python\Scripts\WellDBData\Welldb_size.txt')
##
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("D:\Python\Scripts\WellDBData\Welldb_size_MR.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()

def getFolderSize(p):
   from functools import partial
   prepend = partial(os.path.join, p)
   return sum([(os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f)) for f in map(prepend, os.listdir(p))])

def get_size(state, root, names):
    paths = [os.path.realpath(os.path.join(root, n)) for n in names]
    state[0] += sum(os.stat(p).st_size for p in paths if os.path.exists(p))

def print_sizes(root, my_folder):
    total = 0
    paths = []
    state = [0]
    n_ind = s_ind = 0
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            continue

        state[0] = 0
        os.path.walk(path, get_size, state)
        total += state[0]
        s_size = locale.format('%8.0f', state[0], 3)
        n_ind = max(n_ind, len(name), 5)
        s_ind = max(s_ind, len(s_size))
        paths.append((name, s_size))

        for name, size in paths:
            name.ljust(n_ind), size.rjust(s_ind)
            s_total = locale.format('%8.0f', total, 3)
            s2=s_total.rjust(s_ind)
            return (s2)

for root, dirs, files in os.walk(folder):
    path = root.split(os.sep)
    f_match=0
    for dir in dirs:
        f_AOI=root.split("\\")
        for result in f_AOI:
            for item in Folder_of_interest:
                if item == result and f_match != 1:
                    f_match=1
                    print root, "size ; ", print_sizes(root, f_match)
