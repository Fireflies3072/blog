---
title: Understanding Flow Matching - A Continuous-Time Generative Framework
date: 2026-05-21 15:44:34
tags: [AI, diffusion, flow, math]
categories: [Articles, Reference]
cover: https://cdn.fireflies3072.com/blog/2026-05-flow-matching/cover.jpg
mathjax: true
excerpt: Generative modeling has seen a paradigm shift from the stochastic nature of Diffusion Models to the deterministic elegance of Flow Matching (FM). While Diffusion Models rely on reversing a noise-adding SDE, Flow Matching simplifies the problem by learning a velocity field that pushes a simple noise distribution toward the data distribution along a smooth path.
---

## Introduction

Generative modeling has seen a paradigm shift from the stochastic nature of Diffusion Models to the deterministic elegance of **Flow Matching (FM)**. While Diffusion Models rely on reversing a noise-adding SDE, Flow Matching simplifies the problem by learning a **velocity field** that pushes a simple noise distribution toward the data distribution along a smooth path.

In this post, we will explore the mathematical framework of Flow Matching and why it is becoming a preferred alternative to traditional diffusion.

## Probability Paths and Velocity Fields

### Key Definitions and Mappings

To understand Flow Matching, we must first align our physical intuition with mathematical concepts. These concepts are deeply rooted in fluid mechanics and statistical physics.

| Concept | Mathematical Symbol | Physical Intuition | Role in Flow Models |
| :--- | :--- | :--- | :--- |
| **Flow Map** | $\phi_t(x)$ | The **trajectory** of a particle (moving an initial point to a destination). | **Inference (Sampling)**: The path from noise $x_0$ to data $x_1$. |
| **Velocity Field** | $v_t(x)$ | The **speed and direction** at every position in space at a given time. | **Training Target**: The neural network $v_\theta(x, t)$ we aim to fit. |
| **Density Field** | $p_t(x)$ | The **concentration** of particles (probability density) at each position. | **Data Distribution**: $p_0$ is noise, $p_1$ is the real data distribution. |
| **Flux Field** | $J_t(x) = p_t(x)v_t(x)$ | The **probability mass** passing through a unit area per unit time. | **Continuity Equation**: Describes how probability "flows" through space. |

### The Continuity Equation: Understanding Flux

The relationship between the density field $p_t(x)$ and the velocity field $v_t(x)$ is governed by the **Continuity Equation**:

$$
\frac{\partial p_t(x)}{\partial t} + \nabla \cdot (p_t(x) v_t(x)) = 0
$$
If we define the flux field as $J_t(x) = p_t(x)v_t(x)$, the equation simplifies to:

$$
\frac{\partial p_t(x)}{\partial t} + \nabla \cdot J_t(x) = 0
$$
This is identical to the mass conservation equation in fluid dynamics or the charge conservation equation in electromagnetism:
*   $\nabla \cdot J_t(x)$ is the **divergence** of the flux, representing how much "probability flow" is exiting (source) or entering (sink) a point.
*   $\frac{\partial p_t(x)}{\partial t}$ is the rate of change of density at that point.
*   **Physical Meaning**: An increase in density at a location ($\frac{\partial p}{\partial t} > 0$) must be balanced by a net inflow of flux ($\nabla \cdot J < 0$). Probability is neither created nor destroyed.

### Main Theory

In Flow Matching, we define a time-dependent probability density $p_t(x)$ for $t \in [0, 1]$.
- At $t=0$, $p_0(x)$ is a simple noise distribution (usually standard Gaussian).
- At $t=1$, $p_1(x)$ is the complex data distribution $q(x)$.

