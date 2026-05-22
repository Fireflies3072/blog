---
title: Understanding Diffusion Models - A Mathematical Derivation
date: 2026-05-21 15:44:15
tags: [AI, diffusion]
categories: [Articles]

mathjax: true
---

## Introduction

Diffusion models have recently taken the generative AI world by storm, powering state-of-the-art systems like DALL-E 2, Imagen, and Stable Diffusion. Unlike GANs or VAEs, diffusion models work by gradually adding noise to data and then learning to reverse this process.

In this post, we will dive deep into the mathematical foundations of Denoising Diffusion Probabilistic Models (DDPM).

## Forward Process (Diffusion)

### Main Theory

The forward process, also known as the diffusion process, gradually adds Gaussian noise to a data point $x_0$ sampled from the real data distribution $q(x)$, or $p_{data}(x)$ over $T$ steps, also denoted as $x_0 \sim q(x_0)$.

Each step in the forward process is defined as:
$$
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t I)
$$

where $\beta_t$ is a variance schedule and $I$ denotes the identity matrix, ensuring that the noise is added independently to each vector dimension.

The formula for adding noise in a single diffusion step is:
$$
x_t = \sqrt{1 - \beta_t} \thinspace x_{t-1} + \sqrt{\beta_t} \thinspace \epsilon_t, \qquad \epsilon_t \sim \mathcal{N}(0, I)
$$

This means at each timestep $t$, we generate $x_t$ by blending the previous sample $x_{t-1}$ with Gaussian noise $\epsilon_t$ scaled by the current variance $\beta_t$.

Although it looks like a step-by-step process, a key property of the forward process is that we can sample $x_t$ at any arbitrary time step $t$ directly from $x_0$. Let $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{i=1}^t \alpha_i$. Then:
$$
q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) I)
$$

Or equivalently:
$$
x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)
$$

### Deriving the Weights: $\sqrt{\bar{\alpha}_t}$ and $\sqrt{1 - \bar{\alpha}_t}$

We begin with the recurrence relation for the forward diffusion process:
$$
x_t = \sqrt{\alpha_t}\thinspace x_{t-1} + \sqrt{1 - \alpha_t}\thinspace \epsilon_t,\qquad \epsilon_t \sim \mathcal{N}(0, I)
$$

Each $\epsilon_t$ follows a standard normal distribution. A key property of normal distributions is that the addition of two independent normal distributions $X \sim \mathcal{N}(\mu_1, \sigma_1^2)$ and $Y \sim \mathcal{N}(\mu_2, \sigma_2^2)$ results in a new normal distribution with mean $\mu_1 + \mu_2$ and standard deviation $\sqrt{\sigma_1^2 + \sigma_2^2}$.

#### Step-By-Step Expansion

Let’s compute the first few steps to reveal the pattern, applying the rule of adding normal distributions at each step:

- **For $t = 1$:**
  $$
  x_1 = \sqrt{\alpha_1}\thinspace x_0 + \sqrt{1 - \alpha_1}\thinspace \epsilon_1
  $$

- **For $t = 2$:**
  $$
  \begin{align}
  x_2 &= \sqrt{\alpha_2}\thinspace x_1 + \sqrt{1 - \alpha_2}\thinspace \epsilon_2 \\
      &= \sqrt{\alpha_2}\left(\sqrt{\alpha_1} x_0 + \sqrt{1 - \alpha_1}\thinspace \epsilon_1\right) + \sqrt{1 - \alpha_2}\thinspace \epsilon_2 \\
      &= \sqrt{\alpha_2\alpha_1}\thinspace x_0 + \sqrt{\alpha_2(1 - \alpha_1)}\thinspace \epsilon_1 + \sqrt{1 - \alpha_2}\thinspace \epsilon_2
  \end{align}
  $$

  Now we merge the two noise terms $\sqrt{\alpha_2(1 - \alpha_1)}\thinspace \epsilon_1$ and $\sqrt{1 - \alpha_2}\thinspace \epsilon_2$. Since both $\epsilon_1$ and $\epsilon_2$ are independent $\mathcal{N}(0, I)$, the combined noise is $\mathcal{N}(0, \sigma_{combined}^2)$ where:
  $$
  \sigma_{combined}^2 = \left(\sqrt{\alpha_2(1 - \alpha_1)}\right)^2 + \left(\sqrt{1 - \alpha_2}\right)^2 = \alpha_2 - \alpha_2\alpha_1 + 1 - \alpha_2 = 1 - \alpha_2\alpha_1
  $$

  Thus, by writing $\bar{\epsilon}_2 \sim \mathcal{N}(0, I)$, we have:
  $$
  x_2 = \sqrt{\alpha_2\alpha_1}\thinspace x_0 + \sqrt{1 - \alpha_2\alpha_1}\thinspace \bar{\epsilon}_2
  $$
  
