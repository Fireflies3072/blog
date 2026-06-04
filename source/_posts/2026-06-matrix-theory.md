---
title: Matrix Theory Reference Sheet
date: 2026-06-04 15:42:47
tags: [math, linear-algebra]
categories: [Articles, Reference]
cover: https://cdn.fireflies3072.com/blog/2026-06-matrix-theory/cover.png
mathjax: true
excerpt: A comprehensive reference sheet of basic matrix operations, algebraic properties, and determinant formulas.
---

Welcome to this comprehensive reference sheet of basic matrix theory. This page covers fundamental matrix definitions, operations, algebraic properties, and the properties of the determinant.

## Definitions

To lay down a solid foundation, here are the definitions of fundamental types of matrices that frequently appear in linear algebra.

| Matrix Type | Mathematical Condition | Description / Notes |
| :--- | :--- | :--- |
| **Square Matrix** | $A \in \mathbb{R}^{n \times n}$ | A matrix with the same number of rows and columns. |
| **Diagonal Matrix** | $a_{ij} = 0$ for $i \neq j$ | A square matrix where all off-diagonal entries are zero. |
| **Identity Matrix** | $a_{ij} = \begin{cases} 1, & i = j \\ 0, & i \neq j \end{cases}$ | A diagonal matrix with ones on the main diagonal. Acts as the multiplicative identity. |
| **Upper Triangular** | $a_{ij} = 0$ for $i > j$ | A square matrix where all entries below the main diagonal are zero. |
| **Lower Triangular** | $a_{ij} = 0$ for $i < j$ | A square matrix where all entries above the main diagonal are zero. |
| **Symmetric Matrix** | $A = A^T$<br>($a_{ij} = a_{ji}$) | A square matrix that is equal to its transpose. |
| **Skew-Symmetric** | $A = -A^T$<br>($a_{ij} = -a_{ji}$) | A square matrix equal to its negative transpose; diagonal entries must be zero ($a_{ii} = 0$). |
| **Hermitian Matrix** | $A = A^H$<br>($a_{ij} = \overline{a_{ji}}$) | A complex square matrix equal to its conjugate transpose (the complex analogue of a symmetric matrix). |
| **Orthogonal Matrix** | $Q^T Q = Q Q^T = I$<br>($Q^{-1} = Q^T$) | A real square matrix whose rows and columns are orthonormal vectors. |
| **Unitary Matrix** | $U^H U = U U^H = I$<br>($U^{-1} = U^H$) | A complex square matrix whose conjugate transpose is its inverse (the complex analogue of an orthogonal matrix). |

## Operations

Matrix operations are the foundational building blocks of linear algebra. The table below outlines the most common operations performed on matrices, along with their mathematical notations, definitions, and constraints.

