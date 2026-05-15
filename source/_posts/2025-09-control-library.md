---
title: Mastering Control with PyController Library
date: 2025-09-20 15:30:09
tags: [control, programming]
categories: [Projects]
cover: https://cdn.fireflies3072.com/blog/2025-09-control-library/cover.jpg
mathjax: true
excerpt: The world of robotics and automation hinges on effective control systems. Whether it's a drone landing precisely on a moving platform, a chemical plant maintaining a perfect reaction temperature, or a complex spacecraft navigating the cosmos, controllers are the brains that manage system dynamics. PyController is an open-source Python library designed to provide a cohesive framework for implementing, testing, and comparing cutting-edge control algorithms across diverse simulation environments.
---

## Introduction

The world of robotics and automation hinges on effective **control systems**. Whether it's a drone landing precisely on a moving platform, a chemical plant maintaining a perfect reaction temperature, or a complex spacecraft navigating the cosmos, controllers are the brains that manage system dynamics. **PyController** is an open-source Python library designed to provide a cohesive framework for implementing, testing, and comparing cutting-edge control algorithms across diverse simulation environments.

PyController makes advanced control techniques accessible, acting as a laboratory where theory meets practice. It’s built on the **Gymnasium** standard, ensuring compatibility with a wide range of popular simulation environments. It is more than just a collection of algorithms; it's a framework for competitive analysis. It offers a standardized interface for various controllers and environments, allowing researchers and engineers to quickly benchmark the performance of different strategies, from classic proportional control to modern data-driven methods. This blog post explores the algorithms and environments currently supported by the library, showcasing its utility for both education and development.

Interested in diving in? You can find the source code and contribute here: https://github.com/Fireflies3072/PyController .



## Algorithms

PyController provides robust implementations of several high-impact control strategies, each suited to different challenges and system complexities.



### PID Controller

The **Proportional-Integral-Derivative (PID) controller** is the workhorse of industrial control. It is arguably the most common control loop feedback mechanism in use today. A PID controller continuously calculates an error value as the difference between a desired setpoint and a measured process variable, and then applies a correction based on three terms:

- **Proportional (P) term:** Responds to the current error.
- **Integral (I) term:** Accounts for past errors, eliminating steady-state offset.
- **Derivative (D) term:** Predicts future errors based on the rate of change.

PID controllers are simple, effective, and require no explicit model of the system, making them incredibly versatile. The library often provides specialized wrappers, like `PID_RocketLander`, to coordinate multiple PID loops for complex systems.



### Model Predictive Control (MPC)

**Model Predictive Control (MPC)** is a sophisticated control method that explicitly uses a system's model to predict future outcomes and optimize current actions. At each time step, MPC solves an online optimization problem over a finite, receding prediction horizon. The core process involves:

1. **Predicting:** Using a mathematical model to forecast the system's behavior for a set number of future steps.
2. **Optimizing:** Calculating the sequence of control inputs that minimizes a cost function (e.g., tracking error, control effort) while satisfying constraints.
3. **Executing:** Applying only the first control action from the optimal sequence.

MPC is renowned for its ability to handle system constraints (like actuator limits) and achieve excellent performance, but it requires an accurate system model and significant computational power.



### Data-Enabled Predictive Control (DeePC)

**Data-enabled Predictive Control (DeePC)** represents a paradigm shift from model-based control (like MPC) to **data-driven control**. Instead of relying on a complex, identified mathematical model, DeePC uses only input-output data collected from the system. Its theoretical foundation is the **fundamental lemma of Willems**, which states that any future trajectory of a linear system can be represented as a linear combination of its past trajectories.

The controller formulates an online **Quadratic Program (QP)** where the decision variable is a vector of weights ($g$) that combines past system trajectories from a large data matrix (**Hankel matrix**). This optimization finds the control inputs that drive the system to the desired state while being consistent with observed system dynamics. DeePC is a powerful technique for systems where developing an accurate physical model is difficult or impossible.



## Environments

