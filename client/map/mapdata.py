# -*- coding: utf-8 -*-
import gtk
import math
import shared.data

class Picture(object):
    path = None
    pixbuf = None
    offset = (0, 0)
    center = False
    marked = False
    is_me = False
    
    def __init__(self, path):
        if path == None:
            self.path = "map/map/data/icons/default.png"
        else:
            self.path = path

#ovärd? JA
#    def draw_picture(self, context, x, y):
#        try:
#            context.set_source_pixbuf(self.get_picture(), x, y)
#        except gobject.GError, message:
#            self.path = "map/data/icons/default.png"
#            context.set_source_pixbuf(self.get_picture(), x, y)
#        context.paint()

    def draw_rectangle(self, context, x, y, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        context.rectangle(x-1, y-1, 34, 34)
        context.set_source_rgb(r, g, b)
        context.stroke() #context.stroke()

    def draw(self, context, x, y):
        if not self.pixbuf:
            self.load()
        if self.center:
            dx = -self.pixbuf.get_width()/2 + self.offset[0]
            dy = -self.pixbuf.get_height()/2 + self.offset[1]
        else:
            dx, dy = (0, 0)
        context.set_source_pixbuf(self.pixbuf, x+dx, y+dy)
        context.paint()
        if self.is_me:
            self.draw_rectangle(context, x+dx, y+dy, (0, 0, 255))
        if self.marked:
            self.draw_rectangle(context, x+dx, y+dy, (0, 0, 0))
        
    def load(self):
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.path)

    def unload(self):
        self.pixbuf = None

# Lagrar en kartbild och dess koordinatavgränsningar
class Tile(object):
    name = "Tile"
    bounds = None
    picture = None
    type = None

    def __init__(self, id, path, bounds, type):
        self.name = id
        self.picture = Picture(path)
        self.bounds = bounds
        self.type = type

