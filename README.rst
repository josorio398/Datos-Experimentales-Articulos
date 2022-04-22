
Solubility Models Library
=========================

The analysis of multicomponent systems leads to elucidate or in its effect to describe in an approximate way the different phenomena
as molecular interactions between the components of a system.

Understanding the behavior of these phenomena allows the development of theoretical models to predict the different properties of the
system, generating computer tools that, in addition to facilitating the analysis, allow a better understanding of the different factors
involved in the solution process.

One of the most important properties is the **solubility**, since it is one of the most important stages in the research and development 
of pharmaceutical products, since it affects the biopharmaceutical and pharmacokinetic characteristics of the pharmaceutical forms. It is,
therefore, that one of the most important lines of research in solution thermodynamics are mathematical models that allow predicting solubility
with very low error ranges.

|travis| |Group| |coveralls| |libraries| |lgtm| |Languages| |IDE| |Education|

.. |travis| image:: https://img.shields.io/badge/python%20-%2314354C.svg?&style=flat&logo=python&logoColor=white
  :target: https://www.python.org/
  :alt: Tests

.. |Group| image:: https://img.shields.io/badge/Pandas%20-2C2D72?style=flat&logo=pandas&logoColor=white
  :target: https://pandas.pydata.org/
  :alt: Dependencies

.. |coveralls| image:: https://img.shields.io/badge/numpy%20-%230095D5.svg?&style=flat&logo=numpy&logoColor=white
  :target: https://numpy.org/
  :alt: Coverage

.. |libraries| image:: https://img.shields.io/badge/scipy%20-00599C?style=flat&logo=scipy&logoColor=white
  :target: https://scipy.org/
  :alt: Dependencies

.. |lgtm| image::  https://img.shields.io/badge/plotly%20-%233B4D98.svg?&style=flat&logo=plotly&logoColor=white
  :target: https://plotly.com/
  :alt: LGTM

.. |Languages| image:: https://img.shields.io/badge/LaTex%20-%23239120.svg?&style=flat&logo=latex&logoColor=white
  :target: https://www.latex-project.org/
  :alt: Dependencies

.. |IDE| image:: https://img.shields.io/badge/Colab%20--FFAD00?style=flat&logo=googlecolab&logoColor=white
  :target: https://colab.research.google.com/
  :alt: Dependencies

.. |Education| image:: https://img.shields.io/badge/Jupyter%20-F79114?style=flat&logo=Jupyter&logoColor=white
  :target: https://jupyter.org/
  :alt: Dependencies

Solubility Models 
=================

Solubility Models is a library for the calculation of fit parameters, calculated values, statisticians and plotting graph of 
calculated values and experimental of solubility models such as :

- Modified Apelblat
- van't Hoff
- van't Hoff-Yaws
- Modified Wilson
- Buchowski Ksiazaczak λh 
- NRTL
- Wilson
- Weibull of two parameters
  
Installation of requirements
============================
Before installing the library you must verify the execution environment and install the following requirements:

Google Colaboratory Support
---------------------------