- **For $t = 3$:**
  Following the same logic:
  $$
  \begin{align}
  x_3 &= \sqrt{\alpha_3}\thinspace x_2 + \sqrt{1 - \alpha_3}\thinspace \epsilon_3 \\
      &= \sqrt{\alpha_3}(\sqrt{\alpha_2\alpha_1}\thinspace x_0 + \sqrt{1 - \alpha_2\alpha_1}\thinspace \bar{\epsilon}_2) + \sqrt{1 - \alpha_3}\thinspace \epsilon_3 \\
      &= \sqrt{\alpha_3\alpha_2\alpha_1}\thinspace x_0 + \sqrt{\alpha_3(1 - \alpha_2\alpha_1)}\thinspace \bar{\epsilon}_2 + \sqrt{1 - \alpha_3}\thinspace \epsilon_3
  \end{align}
  $$

  Merging the noise terms again:
  $$
  \sigma_{combined}^2 = \alpha_3(1 - \alpha_2\alpha_1) + 1 - \alpha_3 = \alpha_3 - \alpha_3\alpha_2\alpha_1 + 1 - \alpha_3 = 1 - \alpha_3\alpha_2\alpha_1
  $$

  So, we have:
  $$
  x_3 = \sqrt{\alpha_3\alpha_2\alpha_1}\thinspace x_0 + \sqrt{1 - \alpha_3\alpha_2\alpha_1}\thinspace \bar{\epsilon}_3
  $$

By induction, we can generalize this pattern for any arbitrary timestep $t$:
$$
x_t = \sqrt{\bar{\alpha}_t}\thinspace x_0 + \sqrt{1 - \bar{\alpha}_t}\thinspace \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)
$$

where $\bar{\alpha}_t = \prod_{i=1}^t \alpha_i$. This powerful result shows that we don't need to iteratively add noise $t$ times; we can jump directly from $x_0$ to any $x_t$ in a single calculation.

#### Intuitive Meaning

- **Signal Decay**: The original image $x_0$ is gradually "faded out" as it is multiplied by $\sqrt{\alpha_t}$ at each step. After $t$ steps, the remaining signal is $\sqrt{\bar{\alpha}_t} x_0$.
- **Noise Accumulation**: Each step adds a new "layer" of random noise. Because these noise layers are independent, they don't just add up linearly; instead, their variances add up, which is why the total noise standard deviation becomes $\sqrt{1 - \bar{\alpha}_t}$.
- **The Diffusion Limit**: As $t$ increases towards $T$, $\bar{\alpha}_t$ approaches 0. This means the original signal eventually vanishes, leaving only pure Gaussian noise.

### Variance Schedules

The choice of the variance schedule $\beta_t$ is crucial for the performance of diffusion models. It determines how quickly the signal is destroyed in the forward process and how much noise the model needs to remove at each step of the reverse process.

#### Linear Schedule

The linear schedule, introduced in the original DDPM paper, defines $\beta_t$ as a linear interpolation between two values (typically $\beta_1 = 10^{-4}$ and $\beta_T = 0.02$):
$$
\beta_t = \beta_1 + \frac{t-1}{T-1}(\beta_T - \beta_1)
$$

While simple, the linear schedule tends to destroy the signal very quickly in the later steps, which can make the reverse process more difficult to learn.

#### Cosine Schedule

To address the rapid signal decay of the linear schedule, the cosine schedule was proposed in "Improved Denoising Diffusion Probabilistic Models". It defines $\bar{\alpha}_t$ directly using a cosine-based function:
$$
\bar{\alpha}_t = \frac{f(t)}{f(0)}, \quad f(t) = \cos\left(\frac{t/T + s}{1 + s} \cdot \frac{\pi}{2}\right)^2
$$

