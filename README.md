# Scolarte Ecuador

[![Travis Build
Status](https://travis-ci.org/tidyverse/ggplot2.svg?branch=master)](https://travis-ci.org/tidyverse/ggplot2)
[![AppVeyor Build
Status](https://ci.appveyor.com/api/projects/status/github/tidyverse/ggplot2?branch=master&svg=true)](https://ci.appveyor.com/project/tidyverse/ggplot2)
[![Coverage
Status](https://img.shields.io/codecov/c/github/tidyverse/ggplot2/master.svg)](https://codecov.io/github/tidyverse/ggplot2?branch=master)
[![CRAN\_Status\_Badge](http://www.r-pkg.org/badges/version/ggplot2)](https://cran.r-project.org/package=ggplot2)

## Resumen

Scolarte es la forma más fácil y rápida para comprar toda la lista de útiles escolares para nuestros pequeños.


## Scolarte apps

La aplicación web cuenta con las siguientes apps:

1.  core: que manejará la lógica principal de la app. Además de ser la app que se encargará de entregar los templates correctos para cada request, será la conexión entre el resto de apps. 

2. roles: Esta app manejará los 3 principales roles para el proyecto: admin, vendedores y clientes.

3. lists: Esta app manejará la lógica para la creación, actualización, elminación de las listas de útiles.

4. products: Esta app será usada para crear los diferentes productos, considerese útiles escolares, que tendrán una llave foránea con 1 o más listas de útiles escolares.

5. brands: Esta app será usada para crear las marcas de los productos. 


