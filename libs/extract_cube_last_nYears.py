import matplotlib.pyplot as plt
import iris.quickplot as qplt
import iris.plot as iplt
from   libs.plot_maps import *

def extract_cube_last_nYears(cube, mapLast_n_years, last_year = None):

    try: iris.coord_categorisation.add_year(cube, 'time', name='year')
    except: pass
    
    if last_year is None: last_year  = cube.coord('year').points[-1]
    years_from = last_year - mapLast_n_years
    years = np.arange(years_from, last_year)

    cube = [cube.extract(iris.Constraint(year = i)) for i in years]
    cube = iris.cube.CubeList(cube).concatenate()[0]

    return cube

def extract_map_and_plot(cube, title, extract = True, last_year = None, *args, **kw):
    cube = extract_cube_last_nYears(cube, 5, last_year)
    cube = cube.collapsed('time', iris.analysis.MEAN)
    
    plot_lonely_cube(cube, N = 1, M = 3, *args, **kw)
    plt.title(title)
    return(cube)

def plot_projection(cubes, names, cmap, dcmap, levels, dlevels, last_year = None, *args, **kw):
    plt.rcParams['figure.figsize'] = (15.0, 5.0)
    
    maps = [extract_map_and_plot(c, j, n = n, extend = 'max', cmap = cmap, levels = levels, last_year = last_year, *args, **kw)
            for c, j, n in zip(cubes, names, [1,2])]
    
    cf = plot_lonely_cube(maps[0] - maps[1], N = 1, M = 3, n = 3, extend = 'both', 
                     cmap = dcmap, levels = dlevels, *args, **kw)

    plt.title('difference' if len(names) < 3  else names[2])
    if last_year is not None: plt.figtext(0.5, 1.0, last_year, fontdict = None, fontweight = 'extra bold')
    return cf

def map_years(plot_years, cubes, jobs, levels, dlevels, cmap, dcmap, yscale = 1, *args, **kw):
    def plotFun(last_year, names = jobs, figsize = (15, yscale * 5.5), colourbar = False):
        plt.figure(figsize=figsize)
        cf = plot_projection(cubes, names, levels = levels, dlevels = dlevels, 
                             cmap = cmap, dcmap = dcmap,
                             colourbar = colourbar, last_year = last_year, *args, **kw)
        plt.show()
        return cf
    
    plotFun(plot_years[0])
    for yr in plot_years[1:-1]:
        plotFun(yr, ['', '', ''])     
    
    cf = plotFun(plot_years[-1], figsize = (15, yscale * 7.8), colourbar = True)
    plt.show()
