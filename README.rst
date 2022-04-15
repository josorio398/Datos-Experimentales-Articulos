

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
  
Installation of Requirements
============================
Before installing the library you must verify the execution environment and install the following requirements 

Google Colaboratory Support
---------------------------

For use in Google Colab (https://colab.research.google.com/) install texlive-fonts, texlive-fonts-extra and dvipng package using:

.. code:: python

    !apt install texlive-fonts-recommended texlive-fonts-extra cm-super dvipng

Jupyter Notebook and JupyterLab Support 
---------------------------------------

For use in Jupyter Notebook and JupyterLab (https://anaconda.org/) install jupyter-dash and  python-kaleido packages using:

.. code:: python

    !apt install texlive-fonts-recommended texlive-fonts-extra cm-super dvipng

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

    from SolubilityModels import Models

To import a particular model you can use the model name e.g:

.. code:: python

    from SolubilityModels import Modified_Apelblat



Classes of Solubility Models
============================

The Solubility Models module essentially uses two classes for computational analysis, the class ``model``, is 
used for the analysis of data from a particular model, the class ``models`` is used for the analysis of such 
data in all solubility models.

Colaboradores
=============

Jhonny Osorio Gallego

https://github.com/josorio398

osoriojohnny1986@gmail.com
