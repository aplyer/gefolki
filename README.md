GeFolki is a coregistration software that has been developped in the framework of the MEDUSA project, first for SAR/SAR co-registration, then for other cases of remote sensing image coregistration, including hetergeneous image co-registration (ex LIDAR/SAR, optics/SAR, hyperspectral/optics and so on)

A very detailed instructions for use is currently being written.

We hope this code will be helpful and we remain to your disposal and we are interested in getting back your remarks.

If you are using the result of GeFolki in your project, we kindly ask you to cite

- for SAR/SAR coregistration (interferometry, change detection, and so on)

Aurélien Plyer, Elise Colin-Koeniguer, Flora Weissgerber, "A New Coregistration Algorithm for Recent Applications on Urban SAR Images", Geoscience and Remote Sensing Letters, IEEE , vol.12, no.11, pp. 2198 – 2202, nov 2015

- for other cases (optics/SAR, optics/hyperspectral, LIDAR/SAR, etc.)

Guillaume Brigot, Elise Colin-Koeniguer, Aurélien Plyer, Fabrice Janez, "Adaptation and Evaluation of an Optical Flow Method Applied to Coregistration of Forest Remote Sensing Images", IEEE Journal of Selected Topics in Applied Earth Observations ans Remote Sensing, Volume 9, Issue 7, July 2016

The source code is provided here in matlab under a GPL license.

After decompression, this directory contains:

- a directory "datasets" that are used in the demonstration file "main.m". Origins of the different datasets are described in the readme.txt
- the different matlab source codes. The demonstration are proposed in the main.m file.

For information, the execution time of the whole script main.m with 3 examples of co-registration is 90 seconds on a Intel® Xeon(R) CPU E5-1603 0 @ 2.80GHz × 4


## Citations for {ge ,e, _}Folki algorithms :

Brigot, G., Colin-Koeniguer, E., Plyer, A., & Janez, F. (2016). Adaptation and Evaluation of an Optical Flow Method Applied to Coregistration of Forest Remote Sensing Images. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 9(7), 2923-2939.

Plyer, A., Colin-Koeniguer, E., & Weissgerber, F. (2015). A new coregistration algorithm for recent applications on urban SAR images. IEEE Geoscience and Remote Sensing Letters, 12(11), 2198-2202.

Plyer, A., Le Besnerais, G., & Champagnat, F. (2016). Massively parallel Lucas Kanade optical flow for real-time video processing applications. Journal of Real-Time Image Processing, 11(4), 713-730.

Champagnat, F., Plyer, A., Le Besnerais, G., Leclaire, B., & Le Sant, Y. (2009, August). How to calculate dense piv vector fields at video rate. In Proceedings of 8th International Symposium on Particle Image Velocimetry-PIV09 (Vol. 11, pp. 15-20).









