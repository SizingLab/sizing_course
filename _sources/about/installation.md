![](../images/header.jpg)

# Installation

The sizing course is available on this repository:
https://github.com/SizingLab/sizing_course

### Colab
Open [Google Colab](https://colab.research.google.com), open a new notebook and clone the repository by running in a cell:

`! git clone https://github.com/SizingLab/sizing_course.git`

Then install the required dependencies by running in a cell:

`!pip install -r sizing_course/requirements.txt`


### Jupyter Hub
Open [Jupyter Hub](https://jupyter.isae-supaero.fr), open a new terminal and clone the repository by running:

`git clone https://github.com/SizingLab/sizing_course.git`

```{tip}
To cancel your local changes and update your project with the lastest version available on the repo you can run:

`git reset --hard`

`git fetch`

`git pull`
```

Then, create a new conda environment by running:

`conda create -n sizing_course python=3.9`

`source activate sizing_course` or `conda activate sizing_course`


Then install the required dependencies by running:

`pip install -r sizing_course/requirements.txt`


Then, create a new kernel accessible from Jupyter Lab:
`conda install ipykernel`

`ipython kernel install --user --name=sizing_course`


```{tip}
To zip the folder you can open a terminal at the father directory of the project and run:

`zip -r my_projet.zip sizing_course`

You can then download the .zip from Jupyter Hub as a normal file.
```

### Binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SizingLab/sizing_course/HEAD)

### Local
Download the zip file from [Github](https://github.com/SizingLab/sizing_course) and unzip it.
Open a Anaconda Prompt terminal and `cd` to the recently unziped folder.

For ISAE-SUPAERO students, you can run the following line to activate conda:
`module load anaconda3/2023`

You can then create a new conda environment by running:

`conda create -n sizing_course python=3.9`

`conda activate sizing_course` or `source activate sizing_course`

Then install required dependencies:
`pip install -r requirements.txt`

Run jupyter lab:
`jupyter lab`