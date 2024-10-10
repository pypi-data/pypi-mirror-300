import numpy as np
import sympy as sp
import math
from HUST_PPS import LapBangTichLagrange, DaThucNoiSuyLagrangeMocCachDeu
from sympy import symbols, Poly, expand, sympify

def TinhTySaiPhan(x: np.ndarray, y: np.ndarray):
    k = len(x) - 1
    zero_matrix = np.zeros((len(x), k + 2))
    zero_matrix[:, 0] = x
    zero_matrix[:, 1] = y
    cnt = 1
    for i in range(1, len(x)):
        index = i - 1
        for j in range(2, 2 + cnt):
            zero_matrix[i, j] = (zero_matrix[i, j - 1] - zero_matrix[i - 1, j - 1]) / (x[i] - x[index])
            index -= 1
        cnt += 1
    return np.array(zero_matrix)

class Term:
    def __init__(self, coefficient, factors):
        self.coefficient = coefficient
        self.factors = factors

    def __str__(self):
        if len(self.factors) == 0:
            return str(self.coefficient)
        factors_str = '*'.join(f'(X - {factor})' for factor in self.factors)
        if self.coefficient == 1:
            return factors_str
        elif self.coefficient == -1:
            return f'-{factors_str}'
        else:
            return f'{self.coefficient}*{factors_str}'

class Polynomial:
    def __init__(self):
        self.terms = []

    def add_term(self, coefficient, factors):
        self.terms.append(Term(coefficient, factors))

    def __str__(self):
        return ' + '.join(str(term) for term in self.terms).replace('+ -', '- ')

def convert_to_float(value):
    if isinstance(value, (np.float64, np.float32, float)):
        return float(value)
    else:
        return value  

def DaThucNoiSuyNewton2(a: np.ndarray, b: np.ndarray):
    a = np.array([convert_to_float(ai) for ai in a])
    b = np.array([convert_to_float(bi) for bi in b])
    
    polynomial = Polynomial()
    polynomial.add_term(b[0], [])
    
    zero_matrix = TinhTySaiPhan(a, b)
    
    for i in range(1, len(a)):
        coefficient = zero_matrix[i, i+1]
        factors = a[:i].tolist()  
        polynomial.add_term(coefficient, factors)
    
    simplified_polynomial = sp.simplify(str(polynomial)) 
    
    return polynomial, simplified_polynomial

def TinhCiNewton(x: np.ndarray, y:np.ndarray):
    ty_sai_phan = TinhTySaiPhan(x,y)
    C = []
    for i in range(0,len(x)):
        C.append(ty_sai_phan[i,i+1])
    return np.array(C)

def DaThucNoiSuyNewton(x: np.ndarray, y:np.ndarray):
    C = TinhCiNewton(x,y)
    # Xóa đi phần tử cuối
    x1 = x[0:len(x)-1]
    A = LapBangTichLagrange(x1)
    return C @ A

def SaiPhanTien(y: np.ndarray, k, s):
    if s == 1:
        return y[k+1] - y[k]
    return SaiPhanTien(y,k+1,s-1) - SaiPhanTien(y,k,s-1)

def SaiPhanLui(y: np.ndarray, k, s):
    if s == 1:
        return y[k] - y[k-1]
    return SaiPhanLui(y,k,s-1) - SaiPhanLui(y,k-1,s-1)

def TinhBangSaiPhan(x: np.ndarray, y: np.ndarray):
    k = len(x) - 1
    zero_matrix = np.zeros((len(x), k + 2))
    zero_matrix[:, 0] = x
    zero_matrix[:, 1] = y
    cnt = 1
    for i in range(1, len(x)):
        for j in range(2, 2 + cnt):
            zero_matrix[i,j] = zero_matrix[i,j-1] - zero_matrix[i-1,j-1]
        cnt += 1
    return np.array(zero_matrix)

def LapBangTichNewtonMocCachDeu(n: int):
    res = np.zeros(n)
    for i in range(1,n):
        res[i] = i
    return LapBangTichLagrange(res)

def TinhCyNewtonMocCachDeu(x: np.ndarray, y:np.ndarray):
    list_of_c = []
    zero_matrix = TinhBangSaiPhan(x,y)
    for i in range(0, len(x)):
        list_of_c.append(zero_matrix[i,i+1])
    for i in range(0,len(list_of_c)):
        list_of_c[i] /= math.factorial(i)
    return np.array(list_of_c)

def DaThucNoiSuyNewtonMocCachDeuThamSoT(x: np.ndarray, y:np.ndarray):
    A = LapBangTichNewtonMocCachDeu(len(x)-1)
    B = TinhCyNewtonMocCachDeu(x,y)
    
    return B @ A

def DaThucNoiSuyNewtonMocCachDeu(x: np.ndarray, y:np.ndarray, n:int, h:float):
    A = DaThucNoiSuyNewtonMocCachDeuThamSoT(y, n)
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