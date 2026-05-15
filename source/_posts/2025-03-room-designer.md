---
title: LLM-supported 3D Modeling Tool for Radio Radiance Field Reconstruction
date: 2025-03-09 16:51:21
tags: [AI, LLM, programming]
categories: [Projects]
cover: https://cdn.fireflies3072.com/blog/2025-03-room-designer/cover.jpg
mathjax: true
excerpt: The paper introduces a locally deployable tool that uses fine-tuned language models (T5-mini) and generative 3D frameworks within Blender to simplify the creation of complex 3D environments via a chat interface, significantly reducing the modeling complexity required for Radio Radiance Field (RRF) reconstruction in wireless research.
---

## Creating 3D Worlds with a Chat: A New Tool for Wireless Research

Imagine designing a complex environment for cutting-edge wireless research just by describing it in a chat. That's the core idea behind a new **LLM-supported 3D modeling tool** developed to simplify the creation of 3D environments for **Radio Radiance Field (RRF)** reconstruction. This tool dramatically lowers the barrier to entry for researchers, making it much easier to build the precise 3D scenes needed for next-generation channel modeling.

💡 **Status:** Submitted to ICC 2026 (Under Review).
📥 **Download:** [Click here to view the Full Paper (PDF)](https://cdn.fireflies3072.com/blog/2025-03-room-designer/3D_modeling.pdf)

### The Challenge: RRF and 3D Modeling

The **Radio Radiance Field (RRF)** has emerged as a promising approach for modeling wireless channels. Unlike traditional methods, RRF provides a comprehensive spatial representation of how radio waves propagate, capturing crucial channel parameters like gain, angle of arrival, and delay in a 3D space.

However, accurately reconstructing an RRF, for example with methods like RF-3DGS, traditionally demands an accurate 3D model of the environment. Creating this model usually requires labor-intensive physical measurements and advanced computer vision techniques, which can be a significant hurdle for researchers.

### The Solution: An Intuitive, Chat-Based Interface

This new tool addresses the complexity of 3D modeling by integrating locally deployed Large Language Models (LLMs) and generative frameworks with the industry-standard **Blender** software. The result is an intuitive, chat-based interface that lets users create and manipulate complex 3D models using simple natural language commands.

![](https://cdn.fireflies3072.com/blog/2025-03-room-designer/structure.drawio.png)

### How the Tool Works: The Core Components

The system has three main components that work together to turn a user's text description into a scene ready for RRF reconstruction: natural language parsing, 3D model creation/selection, and output interfacing.

1.  **User Command Parsing**: This is where natural language meets machine code. A fine-tuned **T5-mini** model is used to convert the user's chat input (e.g., "Add a nightstand, then put a lamp on it") into a structured, machine-readable format: a **JSON array of action objects**. The fine-tuned T5-mini model was chosen for its excellent balance of high accuracy (85.91%) and low computational cost, achieving the best trade-off for a locally deployable tool.

2.  **3D Model Creation and Selection**: When the system needs an object, it can either **create a new 3D model** or **retrieve one from a local library**.
    * **Creation**: Two generative models are available: **Shap-E** for higher visual quality (slower) and **LLaMA-Mesh** for faster, text-token-based generation (lower detail). Users can choose based on their need for speed versus fidelity.
    * **Selection**: To find an existing object, the system uses a fine-tuned **all-MiniLM-L6-v2** model for semantic search, allowing users to describe the object (e.g., "a vase with a wide base") instead of requiring a specific file name.

3.  **Blender Integration and Output Interfacing**: The final step ensures compatibility with the RRF pipeline.
    * An **Executor Plugin** is created as a server in Blender that listens to requests and executes the structured JSON commands, applying the requested modifications to the 3D scene.
    * A custom **Export Plugin** is critical for compatibility. It converts all mesh objects into individual **Polygon File Format (PLY)** files and generates a single **Extensible Markup Language (XML) file** that describes the scene structure and material properties, making it ready for the RF-3DGS pipeline.

### Real-World Demonstrations

The tool was successfully demonstrated by constructing two complex indoor environments: the **NIST lobby** and the **wireless lab at the University of Wisconsin-Madison (UW-Madison)**. The system was able to generate scenes that were highly comparable to those built using traditional manual methods.

**NIST**

![](https://cdn.fireflies3072.com/blog/2025-03-room-designer/nist.jpg)

**UW-Madison**

![](https://cdn.fireflies3072.com/blog/2025-03-room-designer/uwm_lab.jpg)
