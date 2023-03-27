import sys
sys.path.append('d:\coding\copilot\wh_opt\modules')
import general_function as gf
from datetime import timedelta


class routings:
    def __init__(self, opt):
        self.opt = opt
        
    def run(self, filelist):
        self.filelist = filelist
        if self.opt == 1:
            return self.s_shape()
        elif self.opt == 2:
            return self.largest_gap()

    def test(self):
        # Reading order file
        fname = gf.reading_file()
        compl_time = []
        for fn in fname:
            np_fn = fn.to_numpy()
            self.filelist = [[[], 0]]
            for idx, order in enumerate(np_fn):
                self.filelist[0][0].extend(order[3])
                self.filelist[0][1] += order[1]
            if self.opt == 1:
                self.s_shape()
            elif self.opt == 2:
                self.largest_gap()
            
            compl_time.append(self.count_completion_time())
        return compl_time
            
    def s_shape(self):
        # s-shape
        for file in self.filelist:
            position = file[0]
            if (len(position)%2) != 0:
                distance = (position[-1][0]-1)*4 + (len(position)-1)*16 + position[-1][1][-1]*2 - 1
            else:
                distance = (position[-1][0]-1)*4 + len(position)*16
            file[0] = distance
        return self.filelist
    
    def largest_gap(self):
        # Largest Gap
        for file in self.filelist:
            position = file[0]
            if len(position) == 1:
                distance = (position[-1][0]-1)*4 + position[-1][1][-1]*2 - 1
            elif len(position) == 2:
                distance = (position[-1][0]-1)*4 + 32
            else:
                distance = (position[-1][0]-1) * 4 + 32
                for a in range(1, len(position)-1):
                    dt = [0] + position[a][1] + [17]
                    gap = [dt[b] - dt[b-1] for b in range(1, len(dt))]
                    gap.sort()
                    gap.pop()
                    totgap = sum(gap)
                    distance += (totgap*2) - 1
            file[0] = distance
        return self.filelist

    def count_completion_time(self):
        # Counting completion time
        for a in range(len(self.filelist)):
            comptime = self.filelist[a][0] + self.filelist[a][1] * 3
            self.filelist[a] = timedelta(seconds=comptime)
        return self.filelist
