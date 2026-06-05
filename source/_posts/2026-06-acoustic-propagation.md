---
title: Acoustic Wave Propagation in 2D Space
date: 2026-06-04 21:36:08
tags: [acoustics, math]
categories: [Articles]
cover: https://cdn.fireflies3072.com/blog/2026-06-acoustic-propagation/cover.jpg
mathjax: true
excerpt: An in-depth look at 2D acoustic wave propagation, exploring the angular spectrum method, propagation operators in frequency and spatial domains, and single-slit diffraction.
---

## Introduction

In this article, we explore the fundamental physics and mathematics of acoustic wave propagation. To keep the analysis clear and mathematically tractable, we focus exclusively on the two-dimensional (2D) situation. 

**Coordinate**

We define a 2D coordinate system where:
- The wave propagation direction is along the $+z$ axis.
- The transverse direction is along the $+x$ axis.

We assume there is a planar acoustic wave coming from $-z$ and propagating towards $+z$. At the plane $z = 0$, we place infinitely thin objects (such as masks, apertures, or obstacles) that modulate or block the wave field.

**Wavenumber**

To describe the wave field mathematically, we define the following key physical quantities:
- **Free-space wavenumber ($k_0$):** Defined as $k_0 = \frac{\omega}{c} = \frac{2\pi}{\lambda}$, where $\omega$ is the angular frequency of the wave, $c$ is the speed of sound in the medium, and $\lambda$ is the wavelength.
- **Transverse wavenumber ($k_x$):** Represents the spatial frequency of the wave along the transverse $x$-axis.
- **Longitudinal wavenumber ($k_z$):** Represents the propagation wavenumber along the $z$-axis.

These wavenumbers are related by the 2D dispersion relation derived from the Helmholtz equation:
$$k_x^2 + k_z^2 = k_0^2 \implies k_z = \sqrt{k_0^2 - k_x^2}$$

The physical interpretation of $k_z$ depends on the relative magnitude of $k_x$ and $k_0$:
- **Propagating Waves ($|k_x| \le k_0$):** Here, $k_z$ is a real number. This represents plane waves propagating at an angle $\theta = \arcsin(k_x / k_0)$ relative to the $z$-axis.
- **Evanescent Waves ($|k_x| > k_0$):** Here, $k_z$ becomes purely imaginary. To satisfy the physical boundary condition that the field must remain bounded as $z \to \infty$, we choose the branch $k_z = -j\sqrt{k_x^2 - k_0^2}$. This represents waves that decay exponentially as they propagate away from the $z=0$ plane.

**Pressure Field**

To describe the acoustic pressure field, we define:
- **Time-independent pressure field ($p(x, z)$):** Represents the spatial distribution of the acoustic pressure field independent of time.
- **Time-dependent pressure field ($\tilde{p}(x, z, t)$):** Represents the full acoustic pressure field that varies with both space and time.

## Helmholtz equation

### Derivation of Wave Equation from Physical Principles

The wave equation is derived from the fundamental laws of classical mechanics and continuum mechanics. For acoustic wave propagation in a fluid medium (such as air or water), the derivation relies on three basic physical principles:

**Newton's Second Law (Conservation of Momentum)**

Imagine a tiny cube within a fluid. If the pressure on the left is greater than that on the right, this pressure difference $\nabla \tilde{p}$ will drive the motion of this fluid element. Based on $\mathbf{F} = m\mathbf{a}$, we can derive Euler's equation of motion:
$$
\rho_0 \frac{\partial \mathbf{u}}{\partial t} = -\nabla \tilde{p}
$$
where $\mathbf{u}$ is the vibrational velocity of the fluid particle and $\rho_0$ is the static density of the medium. In other words, the acceleration resulting from spatial pressure non-uniformity causes a change in the particle's velocity.

**Equation of Continuity (Conservation of Mass)**

If fluid particles are flowing out of a region (meaning the divergence of the velocity is positive, $\nabla \cdot \mathbf{u} > 0$), the mass within that region must decrease, resulting in a drop in the local density $\rho$. The continuity equation is:
$$
\frac{\partial \rho}{\partial t} + \rho_0 (\nabla \cdot \mathbf{u}) = 0
$$