The transformation of samples from $p_0$ to $p_1$ is described by an **Ordinary Differential Equation (ODE)**:
$$
\frac{dx}{dt} = v_t(x)
$$
If we know this velocity field, we can generate data by starting with noise $x_0 \sim p_0$ and integrating the ODE to find $x_1$:
$$
x_1 = \phi_1(x_0) = x_0 + \int_{0}^{1} v_t(x_t) dt
$$
The relationship between the probability path $p_t$ and the velocity field $v_t$ is governed by the **Continuity Equation**:
$$
\frac{\partial p_t(x)}{\partial t} + \nabla \cdot (p_t(x) v_t(x)) = 0
$$
This equation ensures that the total probability is conserved as the density "flows" from noise to data.

Our goal is to find the velocity field $v_t(x; \theta)$ parameterized by a neural network to transfer the simple distribution $p_0(x)$ to the real image distribution $p_1(x)$.

## Conditional Flow Matching (CFM)

If we try to optimize a neural network to match the true velocity field $v_t(x)$ directly using the unconditional continuity equation, we immediately hit a massive computational bottleneck.

Recall that the true time-dependent density field $p_t(x)$ is a **marginal distribution** obtained by integrating over the entire, intractable data distribution $q(x_1)$:
$$
p_t(x) = \int p_t(x|x_1) q(x_1) dx_1
$$
Because computing $p_t(x)$ requires integrating over the entire high-dimensional dataset $q(x_1)$, calculating the ideal unconditional velocity field $v_t(x) = J_t(x)/p_t(x)$ directly is impossible.

### Flow Matching Theorem

To bypass this density bottleneck, we can leverage a beautiful theorem from Flow Matching (Lipman et al., 2022). The core idea is simple: **instead of fighting the intractable global distribution, we can break the problem down by conditioning everything on a single, sampled data point $x_1 \sim q(x_1)$.**

**Theorem:**

Let $p_t(x|x_1)$ be a chosen **conditional probability path**, and $v_t(x|x_1)$ be its associated **conditional velocity field** that satisfies the **conditional continuity equation**:
$$
\frac{\partial p_t(x|x_1)}{\partial t} + \nabla \cdot (p_t(x|x_1) v_t(x|x_1)) = 0
$$
If we define an aggregate, marginal velocity field $v_t(x)$ by taking a posterior-weighted average of all possible conditional fields:
$$
v_t(x) = \int v_t(x|x_1) p_t(x_1|x) dx_1 = \int v_t(x|x_1) \frac{p_t(x|x_1)q(x_1)}{p_t(x)} dx_1
$$
Then, this $v_t(x)$ is guaranteed to satisfy the **unconditional continuity equation** for the marginal density $p_t(x)$.

> **The Inference Insight:** This theorem addresses a fundamental paradox: during training, we can use the knowledge of $x_1$ to construct simple trajectories, but during inference, $x_1$ does not exist. The theorem proves that if a neural network $v_\theta(x, t)$ learns to match the conditional fields $v_t(x|x_1)$ *on average*, it will automatically converge to the true, aggregate velocity field $v_t(x)$ needed for generation.

### Proof

We want to prove that the defined velocity field $v_t(x)$ satisfies:
$$
\frac{\partial p_t(x)}{\partial t} + \nabla \cdot (p_t(x) v_t(x)) = 0
$$
From the velocity field we defined above, we will derive to this expression:
$$
v_t(x) = \int v_t(x|x_1) \frac{p_t(x|x_1)q(x_1)}{p_t(x)} dx_1
$$
Multiply by $p_t(x)$ on both sides:
$$
p_t(x)v_t(x) = \int v_t(x|x_1)p_t(x|x_1)q(x_1) dx_1
$$
Take divergence on both sides:
$$
\nabla \cdot (p_t(x) v_t(x)) = \nabla \cdot \left( \int v_t(x|x_1) p_t(x|x_1) q(x_1) dx_1 \right)
$$
By Leibniz Rule, we can move the $\nabla$ symbol inside the integral:
$$
\nabla \cdot (p_t(x) v_t(x)) = \int \nabla \cdot \big( p_t(x|x_1) v_t(x|x_1) \big) q(x_1) dx_1
$$
From the conditional continuity equation, we have $\nabla \cdot (p_t(x|x_1) v_t(x|x_1)) = -\frac{\partial p_t(x|x_1)}{\partial t}$ and plug this into the expression:
$$
\nabla \cdot (p_t(x) v_t(x)) = \int \left( -\frac{\partial p_t(x|x_1)}{\partial t} \right) q(x_1) dx_1
$$
Move derivative outside the integral:
$$
\nabla \cdot (p_t(x) v_t(x)) = -\frac{\partial}{\partial t} \int p_t(x|x_1) q(x_1) dx_1
$$
The marginal distribution definition is $p_t(x) = \int p_t(x|x_1) q(x_1) dx_1$ and plug this in:
$$
\nabla \cdot (p_t(x) v_t(x)) = -\frac{\partial p_t(x)}{\partial t}
$$
Finally, we have:
$$
\frac{\partial p_t(x)}{\partial t} + \nabla \cdot (p_t(x) v_t(x)) = 0
$$
**Q.E.D.**

