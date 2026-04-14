import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Fourier Series Tool", layout="centered")

st.title("🔥 Fourier Series Tool ")
st.caption("Created by Sujith E — Engineering Student Project")

st.markdown("🔗 GitHub: https://github.com/sujith0718-coder")

# ---------- INPUT CONVERTER ----------
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


# ---------- FUNCTION ----------
def f(x, expr, L):
    xp = ((x + L) % (2 * L)) - L
    return eval(expr, {"x": x, "xp": xp, "np": np})


# ---------- FOURIER ----------
def a0(expr, L):
    x = np.linspace(-L, L, 1000)
    return (1 / (2 * L)) * np.trapezoid(f(x, expr, L), x)

def an(n, expr, L):
    x = np.linspace(-L, L, 1000)
    return (1 / L) * np.trapezoid(f(x, expr, L) * np.cos(n * np.pi * x / L), x)

def bn(n, expr, L):
    x = np.linspace(-L, L, 1000)
    return (1 / L) * np.trapezoid(f(x, expr, L) * np.sin(n * np.pi * x / L), x)

def fourier_sum(x, N, expr, L):
    S = a0(expr, L)
    for n in range(1, N + 1):
        S += an(n, expr, L) * np.cos(n * np.pi * x / L) + bn(n, expr, L) * np.sin(n * np.pi * x / L)
    return S


# ---------- UI CONTROLS ----------
user_expr = st.text_input("Enter function (square, triangle, x, sin(x), etc.)", "square")

T = st.slider("Period (T)", 1.0, 10.0, 2.0)
max_N = st.slider("Max Fourier terms (N)", 1, 50, 10)

mode = st.radio("Mode", ["Compare", "Interactive"])

expr = convert_input(user_expr)
L = T / 2

x = np.linspace(-L, L, 1000)
fx = f(x, expr, L)

fig, ax = plt.subplots()

# ---------- COMPARE MODE ----------
if mode == "Compare":
    ax.plot(x, fx, 'k', label="Original f(x)")

    for n in [1, 2, 3, 5, max_N]:
        if n <= max_N:
            ax.plot(x, fourier_sum(x, n, expr, L), label=f"S{n}")

    ax.set_title("Fourier Series Comparison")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

# ---------- INTERACTIVE MODE ----------
else:
    N = st.slider("Choose N", 1, max_N, 1)

    ax.plot(x, fx, 'k', label="Original f(x)")
    ax.plot(x, fourier_sum(x, N, expr, L), 'r', label=f"S{N}")

    ax.set_title("Fourier Series Approximation")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
