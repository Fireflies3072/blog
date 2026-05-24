---
title: Signal Processing Formula Sheet
date: 2023-11-07 15:43:17
tags: [signal]
categories: [Articles, Reference]
cover: https://cdn.fireflies3072.com/blog/2023-11-signal-processing/cover.webp
mathjax: true
excerpt: This is a concise Signal Formula Sheet containing essential formulas for Signals and Systems, covering system properties (Linear, Causal, Stable), convolution, Fourier Transforms (FT, FS, DTFT) pairs and properties, the Hilbert Transform, and Amplitude Modulation (AM) techniques.
---

## Basics

### Trig Identities

- $\cos(A) \cos(B) = \frac{1}{2}[\cos(A - B) + \cos(A + B)]$

### Basic Functions

- $\delta(t)=\begin{cases}\infty,&t=0\\0,&\text{otherwise}\end{cases}$
- $u(t)=\begin{cases}0,&t<0\\1,&t\ge 0\end{cases}$
- $\int_{-\infty}^{\infty}\delta(t)dt=1$
- $\frac{d}{dt}u(t) = \delta(t)$
- $\int_{-\infty}^{t} \delta(\tau) d\tau = u(t)$

### Sifting Property

- $\int_{-\infty}^{\infty}f(t)\delta(t-a)dt=f(a)$

### System Properties

- **Linear:** $a x_{1}(t)+b x_{2}(t) \rightarrow H \rightarrow a y_{1}(t)+b y_{2}(t)$
- **Time-Invariant:** $x(t-t_{o}) \rightarrow H \rightarrow y(t-t_{o})$
- **Causal:** Output does not depend on future input. For an LTI system, $h(t)=0$ for $t<0$ or $h[n]=0$ for $n<0$.
- **BIBO Stable:** $|x(t)|<\infty \Rightarrow |y(t)|<\infty$. For an LTI system:
  - Continuous-Time: $\int_{-\infty}^{\infty}|h(t)|dt<\infty$
  - Discrete-Time: $\sum_{n=-\infty}^{\infty}|h[n]|<\infty$

### Convolution

- **Continuous-Time:** $y(t)=x(t)*h(t)=\int_{-\infty}^{\infty}x(\tau)h(t-\tau)d\tau$
- **Discrete-Time:** $y[n]=x[n]*h[n]=\sum_{k=-\infty}^{\infty}x[k]h[n-k]$

### Differential & Difference Equations

- **Differential (CT):** $\sum_{k=0}^{N}a_{k}\frac{d^{k}}{dt^{k}}y(t)=\sum_{k=0}^{M}b_{k}\frac{d^{k}}{dt^{k}}x(t)$
  - System Function: $H(s)=\frac{\sum_{k=0}^{M}b_{k}s^{k}}{\sum_{k=0}^{N}a_{k}s^{k}}$
- **Difference (DT):** $\sum_{k=0}^{N}a_{k}y[n-k]=\sum_{k=0}^{M}b_{k}x[n-k]$, with $a_{0}=1$
  - System Function: $H(z)=\frac{\sum_{k=0}^{M}b_{k}z^{-k}}{\sum_{k=0}^{N}a_{k}z^{-k}}$

### Common Functions

- $\text{rect}(x)=\begin{cases} 1, & |x|\le \frac{1}{2} \\ 0, & \text{otherwise} \end{cases}$
- $\text{rect}(\frac{x}{2c})=\begin{cases} 1, & |x|\le c \\ 0, & \text{otherwise} \end{cases}$
- $\text{sinc}(t)=\frac{\sin(\pi t)}{\pi t}$

### Definitions

- **Inner product**
  - Periodic signal: $\langle x_T(t),y_T(t)\rangle=\frac{1}{T} \int_T x_T(t) y_T^*(t) dt=\sum_{k=-\infty}^{\infty} X[k] Y^*[k]$
  - Nonperiodic signal: $\langle x(t),y(t)\rangle=\int_{-\infty}^{\infty} x(t) y^*(t) dt=\int_{-\infty}^{\infty} X(f) Y^*(f) df$
  - Inner product with self: $||x(t)||=\langle x(t),x(t)\rangle=\int_{-\infty}^{\infty} |x(t)|^2 dt=\int_{-\infty}^{\infty} |X(f)|^2 df=\langle X(f),X(f)\rangle$



## Fourier Transform (FT)

### FT Pairs