| Operation | Notation / Formula | Description | Constraints & Dimensions |
| :--- | :--- | :--- | :--- |
| **Matrix Addition** | $C = A + B$<br>$c_{ij} = a_{ij} + b_{ij}$ | Component-wise sum of two matrices. | Same dimensions: $A, B \in \mathbb{R}^{m \times n}$ |
| **Scalar Multiplication** | $B = kA$<br>$b_{ij} = k \cdot a_{ij}$ | Multiplies every element of the matrix by a scalar $k$. | $A \in \mathbb{R}^{m \times n}, k \in \mathbb{R}$ |
| **Matrix Multiplication** | $C = AB$<br>$c_{ij} = \sum_{k=1}^n a_{ik} b_{kj}$ | Standard dot-product of rows of $A$ and columns of $B$. | Inner dimensions must match: $A \in \mathbb{R}^{m \times n}, B \in \mathbb{R}^{n \times p}$ |
| **Transpose** | $B = A^T$<br>$b_{ij} = a_{ji}$ | Swaps rows and columns. | $A \in \mathbb{R}^{m \times n}$<br>$\implies A^T \in \mathbb{R}^{n \times m}$ |
| **Conjugate Transpose** | $B = A^H$ (or $A^*$)<br>$b_{ij} = \overline{a_{ji}}$ | Transposes the matrix and takes the complex conjugate of each entry. | $A \in \mathbb{C}^{m \times n}$<br>$\implies A^H \in \mathbb{C}^{n \times m}$ |
| **Matrix Inverse** | $B = A^{-1}$<br>$AA^{-1} = A^{-1}A = I$ | The unique matrix that yields the identity matrix $I$ when multiplied with $A$. | Square matrix ($n \times n$)<br>and non-singular ($\det(A) \neq 0$) |
| **Hadamard Product** | $C = A \odot B$<br>$c_{ij} = a_{ij} \cdot b_{ij}$ | Element-wise multiplication of two matrices. | Same dimensions:<br>$A, B \in \mathbb{R}^{m \times n}$ |
| **Kronecker Product** | $C = A \otimes B$<br>$C = [a_{ij}B]$ | Tensor product creating a block matrix where each element of $A$ scales $B$. | $A \in \mathbb{R}^{m \times n}, B \in \mathbb{R}^{p \times q}$<br>$\implies C \in \mathbb{R}^{mp \times nq}$ |
| **Trace** | $\operatorname{tr}(A) = \sum_{i=1}^n a_{ii}$ | Sum of the elements on the main diagonal. | Square matrix ($n \times n$) |

## Properties

Matrix algebra differs significantly from standard scalar algebra, most notably because matrix multiplication is non-commutative. The following table summarizes the key algebraic properties of matrix addition, multiplication, transposes, and inverses.

| Property Category | Mathematical Law / Identity | Description & Notes |
| :--- | :--- | :--- |
| **Commutative Law** | **Addition**: $A + B = B + A$<br>**Multiplication**: $AB \neq BA$ *(In general)* | Matrix addition is always commutative. However, matrix multiplication is strictly **non-commutative** ($AB = BA$ is only true for specific commuting matrices). |
| **Associative Law** | **Addition**: $(A + B) + C = A + (B + C)$<br>**Multiplication**: $(AB)C = A(BC)$<br>**Scalar**: $a(bA) = (ab)A$ | Parentheses can be grouped freely for addition, multiplication, and scalar scaling. |
| **Distributive Law** | **Left Distributive**: $A(B + C) = AB + AC$<br>**Right Distributive**: $(A + B)C = AC + BC$<br>**Scalar Distributive**: $k(A + B) = kA + kB$ | Matrix multiplication distributes over matrix addition from both the left and right sides. |
| **Identity & Zero** | **Identity**: $AI_n = I_m A = A$<br>**Zero Addition**: $A + 0 = A$<br>**Zero Product**: $A \cdot 0 = 0$ and $0 \cdot A = 0$ | $I$ represents the identity matrix, and $0$ is the zero matrix of matching dimensions. |
| **Transpose Properties** | **Involution**: $(A^T)^T = A$<br>**Sum**: $(A + B)^T = A^T + B^T$<br>**Scalar**: $(kA)^T = kA^T$<br>**Product**: $(AB)^T = B^T A^T$ | **Note the reversed order** in the product transpose: $(AB)^T = B^T A^T$. |
| **Inverse Properties** | **Involution**: $(A^{-1})^{-1} = A$<br>**Scalar**: $(kA)^{-1} = \frac{1}{k}A^{-1}$ ($k \neq 0$)<br>**Product**: $(AB)^{-1} = B^{-1}A^{-1}$<br>**Transpose**: $(A^T)^{-1} = (A^{-1})^T$<br>**Hermitian**: $(A^H)^{-1} = (A^{-1})^H$ | Appliable only to non-singular, square matrices. **Note the reversed order** in the product inverse: $(AB)^{-1} = B^{-1}A^{-1}$. |
| **Hermitian Properties** | **Involution**: $(A^H)^H = A$<br>**Sum**: $(A + B)^H = A^H + B^H$<br>**Scalar**: $(kA)^H = \overline{k}A^H$<br>**Product**: $(AB)^H = B^H A^H$ | Applies to conjugate transposes over the complex field $\mathbb{C}$. $\overline{k}$ is the complex conjugate of $k$. |

