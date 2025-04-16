![PyPI](https://img.shields.io/pypi/v/datosgobes) 
# datosgobes

## Introduction
datosgobes is a python library that provides a simple interface to access the open data API of [https://datos.gob.es/es/](https://datos.gob.es/es/). The package is designed to make it easy for users to retrieve and analyze data from the API.

It is inspired in the R library [rOpenSpain/opendataes](https://github.com/rOpenSpain/opendataes).

## Installation

You can install datosgobes using pip:

```python
pip install datosgobes
```


## Usage
Once installed, you can start using datosgobes by importing it in your python script:

```python
import datosgobes 
```

First, you need to initialize the manager:

```python
manager = datosgobes.Manager()
```

Then, you can use the manager to search for datasets:

```python
datasets = manager.search_datasets('sanidad')
```

You can also retrieve a dataset by its identifier:

```python
dataset = manager.get_dataset('l01080193-resultados-absolutos-de-las-elecciones-al-parlamento-europeo-de-la-ciudad-de-barcelona')
```

Once you have a dataset, you can retrieve its metadata, title, description...:

```python
print(dataset.title)
print(dataset.description)
```

Each dataset can contain multiple distributions. They are stored in a list called `distributions`:

```python
print(dataset.distributions)
```

You can retrieve the data from a distribution by its list index:

```python
distribution = dataset.distribution[0]
```

The distribution is a class that contains information about the data, such as its title, description, format...:

```python
print(distribution.title)
print(distribution.description)
print(distribution.format)
```
Finally, you can retrieve the data from the distribution:

```python
data = distribution.data
```

The data is returned as a pandas DataFrame, if the format is recognized, or as a raw string otherwise.
You can use it as you wish.

## Collaboration

If you want to contribute to the project, you can fork the repository and submit a pull request. Please make sure to follow the coding standards and documentation guidelines.

## License

datosgobes is released under the MIT license.

