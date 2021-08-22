import numpy as np
# x = [[a11,a12,a13,a14],[a21,a22,a23,a24],[a31,a32,a33,a34],[a41,a42,a43,a44]]
# axis=0: out[x] = a(i+1)x - a(i)x
# axis=1: out[x] = ax(i+1) - ax(i)

x = [[1,2,3,4],[4,3,2,1],[1,4,7,9],[2,6,5,8]]
diff_x_0 = np.diff(x, n=1, axis=0)
print("diff_x_0:"+str(diff_x_0))

diff_x_1 = np.diff(x, n=1, axis=1)
print("diff_x_1:"+str(diff_x_1))

diff_x_2 = np.diff(x, n=2, axis=1)
print("diff_2:"+str(diff_x_2))

# y = [[[a111,a112],[a121,a122]],[[a211,a212],[a221,a222]],[[a311,a312],[a321,a322]]]
# axis=2: out[x] = axy(i+1) - axy(i)
y = [[[1,2],[3,4]],[[4,3],[2,1]],[[1,4],[7,9]],[[2,6],[5,8]]]
diff_y_2 = np.diff(y, n=1, axis=2)
print("diff_y_2:"+str(diff_y_2))
#
# diff_y_2 = np.diff(y, n=1, axis=1)
# print("diff_2:"+str(diff_y_2))