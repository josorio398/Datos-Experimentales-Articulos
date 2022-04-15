
import sys 
import pandas as pd
import numpy as np
from IPython.display import display, Math, Latex, Markdown,HTML
from IPython.core.display import display, HTML
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import ceil
import  tikzplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import rcParams

import os
import platform
import subprocess
import warnings

from IPython.display import FileLink

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


global entorno
entorno = str(sys.executable)

if entorno == "/usr/bin/python3" :
    from google.colab import files


def data_upload(name):
    nombre = name
    uploaded = files.upload()
    for fn in uploaded.keys():
        nombre = fn
    return nombre

def generate_pdf(filename_tex):

    # TeX source filename
    tex_filename = filename_tex+".tex"
    filename, ext = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + '.pdf'

    # compile TeX file
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))

    if entorno == "/usr/bin/python3" :
        path = "/content/"+ filename_tex +".pdf"
        files.download(path)
    else:
        display(FileLink(filename_tex +".pdf"))


def environment_table(file_name):

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    line = "\\documentclass{article}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{makecell}\n\\usepackage{graphicx}\n\\begin{document}\n"

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

    text_to_append = "\\end{document}"

    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def environment_graph(file_name):

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    line = "\\documentclass[tikz]{standalone}\n\\usepackage{pgfplots}\n\\begin{document}\n"

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

    text_to_append = "\\end{document}"

    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def environment_graph_apart(file_name,cols,rows):

    with open(file_name,'r') as read_file:
        lines = read_file.readlines()

    currentLine = 1
    with open(file_name,'w') as write_file:
        for line in lines:
            if currentLine < 7:
                pass
            else:
                write_file.write(line)
        
            currentLine += 1

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    line = "\\documentclass[tikz]{standalone}\n\\usepackage{pgfplots}\n\\usepgfplotslibrary{groupplots}\n\\pgfkeys{/pgf/number format/.cd,fixed,precision=3}\n\\pgfplotsset{compat=1.3,every axis/.append style={scale only axis,height=5.5cm}}\n\\begin{document}\n\\begin{tikzpicture}\n\\definecolor{darkgray176}{RGB}{176,176,176}\n\\begin{groupplot}[group style={group size="+str(cols)+ " by " + str(rows)+", horizontal sep=2cm, vertical sep=3cm}]"

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

    text_to_append = "\\end{document}"

    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)



