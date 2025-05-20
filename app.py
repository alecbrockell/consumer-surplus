import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── PARAMETERS ──
Q_eq, P_eq = 10, 50    # original equilibrium
P_new      = 40        # new, lower price
Q_max      = 40        # x-axis limit

st.markdown("""
## 💡 Consumer Welfare and Demand

This app visualizes **consumer surplus** under a linear demand curve that always pivots through the same initial consumption bundle (Q = 10, P = 50). Use the slider to change the **slope of the demand curve** (i.e., elasticity) and see how:

- The **original CS** and the **additional CS** from a price drop (from 50 to 40) change
- The **shape** of the demand curve affects total consumer welfare, even with the same price drop
""")

# ── SLIDER ──
s = st.slider("Slope of Demand Curve", 0.5, 5.0, 1.0, 0.1)

# ── CALCULATIONS ──
b = P_eq + s * Q_eq                      # demand intercept for pivot
orig_cs = 0.5 * s * Q_eq**2              # original CS up to Q_eq

# where demand hits the new price
Q_new = (b - P_new) / s                  

# additional CS = rectangle + triangle from Q_eq→Q_new
rect_cs = (P_eq - P_new) * Q_eq
tri_cs  = (
    b * (Q_new - Q_eq)
    - 0.5 * s * (Q_new**2 - Q_eq**2)
    - P_new * (Q_new - Q_eq)
)
add_cs   = rect_cs + tri_cs              # now defined!
total_cs = orig_cs + add_cs              # and total CS

# ── DISPLAY NUMBERS ──
st.markdown(
    f"""
    <div style="text-align: center; font-size:14px; line-height:1.1; margin-bottom: -30px;">
      <p><strong>Demand Curve:</strong> P = {b:.1f} – {s:.1f}·Q</p>
      <p><strong>Original Consumer Surplus:</strong> {orig_cs:.1f}</p>
      <p><strong>Additional Consumer Surplus:</strong> {add_cs:.1f}</p>
      <p><strong>Total Consumer Surplus:</strong> {total_cs:.1f}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ── PREPARE PLOTTING DATA ──
Q  = np.linspace(0, Q_max, 400)
Pd = b - s * Q
Qc = Q[Q <= Q_eq]
Qa = Q[(Q >= Q_eq) & (Q <= Q_new)]

# ── BUILD FIGURE ──
fig = go.Figure()

# Demand
fig.add_trace(go.Scatter(x=Q, y=Pd, mode='lines', name='Demand'))

# Original Price
fig.add_trace(go.Scatter(
    x=[0, Q_max], y=[P_eq, P_eq],
    mode='lines', name='Original Price',
    line=dict(dash='dash')
))

# New Price
fig.add_trace(go.Scatter(
    x=[0, Q_max], y=[P_new, P_new],
    mode='lines', name='New Price',
    line=dict(color='purple', dash='dot')
))

# Original CS polygon
fig.add_trace(go.Scatter(
    x=np.concatenate([Qc, Qc[::-1]]),
    y=np.concatenate([b - s*Qc, np.full_like(Qc, P_eq)]),
    fill='toself', name='Original Consumer Surplus', opacity=0.4
))

# 1) Rectangle part of Additional CS (0 → Q_eq, P_eq → P_new)
fig.add_trace(go.Scatter(
    x=[0, Q_eq, Q_eq, 0],
    y=[P_eq, P_eq, P_new, P_new],
    fill='toself',
    name='Additional Consumer Surplus',
    fillcolor='purple',
    line=dict(color='purple'),
    opacity=0.4,
))

# 2) Triangle part of Additional CS (Q_eq → Q_new under demand)
if Q_new > Q_eq:
    # sample the demand curve between Q_eq and Q_new
    Qt = np.linspace(Q_eq, Q_new, 200)
    Pt = b - s * Qt
    fig.add_trace(go.Scatter(
        x=np.concatenate([Qt, Qt[::-1]]),
        y=np.concatenate([Pt, np.full_like(Qt, P_new)]),
        fill='toself',
        showlegend=False,   # only show one legend item for purple
        fillcolor='purple',
        line=dict(color='purple'),
        opacity=0.4,
    ))

# Lock axes at 0–40 & 0–100
fig.update_layout(
    xaxis=dict(range=[0, Q_max], autorange=False, fixedrange=True, title="Quantity"),
    yaxis=dict(range=[0, 100],  autorange=False, fixedrange=True, title="Price"),
    
    # ← New legend settings:
    legend=dict(
        orientation="h",     # horizontal legend
        yanchor="top",
        y=-0.2,              # move it below the plot (tweak as needed)
        xanchor="center",
        x=0.5                # center horizontally
    ),
    
    width=800, height=600
)

st.plotly_chart(fig)
