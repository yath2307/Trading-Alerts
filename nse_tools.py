from nsetools import Nse
nse = Nse()
print(nse)
list = nse.get_index_list()
print(list)
all_stock_codes = nse.get_stock_codes()
print(all_stock_codes)