#!/usr/bin/env python3
"""Conditional OPH-inspired discrete overlap wave limit.

Periodic 3D cubic lattice, source manufactured from smooth exact solution.
This is NOT the canonical OPH repair dynamics, and does not derive EFMW physics.
No third-party dependencies beyond NumPy.
"""
import math
import numpy as np

C = 1.0
L = 1.0
K = 2.0 * math.pi / L
OMEGA = 0.8 * C * K * math.sqrt(3)
T_FINAL = 0.5

def test_resolution(n):
    h = L / n
    steps = math.ceil(T_FINAL / (0.4 * h / C))
    dt = T_FINAL / steps
    coords = np.arange(n, dtype=float) * h
    f = np.sin(K * coords)
    spatial = f[:, None, None] * f[None, :, None] * f[None, None, :]
    def exact(t):
        return spatial * math.cos(OMEGA * t)
    def S(t):
        # phi_tt = c^2 Laplacian(phi) - 4*pi*S, exactly.
        return ((OMEGA**2 - 3*(C*K)**2) / (4*math.pi)) * exact(t)
    def lap(u):
        return sum((np.roll(u, 1, axis=d) - 2*u + np.roll(u, -1, axis=d)) / h**2
                   for d in range(3))
    u0 = exact(0)
    u_prev = u0.copy()
    u_curr = u0 + 0.5 * dt*dt * (C*C * lap(u0) - 4*math.pi * S(0))
    for step in range(1, steps):
        t = step * dt
        next_u = (2*u_curr - u_prev + dt*dt*(C*C*lap(u_curr) - 4*math.pi*S(t)))
        u_prev, u_curr = u_curr, next_u
    error = math.sqrt(float(np.mean((u_curr - exact(T_FINAL))**2)))
    # Conservative L2/RMS global bound from Fourier-stable recurrence and Taylor remainders.
    M_t3 = OMEGA**3
    M_t4 = OMEGA**4
    sum_M_x4 = 3*K**4
    start_err = (dt**3/6)*M_t3 + (C*C*dt*dt*h*h/24)*sum_M_x4
    residual = (dt*dt/12)*M_t4 + (C*C*h*h/12)*sum_M_x4
    error_bound = (T_FINAL/dt)*start_err + (T_FINAL**2/2)*residual
    cfl = C*dt/h
    assert math.sqrt(3)*cfl < 1
    assert error <= error_bound + 1e-12
    return n, steps, h, dt, cfl, error, error_bound

if __name__ == '__main__':
    data = [test_resolution(n) for n in [12, 18, 24, 36, 48]]
    print('N steps h dt CFL RMS_error rigorous_conservative_bound')
    for r in data:
        print('%2d %3d %.7f %.7f %.4f %.9f %.6f' % r)
    orders = [math.log(a[5]/b[5])/math.log(a[2]/b[2]) for a,b in zip(data[:-1],data[1:])]
    print('observed_spatial_refinement_orders:', [round(x,3) for x in orders])
    assert all(x > 1.75 for x in orders), 'Expected near-second-order convergence'
    print('TEST PASS: 3D sourced wave, stable CFL, error below stated bound, near-quadratic refinement')