# Lagrar alla MapTiles (kartbilder)
class Tiles:
    # Håller reda på vilket område samtliga tiles omfattar
    bounds = {"min_latitude":None,
                "max_latitude":None,
                "min_longitude":None,
                "max_longitude":None}

    # Lagrar alla tiles
    tiles = None
    width = 0
    height = 0
    # Behövs för att lägga in tiles
    col_pos = 0
    row_pos = 0
    # Behövs för matematiska beräkningar
    cols = 0
    rows = 0

    def __init__(self, width, height):
        # Lagrar basbildens bredd och höjd
        self.width = int(width)
        self.height = int(height)

    def update_bounds(self, bounds):
        if self.bounds["min_latitude"] == None:
            self.bounds["min_latitude"] = bounds["min_latitude"]
        elif bounds["min_latitude"] > self.bounds["min_latitude"]:
            self.bounds["min_latitude"] = bounds["min_latitude"]

        if self.bounds["max_latitude"] == None:
            self.bounds["max_latitude"] = bounds["max_latitude"]
        elif bounds["max_latitude"] < self.bounds["max_latitude"]:
            self.bounds["max_latitude"] = bounds["max_latitude"]

        if self.bounds["min_longitude"] == None:
            self.bounds["min_longitude"] = bounds["min_longitude"]
        elif bounds["min_longitude"] < self.bounds["min_longitude"]:
            self.bounds["min_longitude"] = bounds["min_longitude"]

        if self.bounds["max_longitude"] == None:
            self.bounds["max_longitude"] = bounds["max_longitude"]
        elif bounds["max_longitude"] > self.bounds["max_longitude"]:
            self.bounds["max_longitude"] = bounds["max_longitude"]

    def create_empty_tiles(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.tiles = [[[] for ni in range(rows)] for mi in range(cols)]

    def add_tile(self, tile):
        self.update_bounds(tile.bounds)
        self.tiles[self.col_pos][self.row_pos] = tile

        if tile.type == "end":
            self.row_pos += 1
            self.col_pos = 0
        else:
            self.col_pos += 1

    # Laddar ur tiles för att frigöra minnet
    def unload_tiles(self, tiles_list):
        if tiles_list == "all":
            tiles_list = self.tiles

        for tiles in tiles_list:
            for tile in tiles:
                tile.picture.unload()

    # Hämtar alla tiles som ligger inom ett avgränsat koordinatområde
    # Kom ihåg att latitude växer från botten mot toppen, inte tvärtom. Dock
    # kallas topppen för min_latitude.
    def get_tiles(self, focus):
        gps_width = self.bounds["max_longitude"] - \
                    self.bounds["min_longitude"]
        gps_height = self.bounds["min_latitude"] - \
                     self.bounds["max_latitude"]
                     
        
        # Skärmen på N810:an är 800x480. Detta bestämmer hur många tiles som
        # är synliga och påverkar inte clicked_coords()
        width = (gps_width / self.width) * 400
        height = (gps_height / self.height) * 240

        bounds = {"min_longitude":(focus["longitude"] - width),
                  "max_longitude":(focus["longitude"] + width),
                  "min_latitude":focus["latitude"] + height,
                  "max_latitude":focus["latitude"] - height}

        # Undviker att vi hamnar utanför det område tiles:en täcker
        if bounds["min_longitude"] < self.bounds["min_longitude"]:
            bounds["min_longitude"] = self.bounds["min_longitude"]

        if bounds["max_longitude"] > self.bounds["max_longitude"]:
            bounds["max_longitude"] = self.bounds["max_longitude"]

        if bounds["min_latitude"] > self.bounds["min_latitude"]:
            bounds["min_latitude"] = self.bounds["min_latitude"]

        if bounds["max_latitude"] < self.bounds["max_latitude"]:
            bounds["max_latitude"] = self.bounds["max_latitude"]

        start_lon = bounds["min_longitude"] - self.bounds["min_longitude"]
        stop_lon = bounds["max_longitude"] - self.bounds["min_longitude"]
        start_lat = self.bounds["min_latitude"] - bounds["min_latitude"]
        stop_lat = self.bounds["min_latitude"] - bounds["max_latitude"]

        # Det bästa sättet att förstå matematiken nedanför är att rita upp ett
        # rutnät med alla tiles, dvs x * y, t ex 3x5. Börja sedan räkna på
        # matematiken nedan utifrån rutnätet. I enkelhet handlar det nedan
        # om att räkna ut i procent var vi befinner oss i x-led och y-led
        # och sedan gångra denna procent med antalet kolumner och rader vi har,
        # och på så vis få reda på vilka rutor som ska visas.
        # Algoritmen är inte på något vis perfekt och bättre lösningar finns
        # säkert.
        x_start = int(math.floor(self.cols * (start_lon / gps_width)))
        x_stop = int(math.ceil(self.cols * (stop_lon / gps_width)))
        if x_stop == self.cols:
            x_stop -= 1 # Så vi inte överskrider max antalet tiles i x-led.

        y_start = int(math.floor(self.rows * (start_lat / gps_height)))
        y_stop = int(math.ceil(self.rows * (stop_lat / gps_height)))
        if y_stop == self.rows:
            y_stop -= 1 # Så vi inte överskrider max antalet tiles i y-led.

        # Frigör minne genom att ladda ur de tiles som inte visas
        tiles_left = []
        if x_start - 1 >= 0:
            self.unload_tiles(self.tiles[0:x_start])

        tiles_right = []
        if x_stop + 1 != self.cols:
            self.unload_tiles(self.tiles[x_stop:self.cols])

        # Returnerar de tiles som efterfrågas
        tiles = self.tiles[x_start:x_stop + 1]
        result = []
        for tile in tiles:
            result += tile[y_start:y_stop + 1]

        return [result,
                x_stop + 1 - x_start,
                y_stop + 1 - y_start]

# Datastruktur som lagrar kartans bild och de generella objekt som ska ritas ut
# på denna.
class MapData():
    name = "MapData"
    bounds = None
    objects = {}
#    __mission_objects = []
    """ Contains all the tiles
    """
    levels = {}
    redraw_function = None
    focus = {"latitude":0,
               "longitude":0}

    # name är namnet på kartan, t ex Ryd.
    # levels är tre stycken Tiles-objekt.
    def __init__(self, name, levels):
        self.name = name
        self.set_level(1, levels[1])
        self.set_level(2, levels[2])
        self.set_level(3, levels[3])
        self.bounds = levels[1].bounds
        # Ställer in vad kartkomponenten ska fokusera på (visa)
        # (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-led.
        self.set_focus(15.5726, 58.4035)

    # Ställer in Tiles-objekt för en bestämd nivå
    def set_level(self, level, tiles):
        self.levels[level] = tiles

    # Returnerar ett Tiles-objekt för en given nivå
    def get_level(self, level):
        return self.levels[level]

    def set_focus(self, longitude, latitude):
        self.focus["longitude"] = longitude
        self.focus["latitude"] = latitude
        self.redraw()

    def remove_objects(self):
        self.objects = {}
        self.redraw()

    def add_object(self, map_object):
        self.objects[mapobject.id] = map_object
        self.redraw()

    def delete_object(self, object_id):
        del self.objects[object_id]
        self.redraw()

    def get_object(self, object_id):
        return self.objects[object_id]

    def redraw(self):
        if self.redraw_function:
            self.redraw_function()

# Är den typen av objekt som lagras i MapData. T ex en ambulans som ska visas
# på kartan eller "blockerad väg"-symbol.
class MapObject():
    map_object_data = None
    picture = None
    visible = True

    def __init__(self, map_object_data):
        self.map_object_data = map_object_data

    
class Unit(MapObject):
    
    def __init__(self, unit_data):
        MapObject.__init__(self, unit_data)
        # default  icon can be changed here
        path = "map/data/icons/default.png"
        if unit_data.type == shared.data.UnitType.ambulance:
            path = "map/data/icons/ambulance.png"
        elif unit_data.type == shared.data.UnitType.commander:
            path = "map/data/icons/commander.png"
        elif unit_data.type == shared.data.UnitType.army:
            path = "map/data/icons/tank.png"
        elif unit_data.type == shared.data.UnitType.srsa:
            path = "map/data/icons/firetruck.png"
        self.picture = Picture(path)
        self.picture.center = True 

class POI(MapObject):
    
    def __init__(self, poi_data):
        MapObject.__init__(self, poi_data)
        offset = (0, 0)
        # default  icon can be changed here
        path = "map/data/icons/default.png"
        sub = poi_data.subtype
        if sub == shared.data.POISubType.tree:
            path = "map/data/icons/tree.png" 
        elif sub == shared.data.POISubType.pasta_wagon:
            path = "map/data/icons/pastawagon.png"
        elif sub == shared.data.POISubType.fire:
            path = "map/data/icons/fire.png"
        elif sub == shared.data.POISubType.accident:
            path = "map/data/icons/accident.png"
        elif sub == shared.data.POISubType.bridge:
            path = "map/data/icons/bridge.png"
        elif poi_data.type == shared.data.POISubType.other:
            path = "map/data/icons/default.png"
            offset = (8, -13)
        elif poi_data.type == shared.data.POIType.flag:
            path = "map/data/icons/default.png"
            offset = (8, -13)
        self.picture = Picture(path)
        self.picture.offset = offset
        self.picture.center = True

class Mission():
    POIs = []
    Units = []
    mission_data = None
    def __init__(self, mission_data):
        self.mission_data = mission_data
