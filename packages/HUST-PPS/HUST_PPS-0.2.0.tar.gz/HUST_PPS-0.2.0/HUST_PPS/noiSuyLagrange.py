import numpy as np
from HUST_PPS import HornerNhanDaThuc, HornerChiaDaThuc
from sympy import symbols, Poly, expand, sympify

def LapBangTichLagrange(a: np.ndarray):
    list_of_arrays = []
    b = [1]
    max_length = len(a) + 1
    temp = np.zeros(max_length)
    temp[-1] = 1
    list_of_arrays.append(temp)
    for i in range(0,len(a)):
        b1 = HornerNhanDaThuc(b,a[i])
        b2 = np.zeros(max_length)
        b2[-len(b1):] = b1
        list_of_arrays.append(b2)
        b = b1.copy()
    return np.array(list_of_arrays)

def LapBangThuongLagrange(a: np.ndarray):
    list_of_c = []
    lap_bang_tich = LapBangTichLagrange(a)[-1]
    for i in range(0,len(a)):
        c, _ = HornerChiaDaThuc(lap_bang_tich,a[i])
        list_of_c.append(c)
    return np.array(list_of_c)
    
def TinhCyLagrange(x: np.ndarray, y: np.ndarray):
    c = [0] * len(x)
    for i in range(0,len(y)):
        res = 1
        for j in range(0,len(x)):
            if i != j:
                res *= (x[i] - x[j])
        c[i] = y[i] / res
    return np.array(c)

def DaThucNoiSuyLagrange(a: np.ndarray, y: np.ndarray):
    A = LapBangThuongLagrange(a)[:, :-1]
    Cy = TinhCyLagrange(a,y)
    return Cy @ A

def TinhDyLagrangeMocCachDeu(n: int):
    res = np.zeros((n+1))
    for i in range(0,n+1):
        temp = 1
        for j in range(0,n+1):
            if j != i:
                temp *= (i - j)
        res[i] = 1 / temp
    return res

def LapBangTichLagrangeMocCachDeu(n: int):
    res = np.zeros((n+1))
    for i in range(1,n+1):
        res[i] = i
    return LapBangTichLagrange(res)

def LapBangThuongLagrangeMocCachDeu(n: int):
    list_of_c = []
    res = np.zeros((n+1))
    for i in range(1,n+1):
        res[i] = i
    
    lap_bang_tich = LapBangTichLagrangeMocCachDeu(n)[-1]
    for i in range(0,n+1):
        c, _ = HornerChiaDaThuc(lap_bang_tich,res[i])
        list_of_c.append(c)
    return np.array(list_of_c)

def DaThucNoiSuyLagrangeMocCachDeuThamSoT(y: np.ndarray,n: int):
    Dy = TinhDyLagrangeMocCachDeu(n)
    A = LapBangThuongLagrangeMocCachDeu(n)[: ,:-1]
    for i in range(0,len(A)):
        t = Dy[i] * y[i]
        for j in range(0,len(A)):
            A[i,j] *= t
    return np.sum(A, axis=0)

def DaThucNoiSuyLagrangeMocCachDeu(x: np.ndarray, y: np.ndarray, n: int, h: float):
    A = DaThucNoiSuyLagrangeMocCachDeuThamSoT(y, n)
    t = symbols('t')
    
    # Chuyển đổi mảng NumPy thành danh sách Python và áp dụng sympify
    A_list = [sympify(float(a)) for a in A[::-1]]
    
    # Tạo đa thức từ danh sách hệ số A_list
    poly = Poly(A_list, t)
    
    # Thay thế t bằng (1/h)*(x-x0)
    x_sym = symbols('x')
    x0 = float(x[0])  # Chuyển x[0] thành float
    substituted_poly = poly.as_expr().subs(t, (1/h)*(x_sym-x0))
    
    # Khai triển đa thức sau khi thay thế
    expanded_poly = expand(substituted_poly)
    
    # Chuyển đổi đa thức đã khai triển thành Poly object
    expanded_poly_obj = Poly(expanded_poly, x_sym)
    
    # Lấy các hệ số của đa thức
    coeffs = expanded_poly_obj.all_coeffs()
    
    # Chuyển đổi các hệ số thành số thực và tạo mảng NumPy
    numpy_coeffs = np.array([float(coeff) for coeff in coeffs])
    
    return numpy_coeffs