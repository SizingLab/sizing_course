(page_lab_vega)=
Lab - Multirotor case study
=======================

```{warning}
This course is under construction...
```

The multirotor sizing and optimization project is available on this repository:
https://github.com/SizingLab/multirotor_sizing_isae_coa_2023_student_version

### Colab
Open [Google Colab](https://colab.research.google.com), open a new notebook and clone the repository by running in a cell:

`! git clone https://github.com/SizingLab/multirotor_sizing_isae_coa_2023_student_version.git`

Then install the required dependencies by running in a cell:

`!pip install -r multirotor_sizing_isae_coa_2023_student_version/requirements.txt`


### Jupyter Hub
Open [Jupyter Hub](https://jupyter.isae-supaero.fr), open a new terminal and clone the repository by running:

`git clone https://github.com/SizingLab/multirotor_sizing_isae_coa_2023_student_version.git`

```{tip}
To cancel your local changes and update your project with the lastest version available on the repo you can run:

`git reset --hard`

`git fetch`

`git pull`
```

Then install the required dependencies by running:

`pip install -r multirotor_sizing_isae_coa_2023_student_version/requirements.txt`

```{tip}
To zip the folder you can open a terminal at the father directory of the project and run:

`zip -r my_projet.zip multirotor_sizing_isae_coa_2023_student_version`

You can then download the .zip from Jupyter Hub as a normal file.
```

### Binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SizingLab/multirotor_sizing_isae_coa_2023_student_version/HEAD)

### Local
Download the zip file from [Github](https://github.com/SizingLab/multirotor_sizing_isae_coa_2023_student_version) and unzip it.
Open a Anaconda Prompt terminal and `cd` to the recently unziped folder.

You can then create a new conda environment by running:

`conda create -n multirotor python=3.8`

`conda activate multirotor`

Then install required dependencies:
`pip install -r requirements.txt`

Run jupyter lab:
`jupyter lab`