$$
\frac{\partial \rho}{\partial t} = -\rho_0 (\nabla \cdot \mathbf{u})
$$

**Equation of State (Medium Elasticity)**

For small-amplitude acoustic perturbations, the change in pressure $\partial \tilde{p}$ is proportional to the change in density $\partial \rho$. The proportionality constant is the square of the speed of sound $c$:
$$
\frac{\partial \tilde{p}}{\partial t} = c^2 \frac{\partial \rho}{\partial t}
$$
**Combining the Equations**

By combining these three equations, we can eliminate the density $\rho$ and velocity $\mathbf{u}$:

Substitute Equation of Continuity into Equation of State:
$$
\frac{\partial \tilde{p}}{\partial t} = -c^2 \rho_0 (\nabla \cdot \mathbf{u})
$$
Differentiate this:
$$
\frac{\partial^2 \tilde{p}}{\partial t^2} = -c^2 \rho_0 \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u})
$$
Taking the divergence of both sides of Euler's equation of motion:
$$
\rho_0 \frac{\partial}{\partial t}(\nabla \cdot \mathbf{u}) = -\nabla^2 \tilde{p}
$$
Substituting this into above:
$$
\frac{\partial^2 \tilde{p}}{\partial t^2} = c^2 \nabla^2 \tilde{p}
$$
Finally, we get the **wave equation**:
$$
\nabla^2 \tilde{p} = \frac{1}{c^2} \frac{\partial^2 \tilde{p}}{\partial t^2}
$$
In a 2D Cartesian coordinate system $(x, z)$, this wave equation is written as:
$$
\frac{\partial^2 \tilde{p}}{\partial x^2} + \frac{\partial^2 \tilde{p}}{\partial z^2} = \frac{1}{c^2} \frac{\partial^2 \tilde{p}}{\partial t^2}
$$
Since no assumptions regarding periodicity or frequency were made during this derivation, the time-domain wave equation is universally valid for any transient waveform, whether it is an impulse, spoken voice, or random noise.

### Derivation of Helmholtz Equation

If we assume that the sound field is excited by a single-frequency (simple harmonic) source, then the sound pressure allows for the separation of variables and can be expressed as the product of a spatial term and a temporal term:
$$
\tilde{p}(x, z, t) = p(x, z) e^{-j\omega t}
$$
Take derivative twice:
$$
\frac{\partial^2 \tilde{p}}{\partial t^2} = -\omega^2 p \thinspace e^{-j\omega t}
$$
Substitute this into wave equation:
$$
\nabla^2 \tilde{p} = -\frac{1}{c^2} \omega^2 p \thinspace e^{-j\omega t}
$$

$$
e^{-j\omega t} \thinspace \nabla^2 p = -\frac{\omega^2}{c^2} p \thinspace e^{-j\omega t}
$$

$$
\nabla^2 p = -k_0^2 \thinspace p
$$

Finally, we get the **Helmholtz equation**:
$$
\nabla^2 p + k_0^2 \thinspace p = 0
$$
In a 2D Cartesian coordinate system $(x, z)$, this Helmholtz equation is written as:
$$
\frac{\partial^2 p}{\partial x^2} + \frac{\partial^2 p}{\partial z^2} + k_0^2 \thinspace p = 0
$$
By Fourier decomposition and the superposition of linear systems, this single-frequency equation can be extended to complex wave.

## Propagation Operator

To propagate an acoustic wave field from the $z = 0$ plane to any plane $z > 0$, we can define a propagation operator by Fourier properties.

### Frequency Domain