where $s$ is a small offset (typically $0.008$) to prevent $\beta_t$ from being too small at $t=0$. This schedule results in a much smoother decay of the signal, preserving more information for a longer period during the forward process.

The following plots compare the signal weight ($\sqrt{\bar{\alpha}_t}$) and noise weight ($\sqrt{1 - \bar{\alpha}_t}$) for both the linear and cosine schedules.

![Comparison of Variance Schedules](https://cdn.fireflies3072.com/blog/2026-05-diffusion-model/scheduler_comparison.jpg)

## Reverse Process (Generative)

The goal of a diffusion model is to reverse the forward process. If we can successfully sample backwards from $x_t$ to $x_{t-1}$, we can start from pure Gaussian noise $x_T \sim \mathcal{N}(0, I)$ and iteratively denoise it to generate a brand-new, high-quality image $x_0$.

Using Bayes' formula, the expression of the true reverse conditional probability $q(x_{t-1} | x_t)$ is:
$$
q(x_{t-1} | x_t) = q(x_t | x_{t-1}) \frac{q(x_{t-1})}{q(x_t)}
$$

This is **intractable** (impossible to compute directly) because the expression of $q(x_t)$ (as well as $q(x_{t-1})$) is:
$$
q(x_t) = \int q(x_t | x_0) q(x_0) dx_0 \approx \frac{1}{N}\sum_{i=1}^{N}q(x_t | x_{0,i})
$$

where the distribution of all real images in the world $q(x_0)$ is:
$$
q(x_0) \approx \frac{1}{N}\sum_{i=1}^{N}\delta(x_0 - x_{0,i})
$$

$q(x_t | x_0)$ is known. However, $q(x_0)$ is the distribution of all possible clean images $x_0$. $q(x_t)$ requires integrating over the entire real data distribution, which is infinitely complex. Even if we try to approximate $q(x_t)$ with a lot of real image samples, the amount of calculation needed is impractical since the dimension of $x_0$ is huge (e.g. the dimension is $512^2=262,144$ if the image has size $512\times 512$).

To solve this, we train a neural network $p_\theta$ to **approximate** this intractable reverse step:
$$
p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))
$$

Our main challenge now is: how do we find the training target for the network's predicted mean $\mu_\theta(x_t, t)$ and variance $\Sigma_\theta(x_t, t)$?

### The Mathematical Trick: Conditioning on $x_0$

Although $q(x_{t-1} | x_t)$ is intractable, it becomes surprisingly **tractable if we condition it on the original clean image $x_0$**. Think of this as a "cheat code"—if the model knows what the final clean image looks like, calculating the exact reverse step $q(x_{t-1} | x_t, x_0)$ becomes straightforward.

Using Bayes' rule, we can rewrite this conditional probability as:
$$
q(x_{t-1} | x_t, x_0) = q(x_t | x_{t-1}, x_0) \frac{q(x_{t-1} | x_0)}{q(x_t | x_0)}
$$

Notice that every single term on the right side of the equation is a forward process probability that we already defined in the previous section.

- $q(x_t | x_{t-1}, x_0)$ is just the standard one-step forward transition $q(x_t | x_{t-1})$, which is $\mathcal{N}(x_t; \sqrt{\alpha_t}\thinspace x_{t-1}, \beta_t \mathbf{I})$.
- $q(x_{t-1} | x_0)$ is the "shortcut" transitions that let us jump directly from $x_0$, which is $\mathcal{N}(x_{t-1}; \sqrt{\bar{\alpha}_{t-1}}\thinspace x_0, (1 - \bar{\alpha}_{t-1})\mathbf{I})$.
- $q(x_t | x_0)$ is similar to above, which is $\mathcal{N}(x_t; \sqrt{\bar{\alpha}_t}\thinspace x_0, (1 - \bar{\alpha}_t)\mathbf{I})$.