class dataset:

    """
    dataset
    =======
    ### `dataset("archive path")` or `dataset()`
    -------------------------------------------------------------------------------
    Class to upload the dataset according to the format of the standard table in 
    extension "xlsx" or "csv", receives a path or url as argument.

    ------------------------------------------------------------------------------
    # Examples
    The data must be loaded in the standard table format in the following ways:
    - Examples for loading standard data table from a path in the format "xlsx" or "csv":
    >>> data = dataset("/content/SMR-MeCN-MeOH.csv")
    >>> data = dataset("/content/SMR-MeCN-MeOH.xlsx")

    - Example for loading standard data table from a url in Github:
    >>> data = dataset("https://raw.githubusercontent.com/SMR-MeCN-MeOH.csv")

    - Example for loading standard data table from the pc in Google Colaboratory:
    >>> data = dataset()

    - Link to see the standard table: https://da.gd/CAx7m
    """


    def __init__(self,url=""):
        global URL
        self.url = url
        entorno = str(sys.executable)
        if self.url == "" and entorno == "/usr/bin/python3" :
            name = data_upload(self.url)
            URL= "/content/"+ name
        else:
            URL =self.url
       
   
    @property
    def show(self):
        """ Method to show the data loaded as a dataframe.
        """

        L = URL.split(".")

        if L[-1]=="csv":
            df = pd.read_csv(URL)
        if L[-1]=="xlsx":
            df = pd.read_excel(URL)
        return df
    
    
    @property
    def temperature_values(self):
        
        """Method to show the values of the temperatures in a dataframe.
        """

        df = self.show
        if "x1" in df.columns or "x2" in df.columns:
            temp = df.drop(['x1',"x2"], axis=1).columns[1:]
        else:
            temp = df.columns[1:]
        return pd.DataFrame({"T":temp})
    
    @property
    def mass_fractions(self):
        
        """ Method to show the values of the mass fractions in a dataframe.
        """
        df = self.show
        fm = df["w1"]
        df_fm = pd.DataFrame({"w1":fm})
        return df_fm

    
    def experimental_values(self,scale = 0,download_format = "None"):
        
        """
        experimental_values
        ===================
        ### `experimental_values(scale=0,download_format="None")`
        -------------------------------------------------------------------------------
        Method to show and download in different formats the dataframe experimental values 
        of the model, the experimental mole fractions of solubility can be multiplied 
        by a power of ten.

        ------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.buchowski_ksiazaczak(data,Tf)
        >>> model_name.experimental_values(scale=0,download_format="xlsx")
            
        >>> data.experimental_values(scale=3,download_format="tex") #other way
        
        -------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Parameters 
        The explanation of the parameters of this method are presented below:
        - ### scale: int, optional
        Option to indicate the exponent of the power of 10. All experimental mole
        fractions are multiplied by this power .e.g. scale = 3 multiply the mole 
        fractions by the power 10^3. Default is scale=0.
        - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
        Option to download the table of experimental values in the chosen format,
        excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
        """

        L = URL.split(".")

        if L[-1]=="csv":
            df = pd.read_csv(URL)
        if L[-1]=="xlsx":
            df = pd.read_excel(URL)


        if "x1" in df.columns or "x2" in df.columns:
            df_ev = df.drop(['x1',"x2"], axis=1)
        else:
            df_ev = df

  
        name_archi = URL.split("/")[-1].split(".")[-2]

        cols = df_ev.columns.astype(str).tolist()

        for i in cols[1:]:
            df_ev[i] = 10**(scale)* df_ev[i]

        nombre ="exp_val_λh"
        
        extension = download_format
        namecols=["$w_1$"]+["$"+i+"$" for i in cols[1:]]


        def f1(x):return '%1.2f' % x

        if scale != 0:
            def f2(x):return '%1.2f' % x
        else:
            def f2(x):return '%1.5f' % x

        if extension == "tex":     
            if entorno == "/usr/bin/python3":
                url_7 = "/content/"+ nombre + "-"+ name_archi +"-latex."+extension
                df_ev.to_latex(url_7,index=False,column_format= len(cols)*"c", formatters=[f1]+(len(cols)-1)*[f2],header=namecols,escape =False)
                files.download(url_7)
            else:
                url_7 = nombre + "-"+ name_archi +"-latex."+extension
                df_ev.to_latex(url_7,index=False,column_format= len(cols)*"c", formatters=[f1]+(len(cols)-1)*[f2],header=namecols,escape =False)
                display(FileLink(url_7))

            environment_table(url_7)
            generate_pdf(nombre + "-"+ name_archi+"-latex")

        if extension == "xlsx":  
            if entorno == "/usr/bin/python3" :
                url_7 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_ev.to_excel(url_7,sheet_name=nombre)
                files.download(url_7)
            else:
                url_7 = nombre + "-"+ name_archi +"."+extension
                df_ev.to_excel(url_7,sheet_name=nombre)
                display(FileLink(url_7))

        if extension == "csv":   
            if entorno == "/usr/bin/python3":
                url_7 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_ev.to_csv(url_7)
                files.download(url_7)
            else:
                url_7 = nombre + "-"+ name_archi +"."+extension
                df_ev.to_csv(url_7)
                display(FileLink(url_7))

        return df_ev

    
    def molar_fractions(self,mf):

        """Method to show the values the molar fractions in a dataframe.
        """
        if mf == "x1":
            df_mf = print("Does not exist mole fraction for "+ mf)
        if mf == "x2":
            df_mf = print("Does not exist mole fraction for "+ mf)
        if mf == "x3":
            df_mf = self.experimental_values()
        return df_mf

#CLASE PARA EL MODELO DE SOLUBILIDAD BUCHOWSKI KSIAZCZAK