> **Note on Expectation Form:** By applying Bayes' rule, we can rewrite the posterior weighting term as $p_t(x_1|x) = \frac{p_t(x|x_1)q(x_1)}{p_t(x)}$. This allows us to express the complex velocity field as a clean, intuitive conditional expectation over the current state:
> $$
> v_t(x) = \int v_t(x|x_1) p_t(x_1|x) dx_1 = \mathbb{E}_{x_1 \sim p_t(x_1|x)} \left[ v_t(x|x_1) \right]
> $$

## Optimal Transport Path & Training Objective

To bridge the gap between abstract theory and scalable training, we must choose a specific conditional probability path $p_t(x|x_1)$. Modern flow matching frameworks typically favor the **Optimal Transport (OT) Path**, which constructs the straightest possible trajectories between noise and data.

There is a subtle but critical distinction between the theoretical definition and the actual implementation variables. Let $x_0 \sim p_0(x_0) = \mathcal{N}(0, I)$ be the source noise and $x_1 \sim q(x_1)$ be a target data point.

### Joint Conditioning

When we condition on both the explicit starting point $x_0$ and the final destination $x_1$, the trajectory is a deterministic linear interpolation:
$$
x_t = \psi_t(x_0, x_1) = (1 - t)x_0 + t x_1
$$
In this case, the conditional distribution $p_t(x \mid x_0, x_1)$ is a Dirac delta function $\delta(x - \psi_t(x_0, x_1))$. Taking the time derivative of this path yields the constant velocity vector:
$$
v_t(x \mid x_0, x_1) = \frac{d}{dt}\psi_t(x_0, x_1) = x_1 - x_0
$$

### Marginal Conditioning on $x_1$

To satisfy our main Flow Matching theorem, we must treat the starting point $x_0 \sim \mathcal{N}(0, I)$ as a distribution instead of a fixed point. Since our trajectory is defined by the linear interpolation $x_t = (1-t)x_0 + t x_1$, we can derive the strict conditional probability path given only the endpoint $x_1$ as an evolving Gaussian distribution:
$$
p_t(x \mid x_1) = \mathcal{N}\big(x; t x_1, (1-t)^2 I\big)
$$
At the boundary $t=0$, this seamlessly simplifies to $p_0(x \mid x_1) = \mathcal{N}(0, I)$, perfectly matching our unconditioned standard Gaussian noise. As $t \to 1$, the variance collapses to $0$ and the distribution sharpens into a Dirac delta function centered exactly at the data point $x_1$.

By applying the continuity equation to this moving Gaussian bubble, the true Eulerian velocity field reveals a clear spatial dependency:
$$
v_t(x \mid x_1) = \frac{x_1 - x}{1 - t}
$$
As the path approaches the data destination ($t \to 1$), this formulation suffers from an analytical singularity where we divide by zero. To ensure numerical stability throughout the entire time horizon, we introduce a minor regularizer $\sigma_{\text{min}}$ (e.g., $10^{-5}$) to the variance:
$$
p_t(x \mid x_1) = \mathcal{N}\big(x; t x_1, [(1-t)^2 + \sigma_{\text{min}}^2] I\big)
$$

