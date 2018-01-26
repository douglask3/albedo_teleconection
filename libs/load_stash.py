import iris
from   pdb import set_trace as browser
from   pylab import sort 
from   libs.ExtractLocation import *
from   libs.listdir_path import *
import numpy as np

def extract_cube_last_nYears(cube, mapLast_n_years):
    try: iris.coord_categorisation.add_year(cube, 'time', name='year')
    except: pass

    last_year  = cube.coord('year').points[-1]
    years_from = last_year - mapLast_n_years
    years = np.arange(years_from, last_year)

    cube = [cube.extract(iris.Constraint(year = i)) for i in years]
    cube = iris.cube.CubeList(cube).concatenate()[0]

    return cube


def loadJobs(dirs, code):
    cubes = [load_stash_dir(dir , code) for dir in dirs]
    for cube in cubes: print(cube)
    return(cubes)


def load_stash_dir(dir, *args, **kw):
    files = listdir_path(dir)
    return load_stash(files, *args, **kw)


def load_stash(files, code, name = None, units = None):
    print name
    print code
    
    stash_constraint = iris.AttributeConstraint(STASH = code)
    try:
        cube = iris.load_cube(files, stash_constraint)
    except:
        cube = iris.load_cube(files, stash_constraint)[0]

    if name  is not None: cube.var_name = name
    cube.standard_name = None
    if units is not None: cube.units = units
    return cube   


def loadCube(dir, data_dir, code = None, *args, **kw):
    files = sort(listdir_path(data_dir + dir))
    files = files[0:120]
    
    dat = iris.load_cube(files)
     
    dat = ExtractLocation(dat, *args, **kw).cubes

    dat.data = (dat.data > 0.00001) / 1.0
    return dat 