PyController leverages the Gymnasium standard to support complex, simulation-based environments for control testing.



### Rocket Lander

The **Rocket Lander** environment simulates the challenging task of landing a reusable rocket stage, akin to a SpaceX Falcon 9, onto an ocean barge. The physics are based on the Box2D engine, offering a realistic, planar (2D) simulation. The goal is to safely bring the lander to a specific target position with minimal velocity and fuel consumption. This scenario is a classic challenge for control algorithms due to the inherent instability, non-linear dynamics, and external disturbances.

**PID**

The specialized `PID_RocketLander` handles the multi-input/multi-output (MIMO) nature of the problem, controlling main engine thrust, side-engine forces, and nozzle vectoring.

<video width="500" height="400" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/rl_pid.mp4" type="video/mp4">   Not support video </video>

**MPC**

To use MPC, a calculated system matrix is needed for the controller to optimize the multi-dimensional thrust and vectoring inputs over a prediction horizon to achieve a soft and accurate touchdown.

<video width="500" height="400" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/rl_mpc.mp4" type="video/mp4">   Not support video </video>

**DeePC with data from PID controller**

Data is collected from the rocket's flight and used to predict the required thrust and vectoring for a stable descent.

<video width="500" height="400" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/rl_deepc_pid.mp4" type="video/mp4">   Not support video </video>

