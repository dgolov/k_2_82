# data_list = ['Kг= 0.31 %\n',
#              '\n',
#              'Kг= 0.72 %\n',
#              '\n',
#              'Kг= 4.73 %\n',
#              '\n',
#              'U= 1.87  В\n',
#              '\n',
#              'U= 1.92  В\n',
#              '\n',
#              'U= 2.01  В\n',
#              '\n',
#              'U= 2.11  В\n',
#              '\n',
#              'U= 2.17  В\n',
# ]
#
# param_list = []
#
# for line in data_list:
#     if 'Kг= ' in line:
#         param_list.append(float(line[4:-3]))
# out_pow = param_list[-2]
#
# for line in data_list:
#     if 'U= ' in line:
#         param_list.append(float(line[3:-4]))
#
# out_kg = param_list[-2]
# print(out_pow, out_kg)