### Derivation of Particle Path and Regularized Velocity Field

To sample a concrete trajectory point $x_t$ from this modified conditional distribution, we apply the standard Gaussian reparameterization trick. Separating the independent variables of the macro-noise $x_0$ and a static micro-noise $\epsilon$ yields:
$$
x_t = (1-t)x_0 + t x_1 + \sigma_{\text{min}}\epsilon, \quad x_0, \epsilon \sim \mathcal{N}(0, I)
$$
> **A Note on Boundary Adjustments:** It is worth noting that at $t=0$, this regularized path actually samples from $\mathcal{N}(0, (1+\sigma_{\text{min}}^2)I)$ rather than a perfect standard Gaussian. However, because $\sigma_{\text{min}}$ is chosen to be incredibly small, this boundary shift is completely negligible in practice, while the numerical safety it grants at $t=1$ is immense.

Now, substituting our regularized mean $\mu_t = t x_1$ and variance $\sigma_t^2 = (1-t)^2 + \sigma_{\text{min}}^2$ into the standard Gaussian transport formula $v_t = \dot{\mu}_t + \frac{\dot{\sigma}_t}{\sigma_t}(x - \mu_t)$, we resolve the true Eulerian velocity field:
$$
\begin{align}
v_t(x \mid x_1) &= \frac{d}{dt} \left(t x_1\right) + \frac{\frac{d}{dt} \left( \sqrt{(1-t)^2 + \sigma_{\text{min}}^2} \right)}{\sqrt{(1-t)^2 + \sigma_{\text{min}}^2}} (x - t x_1) \\
&= x_1 + \frac{-\frac{-2(1-t)}{2\sqrt{(1-t)^2 + \sigma_{\text{min}}^2}}}{\sqrt{(1-t)^2 + \sigma_{\text{min}}^2}} (x - t x_1) \\
&= x_1 - \frac{1-t}{(1-t)^2 + \sigma_{\text{min}}^2} (x - t x_1)
\end{align}
$$
Finding a common denominator and grouping terms containing $(1-t)$ simplifies the expression into its final, singularity-free formulation:

$$
v_t(x \mid x_1) = \frac{(1-t)(x_1 - x) + x_1 \sigma_{\text{min}}^2}{(1-t)^2 + \sigma_{\text{min}}^2}
$$
As $t \to 1$, the first term in the numerator vanishes, and the vector field smoothly stabilizes to $v_{t=1}(x \mid x_1) = x_1$, preventing any analytical explosion.

### Geometric Intuition: Giving the Data Manifold "Thickness"

Beyond fixing the division-by-zero anomaly, the introduction of $\sigma_{\text{min}}$ plays a profound role in smoothing the high-dimensional space.

Real-world datasets concentrate on a low-dimensional sub-space—known as the **data manifold**—embedded within a massive ambient space. Because this manifold has a lower intrinsic dimensionality, its geometric volume (measure) is strictly zero, behaving like an infinitely thin, sharply folded sheet of paper.

If $\sigma_{\text{min}} = 0$, the generative flow forces the model to transport noise vectors onto this zero-thickness boundary with absolute precision at $t=1$. This causes the spatial gradient (Jacobian) of the velocity field to become excessively steep and unstable near the target, introducing optimization friction and causing pixel-level artifacts during generation.

By adding a tiny bit of noise ($\sigma_{\text{min}}\epsilon$), we slightly blur each data point. Geometrically, this turns the data from an infinitely thin, sharp surface into a slightly "thickened" layer, making it much easier for the model to learn and generate samples.

This "thickness" acts as a soft-landing pad, allowing simple ODE solvers (like the Euler method) to safely converge with large, discrete step sizes without drifting into unstable space.

### Training Objective

