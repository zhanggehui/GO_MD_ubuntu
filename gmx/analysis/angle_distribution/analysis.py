import pandas as pd
import numpy as np
import analyze_theta as at
import matplotlib.pyplot as plt
import sys
import scipy.io as sio
import commons as cmval


class Analysis:
    def __init__(self, fname, oname, omatname, center, ori):
        self.fname = fname
        self.oname = oname
        self.omatname = omatname
        self.center = center
        self.ori = ori
        gLength = int(cmval.gridLength)
        self.n_grid = np.zeros(shape=(gLength, gLength))
        self.v1_grid = np.zeros(shape=(gLength, gLength))
        self.v2_grid = np.zeros(shape=(gLength, gLength))
        self.df_list = []
        self.angle_list = []
        self.__read_gro_file()

    def __read_gro_file(self):
        count = 0
        frame = 0
        # col_list = ['atomName', 'x', 'y', 'z','vx','vy','vz']
        atom_name_list = []
        with open(self.fname, 'r') as f:
            for line in f:
                count = count + 1
                if count == 1:
                    pass
                elif count == 2:
                    if frame == 0:
                        n_atoms = int(line[0:5])
                        x_arry = np.empty(n_atoms, dtype=float)
                        y_arry = np.empty(n_atoms, dtype=float)
                        z_arry = np.empty(n_atoms, dtype=float)
                        v_x_arry = np.empty(n_atoms, dtype=float)
                        v_y_arry = np.empty(n_atoms, dtype=float)
                        v_z_arry = np.empty(n_atoms, dtype=float)
                    if frame % 1000 == 0:
                        print("------ 正在读入第", frame, "帧 ------")
                elif 3 <= count <= n_atoms + 2:
                    if frame == 0:
                        atom_name_list.append(line[10:15].lstrip())
                    index = count - 3
                    add_record(x_arry, y_arry, z_arry,
                               v_x_arry, v_y_arry, v_z_arry, index, line)
                else:
                    df_tmp = pd.DataFrame({
                        'atomName': atom_name_list,
                        'x': x_arry,
                        'y': y_arry,
                        'z': z_arry,
                        'vx': v_x_arry,
                        'vy': v_y_arry,
                        'vz': v_z_arry
                    })
                    self.df_list.append(df_tmp)
                    frame = frame + 1
                    count = 0

    def analysis(self):
        for i in range(len(self.df_list)):
            if i % 1000 == 0:
                print("------ 正在分析第", i, "帧 ------")
            self.analyze_frame(i)
        self.finish_analysis()

    def analyze_frame(self, i):
        df = self.df_list[i]
        a_list, n_grid, v1_grid, v2_grid = at.Theta(df, self.center, self.ori).analyze_theta()
        self.angle_list.extend(a_list)
        self.n_grid = self.n_grid + n_grid
        self.v1_grid = self.v1_grid + v1_grid
        self.v2_grid = self.v2_grid + v2_grid

    def finish_analysis(self):
        self.n, bins = np.histogram(self.angle_list, bins=180, range=[0, 180])
        self.bins = bins[0: len(bins) - 1]
        if sys.platform == 'win32':
            y = self.n * np.sin(np.deg2rad(self.bins))
            plt.plot(self.bins, y, 'o')
            plt.show()
        self.v1_grid = self.v1_grid / self.n_grid
        self.v2_grid = self.v2_grid / self.n_grid
        self.write_output()

    def write_output(self):
        arr = np.vstack([self.bins, self.n]).T
        np.savetxt(self.oname, arr, fmt='%g', delimiter=',')
        sio.savemat(self.omatname, {'n_grid': self.n_grid,
                                    'v1_grid': self.v1_grid,
                                    'v2_grid': self.v2_grid})


def add_record(x_arry, y_arry, z_arry,
               v_x_arry, v_y_arry, v_z_arry,
               index, line):
    x_arry[index] = float(line[20 + 0 * 8: 28 + 0 * 8])
    y_arry[index] = float(line[20 + 1 * 8: 28 + 1 * 8])
    z_arry[index] = float(line[20 + 2 * 8: 28 + 2 * 8])
    v_x_arry[index] = float(line[44 + 0 * 8: 52 + 0 * 8])
    v_y_arry[index] = float(line[44 + 1 * 8: 52 + 1 * 8])
    v_z_arry[index] = float(line[44 + 2 * 8: 52 + 2 * 8])