## Determinant

The determinant is a scalar value computed from a square matrix that encodes crucial properties of the linear transformation represented by the matrix, such as its volume scaling factor and invertibility.

### Fundamental Calculations

For small square matrices, the determinant is calculated as:

- **$2 \times 2$ Matrix:**
  $$\det \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$

- **$3 \times 3$ Matrix (Sarrus' Rule / Cofactor Expansion):**
  $$\det \begin{pmatrix} a & b & c \\ d & e & f \\ g & h & i \end{pmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)$$

- **Higher Dimensions ($n \times n$ Matrices):**
  For $n > 3$, the determinant can be calculated recursively using **Laplace (Cofactor) Expansion** along any row $i$ or column $j$:
  $$\det(A) = \sum_{j=1}^n (-1)^{i+j} a_{ij} \det(M_{ij})$$
  where $M_{ij}$ is the $(n-1) \times (n-1)$ submatrix (minor) obtained by deleting the $i$-th row and $j$-th column of $A$.
  
  Alternatively, the general **Leibniz Formula** defines the determinant for any dimension:
  $$\det(A) = \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma) \prod_{i=1}^n a_{i, \sigma(i)}$$
  where $S_n$ is the set of all permutations of $\{1, 2, \dots, n\}$, and $\operatorname{sgn}(\sigma) \in \{+1, -1\}$ is the signature of the permutation $\sigma$.

### Core Properties of Determinants

Let $A$ and $B$ be $n \times n$ square matrices, and let $k$ be a scalar.

| Property | Mathematical Formula | Description / Notes |
| :--- | :--- | :--- |
| **Multiplicative** | $\det(AB) = \det(A) \cdot \det(B)$ | Generalizes to: $\det(A_1 A_2 \cdots A_m) = \prod_{i=1}^m \det(A_i)$ |
| **Transpose** | $\det(A^T) = \det(A)$ | The determinant of a matrix equals the determinant of its transpose. |
| **Conjugate Transpose** | $\det(A^H) = \overline{\det(A)}$ | The determinant of the conjugate transpose is the complex conjugate of the determinant. |
| **Inverse** | $\det(A^{-1}) = \frac{1}{\det(A)}$ | Applies if $A$ is invertible ($\det(A) \neq 0$). |
| **Scalar Multiplication** | $\det(kA) = k^n \det(A)$ | Scaling an $n \times n$ matrix scales each of its $n$ rows. |
| **Determinant of Powers** | $\det(A^p) = (\det(A))^p$ | For any integer $p \ge 1$ (and $p < 0$ if $A$ is invertible). |
| **Singularity & Invertibility** | $A \text{ is invertible}$<br>$\iff \det(A) \neq 0$ | A square matrix is invertible if and only if its determinant is non-zero. |
| **Diagonal & Triangular** | $\det(A) = \prod_{i=1}^n a_{ii}$ | If $A$ is diagonal, upper triangular, or lower triangular. |
| **Orthogonal Matrix** | $\det(Q) = \pm 1$ | If $Q$ is real orthogonal ($Q^T Q = I$). |
| **Unitary Matrix** | $|\det(U)| = 1$ | If $U$ is complex unitary ($U^H U = I$). |

### Effects of Elementary Row Operations

When performing Gaussian elimination, the determinant changes predictably with each type of elementary row operation:

1. **Row Interchanges (Swapping two rows):**
   Swapping any two rows multiplies the determinant by $-1$.
   $$\det(E_{\text{swap}} A) = -\det(A)$$

2. **Row Scaling (Multiplying a row by a scalar $c$):**
   Multiplying a single row by a scalar $c$ multiplies the determinant by $c$.
   $$\det(E_{\text{scale}} A) = c \det(A)$$

3. **Row Addition (Adding a multiple of one row to another):**
   Adding a scalar multiple of one row to another row does not change the determinant.
   $$\det(E_{\text{add}} A) = \det(A)$$
