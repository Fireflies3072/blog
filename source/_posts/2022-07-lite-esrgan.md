---
title: Lite-ESRGAN, High-Quality Super-Resolution for Everyone (Even on Low-VRAM GPUs)
date: 2022-07-21 15:20:41
tags: [AI, programming]
categories: [Projects]
cover: https://cdn.fireflies3072.com/blog/2022-07-lite-esrgan/comparison1.jpg
excerpt: Super-resolution (SR) models like Real-ESRGAN have revolutionized image upscaling, delivering incredible clarity and detail. However, their computational demands, particularly VRAM consumption, often put them out of reach for users without high-end GPUs. Enter Lite-ESRGAN, a project built to democratize high-quality SR. It is a streamlined, low-VRAM implementation of the powerful Real-ESRGAN model, ensuring you can achieve professional-grade upscaling without needing a massive graphics card.
---

## The Low-VRAM Advantage 💡

The most significant feature of Lite-ESRGAN is its efficiency. It has been optimized to drastically reduce memory usage compared to the original implementation.

For context, on a standard **4GB GPU**, the original Real-ESRGAN could typically only handle an image patch of about **300x300** pixels at a time. Lite-ESRGAN, through its optimizations, can handle an image patch up to approximately **1000x1000** pixels on the exact same hardware! This massive increase in usable patch size means faster inference, fewer memory-related issues, and the ability to process larger images seamlessly.

The project is on Github: [Fireflies3072/Lite-ESRGAN: Lite-ESRGAN: High-Quality Super-Resolution for Everyone. A streamlined, low-VRAM implementation of the Real-ESRGAN model.](https://github.com/Fireflies3072/Lite-ESRGAN)

## Getting Started 🛠️

Lite-ESRGAN is structured simply, making it easy to jump into training or inference. The core components are organized across files like `src/utils.py` (helpers), `src/dataset.py` (realistic degradations), and `src/model.py` (the `SRNet` Generator and `Discriminator`).

### Installation

You can install the package directly from the source directory:

```bash
pip install .
```

### Datasets

For training, simply place your high-resolution images under a dedicated directory, typically `data/` (or adjust the path within the training scripts).

For evaluation during training, place a sample image, such as `sample.png`, into the `test_data` folder. The model will generate an upscaled sample every few hundred steps to help you evaluate progress.

### Training (Two-Stage Process)

Training is a robust two-stage process that can be achieved on modest hardware, even a **4GB GPU**. If you have a better GPU, you can increase the `batch_size` for faster training and potentially better results.

1. Stage 1: Base Model Training

   This stage focuses on pixel-wise and perceptual loss (VGG19) to establish a strong foundation for image quality.

   ```bash
   python src/train_base.py
   ```

2. Stage 2: GAN Training

   This stage introduces the Generative Adversarial Network (GAN) loss via the Discriminator to sharpen details and produce highly realistic, photo-like textures.

   ```bash
   python src/train_gan.py
   ```

Trained models and test outputs are saved under dedicated directories, such as `./model_gan` and `./test_gan`.

### Inference

Once you have a trained model, upscaling an image is straightforward.

1. Edit `src/inference.py` to set the path of your input image (`test.png` by default).

2. Run the inference script:

   ```bash
   python src/inference.py
   ```

## Sample Result ✨

The proof of any super-resolution model is in the results. Below are side-by-side comparisons demonstrating the quality of the upscaling. The comparisons are at the same scale, showing how Lite-ESRGAN preserves and enhances details far beyond simple linear upscaling.

**Same-scale comparison:** (Left: Linear, Right: Lite-ESRGAN)

![](https://cdn.fireflies3072.com/blog/2022-07-lite-esrgan/comparison1.jpg)

![](https://cdn.fireflies3072.com/blog/2022-07-lite-esrgan/comparison2.jpg)