| Time Domain                                                  | Frequency Domain                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $x(t) = \int_{-\infty}^{\infty} X(f) e^{j2\pi f t} df$       | $X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi f t} dt$      |
| $x(t) = \text{rect}\left(\frac{t}{2T}\right) = \begin{cases} 1, & |t|<T \\ 0, & \text{otherwise} \end{cases}$ | $X(f) = \frac{\sin(2\pi f T)}{\pi f}=2T\cdot \text{sinc}(2fT)$ |
| $x(t) = \frac{\sin(2\pi Wt)}{\pi t}=2W\cdot \text{sinc}(2Wt)$ | $X(f) = \text{rect}\left(\frac{f}{2W}\right) = \begin{cases} 1, & |f|<W \\ 0, & \text{otherwise} \end{cases}$ |
| $x(t) = \delta(t)$                                           | $X(f) = 1$                                                   |
| $x(t) = 1$                                                   | $X(f) = \delta(f)$                                           |
| $x(t) = u(t)$                                                | $X(f) = \frac{1}{j2\pi f} + \frac{1}{2}\delta(f)$            |
| $x(t) = e^{-at} u(t), \quad a > 0$                           | $X(f) = \frac{1}{a + j2\pi f}$                               |
| $x(t) = t e^{-at} u(t), \quad a > 0$                         | $X(f) = \frac{1}{(a + j2\pi f)^2}$                           |
| $x(t) = e^{-a|t|}, \quad a>0$                                | $X(f) = \frac{2a}{a^2 + (2\pi f)^2}$                         |
| $x(t) = \frac{1}{\sqrt{2\pi}} e^{-\frac{t^2}{2}}$            | $X(f) = e^{-\frac{(2\pi f)^2}{2}} = e^{-2\pi^2 f^2}$         |

### FT Properties

| Property                         | Transform                                                    |
| -------------------------------- | ------------------------------------------------------------ |
| **Linearity**                    | $ax(t)+by(t) \leftrightarrow aX(f)+bY(f)$                    |
| **Time Shift**                   | $x(t-t_{o}) \leftrightarrow e^{-j2\pi f t_{o}}X(f)$          |
| **Frequency Shift**              | $e^{j2\pi f_0 t}x(t) \leftrightarrow X(f-f_0)$               |
| **Scaling**                      | $x(at) \leftrightarrow \frac{1}{|a|}X(\frac{f}{a})$          |
| **Differentiation in Time**      | $\frac{d}{dt}x(t) \leftrightarrow j2\pi f X(f)$              |
| **Differentiation in Frequency** | $-jtx(t) \leftrightarrow \frac{1}{2\pi}\frac{d}{df}X(f)$     |
| **Integration**                  | $\int_{-\infty}^{t}x(\tau)d\tau \leftrightarrow \frac{1}{j2\pi f}X(f) + \frac{1}{2}X(0)\delta(f)$ |
| **Convolution-Multiplication**   | $x(t) * y(t) \leftrightarrow X(f)Y(f)$                       |
| **Multiplication-Convolution**   | $x(t)y(t) \leftrightarrow X(f) * Y(f)$                       |
| **Parseval's Theorem**           | $\int_{-\infty}^{\infty}{|x(t)|^2dt}=\int_{-\infty}^{\infty}{|X(f)|^2df}$ |

### Fourier Transform of Periodic Signals

| **Periodic Time Domain Signal**                     | **Fourier Transform X(f)**                                   |
| --------------------------------------------------- | ------------------------------------------------------------ |
| $x(t) \stackrel{FS; f_0}{\longleftrightarrow} X[k]$ | $X(f) = \sum_{k=-\infty}^{\infty} X[k]\delta(f - kf_0)$      |
| $x(t) = \cos(2\pi pf_0 t)$                          | $X(f) = \frac{1}{2}\delta(f + pf_0) + \frac{1}{2}\delta(f - pf_0)$ |
| $x(t) = \sin(2\pi pf_0 t)$                          | $X(f) = \frac{1}{2j}\delta(f - pf_0) - \frac{1}{2j}\delta(f + pf_0)$ |
| $x(t) = e^{j2\pi pf_0 t}$                           | $X(f) = \delta(f - pf_0)$                                    |
| $x(t) = \sum_{n=-\infty}^{\infty} \delta(t - nT_s)$ | $X(f) = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} \delta(f - \frac{k}{T_s})$ |



## Fourier Series (FS)

**Basis function:** $\phi_k(t) = e^{jk(2\pi F_0)t}$

### FS Pairs