While we have derived the exact formulation for the marginal velocity field $v_t(x \mid x_1)$, directly applying a $(1-t)$ denominator introduces severe numerical instability during training.

Fortunately, the core Flow Matching theorem provides a beautiful workaround: if we re-introduce the initial noise source $x_0 \sim \mathcal{N}(0, I)$ as a conditioning variable, the complex conditional velocity field can be simplified into a constant displacement vector. Lipman et al. proved that the marginal conditional field is simply the posterior expectation of the joint conditional field:
$$
v_t(x \mid x_1) = \mathbb{E}_{x_0 \sim p_t(x_0 \mid x, x_1)} \left[ v_t(x \mid x_0, x_1) \right] = \mathbb{E}_{x_0 \sim p_t(x_0 \mid x, x_1)} [x_1 - x_0]
$$
Because the neural network $v_\theta(x, t)$ minimizes the objective across the entire data distribution, optimizing it to predict the straightforward joint velocity $x_1 - x_0$ will forces it to automatically converge to the correct, aggregate marginal field $v_t(x)$ in expectation. This completely bypasses the density bottleneck and the division-by-zero anomaly during training.

By using the joint formulation $v_t(x_t \mid x_0, x_1) = x_1 - x_0$, the expectation over the complex aggregate velocity field simplifies into a straightforward Mean Squared Error (MSE) regression. The neural network $v_\theta(x, t)$ simply takes the current interpolated position and time, and predicts the displacement vector:
$$
\mathcal{L}_{\text{CFM}}(\theta) = \mathbb{E}_{t \sim U[0,1], x_1 \sim q(x_1), x_0 \sim \mathcal{N}(0,I)} \left\| v_\theta\big((1-t)x_0 + t x_1, t\big) - (x_1 - x_0) \right\|_2^2
$$
To address the manifold thickness issue, we can apply a small noise to the interpolated data point:
$$
\mathcal{L}_{\text{CFM}}(\theta) = \mathbb{E}_{t \sim U[0,1], x_1 \sim q(x_1), x_0 \sim \mathcal{N}(0,I)} \left\| v_\theta\big((1-t)x_0 + t x_1 + \sigma_{\text{min}}\epsilon, t\big) - (x_1 - x_0) \right\|_2^2
$$

## Sampling Process (Inference)

Generating a new sample is as simple as solving the learned ODE. We start with $x_0 \sim \mathcal{N}(0, I)$ and solve:
$$
x_1 = x_0 + \int_0^1 v_\theta(x_t, t) dt
$$

**ODE Solvers**

Because Flow Matching often learns "straighter" paths than the curved trajectories of diffusion models, we can use efficient ODE solvers:
- **Euler Method**: The simplest first-order solver.
  $$x_{t+\Delta t} = x_t + v_\theta(x_t, t) \Delta t$$
- **Higher-order solvers**: Methods like RK4 or adaptive step-size solvers (Dormand-Prince) can achieve high accuracy with very few steps.

Compared to Diffusion Models, Flow Matching typically requires significantly fewer steps (e.g., 10-20 steps) to produce high-quality samples.

## Conclusion

The brilliance of Flow Matching lies in its ability to bridge the gap between abstract probability densities and concrete particle trajectories. By reformulating generative modeling as a velocity-fitting problem, it replaces the complex stochastic differential equations (SDEs) of diffusion with intuitive, deterministic ordinary differential equations (ODEs).

This shift offers three transformative advantages:
1. **Geometric Efficiency**: By learning "straighter" paths from noise to data, Flow Matching enables high-quality generation in significantly fewer steps.
2. **Mathematical Clarity**: The training objective is reduced to a simple MSE regression, removing the need for complex ELBO derivations or variance schedules.
3. **Robustness**: Techniques like manifold thickening ensure that the model remains stable even when dealing with high-dimensional, complex data.

As we move toward larger and more capable generative systems, Flow Matching provides a cleaner, faster, and more scalable foundation for the next generation of AI.
