from shapely.geometry import Point
import pandas as pd 
import glob 
import pickle

class GridIndex:
    
    class Bound:
        x1=0
        x2=0
        y1=0
        y2=0
    
    class Node:
        polys=[]
        
    def __init__(self):
        self.xs=0
        self.ys=0
        self.grid=[] 
        self.width=0
        self.height=0
        self.polygon_dict=None
    
    def GridIndex (self, xsize, ysize):
        self.xs=xsize
        self.ys=ysize
        for x in range (xsize):
            a=[]
            for y in range(ysize):
                a.append([])
            self.grid.append(a)
    
    def buildGrid(self, polygons):
        self.polygon_dict=polygons
        maxx=-float("inf")
        maxy=-float("inf")
        minx=float("inf")
        miny=float("inf")
        bounds=[]
        i=0
        for index, polygon in self.polygon_dict.items():
            rect= polygon.bounds
            bound_new=self.Bound()
            bound_new.x1=rect[0]
            bound_new.y1=rect[1]
            bound_new.x2=rect[2]
            bound_new.y2=rect[3]
            bounds.append((index, bound_new))
            minx = min(bound_new.x1, minx)
            miny = min(bound_new.y1, miny)
            maxx = max(bound_new.x2, maxx)
            maxy = max(bound_new.y2, maxy)
        self.width=(maxx-minx)/self.xs
        self.height=(maxy-miny)/self.ys
        self.Bound.x1=minx
        self.Bound.x2=maxx
        self.Bound.y1=miny
        self.Bound.y2=maxy
        for index, bound in bounds:
            stx=self.getXIndex(bound.x1)
            enx=self.getXIndex(bound.x2)+1
            sty=self.getYIndex(bound.y1)
            eny=self.getYIndex(bound.y2)+1
            if (enx>=self.xs):
                enx=self.xs-1
            if (eny>=self.ys):
                eny=self.ys-1
            for x in range(self.xs):
                for y in range(self.ys):
                    self.grid[x][y].append(index)
    
    def getXIndex(self, x):
        x_in=(x- self.Bound.x1)/self.width
        return int (x_in)
    
    def getYIndex(self, y):
        y_in=(y- self.Bound.y1)/self.height
        return int (y_in)
    
    def getRegion(self, x, y):
        stx=self.getXIndex(x)
        sty=self.getYIndex(y)
        if (stx>=self.xs):
            stx=self.xs-1
        if (sty>=self.ys):
            sty=self.ys-1
        if (stx<0):
            stx=0
        if (sty<0):
            sty=0
        # if (len(self.grid[stx][sty])==1):
        try:
            return self.grid[stx][sty][0]
        # for polygon_index in self.grid[stx][sty]:
        #     if (self.polygon_dict[polygon_index].contains(Point(x, y))):
        #         return polygon_index
        except:
            return -1

def matching_start_station(entry, stations_GPS_Dict):
    start_station_name=entry.iloc[4]#['start station name']
    #end_station_name=entry['end station name']
    if (start_station_name not in stations_GPS_Dict.keys()):
        start_longtitude=float(entry.iloc[6])
        start_latitude=float(entry.iloc[5])
        stations_GPS_Dict[start_station_name]=zipcode_index.getRegion(start_longtitude, start_latitude)
    return stations_GPS_Dict[start_station_name]

def matching_end_station(entry, stations_GPS_Dict):
    end_station_name=entry.iloc[8]
    #end_station_name=entry['end station name']
    if (end_station_name not in stations_GPS_Dict.keys()):
        end_longtitude=float(entry.iloc[10])
        end_latitude=float(entry.iloc[9])
        stations_GPS_Dict[end_station_name]=zipcode_index.getRegion(end_longtitude, end_latitude)
    return stations_GPS_Dict[end_station_name]

print ("Read Zipcode.pickle")

with open("/scratch/jw4937/Big_Data_Proj/zipcode.pickle", 'rb') as f:
    zipcode_dict= pickle.load(f)

print ("Read Neighborhood.pickle")
with open("/scratch/jw4937/Big_Data_Proj/Neighborhood.pickle", 'rb') as f:
    Neighborhood_dict= pickle.load(f)
print ("Building zipcode index")

zipcode_index=GridIndex()
zipcode_index.GridIndex(1000, 1000)
zipcode_index.buildGrid(zipcode_dict)

# print ("Building neighborhood index")
# neighborhood_index=GridIndex()
# neighborhood_index.GridIndex(1000, 1000)
# neighborhood_index.buildGrid(Neighborhood_dict)

print ("Converting dataframes")


stations_GPS_Dict={}

for file_name in glob.glob("/scratch/jw4937/Big_Data_Proj/Citibike_3/*.*"):
    
    name=file_name.split("/")[-1]

    print ("Currently working on:", name)
    
    Citibike_df=pd.read_csv(file_name)
    #unique_names=df_311_Service["start station name"].unique()
    # Citibike_df["start_neighborhood"]=Citibike_df.apply(matching_start_station, axis=1)
    # Citibike_df["end_neighborhood"]=Citibike_df.apply(lambda entry: neighborhood_index.getRegion(float(entry['end station longitude']), float(entry['end station latitude'])), axis=1)
    Citibike_df["start_zipcode"]=Citibike_df.apply(lambda entry: matching_start_station(entry, stations_GPS_Dict), axis=1)
    Citibike_df["end_zipcode"]=Citibike_df.apply(lambda entry: matching_end_station(entry, stations_GPS_Dict), axis=1)
    
    Citibike_df.drop(columns=['start station longitude', 'end station longitude', 'start station latitude', 'end station latitude'], inplace=True)
    
    Citibike_df.to_csv("/scratch/jw4937/Big_Data_Proj/Citibike_3/Preprocessed_{}".format(name))