| Time Domain                                                  | Frequency Domain                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $x(t) = \sum_{k=-\infty}^{\infty} X[k] e^{jk(2\pi F_0)t}$    | $X[k] = \langle x(t),\phi_k(t) \rangle = \frac{1}{T_0} \int_{\langle T_0\rangle} x(t)e^{-jk(2\pi F_0)t}dt \quad F_0 = \frac{1}{T_0}$ |
| $x(t) = \begin{cases} 1, & |t|\le T \\ 0, & T<|t|\le \frac{T_0}{2} &\end{cases}$ | $X[k]=\frac{\sin(k(2\pi F_0)T)}{k\pi}=2F_0T\cdot \text{sinc}(k\cdot 2 F_0T))$ |
| $x(t) = e^{jp(2\pi F_0)t}$                                   | $X[k] = \delta[k - p]$                                       |
| $x(t) = \cos(p(2\pi F_0)t)$                                  | $X[k] = \frac{1}{2}\delta[k - p] + \frac{1}{2}\delta[k + p]$ |
| $x(t) = \sin(p(2\pi F_0)t)$                                  | $X[k] = \frac{1}{2j}\delta[k - p] - \frac{1}{2j}\delta[k + p]$ |
| $x(t) = \sum_{p=-\infty}^{\infty} \delta(t - pT)$            | $X[k] = \frac{1}{T} = f_o$                                   |

### FS Properties