The probability density function (PDF) of normal distribution is $f(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left( -\frac{(x-\mu)^2}{2\sigma^2} \right)$.

Multiplying these Gaussian densities together, the exponent part of $q(x_{t-1} | x_t, x_0)$ is:
$$
\text{Exp} \propto \exp \left( -\frac{1}{2} \left[ \frac{(x_t - \sqrt{\alpha_t}x_{t-1})^2}{\beta_t} + \frac{(x_{t-1} - \sqrt{\bar{\alpha}_{t-1}}x_0)^2}{1 - \bar{\alpha}_{t-1}} - \frac{(x_t - \sqrt{\bar{\alpha}_t}x_0)^2}{1 - \bar{\alpha}_t} \right] \right)
$$

We want the exponent to be in the form of this:
$$
-\frac{1}{2}\frac{(x_{t-1} - \tilde{\mu}_t)^2}{\tilde{\beta}_t}
$$

### Derive Expression of $\tilde{\mu}_t$ and $\tilde{\beta}_t$

Since $x_{t-1}$ is the variable, we will consider everything else as constant, including $x_t$.

Constant can be removed from the exponent because $e^{c+x} = e^c \cdot e^x$ where $e^c$ is a constant coefficient and does not affect mean and std.

Expand everything and combine:
$$
\begin{align}
\mathbf{E} &= -\frac{1}{2} \left[ \frac{(x_t - \sqrt{\alpha_t}x_{t-1})^2}{\beta_t} + \frac{(x_{t-1} - \sqrt{\bar{\alpha}_{t-1}}x_0)^2}{1 - \bar{\alpha}_{t-1}} - \frac{(x_t - \sqrt{\bar{\alpha}_t}x_0)^2}{1 - \bar{\alpha}_t} \right] \\
&= -\frac{1}{2} \left[ \frac{x_t^2 - 2\sqrt{\alpha_t}x_t x_{t-1} + \alpha_t x_{t-1}^2}{\beta_t} + \frac{x_{t-1}^2 - 2\sqrt{\bar{\alpha}_{t-1}}x_0 x_{t-1} + \bar{\alpha}_{t-1}x_0^2}{1 - \bar{\alpha}_{t-1}} + \text{constant} \right] \\
&= -\frac{1}{2} \left[ \left( \frac{\alpha_t}{\beta_t} + \frac{1}{1 - \bar{\alpha}_{t-1}} \right) x_{t-1}^2 - 2 \left( \frac{\sqrt{\alpha_t}x_t}{\beta_t} + \frac{\sqrt{\bar{\alpha}_{t-1}}x_0}{1 - \bar{\alpha}_{t-1}} \right) x_{t-1} + \text{constant} \right]
\end{align}
$$

Now we have this form in the exponent:
$$
A \cdot x_{t-1}^2 - 2B \cdot x_{t-1} + \text{constant} = \frac{x_{t-1}^2 - 2\frac{B}{A} x_{t-1} + \left( \frac{B}{A} \right)^2 + \left[-\left( \frac{B}{A} \right)^2 + \text{constant}\right]}{\frac{1}{A}}
$$

where
$$
A = \frac{\alpha_t}{\beta_t} + \frac{1}{1 - \bar{\alpha}_{t-1}}
$$

$$
B = \frac{\sqrt{\alpha_t}x_t}{\beta_t} + \frac{\sqrt{\bar{\alpha}_{t-1}}x_0}{1 - \bar{\alpha}_{t-1}}
$$

After removing $\frac{-\frac{C}{A} + \text{constant}}{\frac{1}{A}}$, we have this form:
$$
\frac{x_{t-1}^2 - 2\frac{B}{A} x_{t-1} + \left( \frac{B}{A} \right)^2}{\frac{1}{A}} = \frac{x_{t-1}^2 - 2\tilde{\mu}_t x_{t-1} + \tilde{\mu}_t^2}{\tilde{\beta}_t}
$$

So:
$$
\begin{align}
\frac{1}{\tilde{\beta}_t} = A &= \frac{\alpha_t}{\beta_t} + \frac{1}{1 - \bar{\alpha}_{t-1}} \\
&= \frac{\alpha_t(1 - \bar{\alpha}_{t-1}) + \beta_t}{\beta_t(1 - \bar{\alpha}_{t-1})} \\
&= \frac{\left(\alpha_t + \beta_t\right) - \alpha_t\bar{\alpha}_{t-1}}{\beta_t(1 - \bar{\alpha}_{t-1})} \\
&= \frac{1 - \bar{\alpha}_t}{\beta_t(1 - \bar{\alpha}_{t-1})}
\end{align}
$$

Take the inverse:
$$
\tilde{\beta}_t = \frac{1}{A} = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t
$$

Similarly:
$$
\begin{align}
\tilde{\mu}_t = \frac{B}{A} &= \tilde{\beta}_t \cdot \left( \frac{\sqrt{\alpha_t}x_t}{\beta_t} + \frac{\sqrt{\bar{\alpha}_{t-1}}x_0}{1 - \bar{\alpha}_{t-1}} \right) \\
&= \left( \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t \right) \cdot \left( \frac{\sqrt{\alpha_t}x_t}{\beta_t} + \frac{\sqrt{\bar{\alpha}_{t-1}}x_0}{1 - \bar{\alpha}_{t-1}} \right) \\
&= \left( \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t \right) \cdot \frac{\sqrt{\alpha_t}x_t}{\beta_t} + \left( \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t \right) \cdot \frac{\sqrt{\bar{\alpha}_{t-1}}x_0}{1 - \bar{\alpha}_{t-1}} \\
&= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} x_0
\end{align}
$$

