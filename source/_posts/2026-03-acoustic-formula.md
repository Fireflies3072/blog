---
title: Electro-Acoustical Engineering Formula Sheet
date: 2026-03-19 20:32:45
tags: [signal]
categories: [Articles, Reference]
cover: https://cdn.fireflies3072.com/blog/2026-03-acoustic-formula/cover.jpg
mathjax: true
excerpt: A comprehensive formula sheet for electro-acoustical engineering, covering fundamental wave parameters, wave equations, acoustic impedance, power, intensity, and spatial modulation.
---

## Fundamental Wave Parameters

| Parameter | Symbol | Relations | Units |
| :--- | :---: | :--- | :---: |
| **Speed of Sound** | $c$ | $c = \frac{\omega}{k} = f\lambda = \frac{\lambda}{T}$ | m/s |
| **Wavenumber** | $k$ | $k = \frac{2\pi}{\lambda} = \frac{\omega}{c} = \frac{2\pi f}{c}$ | rad/m |
| **Wavelength** | $\lambda$ | $\lambda = \frac{2\pi}{k} = \frac{c}{f} = cT$ | m |
| **Angular Freq.** | $\omega$ | $\omega = 2\pi f = \frac{2\pi}{T} = ck$ | rad/s |
| **Frequency** | $f$ | $f = \frac{\omega}{2\pi} = \frac{1}{T} = \frac{c}{\lambda} = \frac{ck}{2\pi}$ | Hz |
| **Period** | $T$ | $T = \frac{1}{f} = \frac{2\pi}{\omega} = \frac{\lambda}{c} = \frac{2\pi}{ck}$ | s |

## Wave Equations & Solutions

### 1-D Sinusoidal Waves
- **Forward Propagating:** $g(x, t) = A \sin(kx - \omega t) = A \sin[k(x - ct)]$
- **Backward Propagating:** $g(x, t) = A \sin(kx + \omega t) = A \sin[k(x + ct)]$
- **General Wave Equation:** $\frac{\partial^2 g}{\partial x^2} - \frac{1}{c^2} \frac{\partial^2 g}{\partial t^2} = 0$

### Waves on a String
- **Wave Speed:** $c = \sqrt{\frac{T}{\rho_L}}$ ($T$: tension, $\rho_L$: linear density $\rho A$)
- **Wave Equation:** $\frac{\partial^2 y}{\partial x^2} - \frac{\rho A}{T} \frac{\partial^2 y}{\partial t^2} = 0$
- **Fixed Ends (Length $L$):**
  - **Solution:** $y(x, t) = \sum_{n=1}^{\infty} A_n \sin(k_n x) \cos(\omega_n t)$
  - **Modes:** $k_n = \frac{n\pi}{L}$, $\lambda_n = \frac{2L}{n}$, $f_n = \frac{n}{2L}c$ ($n = 1, 2, 3, \dots$)

### Waves in Tubes
- **Conservation of Mass:** $\frac{\partial \rho_1}{\partial t} = -\frac{\rho_0}{A} \frac{\partial U_1}{\partial x}$
- **Newton’s Law (Euler):** $\rho_0 \frac{\partial U_1}{\partial t} = -A \frac{\partial p_1}{\partial x}$
- **Resonant Frequencies ($f_n$):**
  - **Open-Open / Closed-Closed:** $f_n = \frac{nc}{2l}$
  - **Open-Closed:** $f_n = \frac{(2n-1)c}{4l}$

## Acoustic Impedance & Lumped Elements

- **Acoustic Impedance:** $Z = \frac{p}{U}$
- **Specific Acoustic Impedance:** $z = \rho_0 c$
- **Short Tubes ($L \ll \lambda/4$):**
  - **Acoustic Mass (Inductor):** $M_A = \frac{\rho_0 L}{A} \implies Z = j\omega M_A$
  - **Acoustic Compliance (Capacitor):** $C_A = \frac{AL}{\rho_0 c^2} \implies Z = \frac{1}{j\omega C_A}$
  - **Acoustic Resistance (Resistor):** $R = \frac{\rho_0 c}{A}$ (Long tube termination)