class model:

    """
    model
    =====
    ### `model.mame_model(dataset, Tf)`
    --------------------------------------------------------------------------------------
    Class to choose the solubility model for a dataset with melting temperature Tf 
    and enthalpy of fusion ΔHf.

    -------------------------------------------------------------------------------------
    # Examples
    >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
    >>> model_λh = model.buchowski_ksiazaczak(data,403.4)

    ----------------------------------------------------------------------------------------
    ##  Solubility models
    The solubility models loaded into the library in this version are presented
    below with their respective parameters:
    >>> model.modified_apelblat(data)
    >>> model.vant_hoff(data)
    >>> model.vant_hoff_yaws(data)
    >>> model.modified_wilson(data)
    >>> model.buchowski_ksiazaczak(data,Tf) #λh model
    >>> model.NRTL(data,Tf,ΔHf)
    >>> model.wilson(data,Tf,ΔHf)
    >>> model.weibull(data,Tf,ΔHf)
    """

#CLASE PARA EL MODELO DE SOLUBILIDAD BUCHOWSKI KSIAZCZAK
    class buchowski_ksiazaczak(dataset):

        """
        Buchowski Ksiazaczak Model
        ==========================
        ### `model.buchowski_ksiazaczak(dataset,Tf)`
        -------------------------------------------------------------------------------------------------
        Class of the Buchowski Ksiazaczak model, receives as argument 
        a dataset and the melting temperature Tf for find the model parameters, 
        calculated values and make the plotting graphs.
        --------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.buchowski_ksiazaczak(data,Tf)

        ---------------------------------------------------------------------------------------------------
        ## Methods
        The methods with their default parameters that can be applied to this model
        are the following:
        >>> model_name.show
        >>> model_name.equation
        >>> model_name.mass_fractions
        >>> model_name.temperature_values
        >>> model_name.experimental_values(scale=0, download_format='None')
        >>> model_name.parameters(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, sd = False, gc = True, cmap="Blues",download_format="None")
        >>> model_name.values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.calculated_values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.relative_deviations(funtion = "fx",method="lm",p0 =[1,1], maxfev=20000, gc = True, cmap="Blues",scale=0,download_format="None")
        >>> model_name.statisticians(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,download_format="None")
        >>> model_name.statisticians_MAPE(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_RMSD(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_AIC(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2a(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.summary(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, sd = False,download_format="None")
        >>> model_name.plot(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, apart = False,download_format="None")
        """

        def __init__(self,url,Tf):
            self.name = url
            self.Tf = Tf
        
        @property
        def show(self):

            """Method to show the data organized in a table according to the chosen solubility model.
            """
            
            L = URL.split(".")

            if L[-1]=="csv":
                df = pd.read_csv(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
            
            if L[-1]=="xlsx":
                df = pd.read_excel(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)

            return DFF

        @property
        def temperature_values(self):

            """Method to show the values of the temperatures in a dataframe.
            """

            df = self.show
            tem = df["T"]
            return pd.DataFrame({"T":tem})
                    

        @property
        def mass_fractions(self):

            """Method to show the values of the mass fractions in a dataframe.
            """

            df = self.show
            mf = df.columns[1:]
            return pd.DataFrame({"w1":mf})

        @property
        def equation(self):
            """ Method to show the equation of the chosen solubility model.
            """
            if entorno == "/usr/bin/python3":
                salida = display(HTML('<h2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Buchowski-Ksiazczak Model Equation</h2>'))
                display(Math(r'$$\large{\ln \left[ 1+ \dfrac{\lambda (1 -x_3)}{x_3} \right] = \lambda h \left( \dfrac{1}{T} - \dfrac{1}{T_f}  \right)}$$'))
            else:
                salida = display(HTML('<h2>Buchowski-Ksiazczak Model Equation</h2>'))
                display(Math(r'$$\large{\ln \left[ 1+ \dfrac{\lambda (1 -x_3)}{x_3} \right] = \lambda h \left( \dfrac{1}{T} - \dfrac{1}{T_f}  \right)}$$'))
            return salida

    
        def __kernel(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, sd = False, opt = "calculate"):

            Tf = self.Tf

            def fx(x,λ,h):
                return 1/((np.log(1+(λ*(1-x)/x))/(λ*h))+1/Tf)

            def fT1(T,λ,h):
                return (λ*np.exp(λ*h/Tf))/(λ*np.exp(λ*h/Tf)-np.exp(λ*h/Tf)+np.exp(λ*h/T))


            def fT2(T,λ,h):
                return (λ*np.exp(h*λ*(T-Tf)/(Tf*T)))/(((λ-1)*np.exp(h*λ*(T-Tf)/(Tf*T)))+1)


            df = self.show
            W  = df.columns[1:].tolist()
            Temp = df["T"].values
            

            para_λ,para_h = [],[]
            desv_λ,desv_h = [],[]
            desv_para_λ,desv_para_h = [],[]
            L_para,L_desv,L_desv_para= [para_λ,para_h],[desv_λ,desv_h],[desv_para_λ,desv_para_h]
            
        
            if funtion== "fx":
                
                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fx,xdat,Tdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            
            if funtion == "fT1":

                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fT1,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            if funtion == "fT2":

                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fT2,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            
            C_w, C_temp, C_exp, C_cal, C_RD  = [],[],[],[],[]
        

            for i in W:

                wdat = len(Temp)*[i]
                Wdat = wdat

                tdat = Temp
                Tdat = tdat.tolist()

                x3_exp = df[i].values
                X3_exp =  x3_exp.tolist()

                x3_cal = fT2(tdat,para_λ[W.index(i)],para_h[W.index(i)])
                X3_cal = x3_cal.tolist()

                RD = (abs((x3_cal - x3_exp))/x3_exp).tolist()

                C_w    += Wdat
                C_temp += Tdat
                C_exp  += X3_exp
                C_cal  += X3_cal
                C_RD   += RD
    
            arr_w   = np.array(C_w)
            arr_temp = np.array(C_temp)
            arr_exp = np.array(C_exp)
            arr_cal = np.array(C_cal)
            arr_RD  = np.array(C_RD )

            dataframe = pd.DataFrame({"w1":arr_w,'RD':arr_RD})

            MAPES = []

            for i in range(len(W)):

                df_mask = dataframe['w1'] == W[i]
                data_filter = dataframe[df_mask]
                MRDP = sum(data_filter["RD"])*100/len(data_filter["w1"])
                MAPES.append(MRDP)

            df_para = pd.DataFrame({"w1":W,'λ':para_λ,'h':para_h,"MAPE":MAPES})
            df_para_desv = pd.DataFrame({"w1":W,'λ ± σ':desv_para_λ,'h ± σ':desv_para_h,"MAPE":MAPES})
            df_cal  = pd.DataFrame({"w1":arr_w,'T': arr_temp,"x3_Exp":arr_exp,"x3_Cal":arr_cal, "RD":arr_RD })

            if opt == "calculate" and sd == False:
                df_kernel = df_cal
            if opt == "parameters" and sd == True:
                df_kernel = df_para_desv
            if opt == "parameters" and sd == False:
                df_kernel = df_para
            return  df_kernel 

        def parameters(self,funtion = "fx",method = "lm",p0 = [1,1], maxfev = 20000,sd = False,cg = True,cmap = "Blues",download_format = "None"):

            """
            parameters
            ==========
            ### `parameters(funtion="fx",method="lm",p0=[1,1],maxfev=20000,sd=False,cg=True,cmap="Blues",download_format="None")`
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            Method to show the model fit parameters with their standard deviation for each mass fraction 
            in a dataframe. Download in different formats the parameters dataframe.
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.parameters(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            Shows the standard deviations for each parameter. Default is False.
            - ### cg: bool, optional
            Shows a color gradient for the "MAPE" column to identify high and low error values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of parameters in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
            """

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx["MAPE"]]

            D = self.__kernel(funtion = funtion, method=method,p0 =p0,maxfev=maxfev, sd = sd, opt = "parameters")
           
            if cg == False:
                DF = D
            if cg == True:
                DF=  D.style.background_gradient(cmap=cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=5,formatter={"w1":"{:.2f}","MAPE":"{:.3f}"})


            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="para_λh"


            extension = download_format
            namecols=["$w_1$","$\lambda$","$h$","$RMD\%$"]
     

            def f1(x): return '%1.2f' % x

            def f2(x):return '%1.3f' % x

            def f3(x):return '%1.2f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre +"-"+ name_archi +"-latex."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"-latex."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    display(FileLink(url_8))

                environment_table(url_8)
                generate_pdf(nombre + "-"+ name_archi+"-latex")


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    display(FileLink(url_8))

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    display(FileLink(url_8))

            return DF
        

        def values(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,scale = 0,download_format = "None"):

            """
            values
            ======
            ### `values(funtion="fx",method="lm",p0=[1,1],maxfev=20000,scale=0,download_format="None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the calculated values, experimental values and relative deviations
            in a dataframe. Download in different formats the values dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.values(scale=0,download_format="xlsx")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:

            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values and calculated values
            in the chosen format, excel format (‘xlsx’), comma separated values format (‘csv’),
            LaTeX format (‘tex’). 
            """
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt = "calculate")

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="values_Buchowski Ksiazczak"

            DF["x3_Exp"] = 10**(scale)*DF["x3_Exp"]
            DF["x3_Cal"] = 10**(scale)*DF["x3_Cal"]

            extension = download_format
            namecols=["$w_1$","$T$","$x_3^{Exp}$","$x_3^{Cal}$","$RD$"]
     

            def f1(x): return '%.2f' % x

            def f2(x): return '%.4f' % x

            def f3(x): return '%.3f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"-latex."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    files.download(url_12)
                else:
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"-latex."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    display(FileLink(url_12))

                environment_table(url_12)
                generate_pdf(nombre + "-"+ name_archi+"-latex")

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    display(FileLink(url_12))

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    display(FileLink(url_12))

            return DF


        def calculated_values(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,scale = 0,download_format = "None"):

            """
            calculated_values
            =================
            ###  `calculated_values(funtion="fx",method="lm",p0=[1,1],maxfev=20000,scale=0,download_format="None")`
            -----------------------------------------------------------------------------------------------------------------------------------------
            Method to show the table of calculated values of the solubility according to temperatures 
            and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

            ---------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.calculated_values(scale =3,download_format="tex")  

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 

            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All calculated mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of calculated values in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            W = self.mass_fractions["w1"]
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","RD"],axis=1).rename({'T':'','x3_Cal':i}, axis=1).set_index('').transpose()
                L.append(line)

            df = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = df.columns[1:].astype(str).tolist()

            for i in self.temperature_values["T"]:
                df[i] = 10**(scale)* df[i]

            nombre ="cal_val_λh"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.5f' % x


            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"-latex."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"-latex."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    display(FileLink(url_9))

                environment_table(url_9)
                generate_pdf(nombre + "-"+ name_archi+"-latex")

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    display(FileLink(url_9))

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    display(FileLink(url_9))

            return df


        def relative_deviations(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,cg = True,cmap = "Blues",scale = 0,download_format = "None"):

            """
            relative_deviations
            ===================
            ### `relative_deviations(funtion="fx",method="lm",p0=[1,1],maxfev=20000,cg=True,cmap="Blues",scale = 0,download_format="None")`
            ----------------------------------------------------------------------------------------------------------------------------
            Method to show the table relative deviations for each value calculated according
            to temperatures and mass fractions in a dataframe. Download in different formats 
            the relative deviations dataframe.
            
            ----------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.relative_deviations(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 

            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### cg: bool, optional
            Shows a color gradient to all columns for identify high and low deviations values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All relative deviations are
            multiplied by this power .e.g. scale = 2 multiply the relative deviations by the
            power 10^2 (relative percentage deviations). Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """


            df = self.show
            Temp = df["T"].values
            
            W = self.mass_fractions["w1"]
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx[Temp[0]:Temp[-1]]]
           
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","x3_Cal"],axis=1).rename({'T':'','RD':i}, axis=1).set_index('').transpose()
                L.append(line)

            d = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            for i in self.temperature_values["T"]:
                d[i] = 10**(scale)* d[i]

            if cg == False:
                df = d
            if cg == True:
                df =d.style.background_gradient(cmap= cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=3,formatter={"w1":"{:.2f}"})

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = d.columns[1:].astype(str).tolist()

            nombre ="RD_ λh"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x
            def f2(x):return '%1.3f' % x

        
            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"-latex."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"-latex."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    display(FileLink(url_10))

                environment_table(url_10)
                generate_pdf(nombre + "-"+ name_archi+"-latex")

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    display(FileLink(url_10))

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    display(FileLink(url_10))

            return df

        def statisticians(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,download_format = "None"):

            """
            statisticians
            =============
            ### `statisticians(funtion="fx",method="lm",p0=[1,1],maxfev=20000,download_format="None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the table of statisticians of the model in a dataframe.

            -Mean Absolute Percentage Error (MAPE).
            -Root Mean Square Deviation (RMSD).
            -Akaike Information Criterion corrected (AICc).
            -Coefficient of Determination (R^2).
            -Adjusted Coefficient of Determination (R^2_a).

            Download in different formats the statisticians dataframe.

            ------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statisticians(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.            
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of statisticians in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            MAPE = sum(abs(DF["RD"]))*100/len(DF["RD"])
            MRD = sum(DF["RD"])/len(DF["RD"])
            MRDP = sum(DF["RD"])*100/len(DF["RD"])

            ss_res = np.sum((DF["x3_Cal"] - DF["x3_Exp"])**2)
            ss_tot = np.sum((DF["x3_Exp"] - np.mean(DF["x3_Exp"]))**2)

            RMSD = np.sqrt(ss_res/len(DF["x3_Exp"]))

            k = 2  # Número de parámetros del modelo
            Q = 1   # Número de variables independientes
            N =len(DF["RD"])
            AIC = N*np.log(ss_res/N)+2*k
            AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

            R2 = 1 - (ss_res / ss_tot)
            R2_a = 1-((N-1)/(N-Q-1))*(1- R2**2)

            L_stad= [MAPE,RMSD,AICc,R2,R2_a]
            names = ["MAPE","RMSD","AICc","R2","R2_a"]
            names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

            df_estadis = pd.DataFrame({"statisticians":names,"values":L_stad})
            df_est= pd.DataFrame({"statisticians":names_tex,"values":L_stad})

            cols = df_estadis.columns
            name_archi = URL.split("/")[-1].split(".")[-2]
            
            nombre ="stat_λh"
            extension = download_format
            

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"-latex."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"-latex."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    display(FileLink(url_11))

                environment_table(url_11)
                generate_pdf(nombre + "-"+ name_archi+"-latex")

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    display(FileLink(url_11))

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    display(FileLink(url_11))

            return df_estadis

        def statistician_MAPE(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000):

            """
            statistician_MAPE
            =================
            ### `statistician_MAPE(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Mean Absolute Percentage Error (MAPE).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_MAPE()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.   
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            MAPE= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][0]
            return print("Mean Absolute Percentage Error, MAPE = ",MAPE)

        def statistician_RMSD(self,funtion = "fx",method = "lm",p0 = [1,1], maxfev = 20000):

            """           
            statistician_RMSD
            =================
            ### `statistician_RMSD(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Root Mean Square Deviation(RMSD).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_RMSD()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.    
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            RMSD= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][1]
            return print("Root Mean Square Deviation, RMSD = ",RMSD)
            
        def statistician_AIC(self,funtion = "fx", method ="lm",p0 = [1,1], maxfev = 20000):

            """           
            statistician_AIC
            =================
            ### `statistician_AIC(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Akaike Information Criterion corrected(AICc).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_AIC()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            AIC= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][2]
            return print("Akaike Information Criterion corrected , AICc = ",AIC)

        def statistician_R2(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000):

            """           
            statistician_R2
            ===============
            ### `statistician_R2(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Coefficient of Determination(R2).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_R2()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.     
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            R2= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][3]
            return print("Coefficient of Determination, R2a =",R2)
        
        def statistician_R2a(self,funtion = "fx",method = "lm", p0 = [1,1],maxfev = 20000):

            """           
            statistician_R2a
            =================
            ### `statistician_R2a(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Adjusted Coefficient of Determination(R2a).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_R2a()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.       
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            R2_a= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][4]
            return print("Adjusted Coefficient of Determination, R2a =",R2_a)


        def summary(self,funtion = "fx", method = "lm",p0 = [1,1], maxfev = 20000, sd = False,download_format = "xlsx"):

            """
            summary
            =======
            ### `summary(funtion="fx",method="lm",p0=[1,1],maxfev=20000,sd=False,download_format="xlsx")`
            ---------------------------------------------------------------------------------------------------------------
            Method to show a summary with calculated values, relative deviations, parameters and statistician
            of the model in a dataframe. Download in different formats the summary dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.summary()
            
            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.                 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            shows the standard deviations for each of the parameters. Default is False.
            - ### download_format: {‘xlsx’, ‘csv’}, optional
            Option to download the dataframe of summary in the chosen format, excel format (‘xlsx’),
            comma separated values format (‘csv’). In the LaTex format the output can be copy/pasted 
            into a main LaTeX document, requires `\\usepackage{booktabs}`. Default is ‘xlsx’.
            """
            

            listaval     = self.values(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)
            calculados   = self.calculated_values(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)
            diferencias  = self.relative_deviations(funtion = funtion, method = method,p0 =p0, maxfev=maxfev,cg = False) 
            parametros   = self.parameters(funtion = funtion, method = method,p0 =p0, maxfev=maxfev,sd = sd,cg = False)
            estadisticos = self.statisticians(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)

            DATA = pd.concat([listaval,calculados,diferencias,parametros,estadisticos], axis=1)
            
            extension = download_format

            nombre = "sum_λh"
            name_archi = URL.split("/")[-1].split(".")[-2]

            if extension == "xlsx":
                if entorno == "/usr/bin/python3":
                    url_1= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    files.download(url_1)
                else:
                    url_1= nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    display(FileLink(url_1))
            
            if extension == "csv":
                if entorno == "/usr/bin/python3":
                    url_3= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    files.download(url_3)
                else:
                    url_3=  nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    display(FileLink(url_3))            
            
            return DATA


        def plot(self,funtion = "fx", method ="lm",p0 = [1,1], maxfev = 20000,apart = False,download_format = "pdf"):
            """
            plot
            ====
            ### `plot(funtion="fx",method="lm",p0 =[1,1],maxfev=20000,apart = False,download_format="pdf")`
            ----------------------------------------------------------------------------------------
            Method to shows the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions. Download in different formats 
            the graph.

            -----------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.plot()
            >>> model_name.plot(separated = True) #separated according to mass fractions

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### separated: bool, optional
            Separates the graph according to mass fractions.
            - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
            Option to download the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions, pdf format (‘pdf’), png format (‘png’),
            LaTeX format (‘tex’).
            """

            nombre= "plot_λh"

            df_values = self.values(funtion =funtion, method= method,p0 =p0, maxfev=maxfev)

            name_archi ="-" + URL.split("/")[-1].split(".")[-2]
            
            if entorno == "/usr/bin/python3":
                url_2 = "/content/"+ nombre +  name_archi +".pdf"
                url_4 = "/content/"+ nombre +  name_archi +".png"
                url_12 = "/content/"+ nombre +  name_archi +"-latex.tex"
                url_5 = "/content/"+ nombre +  name_archi +"_sep"+".pdf"
                url_6 = "/content/"+ nombre +  name_archi +"_sep"+".png"
                url_13 = "/content/"+ nombre +  name_archi +"_sep"+"-latex.tex"
            else:
                url_2 = nombre +  name_archi +".pdf"
                url_4 = nombre +  name_archi +".png"
                url_12 = nombre +  name_archi +"-latex.tex"
                url_5 = nombre +  name_archi +"_sep"+".pdf"
                url_6 = nombre +  name_archi +"_sep"+".png"
                url_13 = nombre +  name_archi +"_sep"+"-latex.tex"

            
            W = self.mass_fractions["w1"]
            Temp = self.temperature_values["T"]


            numerofilas = len(Temp)
            numerocolumnas = len(W)

            L = [numerofilas*i for i in range(numerocolumnas+2)]

            extension= download_format

            if apart == False :
                
                if extension != "tex":
                
                    fig = go.Figure()
                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                name="w<sub>1</sub> = {w}".format(w=W[i]),
                                                text= Temp.tolist(),
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))


                    fig.add_trace(go.Scatter(x=X,y=X,name="x<sub>3</sub><sup>Exp</sup>=x<sub>3</sub><sup>Cal</sup>",hoverinfo = "skip"))


                    fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")
                    fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
                    fig.update_layout(title="Buchowski-Ksiazczak λh model",showlegend=True,title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)
                    #fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
                    fig.write_image(url_2)
                    fig.write_image(url_4)

                    if entorno == "/usr/bin/python3":
                        url= "/content/"+nombre + name_archi +"."+extension
                        files.download(url)
                        
                    else:
                        url= nombre + name_archi +"."+extension
                        display(FileLink(url)) 
                        
                    fig.show()

              
                if extension == "tex":

                    plt.rcParams["figure.figsize"] = (10, 8)
                    fig, ax = plt.subplots()

                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X"]

                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        plt.scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]], c = "k",marker=marker[i])

                    x = [min(df_values["x3_Exp"]),max(df_values["x3_Exp"])]
                    y = [min(df_values["x3_Cal"]),max(df_values["x3_Cal"])]

                    ax.plot(x,y,color='black',markersize=0.1)
                    ax.set_title("Buchowski-Ksiazczak "+ r"$\lambda h$" + " model",fontsize='large')


                    ax.xaxis.set_ticks_position('both')
                    ax.yaxis.set_ticks_position('both')
                    ax.tick_params(direction='in')


                    ax.set_xlabel("$x_{3}^{exp}$")
                    ax.set_ylabel("$x_{3}^{cal}$")
                    
                    tikzplotlib.save(url_12)


                    environment_graph(url_12)
                    generate_pdf(nombre +  name_archi+"-latex")

                    if entorno == "/usr/bin/python3":
                        url= "/content/"+nombre + name_archi +"-latex."+extension
                        files.download(url)
                    else:
                        url= nombre + name_archi +"-latex."+extension
                        display(FileLink(url)) 
                        
                    plt.show()

            if  apart == True:

                if extension != "tex":

                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(1,rows+1):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(1,cols+1))

                    DF = self.__kernel(method=method,p0 =p0,maxfev=maxfev, opt = "parameters")

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =["w<sub>1</sub>"+" = "+str(i)+", "+"MAPE = "+str(RMDP[w.index(i)].round(1)) for i in w]

                    fig = make_subplots(rows=rows, cols=cols,subplot_titles=name)

        
                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                text= Temp.tolist(),
                                                name = "",
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                showlegend= False,
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        X = np.linspace(min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]]),200)
                        fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color='Red')),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

                    for i in range(len(W)):
                        fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")

                    fig.update_layout(title ="Buchowski-Ksiazczak λh model",height=100*len(W)+300, width= 1300,showlegend=False)

                    fig.write_image(url_5,height=100*len(W)+300, width= 1300)
                    fig.write_image(url_6,height=100*len(W)+300, width= 1300)

                    grafica = fig.show()

                if extension == "tex":
                    
                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(0,rows):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(0,cols))


                    DF =self.parameters(cg = False)

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =[r"$w_1$"+" = "+str(i)+", "+"$MAPE = $"+str(RMDP[w.index(i)].round(1)) for i in w]


                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X","D"]

                    plt.rcParams["figure.figsize"] = (30, 50)

                    fig, axs = plt.subplots(rows, cols)

                    for i in range(len(W)):
                        x=df_values["x3_Exp"][L[i]:L[i+1]]
                        y=df_values["x3_Cal"][L[i]:L[i+1]]

                        axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker=marker[i])
                        axs[L_row[i], L_col[i]].set_title(name[i],fontsize='large')
                        axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                        axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                        axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].tick_params(direction='in')

                        X = [min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]])]
                        Y = [min(df_values["x3_Cal"][L[i]:L[i+1]]),max(df_values["x3_Cal"][L[i]:L[i+1]])]
                        axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

                    fig.subplots_adjust(hspace=0.5)


                    tikzplotlib.save(url_13)

                    environment_graph_apart(url_13,cols,rows)
                    generate_pdf(nombre + name_archi+"_sep-latex")

                    if entorno == "/usr/bin/python3":
                        url= "/content/"+nombre + name_archi +"_sep-latex."+extension
                        files.download(url)
                    else:
                        url= nombre + name_archi +"_sep-latex."+extension
                        display(FileLink(url)) 
                        
                    plt.show()
