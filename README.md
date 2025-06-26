
# Mini Programming Language Model

An LSTM-based neural network that generates simple programming code sequences, designed for educational purposes.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Architecture](#model-architecture)
- [Data Generation](#data-generation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

-  **LSTM-based** sequence generation
-  Generates pseudo-code with:
  - Variable assignments (`x = y + 1`)
  - Conditional statements (`if x > 0 then ...`)
  - For-loops (`for x in 0..5 ...`)
  - Print statements (`print x`)

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Steps
1. Clone the repository:
```bash
git clone https://github.com/aivazovaa/mini_lang_model.git
cd mini_lang_model
```

2. Install dependencies:
```bash
pip install -r src/requirements.txt
```

## Usage

### 1. Generate Training Data
```bash
python src/data_generator.py
```
This creates a `data.txt` file with 100,000 synthetic samples.

### 2. Train the Model
```bash
python src/train.py data/data.txt
```
Training parameters (configurable in `train.py`):
- Sequence length: 20 tokens
- Embedding dimension: 128
- LSTM units: 256
- Batch size: 64
- Epochs: 10

### 3. Generate Code Interactively
```bash
python src/generate.py
```
Example session:
```
Enter partial code (empty line to finish):
if x > 0 then

Generated code: if x > 0 then print 1 <EOS>
```

## Project Structure

```
mini_lang_model/
├── src/
│   ├── model.py            
│   ├── train.py            
│   ├── generate.py         
│   ├── data_generator.py   
│   └── requirements.txt    
├── data/                   
├── docs/                   
└── README.md
```


Key components:
- **Embedding Layer**: 128-dimensional word embeddings
- **LSTM Layers**: Two layers with 256 units each
- **Dropout**: 20% dropout for regularization
- **Output**: Softmax over vocabulary



Supported constructs:
- Arithmetic operations (`+`, `-`, `<`, `>`)
- Variables (`x`, `y`)
- Constants (`0`, `1`, `2`)
- Control flow (`if-then`, `for` loops)

## Examples

### Sample Generated Code
```
1. x = y + 1
2. if x > 0 then print x
3. for x 0 5 print x
```

### Training Output
```
Epoch 1/10
1875/1875 [==============================] - 45s 24ms/step - loss: 1.2345 - accuracy: 0.5678
Epoch 2/10
1875/1875 [==============================] - 44s 23ms/step - loss: 0.8765 - accuracy: 0.6789
```

 Generate Code Interactively


```
python src/generate.py
```

Example session:

```
Enter partial code lines (empty line to finish):
if x > 0 then

--- Generation Result ---
Generated code: if x > 0 then print 1 <EOS>
```
