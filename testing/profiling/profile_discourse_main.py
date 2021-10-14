import cProfile
import pstats

p = pstats.Stats('/Users/ericlemmon/Google Drive/PhD/PhD_Project_v2/Profile_Files/output.txt')
p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(100)