For use in Google Colab (https://colab.research.google.com/) install texlive-fonts, texlive-fonts-extra and dvipng package using:

.. code:: python

    !apt install texlive-fonts-recommended texlive-fonts-extra cm-super dvipng

Jupyter Notebook and JupyterLab Support 
---------------------------------------

For use in Jupyter Notebook and JupyterLab (https://anaconda.org/) install jupyter-dash and  python-kaleido packages using:

.. code:: python

    conda install -c plotly jupyter-dash
    conda install -c plotly python-kaleido

Datalore Support 
----------------

For use in the enviroment Datalore (https://datalore.jetbrains.com) install texlive-fonts, texlive-fonts-extra and dvipng 
package using:

.. code:: python

    !sudo apt-get update
    !sudo apt install texlive-fonts-recommended texlive-fonts-extra cm-super dvipng -y

Installation and import of SolubilityModels
===========================================

Solubility models may be installed using pip...
  
.. code:: python

    !pip install SolubilityModels

To import all solubility models you can use:

.. code:: python

    from SolubilityModels.Models import *

To import a particular model you can use the model name e.g:

.. code:: python

    from SolubilityModels.Modified_Apelblat import *

Data Upload
===========

For upload the dataset according to the format of the standard table (https://da.gd/CAx7m) as a path or url in extension 
"xlsx" or "csv" using:

.. code:: python

    data = dataset("url or path")

Class model
===========

The model class allows the computational analysis of the data according to a particular solubility model,
as an example, the following code is presented:

.. code:: python

  from SolubilityModels.Models import *
  data = dataset("https://raw.githubusercontent.com/SolubilityGroup/Thermodynamic_Solutions/main/Test%20data/SMT-MeCN-MeOH.csv")
 
  model_λh = model.buchowski_ksiazaczak(data,Tf = 471.55)

Equation method
---------------
Method to show the equation of the chosen solubility model.

.. code:: python

  model_λh.equation

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/equation.png?raw=true
   :height: 80
   :align: center
   :alt: alternate text 

Experimental values method
--------------------------

Method to show and download in different formats ("xlsx","csv","tex","pdf") the dataframe experimental values of the model, 
the experimental mole fractions of solubility can be multiplied by a power of ten.

.. code:: python

  model_λh.experimental_values(scale = 2, download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/experimental.png?raw=true
   :height: 380
   :align: center
   :alt: alternate text 

Parameters method
-----------------

Method to show the model fit parameters with their standard deviation for each mass fraction 
in a dataframe. Download in different formats the parameters dataframe.

.. code:: python

  model_λh.parameters(cmap ="Reds",download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/parameters.png?raw=true
   :height: 350
   :align: center
   :alt: alternate text 

Calculate values method
-----------------------

Method to show the table of calculated values of the solubility according to temperatures 
and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

.. code:: python

  model_λh.calculated_values(scale=2,download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/calculate.png?raw=true
   :height: 350
   :align: center
   :alt: alternate text 

Relative deviations method
--------------------------

Method to show the table relative deviations for each value calculated according
to temperatures and mass fractions in a dataframe. Download in different formats 
the relative deviations dataframe.

.. code:: python

  model_λh.relative_deviations(scale = 2,download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/relative.png?raw=true
   :height: 350
   :align: center
   :alt: alternate text 

Statisticians method
--------------------

Method to show the table of statisticians of the model in a dataframe.

.. code:: python

  model_λh.statisticians(download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/statisticians.png?raw=true
   :height: 200
   :align: center
   :alt: alternate text 

Plot method
-----------

Method to shows the graph of calculated values and experimental values of solubility
completely or separately according to mass fractions. Download in different formats 
the graph.

.. code:: python

  model_λh.plot()

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/plotpng.png?raw=true
   :height: 400
   :align: center
   :alt: alternate text 

.. code:: python

  model_λh.plot(download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/plotex.png?raw=true
   :height: 350
   :align: center
   :alt: alternate text 

.. code:: python

  model_λh.plot(apart=True)

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/plotapart.png?raw=true
   :height: 400
   :align: center
   :alt: alternate text 

.. code:: python

  model_λh.plot(apart=True,download_format="tex")

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/plotapartlatex.png?raw=true
   :height: 600
   :align: center
   :alt: alternate text 

Class models
============

The models class allows the computational analysis of the data in all the models loaded in the library, with the 
``statisticians``  and  ``plots`` methods.

Statisticians method
--------------------

Method to show the table of statisticians of all models in a dataframe.

.. code:: python

  models.statisticians(data,Tf = 403.4)

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/stadall.png?raw=true
   :height: 180
   :align: center
   :alt: alternate text 

.. code:: python

  models.statisticians(data,Tf = 403.4,download_format='tex')

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/stadallatex.png?raw=true
   :height: 250
   :align: center
   :alt: alternate text 


Plots method
--------------------

Method to shows the graphs of calculated values and experimental values of solubility
for all models. Download in different formats the graph.

.. code:: python

  models.plots(data,Tf = 403.4)

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/plotmodelspng.png?raw=true
   :height: 350
   :align: center
   :alt: alternate text 

.. code:: python

  models.plots(data,Tf = 403.4,download_format='tex')

.. image:: https://github.com/josorio398/Solubility_Models_Library/blob/main/Test%20data/images/plotallatex.png?raw=true
   :height: 600
   :align: center
   :alt: alternate text 

Citation
========

To cite SolubilityModels in publications use:

-  J. Osorio Gallego, R.E. Cárdenas Torres, C.D. Rodriguez Quiroga, C.P. Ortiz, D.R. Delgado, Solubility Models Library, Python Package Index. (2022). https://pypi.org/project/SolubilityModels/


Contributors
============

- **Prof. Jhonny Osorio Gallego, M.Sc.**

https://github.com/josorio398

Fundación Universidad de América

jhonny.osorio@profesores.uamerica.edu.co


- **Prof. Rossember Eden Cárdenas Torres, M.Sc.**

https://github.com/Rossember555

Fundación Universidad de América

rossember.cardenas@profesores.uamerica.edu.co

- **Ing. Cristhian David Rodriguez Quiroga**

https://github.com/CQuiroga97

Universidad Central

crodriguezq@ucentral.edu.co

- **Prof. Claudia Patricia Ortiz, M.Sc.**

https://github.com/cportiz/cportiz

Corporación Universitaria Mininuto de Dios - UNIMINUTO

claudia.ortiz.d@uniminuto.edu.co

- **Prof. Daniel Ricardo Delgado, Ph.D**

https://github.com/drdelgad0

Universidad Cooperativa de Colombia

danielr.delgado@campusucc.edu.co
