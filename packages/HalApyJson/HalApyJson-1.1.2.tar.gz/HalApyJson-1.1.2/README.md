# HalApyJson
## Description
A light interface to query [HAL](https://api.archives-ouvertes.fr/docs) through its API.

## Installation
Run the following to install:
```python
pip install HalApyJson
```

## Usage example
```python
import HalApyJson as haj
year = "2023"
institute = "Liten"
hal_df = haj.build_hal_df_from_api(year,institute)
hal_df.to_excel(<your_fullpath_file.xlsx>, index = False)
```
**CLI exemple**
```python
cli_hal -y 2023 -i liten
```
**for more exemples refer to** [HalApyJson-exemples](https://github.com/Bertin-fap/HalApyJson/blob/main/Demo_HalApyJson.ipynb).


# Release History
- 1.0.0 first release
- 1.1.0 added CLI
- 1.1.1 removed prints
- 1.1.2 updated CLI


# Meta
	- authors : BiblioAnalysis team

Distributed under the [MIT license](https://mit-license.org/)