| Property                       | Transform                                                    |
| ------------------------------ | ------------------------------------------------------------ |
| **Linearity**                  | $ax(t)+by(t) \leftrightarrow aX[k]+bY[k]$                    |
| **Time Shift**                 | $x(t-t_{0}) \leftrightarrow e^{-jk2\pi f_{0}t_{0}}X[k]$      |
| **Frequency Shift**            | $e^{jk_{0}2\pi f_{0}t}x(t) \leftrightarrow X[k-k_{0}]$       |
| **Scaling**                    | $x(at) \leftrightarrow X[k]$ (with $f_0'=af_0$)              |
| **Differentiation in Time**    | $\frac{d}{dt}x(t) \leftrightarrow jk2\pi f_{0}X[k]$          |
| **Multiplication-Convolution** | $x(t)y(t) \leftrightarrow \sum_{p=-\infty}^{\infty}X[p]Y[k-p]$ |
| **Parseval's Theorem**         | $\frac{1}{T}\int_{\langle T\rangle}{|x(t)|^2dt}=\Sigma_{k=-\infty}^{\infty}{|X[k]|^2}$ |



## Discrete-Time Fourier Transform (DTFT)

### DTFT Pairs

| Time Domain                                                  | Frequency Domain                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $x[n] = \int_{\langle 1\rangle} X(e^{j2\pi\hat{f}}) e^{j2\pi\hat{f} n} d\hat{f}$ | $X(e^{j2\pi\hat{f}}) = \sum_{n=-\infty}^{\infty} x[n]e^{-j2\pi\hat{f} n}$ |
| $x[n] = \begin{cases} 1, & |n| \le M \\ 0, & \text{otherwise} \end{cases}$ | $X(e^{j2\pi\hat{f}}) = \frac{\sin[2\pi\hat{f}(\frac{2M+1}{2})]}{\sin(\frac{2\pi\hat{f}}{2})} = \frac{\sin(\pi\hat{f}(2M+1))}{\sin(\pi\hat{f})}$ |
| $x[n] = a^n u[n], \quad |a|<1$                               | $X(e^{j2\pi\hat{f}}) = \frac{1}{1-ae^{-j2\pi\hat{f}}}$       |
| $x[n] = \delta[n]$                                           | $X(e^{j2\pi\hat{f}}) = 1$                                    |
| $x[n] = u[n]$                                                | $X(e^{j2\pi\hat{f}}) = \frac{1}{1-e^{-j2\pi\hat{f}}} + \frac{1}{2} \sum_{p=-\infty}^{\infty} \delta(\hat{f} - p)$ |
| $x[n] = \frac{\sin(2\pi Wn)}{\pi n} = 2W\cdot \text{sinc}(2Wn), \quad 0 < W \le \frac{1}{2}$ | $X(e^{j2\pi\hat{f}}) = \text{rect}(\frac{\hat{f}}{2W}) = \begin{cases} 1,&|\hat{f}|<W \\ 0,&\text{otherwise} \end{cases}$ |
| $x[n] = (n+1)a^n u[n]$                                       | $X(e^{j2\pi\hat{f}}) = \frac{1}{(1-ae^{-j2\pi\hat{f}})^2}$   |

### DTFT Properties

| Property                         | Transform                                                    |
| -------------------------------- | ------------------------------------------------------------ |
| **Linearity**                    | $ax[n]+by[n] \leftrightarrow aX(e^{j2\pi\hat{f}})+bY(e^{j2\pi\hat{f}})$ |
| **Time Shift**                   | $x[n-n_0] \leftrightarrow e^{-j2\pi\hat{f} n_0}X(e^{j2\pi\hat{f}})$ |
| **Frequency Shift**              | $e^{j2\pi\gamma n}x[n] \leftrightarrow X(e^{j2\pi(\hat{f}-\gamma)})$ |
| **Differentiation in Frequency** | $-j2\pi nx[n] \leftrightarrow \frac{d}{df}X(e^{j2\pi\hat{f}})$ |
| **Convolution-Multiplication**   | $x[n] * y[n] \leftrightarrow X(e^{j2\pi\hat{f}})Y(e^{j2\pi\hat{f}})$ |
| **Multiplication-Convolution**   | $x[n]y[n] \leftrightarrow \int_{-\frac{1}{2}}^{\frac{1}{2}}X(e^{j2\pi\gamma})Y(e^{j2\pi(\hat{f}-\gamma)})d\gamma$ |
| **Parseval's Theorem**           | $\sum_{n=-\infty}^{\infty}{|x[n]|^2}=\int_{-\frac{1}{2}}^{\frac{1}{2}}{|X(e^{j2\pi\hat{f}})|^2d\hat{f}}$ |

### Discrete-Time Fourier Transform of Periodic signals

| **Periodic Time Domain Signal**                              | **Discrete-Time Fourier Transform**                          |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $x[n] = \cos(2\pi \hat{f}_0 n), \quad |\hat{f}_0|<\frac{1}{2}$ | $X(e^{j2\pi\hat{f}}) = \frac{1}{2}\delta(\hat{f} + \hat{f}_0) + \frac{1}{2}\delta(\hat{f} - \hat{f}_0), \quad |\hat{f}|< \frac{1}{2}$ |
| $x[n] = \sin(2\pi \hat{f}_0 n), \quad |\hat{f}_0|<\frac{1}{2}$ | $X(e^{j2\pi\hat{f}}) = \frac{1}{2j}\delta(\hat{f} - \hat{f}_0) - \frac{1}{2j}\delta(\hat{f} + \hat{f}_0), \quad|\hat{f}|< \frac{1}{2}$ |
| $x[n] = e^{j2\pi\hat{f}_0 n}, \quad |\hat{f}_0|<\frac{1}{2}$ | $X(e^{j2\pi\hat{f}}) = \delta(\hat{f} - \hat{f}_0), \quad |\hat{f}|< \frac{1}{2}$ |



## Sampling Theorem



## Laplace Transform



## Z-Transform





## Hilbert Transform

### Definition

The Hilbert Transform of $x(t)$ is denoted $\hat{x}(t)$ or $\mathcal{H}\{x(t)\}$.

**Time domain**

$h(t) = \frac{1}{\pi t}$

$\hat{x}(t) = x(t) * h(t) = \frac{1}{\pi} \int_{-\infty}^{\infty} \frac{x(\tau)}{t-\tau} d\tau$

**Frequency domain**

$H(f) = -j \cdot \text{sgn}(f)$

$\hat{X}(f) = X(f) \cdot H(f) = -j\cdot \text{sgn}(f)X(f) = \begin{cases} -jX(f), & f > 0 \\ jX(f), & f < 0 \\ 0, & f = 0 \end{cases}$

This applies a **-90° phase shift** to all positive frequency components and a **+90° phase shift** to all negative frequency components.

### Properties

- **Linearity:** $\mathcal{H}\{a x_1(t) + b x_2(t)\} = a \hat{x}_1(t) + b \hat{x}_2(t)$
- **Double Transform:** $\hat{\hat{x}}(t) = \mathcal{H}\{\mathcal{H}\{x(t)\}\} = -x(t)$
- **Orthogonality:** $\int_{-\infty}^{\infty} x(t)\hat{x}(t)dt = 0$
- **Energy Preservation:** $\int_{-\infty}^{\infty} |x(t)|^2 dt = \int_{-\infty}^{\infty} |\hat{x}(t)|^2 dt$
- **Bedrosian Theorem:** $\mathcal{H}\{m(t)x(t)\} = m(t)\hat{x}(t)$
  - $m(t)$ is a lowpass signal and $x(t)$ is a bandpass signal. Their bands don't overlap.
- **Common Pairs:**
  - $\mathcal{H}\{\cos(2\pi f_c t)\} = \sin(2\pi f_c t)$
  - $\mathcal{H}\{\sin(2\pi f_c t)\} = -\cos(2\pi f_c t)$
- **Analytic Signal**
  - $z(t)=x_a(t) = x(t) + j\hat{x}(t)$
  - $Z(f) = X(f) + j \cdot \hat{X}(f) = X(f) + (-j^2) \cdot \text{sgn}(f) \cdot X(f) = X(f)[1+\text{sgn}(f)]$
  - $Z(f) = \begin{cases} 2X(f) & \text{if } f > 0 \\ X(f) & \text{if } f = 0 \\ 0 & \text{if } f < 0 \end{cases}$



## Amplitude Modulation (AM)

### Double-Sideband, Suppressed Carrier AM (DSB-SC)

**Modulation**

$c(t)=A_c \cos(2\pi f_c t + \phi_c)$

$u(t) = m(t) c(t) = A_c m(t) \cos(2\pi f_c t + \phi_c)$

$U(f) = \frac{A_c}{2} [M(f - f_c)e^{j\phi_c} + M(f + f_c)e^{-j\phi_c}]$

**Demodulation**

$u(t) \cos(2\pi f_c t + \phi) = \frac{1}{2} A_c m(t) \cos(\phi_c - \phi) + \frac{1}{2} A_c m(t) \cos(4\pi f_c t + \phi + \phi_c)$

$\text{LP}\{u(t) \cos(2\pi f_c t + \phi)\} = \frac{1}{2} A_c m(t) \cos(\phi_c - \phi)$

**Power**

$P_u = \frac{A_c^2}{2}P_m$



### Double-Sideband, Transmitted Carrier AM (DSB-TC / Conventional AM)

**Modulation**

$m_n(t) = \frac{m(t)}{\max|m(t)|}$

$u(t) = A_c [1 + m(t)] \cos(2\pi f_c t) \quad |m(t)|<1$

$u(t) = A_c [1 + a m_n(t)] \cos (2\pi f_c t + \phi_c)$

$U(f) = \frac{A_c}{2} [e^{j\phi_c} a M_n(f - f_c) + e^{j\phi_c} \delta(f - f_c) + e^{-j\phi_c} a M_n(f + f_c) + e^{-j\phi_c} \delta(f + f_c)]$

**Demodulation**

$r(t)$ is rectified signal. It brings the band centered from $f_c$ and $-f_c$ back to $0$ and create harmonics.

- Half-wave rectification: $r(t) = \begin{cases} u(t) & \text{for } u(t) \ge 0 \\ 0 & \text{for } u(t) < 0 \end{cases}$

  > Create harmonics around $nf_c$

- Full-wave rectification: $r(t)=|r(t)|$

  > Create harmonics around $2nf_c$

$d(t) = \text{LP}\{r(t)\} = g_1 + g_2 m(t)$

$m(t)=\frac{d(t)-g_1}{g_2}$

**Power**

$P_u = \frac{A_c^2}{2} + \frac{A_c^2}{2} a^2 P_{m_n} = \frac{A_c^2}{2} + \frac{A_c^2}{2} a^2 \left[ \frac{P_m}{(\max|m(t)|)^2} \right]$

$P_u=\frac{A_c^2}{2} + \frac{A_c^2}{2} P_{m} \quad a=1$



### Single-Sideband AM (SSB)

**Modulation**

$u(t) = A_c m(t) \cos(2\pi f_c t) \mp A_c \hat{m}(t) \sin(2\pi f_c t)$

- Minus sign ($-$) results in the Upper Sideband (USB) signal.
- Plus sign ($+$) results in the Lower Sideband (LSB) signal.

**Demodulation**

$u(t) \cos(2\pi f_c t + \phi) = \frac{1}{2} A_c m(t) \cos (\phi) + \frac{1}{2} A_c \hat{m}(t) \sin (\phi) + \text{double frequency terms}$

$y_\ell(t) = \text{LP}\{u(t) \cos(2\pi f_c t + \phi)\} = \frac{1}{2} A_c m(t) \cos (\phi) + \frac{1}{2} A_c \hat{m}(t) \sin (\phi)$

$y_\ell(t) = \frac{1}{2} A_c m(t) \quad \phi=0$



### Vestigial-Sideband AM (VSB)
