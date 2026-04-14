import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🔥 Fourier Series Tool (Your Project)")

# ---------- INPUT ----------
user_expr = st.text_input("Enter function (type help or square, triangle, etc.)")

# ---------- HELP ----------
if user_expr.lower() == "help":
    st.write("""
### Allowed Inputs:
- x, x^2, x^3
- |x|
- sin(x), cos(x), tan(x)
- exp(x), log(x)

### Piecewise:
- np.where(x < 0, -1, 1)

### Predefined:
- square
- triangle
- sawtooth
""")

# ---------- CONVERT ----------
def convert_input(expr):
    expr = expr.replace("^", "**")
    expr = expr.replace("|x|", "abs(x)")
    expr = expr.replace("sin", "np.sin")
    expr = expr.replace("cos", "np.cos")
    expr = expr.replace("tan", "np.tan")
    expr = expr.replace("exp", "np.exp")
    expr = expr.replace("log", "np.log")

    if expr.lower() == "square":
        return "np.where(xp < 0, -1, 1)"
    elif expr.lower() == "triangle":
        return "abs(xp)"
    elif expr.lower() == "sawtooth":
        return "xp"

    return expr

# ---------- ONLY RUN IF INPUT EXISTS ----------
if user_expr and user_expr.lower() != "help":

    expr = convert_input(user_expr)

    T = st.number_input("Enter period T", value=6.28)
    max_N = st.slider("Max N", 1, 20, 10)
    N = st.slider("Select N (Fourier terms)", 1, max_N, 5)

    L = T / 2

    # ---------- FUNCTION ----------
    def f(x, expr, L):
        xp = ((x + L) % (2*L)) - L
        return eval(expr, {"x": x, "xp": xp, "np": np})

    # ---------- FOURIER ----------
    def a0(expr, L):
        x = np.linspace(-L, L, 1000)
        return (1/(2*L)) * np.trapezoid(f(x, expr, L), x)

    def an(n, expr, L):
        x = np.linspace(-L, L, 1000)
        return (1/L) * np.trapezoid(f(x, expr, L)*np.cos(n*np.pi*x/L), x)

    def bn(n, expr, L):
        x = np.linspace(-L, L, 1000)
        return (1/L) * np.trapezoid(f(x, expr, L)*np.sin(n*np.pi*x/L), x)

    def fourier_sum(x, N, expr, L):
        S = a0(expr, L)
        for n in range(1, N+1):
            S += an(n, expr, L)*np.cos(n*np.pi*x/L) + bn(n, expr, L)*np.sin(n*np.pi*x/L)
        return S

    # ---------- DATA ----------
    x = np.linspace(-L, L, 1000)
    fx = f(x, expr, L)
    approx = fourier_sum(x, N, expr, L)

    # ---------- PLOT ----------
    fig, ax = plt.subplots()

    ax.plot(x, fx, 'k', label="f(x)")
    ax.plot(x, approx, 'r', label=f"S{N}")

    ax.legend()
    ax.grid()

    st.pyplot(fig)
