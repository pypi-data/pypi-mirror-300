# minigrad

**minigrad** is a toy implementation of an autograd engine, inspired by Andrej Karpathy's [micrograd](https://github.com/karpathy/micrograd) project, with and API similar to that of **PyTorch**. It supports both CPU and GPU operations using `NumPy` and `CuPy`, respectively.

My goal with minigrad is to explore and learn the internals of deep learning frameworks — minigrad is not optimized for speed or efficiency. As of now it provides basic tensor operations, back propagation, neural network layers, optimizers, and loss functions.

## Features

- **Tensor Operations**: Supports basic tensor operations with automatic differentiation.
- **CPU and GPU Support**: Use `NumPy` for CPU operations and `CuPy` for GPU operations.
- **Neural Networks**: Includes simple layers like `Linear` and activations like `ReLU`
- **Optimizers**: Implements basic optimizers like `SGD`.
- **Loss Functions**: Provides loss functions like `MSELoss`.

## Requirements

If you plan to use CuPy with GPU support, make sure you have the following installed:

- **CUDA Toolkit**: Ensure that the appropriate CUDA Toolkit is installed on your machine. You can download it from [NVIDIA CUDA Website](https://developer.nvidia.com/cuda-downloads).

- `nvcc`: The CUDA compiler (`nvcc`) should be available in your environment, as it is used to detect the installed CUDA version. You can check if `nvcc` is installed by running:

```bash
nvcc --version
```

## Installation

To install minigrad:

```bash
pip install minigrad-python
```

## Usage

### Basic Usage

```python
import minigrad as mg

a = mg.Tensor([1, 2, 3], device='gpu')
b = mg.Tensor([2, 3, 4], device='gpu')
c = a + b
d = c.sum()
d.backward()
print(a.grad)
print(b.grad)
```

### Training a Neural Network

- A very simple example of training a neural network can be found in `examples/simple_nn.py`
- TODO: Add more examples.

## Run Tests

To run the unit tests and benchmarks for the project

```bash
pytest
```
