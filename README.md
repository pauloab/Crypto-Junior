# Crypto-Junior
A didactic example of cryptography using matricial product.

## Installation

1. Clone repo using  `git clone`

```bash
git clone https://github.com/pauloab/Crypto-Junior/
```

2. Run it with python interpreter

```python
python encriptador.py
```

 Or just run `encriptador.exe` version in `dist` folder
	 
## Usage

### Enctypt

1. Pass a string with a length major to 3 characters

2. Pass a invertible matrix of 3X3 order separated by a space. For example

```
2 -1 1 1 3 -1 1 2 1
```

Note: Isn't necessary separate each row, automatically the program will catch it.

### De-encrypt

1. Pass a cripted string by this program exactly as it passed. For example:

```
52 65 -13 51 106 10 43 6 16 30 65 20 32 72 5 29 3 7 24 56 -3 30 41 -9
```

2. Pass the key/password (invertible matrix) with it was crypted by, in this case:

```
2 -1 1 1 3 -1 1 2 1
```

## How it works

It's a simple encryptation algorithm, first it take the letters and replace it with a dictionary of numbers, and create 1x3 matrices, if the text don't populate all the matrix, it will be populated with 0.

Then, it just take an invertible matrix and multiply it for each 1x3 matrix.

Is important that the crypter matrix be invetible, because to the de-cryptation process, we'll do the inverse process, and need to found the inverse of the crypter matrix to multiply it for each 1x3 chunked matrix.

## License
[MIT](https://choosealicense.com/licenses/mit/)
