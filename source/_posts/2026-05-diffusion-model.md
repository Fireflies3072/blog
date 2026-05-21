---
title: Understanding Diffusion Models - A Mathematical Derivation
date: 2026-05-21 15:44:15
tags: [AI, diffusion]
categories: [Articles]
---

## Introduction

Diffusion models have recently taken the generative AI world by storm, powering state-of-the-art systems like DALL-E 2, Imagen, and Stable Diffusion. Unlike GANs or VAEs, diffusion models work by gradually adding noise to data and then learning to reverse this process.

In this post, we will dive deep into the mathematical foundations of Denoising Diffusion Probabilistic Models (DDPM).

## The Forward Process (Diffusion)

The forward process, also known as the diffusion process, gradually adds Gaussian noise to the data $x_0 \sim q(x_0)$ over $T$ steps.

Each step in the forward process is defined as:
$$
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t I)
$$
where $\beta_t$ is a variance schedule.

A key property of the forward process is that we can sample $x_t$ at any arbitrary time step $t$ directly from $x_0$. Let $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t = \prod_{i=1}^t \alpha_i$. Then:
$$
x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)
$$
Or equivalently:
$$
q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) I)
$$

## The Reverse Process (Generative)

The goal of a diffusion model is to learn the reverse process $q(x_{t-1} | x_t)$. If we can reverse the noise addition, we can start from pure noise $x_T \sim \mathcal{N}(0, I)$ and generate new data samples.

However, $q(x_{t-1} | x_t)$ is intractable because it depends on the entire data distribution. Instead, we approximate it with a learned model $p_\theta$:
$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

## The Evidence Lower Bound (ELBO)

To train the model, we want to maximize the log-likelihood of the data $\log p_\theta(x_0)$. Similar to VAEs, we optimize the Evidence Lower Bound (ELBO):
$$\log p_\theta(x_0) \geq \mathbb{E}_{q(x_{1:T} | x_0)} \left[ \log \frac{p_\theta(x_{0:T})}{q(x_{1:T} | x_0)} \right]$$

After some algebraic manipulation, the ELBO can be decomposed into several terms:
$$L = \mathbb{E}_q [ \underbrace{D_{KL}(q(x_T | x_0) || p(x_T))}_{L_T} + \sum_{t>1} \underbrace{D_{KL}(q(x_{t-1} | x_t, x_0) || p_\theta(x_{t-1} | x_t))}_{L_{t-1}} \underbrace{- \log p_\theta(x_0 | x_1)}_{L_0} ]$$

The term $L_{t-1}$ is the most important. It compares the learned reverse step $p_\theta(x_{t-1} | x_t)$ with the ground truth reverse step conditioned on $x_0$, which is tractable:
$$q(x_{t-1} | x_t, x_0) = \mathcal{N}(x_{t-1}; \tilde{\mu}_t(x_t, x_0), \tilde{\beta}_t I)$$
where:
$$\tilde{\mu}_t(x_t, x_0) = \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} x_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} x_0$$

## Simplifying the Loss

Ho et al. (2020) found that a simplified version of this loss works better in practice. By reparameterizing $x_0$ in terms of $x_t$ and $\epsilon$:
$$x_0 = \frac{1}{\sqrt{\bar{\alpha}_t}} (x_t - \sqrt{1 - \bar{\alpha}_t} \epsilon)$$
we can rewrite the mean $\tilde{\mu}_t$ as a function of $x_t$ and the noise $\epsilon$. The model $\mu_\theta$ then becomes a noise predictor $\epsilon_\theta$:
$$L_{simple} = \mathbb{E}_{t, x_0, \epsilon} [ || \epsilon - \epsilon_\theta(x_t, t) ||^2 ]$$
where $x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$.

## Conclusion

The mathematical beauty of diffusion models lies in how they transform a complex generative task into a simple iterative denoising problem. By minimizing the difference between the actual noise added and the noise predicted by the network, we enable the model to generate high-quality, diverse samples from pure Gaussian noise.

Stay tuned for the next post where we will implement a DDPM from scratch using PyTorch!
