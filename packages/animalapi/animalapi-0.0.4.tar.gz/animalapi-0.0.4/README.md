<h1 align="center">animalapi</h1>

<p align="center">
  A simple Python wrapper for the <a href="https://some-random-api.ml/">some-random-api.ml</a> API.
  <br />
  <a href="https://pypi.org/project/animalapi">
    <img src="https://img.shields.io/pypi/v/animalapi.svg" alt="PyPI version" />
  </a>
  <a href="https://github.com/dashutosh04/animalapi/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/dashutosh04/animalapi.svg" alt="License" />
  </a>
</p>

<p align="center">
  Easily access animal images and facts in your Python projects.
</p>

## Features

* **Random Animal Data:** Get randomized animal data (image and fact) with `rand_animals()`.
* **Specific Animal Data:** Fetch data for a specific animal using `animal_data(animal_name)`.
* **Supported Animals:**  Currently supports "dog", "cat", "bird" and "koala".
* **Error Handling:**  Provides informative error messages and handles invalid animal names and API request errors.

## Installation

```bash
pip install animalapi
```

## Usage
> Get random animal data

```Python
import animalapi as a

data = a.rand_animals()
img = data["image"]
fact = data["fact"]

print(img) 
print(fact) 
```

> Get data for a specific animal
```Python
import animalapi as a

data = a.animal_data("dog")
img = data["image"]
fact = data["fact"]

print(img)
print(fact)
```

### Contributing
Contributions are welcome! Feel free to open issues or pull requests.

### License
This project is licensed under the MIT License - see the LICENSE file for details. 