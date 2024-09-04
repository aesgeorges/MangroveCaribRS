# MangroveCaribRS
## Remote Sensing Health Analysis of Mangrove Forests in the Caribbean. 

<br />
<a name="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br />

## About the Project
This analysis makes use of an HistGradientClassifier and NDWI, NDVI indices for land classification to  track the canopy cover of mangroves in the region over the past decade (2010-2022). 
Metrics such as NDVI, UVVR, and Gross Cover Change are used to evaluate the evolution of mangrove health at three major Caribbean Sites: 
* Baie de Grand-Pierre, Artibonite, Haiti
* Baie de Caracol, Nord-Est, Haiti
* Caroni Swamp, Trinidad, Trinidad-and-Tobago

<img width="3456" alt="GRC Poster Draft" src="https://github.com/AlexandreSeb97/RSHaiti-GPBay/assets/7967578/8b53d052-73c6-4a50-8476-4499693342ab">

[GRC Poster_Alexandre Georges.pdf](https://github.com/AlexandreSeb97/RSHaiti-GPBay/files/12761175/GRC.Poster_Alexandre.Georges.pdf)


This project is being developed by Alexandre E. S. Georges, PhD Student in Environmental Engineering at the University of California, Berkeley, supervised by Mark T. Stacey.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
* Python
* Jupyter
* scikit-learn
* xarray
* pandas
* rasterio
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started
This project and analysis involve three major steps using different scripts and notebooks. These steps, in order are:

1. Data Acquisition and Mosaic Merging 

`data_acq.ipynb` &rarr; `merge.py`

2. Model Training

`model_selection.ipynb`

3. Data Processing and Analysis

`preprocess.ipynb` &rarr; `classification.ipynb` &rarr; `analysis.ipynb`

### Requirements
All the libraries used for this project are loaded in a conda environment. Their names and versions can be found in `requirements.txt`. The file can be directly used in conda to create a copy of the development environemnt.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage
Here is a usage case of this code to analyze the mangrove forest in Caracol Bay, Haiti (codenamed CCHT):

1. Data Acquisition

    1.1. Data Download

    Assuming the site shapefile is correctly named (`CCHT.shp`) and placed (`./datasets/Shapefiles/CCHT.shp`). Run the `data_acq.ipynb` notebook, after making sure that the search and download filters (as defined in the params file `./codebase/params.py`) are corrected.

    - Input the correct sitecode (here CCHT) when prompted so the images are downloaded to the right folder.
       
   1.2. Mosaic Merge

   Once the download is completed (usually after 15-20mn), make sure to mosaic them as they are downloaded as individual images to clipped to your aoi.

   Run `./scripts/merge.py`, specifiying which site (CCHT) you want to mosaic for.

   - If the downloaded images will be used to train the land classification model, input True when prompted. Otherwise, input false. 

2.  Model Training

    Assuming the model training images and training labels exist and are properly named (`CCHT_training.shp`). Run the `model_selection.ipynb` notebook. Make sure to specify under the variable site_code in the beginning of the notebook which sites you want to use training labels for.

    This notebook will output a .joblib file, a dumped version of the classification model to be used later, in the `./outputs/models/` directory. 

3. Data Processing Analysis

    3.1 Visualize your mosaics using `data_vis.ipynb`, making sure to discard any image that is unsatisfacory that might have slipped past `merge.py` tolerance factors.

    3.2 Preprocess your images using `preprocess.ipynb`

    Output: `./datasets/Processed/CCHT_obs.nc`

    3.3 Classify the images using `classification.ipynb`

    Output: `./datasets/Processed/CCHT_classified.nc`

    3.4 Run the analysis using `analysis.ipynb`. Enjoy your final figures!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I would like to acknowledge PlanetLabs who provided the data for this project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