In the frequency domain (or angular spectrum domain), the propagation of the wave field is remarkably simple. Let $p(x, z)$ represent the acoustic pressure field. At any plane $z$, we can define its spatial Fourier transform $P(k_x, z)$ as:
$$
P(k_x, z) = \mathcal{F}\{p(x, z)\} = \int_{-\infty}^{\infty} p(x, z) e^{-j k_x x} dx
$$
The inverse Fourier transform is given by:
$$
p(x, z) = \frac{1}{2\pi} \int_{-\infty}^{\infty} P(k_x, z) e^{j k_x x} dk_x
$$
Calculate $\frac{\partial^2 p(x, z)}{\partial x^2}$:
$$
\begin{align}
\frac{\partial p(x, z)}{\partial x} &= \frac{\partial}{\partial x} \left[ \frac{1}{2\pi} \int_{-\infty}^{\infty} P(k_x, z) e^{j k_x x} dk_x \right] \\
&= \frac{1}{2\pi} \int_{-\infty}^{\infty} P(k_x, z) \cdot \left( \frac{\partial}{\partial x} e^{j k_x x} \right) dk_x \\
&= \frac{1}{2\pi} \int_{-\infty}^{\infty} P(k_x, z) \cdot (j k_x) e^{j k_x x} dk_x
\end{align}
$$

$$
\begin{align}
\frac{\partial^2 p(x, z)}{\partial x^2} &= \frac{1}{2\pi} \int_{-\infty}^{\infty} P(k_x, z) \cdot (j k_x)^2 e^{j k_x x} dk_x \\
&= \frac{1}{2\pi} \int_{-\infty}^{\infty} \left[ -k_x^2 P(k_x, z) \right] e^{j k_x x} dk_x
\end{align}
$$

Besides, we have:
$$
\frac{\partial^2 p}{\partial z^2} = \frac{1}{2\pi} \int_{-\infty}^{\infty} \left[ \frac{\partial^2 P(k_x, z)}{\partial z^2} \right] e^{j k_x x} dk_x
$$

$$
k_0^2 p = \frac{1}{2\pi} \int_{-\infty}^{\infty} \left[ k_0^2 P(k_x, z) \right] e^{j k_x x} dk_x
$$

Substitute these into the 2D Helmholtz equation:
$$
\left(\frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial z^2} + k_0^2\right) p(x, z) = 0
$$

$$
\frac{1}{2\pi} \int_{-\infty}^{\infty} \left[ -k_x^2 P(k_x, z) + \frac{\partial^2 P(k_x, z)}{\partial z^2} + k_0^2 P(k_x, z) \right] e^{j k_x x} dk_x = 0
$$

$$
\frac{1}{2\pi} \int_{-\infty}^{\infty} \left[ \frac{\partial^2 P(k_x, z)}{\partial z^2} + (k_0^2 - k_x^2) P(k_x, z) \right] e^{j k_x x} dk_x = 0
$$

By the uniqueness of the Fourier transform (or the property that if the Fourier transform of a function is zero, the function itself must be zero almost everywhere):
$$
\frac{\partial^2 P(k_x, z)}{\partial z^2} + (k_0^2 - k_x^2) P(k_x, z) = 0
$$

$$
\left(\frac{\partial^2}{\partial z^2} + (k_0^2 - k_x^2)\right) P(k_x, z) = 0
$$

For waves propagating in the $+z$ direction, the solution to this equation is:
$$
P(k_x, z) = P(k_x, 0) e^{-j z \sqrt{k_0^2 - k_x^2}}
$$

where $P(k_x, 0)$ is the Fourier transform of the initial field $p_0(x) = p(x, 0)$ at $z=0$. This indicates that propagating the field $p(x)$ from $0$ to $z$ in the frequency domain is equivalent to multiplying its spectrum $P(k_x, 0)$ by the propagation operator:
$$H(k_x, z) = e^{-j z \sqrt{k_0^2 - k_x^2}}$$

### Matrix Form

In numerical simulations, the continuous coordinate $x$ is sampled at $N$ discrete points, and the continuous Fourier transform is approximated by the Discrete Fourier Transform (DFT), which is computed efficiently using the Fast Fourier Transform (FFT).

Let $\mathbf{p}_0$ be the vector of sampled pressure values at $z=0$. The propagation process can be expressed in matrix form as:
$$\mathbf{p}(z) = \mathbf{F}^{-1} \mathbf{H}(z) \mathbf{F} \mathbf{p}_0$$

