class coordRangeExtract(object):
    def __init__(self, dat, lon = None, lat = None, point = None, point_as_ij = False):
        def coordRange2List(c, r):
            if c is not None:
                if  isinstance(c, list) and  len(c) == 1: c = c[0]
            return c    
  
        if point is not None and point != "":
            latlon = point.split(';')  
            latlon = [i.split(':') for i in latlon]
            lon, lat = [[float(j) for j in i] for i in latlon]
            if point_as_ij:                
                lon = dat.coord('longitude').points[lon][0]
                lat = dat.coord('latitude' ).points[lat][0]
                dat.long_name += '-' + 'ijs:'
            dat.long_name += '-' + point
       
        self.lon = coordRange2List(lon, [-180, 180])
        self.lat = coordRange2List(lat, [-90 ,  90])

        if isinstance(self.lon, list):
            def lonRange(cell): return self.lon[0] <= cell <= self.lon[1]
        else:
            def lonRange(cell): return cell == self.lon

        if isinstance(self.lat, list):
            def latRange(cell): return self.lat[0] <= cell <= self.lat[1]
        else:
            def latRange(cell): return cell == self.lat

        try: dat.coord('latitude' ).guess_bounds()
        except: pass
        try: dat.coord('longitude').guess_bounds() 
        except: pass
        
        if self.lon is not None: dat = dat.extract(iris.Constraint(longitude = lonRange))
        if self.lat is not None: dat = dat.extract(iris.Constraint(latitude  = latRange))
        try:
            if self.lat[0] == self.lat[1] and self.lon[0] == self.lon[1]:
                if dat.coord('latitude').shape != (1,) or dat.coord('longitude').shape != (1,):
                    dat = [i.collapsed(['latitude', 'longitude'], iris.analysis.MEAN) for i in dat]
        except:
            pass
        self.dat = dat


def coordRangeExtractCubes(cubes, *args, **kw):
    return [coordRangeExtract(cube, *args, **kw).dat for cube in cubes]