![](https://cdn.fireflies3072.com/blog/2025-09-control-library/rl_deepc_pid.png)

**DeePC with data from random actions**

<video width="500" height="400" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/rl_deepc_random.mp4" type="video/mp4">   Not support video </video>

![](https://cdn.fireflies3072.com/blog/2025-09-control-library/rl_deepc_random.png)



### Room Temperature

The **Room Temperature** environment models a simple, yet fundamental, problem in process control: maintaining a desired interior temperature against external thermal dynamics. This is a **Single-Input, Single-Output (SISO)** system. The state is the room's temperature ($T_{\text{current}}$), and the input is the electric **power supplied by a heater (**$P_{\text{heater}}$**)**.

The simulation is based on **Newton's Law of Cooling**, where the rate of temperature change is proportional to the difference between the room temperature and the outside temperature ($T_{\text{out}}$), plus the heat added by the controller. Key system parameters include the **cooling constant**, the **initial room temperature**, and the constant **outside temperature**. The primary objective is to drive and maintain the room temperature exactly at the comfortable setpoint of **22°C**. A control run is considered **successful** if the temperature remains within $\mathbf{0.1^\circ C}$ of the $22^\circ C$ setpoint for **20 continuous samples**.

**PID**

![](https://cdn.fireflies3072.com/blog/2025-09-control-library/rt_deepc_random.png)

**DeePC with data from random actions**

![](https://cdn.fireflies3072.com/blog/2025-09-control-library/rt_deepc_random.png)



### Inverted Pendulum

The **Inverted Pendulum** is a canonical problem in control theory. It involves a pendulum mounted on a cart, where the goal is to keep the pendulum balanced vertically upright by applying forces to the cart. This environment is inherently unstable and non-linear, making it a perfect testbed for evaluating the stability and response of control algorithms. The complexity can vary from a simple one-dimensional setup to a full-fledged cart-pole system.

**PID**

Although a standard PID can respond to position and angle at the same time with a weight, its performance is very poor. A cascaded PID is a applied here. The first PID takes position input and gives a target angle output. The second PID takes the actual angle and target angle and gives force output.

<video width="480" height="480" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/ip_pid.mp4" type="video/mp4">   Not support video </video>

**DeePC with data from PID controller**

Collecting data using the cascaded PID controller described earlier allows DeePC to replicate its stable balancing behavior, as illustrated in the following video.

<video width="480" height="480" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/ip_deepc_pid.mp4" type="video/mp4">   Not support video </video>

However, this initial implementation isn't entirely stable. The PID controller tends to produce control actions very close to zero, resulting in a Hankel matrix with a low rank of around 17. For DeePC to be effective, this matrix requires a full rank, which for our setup ($T_{\text{ini}}=3$, $T_f=5$, $u_{\text{size}}=1$, $y_{\text{size}}=4$) is calculated as $(T_{\text{ini}} + T_f) \times (u_{\text{size}} + y_{\text{size}}) = 40$.

In DeePC, the rank of the Hankel matrix reflects the diversity and richness of the collected data. A full rank indicates that the data spans the system's entire behavioral subspace, allowing the controller to accurately predict a wide range of future behaviors. Conversely, a rank-deficient matrix signals a lack of variety, constraining the controller and leading to suboptimal or unstable performance.

To resolve the rank deficiency, we introduced a small amount of Gaussian noise to the PID outputs during data collection. This successfully excited the system, increasing the rank to the required 40. With the data quality issue addressed, we tuned the regularization parameter $\lambda_g$ by searching over a logarithmic space, which yielded an optimal value of approximately 2814 based on the average number of steps per episode.

It is important to note that these results are highly sensitive to randomness in the data collection process. By default, we gather enough trajectories to form a Hankel matrix with $(T_{\text{ini}} + T_f) \times (u_{\text{size}} + y_{\text{size}} + 2) = 56$ columns. Increasing the volume of data helps mitigate this randomness, leading to more consistent and improved performance. For instance, after we increase the columns of the Hankel matrix to 200, the controller becomes much more stable, as demonstrated in the following video.

<video width="480" height="480" controls>   <source src="https://cdn.fireflies3072.com/blog/2025-09-control-library/ip_deepc_pid2.mp4" type="video/mp4">   Not support video </video>

![](https://cdn.fireflies3072.com/blog/2025-09-control-library/ip_deepc_pid2.png)



## Future Updates

The journey for PyController is just getting started, and we're excited about the road ahead. Our main focus is on expanding and refining the library to make it an even more powerful tool for the control systems community.

One of our top priorities is to enhance our existing environments. We'll be revisiting the **Lunar Lander** simulation, tuning its parameters and exploring new control strategies to create more robust and illustrative examples. We're also looking to broaden our horizons by integrating environments from different domains. The **ICU Sepsis** and **Gym Any Trading** environments, for example, present an exciting challenge. We plan to adapt and improve it to make it a better fit for classic control strategies, showcasing the versatility of PyController.

Stay tuned for more updates, and as always, we welcome contributions from the community!

## Acknowledgement

We extend our sincere thanks to the following individuals and projects:

* **Project Supervision and Guidance**
    * We are deeply grateful to our advisor, **Professor Jeremy Coulson** (Assistant Professor, University of Wisconsin–Madison), for his guidance, expertise in data-driven control, and foundational support for this project.

    * **Personal Website:** https://jeremycoulson.github.io/

* **Rocket Lander Environment**
    * **Modified by** Dylan Vogel and Gerasimos Maltezos for the 2023 Computation Control course at ETH Zurich.
    * **Original environment** created by Reuben Ferrante: [https://github.com/arex18/rocket-lander](https://github.com/arex18/rocket-lander).
* **ICU-Sepsis Environment**
    * This benchmark MDP for sepsis treatment simulation was introduced in the paper [**ICU-Sepsis: A Benchmark MDP Built from Real Medical Data**](https://arxiv.org/abs/2406.05646) by **Choudhary et al. (2024)**. It is built using the **MIMIC-III dataset**.
    * **Github link:** [icu-sepsis/icu-sepsis: ICU-Sepsis is a lightweight, yet challenging RL environment that models the treatment of sepsis in the ICU.](https://github.com/icu-sepsis/icu-sepsis)
* **gym-anytrading**
    * We utilize the Gym environment framework for reinforcement learning-based trading, as provided by the **gym-anytrading** project.
    * **Github link:** [AminHP/gym-anytrading: The most simple, flexible, and comprehensive OpenAI Gym trading environment (Approved by OpenAI Gym)](https://github.com/AminHP/gym-anytrading)