Finally, we find that $q(x_{t-1} | x_t, x_0)$ is also a Gaussian distribution:
$$
q(x_{t-1} | x_t, x_0) = \mathcal{N}(x_{t-1}; \tilde{\mu}_t(x_t, x_0), \tilde{\beta}_t I)
$$

$$
\tilde{\mu}_t(x_t, x_0) = \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} x_0
$$

$$
\tilde{\beta}_t = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t
$$

### Making Sense of the Ground-Truth Mean

Don't be intimidated by these heavy coefficients! The physical meaning of $\tilde{\mu}_t$ is beautifully intuitive. It tells us that the best guess for the previous image $x_{t-1}$ is a **weighted average** of two things:

1. The current noisy image $x_t$.
2. The final clean image $x_0$.

## Shifting from Image Predictor to Noise Predictor

Ideally, we want our neural network's $\mu_\theta(x_t, t)$ to match the ground-truth mean $\tilde{\mu}_t(x_t, x_0)$ as closely as possible. However, during real generation, the network **does not have access** to the clean image $x_0$.

To bypass this, we use the forward shortcut formula we derived earlier to express $x_0$ in terms of $x_t$ and the actual added noise $\epsilon$:
$$
x_0 = \frac{1}{\sqrt{\bar{\alpha}_t}} \left(x_t - \sqrt{1 - \bar{\alpha}_t} \epsilon\right)
$$

If we substitute this definition of $x_0$ back into the complex $\tilde{\mu}_t$ equation above, a gorgeous simplification happens after the algebra settles:
$$
\begin{align}
\tilde{\mu}_t(x_t, x_0) &= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} \cdot \frac{1}{\sqrt{\bar{\alpha}_t}} \left(x_t - \sqrt{1 - \bar{\alpha}_t} \epsilon\right) \\
&= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{(1 - \bar{\alpha}_t)\sqrt{\bar{\alpha}_t}} x_t - \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t \cdot \sqrt{1 - \bar{\alpha}_t}}{(1 - \bar{\alpha}_t)\sqrt{\bar{\alpha}_t}} \epsilon \\
&= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\beta_t}{\sqrt{\alpha_t}(1 - \bar{\alpha}_t)} x_t - \frac{\beta_t \cdot \sqrt{1 - \bar{\alpha}_t}}{\sqrt{\alpha_t}(1 - \bar{\alpha}_t)} \epsilon \\
&= \frac{\alpha_t(1 - \bar{\alpha}_{t-1}) + \beta_t}{\sqrt{\alpha_t}(1 - \bar{\alpha}_t)} x_t - \frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1 - \bar{\alpha}_t}} \epsilon \\
&= \frac{(\alpha_t + \beta_t) - \bar{\alpha}_{t}}{\sqrt{\alpha_t}(1 - \bar{\alpha}_t)} x_t - \frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1 - \bar{\alpha}_t}} \epsilon \\
&= \frac{1 - \bar{\alpha}_{t}}{\sqrt{\alpha_t}(1 - \bar{\alpha}_t)} x_t - \frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1 - \bar{\alpha}_t}} \epsilon \\
&= \frac{1}{\sqrt{\alpha_t}} x_t - \frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1 - \bar{\alpha}_t}} \epsilon \\
&= \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon \right)
\end{align}
$$

Look at this elegant result! The only unknown variable left in this ground-truth mean is $\epsilon$—the random noise that was added at timestep $t$.

