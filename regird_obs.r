library(raster)
source("libs/convert_pacific_centric_2_regular.r")
library(gitBasedProjects)
sourceAllLibs('../rasterextrafuns/rasterExtras/R/')

n96_file = 'data/N96_example.nc'
obs_dir  = 'data/global_albedo/'
varnames  = c('DHR_VIS', 'BHR_VIS', 'DHR_SW', 'BHR_VIS')

n96 = raster(n96_file)
fnames = list.files(obs_dir, full.names = TRUE)

memSafeFile.remove()
memSafeFile.initialise('temp/')
regrid_layer <- function(fname, varname) {
    
    r = stack(fname, varname = varname)   
    r = convert_regular_2_pacific_centric(r)
    r = raster::resample(r, n96)
    fname = memSafeFile()
    r = writeRaster(r, fname, overwrite = TRUE)
    return(r)
}

regrid_variable <- function(varname) {

    obs = layer.apply(fnames, regrid_layer, varname)
    writeRaster(obs, paste('outputs/global_albedo/', varname, '-regridded.nc', sep = ''), 
                overwrite = TRUE)
}

lapply(varnames, regrid_variable)