where:
- $\mathbf{F}$ is the forward FFT matrix that transforms the spatial field into the frequency domain.
- $\mathbf{H}(z)$ is a diagonal matrix representing the propagation operator, where the diagonal elements are $H_{nn} = e^{-j z \sqrt{k_0^2 - k_{x,n}^2}}$ for each discrete transverse wavenumber $k_{x,n}$.
- $\mathbf{F}^{-1}$ is the inverse FFT matrix that transforms the propagated spectrum back into the spatial domain.

Thus, the overall spatial propagation is represented by the product of the inverse Fourier matrix, the diagonal propagation operator matrix, and the forward Fourier matrix.

### Spatial Domain

Alternatively, we can express the propagation directly in the spatial domain. Since multiplication in the frequency domain corresponds to convolution in the spatial domain, we can write:
$$p(x, z) = p_0(x) * h(x, z) = \int_{-\infty}^{\infty} p_0(x') h(x - x', z) dx'$$

where $h(x, z)$ is the spatial propagation impulse response (the Green's function or propagator), which is the inverse Fourier transform of the frequency-domain operator $H(k_x, z)$:
$$h(x, z) = \mathcal{F}^{-1}\{H(k_x, z)\} = \frac{1}{2\pi} \int_{-\infty}^{\infty} e^{-j z \sqrt{k_0^2 - k_x^2}} e^{j k_x x} dk_x$$

To derive the analytical form of $h(x, z)$, we recall that the 2D free-space Green's function $G(x, z)$ for the Helmholtz equation representing an outgoing cylindrical wave is:
$$G(x, z) = \frac{j}{4} H_0^{(2)}(k_0 \sqrt{x^2 + z^2})$$

where $H_0^{(2)}$ is the zeroth-order Hankel function of the second kind. Using the Weyl expansion, the Green's function can be written as:
$$\frac{j}{4} H_0^{(2)}(k_0 \sqrt{x^2 + z^2}) = \frac{j}{4\pi} \int_{-\infty}^{\infty} \frac{e^{-j z \sqrt{k_0^2 - k_x^2}}}{\sqrt{k_0^2 - k_x^2}} e^{j k_x x} dk_x$$

Differentiating both sides with respect to $z$ yields:
$$\frac{\partial}{\partial z} \left[ \frac{j}{4} H_0^{(2)}(k_0 \sqrt{x^2 + z^2}) \right] = \frac{1}{4\pi} \int_{-\infty}^{\infty} e^{-j z \sqrt{k_0^2 - k_x^2}} e^{j k_x x} dk_x = \frac{1}{2} h(x, z)$$

Therefore, the propagator $h(x, z)$ is:
$$h(x, z) = \frac{j}{2} \frac{\partial}{\partial z} H_0^{(2)}(k_0 \sqrt{x^2 + z^2})$$

Using the derivative identity for Hankel functions, $\frac{d}{du} H_0^{(2)}(u) = -H_1^{(2)}(u)$, and applying the chain rule, we get:
$$\frac{\partial}{\partial z} H_0^{(2)}(k_0 \sqrt{x^2 + z^2}) = -H_1^{(2)}(k_0 \sqrt{x^2 + z^2}) \cdot \frac{k_0 z}{\sqrt{x^2 + z^2}}$$

Substituting this back, we obtain the exact analytical expression for the 2D spatial propagation operator:
$$h(x, z) = \frac{j k_0 z}{2 \sqrt{x^2 + z^2}} H_1^{(2)}(k_0 \sqrt{x^2 + z^2})$$

This is the 2D equivalent of the Rayleigh-Sommerfeld diffraction formula, which allows us to compute the propagated field directly via spatial convolution.

## Basic Propagation

To understand how these propagation operators behave in practice, let us consider a fundamental scenario. Assume that the entire plane at $z = 0$ is blocked by an infinitely thin, perfectly absorbing object, except for a single gap (slit) of width $W$ that is left open for propagation.

If a planar wave of amplitude $A$ is incident on this slit from $-z$, the initial field $p_0(x)$ at $z = 0$ can be modeled as a rectangular function:
$$p_0(x) = A \cdot \text{rect}\left(\frac{x}{W}\right) = \begin{cases} A, & |x| \le \frac{W}{2} \\ 0, & |x| > \frac{W}{2} \end{cases}$$

We can derive the analytical solution for the propagated field $p(x, z)$ at any distance $z > 0$ using the following steps:

### 1. Initial Field's Angular Spectrum (Fourier Transform)

First, we compute the spatial Fourier transform (angular spectrum) of the initial field $p_0(x)$. The Fourier transform of a rectangular function is a sinc function:
$$P_0(k_x) = \mathcal{F}\{p_0(x)\} = A W \cdot \text{sinc}\left(\frac{k_x W}{2\pi}\right)$$

where the normalized sinc function is defined as $\text{sinc}(u) = \frac{\sin(\pi u)}{\pi u}$. 

*(Note: If we use the non-normalized definition common in physics, this is written as $A W \frac{\sin(k_x W / 2)}{k_x W / 2}$.)*

### 2. Analytical Expression of the Propagation Process

By multiplying the initial spectrum by the free-space transfer function $H(k_x, z)$, we obtain the angular spectrum at the distance $z$:
$$P(k_x, z) = A W \cdot \text{sinc}\left(\frac{k_x W}{2\pi}\right) e^{-j z \sqrt{k_0^2 - k_x^2}}$$

### 3. Analytical Integral Solution for $p(x, z)$

The propagated field $p(x, z)$ is the inverse Fourier transform of the angular spectrum. Due to the square root term $\sqrt{k_0^2 - k_x^2}$, this integral does not possess a closed-form solution in terms of elementary functions and must be written in integral form:
$$p(x, z) = \frac{AW}{2\pi} \int_{-\infty}^{\infty} \text{sinc}\left(\frac{k_x W}{2\pi}\right) e^{-j z \sqrt{k_0^2 - k_x^2}} e^{j k_x x} dk_x$$

To gain deeper physical insight, we can divide this integral into two distinct parts:

#### A. Propagating (Traveling) Wave Part ($|k_x| \le k_0$)

This part consists of the spatial frequencies that propagate into the far field without attenuation, forming the smooth profile observed at larger distances:
$$p_{\text{prop}}(x, z) = \frac{AW}{2\pi} \int_{-k_0}^{k_0} \text{sinc}\left(\frac{k_x W}{2\pi}\right) e^{-j z \sqrt{k_0^2 - k_x^2}} e^{j k_x x} dk_x$$

#### B. Evanescent Wave Part ($|k_x| > k_0$)

This part consists of high spatial frequencies that carry fine details of the aperture. These waves decay exponentially as they leave the $z = 0$ boundary:
$$p_{\text{evan}}(x, z) = \frac{AW}{2\pi} \int_{|k_x| > k_0} \text{sinc}\left(\frac{k_x W}{2\pi}\right) e^{-z \sqrt{k_x^2 - k_0^2}} e^{j k_x x} dk_x$$

### 4. Far-field Approximation (Fraunhofer Approximation)

If the propagation distance $z$ is sufficiently large such that it satisfies the far-field condition $z \gg \frac{W^2}{\lambda}$, the received field $p(x, z)$ approaches a scaled version of the initial field's angular spectrum. Under this Fraunhofer approximation, the analytical solution simplifies to:
$$p(x, z) \approx \frac{e^{-jk_0 z}}{\sqrt{j\lambda z}} \cdot P_0\left(\frac{k_0 x}{z}\right)$$

Substituting the expression for $P_0(k_x)$, we get:
$$p(x, z) \approx C \cdot \text{sinc}\left(\frac{k_0 W x}{2\pi z}\right)$$

where $C = \frac{A W e^{-j k_0 z}}{\sqrt{j \lambda z}}$ is a complex scaling factor.

This result explains why, even though the initial field at the slit is a sharp rectangular function, the wave field becomes smooth and spreads out as it propagates. It is physically evolving into a sinc function shape due to the diffraction and interference of the propagating plane wave components.