This reveals the core breakthrough of the DDPM paper: instead of training the neural network to predict the entire complex image mean $\mu_\theta$, we can train it to be **a simple noise predictor $\epsilon_\theta(x_t, t)$** with a simple MSE loss function:
$$
L = \mathbb{E}_{t, x_0, \epsilon} \left[ \| \epsilon - \epsilon_\theta(x_t, t) \|^2 \right]
$$

## Sampling Process (Inference)

### Basic

Now that our neural network $\epsilon_\theta(x_t, t)$ has been trained to predict the noise injected at any given timestep, how do we actually use it to generate a brand-new image?

We start from pure Gaussian noise $x_T \sim \mathcal{N}(0, I)$ and run the reverse process step-by-step from $t = T$ down to $t = 1$.

At each reverse step, we want to sample $x_{t-1}$ from the predicted distribution $p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \sigma_t^2 I)$.

Using the mathematical breakthrough we derived in the previous section, we can parameterize the network's predicted mean $\mu_\theta(x_t, t)$ by replacing the true unknown noise $\epsilon$ with our network's prediction $\epsilon_\theta(x_t, t)$:
$$
\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(x_t, t) \right)
$$

For the standard deviation $\sigma_t$, DDPM sets it as a fixed constant, choosing either of the following (the second one produces a more accurate approximation):
$$
\sigma_t = \sqrt{\beta_t}
$$

$$
\sigma_t = \sqrt{\tilde{\beta}_t} = \sqrt{\frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t}
$$

We sample a random noise vector $z \sim \mathcal{N}(0, I)$ at each step to ensure generation diversity. The final **sampling formula** for a single reverse step is:
$$
\begin{align}
x_{t-1} &= \mu_\theta(x_t, t) + \sigma_t z \\
&= \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(x_t, t) \right) + \sigma_t z, \quad \text{where } z \sim \mathcal{N}(0, I)
\end{align}
$$

> **Note on the final step:** When $t=1$, we are generating the final clean image $x_0$. At this last step, we no longer add random noise, so we set $z = 0$ to get the clean deterministic output.

### Practical Implementation

Using the sampling process above, the result will be unstable. This is mainly caused by the $\frac{1}{\sqrt{\alpha_t}}$ term.

When the sampling process starts, the first $\alpha_t = 0.001$ if using cosine scheduler with default parameters. It causes $\frac{1}{\sqrt{\alpha_T}} = \frac{1}{\sqrt{0.001}} \approx 31.6228$ which makes the value of $x_{t-1}$ completely off track.

Besides, the value of the $\frac{1}{\sqrt{1 - \bar{\alpha}_t}}$ term is also unstable. When the process is close to end, $\frac{1}{\sqrt{1 - \bar{\alpha}_1}} \approx \frac{1}{0.01} = 100$, causing the noise weight to explode.

Therefore, we will do the following sampling steps.

First, approximate the clean image by the predicted noise:
$$
\hat{x}_0 = \frac{1}{\sqrt{\bar{\alpha}_t}} \left( x_t - \sqrt{1 - \bar{\alpha}_t} \thinspace \epsilon_\theta(x_t, t) \right)
$$
Then clip the value to a valid range (usually $[-1, 1]$ for pixel values):
$$
\hat{x}_{0,\text{clipped}} = \text{clamp}(\hat{x}_0, -1, 1)
$$
Finally, inject the clipped predicted clean image back to the original mean formula to get a more stable result.
$$
\mu_\theta = \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} \hat{x}_{0,\text{clipped}}
$$

$$
x_{t-1} = \mu_\theta + \sigma_t z, \quad z \sim \mathcal{N}(0, I)
$$

## Conclusion

The genius of DDPM lies in avoiding the direct calculation of the intractable real data distribution $q(x_t)$. Instead of forcing a neural network to model a highly complex, multi-modal image manifold all at once, Bayes' rule allows us to break down the task into **$T$ tiny, tractable, Gaussian-distributed denoising steps**.

By shifting the training objective from "predicting a perfect clean image" to "predicting a standard normal noise vector $\epsilon$", the model transforms a daunting generative task into a stable, iterative regression problem.

With these foundational math formulas locked down, we are now fully equipped to implement this elegant system in PyTorch from scratch!