### Helmholtz Resonator ($A_B / A_F \gg 1$)
- **Front/Back Resonance:** $F_n = \frac{nc}{2L_F}$, $B_n = \frac{nc}{2L_B}$
- **Helmholtz Resonance:** $F_H = \frac{c}{2\pi} \sqrt{\frac{A_F / A_B}{L_F L_B}}$

## Power, Intensity & Decibels

- **Acoustic Intensity ($I$):** $I = \frac{p^2}{\rho_0 c}$ (Plane wave)
- **Acoustic Power ($W$):** $W = \oint \vec{I} \cdot d\vec{S}$
- **Spherical Wave (Point Source):**
  - **Pressure:** $p(r, t) = \frac{A}{r} e^{j(kr - \omega t)} \implies |p|^2 = \frac{A^2}{r^2}$
  - **Intensity:** $I = \frac{W}{4\pi r^2} = \frac{A^2}{\rho_0 c r^2}$
  - **Power:** $W = \frac{4\pi A^2}{\rho_0 c}$
  - **Source Strength:** $A^2 = \frac{W \rho_0 c}{4\pi} = I \rho_0 c r^2$

### Decibels & Sonar Equation
- **Sound Power Level (PWL):** $L_W = 10 \log_{10}\left(\frac{W}{W_{ref}}\right)$
- **Sound Pressure Level (SPL):** $L_p = 10 \log_{10}\left|\frac{p}{p_{ref}}\right|^2 = L_S - H$
- **Source Level (SL):** $L_S = 10 \log_{10}\left(\frac{A^2}{r_{ref}^2 p_{ref}^2}\right)$
- **Transmission Loss (TL):** $H = 10 \log_{10}\left(\frac{r^2}{r_{ref}^2}\right)$
- **Reference Values:**
  - **Reference power:** $W_{ref} = 1 \text{ W}$
  - **Reference distance:** $r_{ref} = 1 \text{ m}$
  - **Reference pressure (Air):** $p_{ref} = 20 \mu\text{Pa} = 2 \times 10^{-5} \text{ Pa}$
  - **Reference pressure (Water):** $p_{ref} = 1 \mu\text{Pa} = 10^{-6} \text{ Pa}$

## 2D/3D Waves & Spatial Modulation

- **2D/3D Plane Wave:** $p = A e^{j(\vec{k} \cdot \vec{r} - \omega t)}$, $|\vec{k}|^2 = k_x^2 + k_y^2 + k_z^2 = (\omega/c)^2$
- **Snell's Law:** $k_{x,inc} = k_{x,refl} = k_{x,trans} \implies \frac{\sin \theta_1}{c_1} = \frac{\sin \theta_2}{c_2}$
- **Normal Incidence Interface:**
  - **Reflection:** $R = \frac{Z_2 - Z_1}{Z_2 + Z_1}$
  - **Transmission:** $T = \frac{2Z_2}{Z_2 + Z_1} = 1 + R$
  - **Energy:** $R_E = R^2$, $T_E = 1 - R^2$

### Spatial Modulation ($p_{out} = p_{in} \cdot t(x)$)
- **Transfer Function:** $t(x) = e^{j\phi(x)}$
- **Wave Steering:** $\phi(x) = (k_{x,out} - k_{x,in})x = k_0 x(\sin(\theta_{out})-\sin(\theta_{in}))$
- **Wave Focusing at $(x_0=0,z_0)$:** $\phi(x) = \frac{2\pi}{\lambda} (z_0 - \sqrt{z_0^2 + x^2}) \approx -\frac{\pi}{\lambda z_0} x^2$
- **Wave Focusing at $(x_0\neq 0,z_0)$:** $\phi(x) = \frac{2\pi}{\lambda} (z_0 - \sqrt{z_0^2 + (x-x_0)^2}) \approx -\frac{\pi}{\lambda z_0} x^2 + \frac{2\pi x_0}{\lambda z_0} x$
- **Diffraction Grating:** $d \sin \theta = m\lambda$
- **Sinusoidal Amplitude Grating:** $T(x) = \frac{1}{2}[1 + \cos(\frac{2\pi}{d}x)] \implies 0, \pm 1$ orders
- **Sinusoidal Phase Grating:** $T(x) = \exp[j A \sin(\frac{2\pi}{d}x)] = \sum_{m=-\infty}^{\infty} J_m(A) \exp(j m \frac{2\pi}{d}x)$
