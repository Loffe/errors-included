# -*- coding: utf-8 -*-
import time
import gtk
import gui
import shared.data
import map.map_xml_reader
import map
from map.mapdata import *
from datetime import datetime

class MapScreen(gtk.DrawingArea, gui.Screen):
    db = None
    sign = False

    bounds = {"min_latitude":0,
                "max_latitude":0,
                "min_longitude":0,
                "max_longitude":0}

    def __init__(self, db):
        gui.Screen.__init__(self, "Map")
        gtk.DrawingArea.__init__(self)
        self.db = db
        self.db.connect('mapobject-added', self.add_map_object)
        self.db.connect('mapobject-changed', self.change_map_object)
        self.db.connect('mapobject-deleted', self.delete_map_object)
        mapxml = map.map_xml_reader.MapXML("map/data/map.xml")
        self.mapdata = map.mapdata.MapData(mapxml.name, mapxml.levels)
        # queue_draw() ärvs från klassen gtk.DrawingArea
        # modellen anropar redraw när något ändras så att vyn uppdateras
        self.mapdata.redraw_function = self.queue_draw
        self.pos = {"x":0, "y":0}
        self.origin_position = None
        self.cols = 0
        self.rows = 0
        self.gps_data = None
        self.movement_from = {"x": 0, "y":0}
        self.allow_movement = False
        self.last_movement_timestamp = 0.0
        self.zoom_level = 1

        self.gps_x = self.mapdata.focus["longitude"]
        self.gps_y = self.mapdata.focus["latitude"]

        # events ;O
        self.set_flags(gtk.CAN_FOCUS)
        self.connect("expose_event", self.handle_expose_event)
        self.connect("button_press_event", self.handle_button_press_event)
        self.connect("button_release_event", self.handle_button_release_event)
        self.connect("motion_notify_event", self.handle_motion_notify_event)
#        self.connect("key_press_event", self.handle_key_press_event)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)
                         #|                        gtk.gdk.KEY_PRESS_MASK)
        # add all current objects in db to map
        self.add_all_mapobjects()
        
    def add_all_mapobjects(self):
        '''
        Add all objects from the database to the dict with objects to draw.
        '''
        mapobjectdata = self.db.get_all_mapobjects()
        for data in mapobjectdata:
            if data.__class__ == shared.data.UnitData:
                self.mapdata.objects[data.id] = Unit(data)
            elif data.__class__ == shared.data.POIData:
                self.mapdata.objects[data.id] = POI(data)
        self.queue_draw()

    def add_map_object(self, database, data):
        if data.__class__ == shared.data.UnitData:
            self.mapdata.objects[data.id] = Unit(data)
        elif data.__class__ == shared.data.POIData:
            self.mapdata.objects[data.id] = POI(data)  
        elif data.__class__ == shared.data.Alarm:
            self.mapdata.objects[data.poi.id] = POI(data.poi)  
        elif data.__class__ == shared.data.MissionData:
            self.mapdata.objects[data.poi.id] = POI(data.poi)
        self.queue_draw()
        
    def change_map_object(self, database, data):
        self.add_map_object(database,data)

    def delete_map_object(self, database, data):
        if data.__class__ == shared.data.Alarm:
            del self.mapdata.objects[data.poi.id]  
        elif data.__class__ == shared.data.MissionData:
            del self.mapdata.objects[data.poi.id]
        else:
            del self.mapdata.objects[data.id]

        self.queue_draw()

    def zoom(self, change):
        # Frigör minnet genom att ladda ur alla tiles för föregående nivå
#        level = self.mapdata.get_level(self.zoom_level)
#        level.unload_tiles("all")
      
        if change == "+":
            if self.zoom_level < 3:
                self.zoom_level += 1
        else:
            if self.zoom_level > 1:
                self.zoom_level -= 1

        # Ritar ny nivå
        self.queue_draw()

#    def handle_key_press_event(self, widget, event):
#        pass

    # Hanterar rörelse av kartbilden
    def handle_button_press_event(self, widget, event):
        self.movement_from["x"] = event.x
        self.movement_from["y"] = event.y
        self.origin_position = self.mapdata.focus
        self.last_movement_timestamp = time.time()
        self.allow_movement = True
        self.draw_clicked_pos(event)
        return True

    def handle_button_release_event(self, widget, event):
        self.allow_movement = False
        return True

    def handle_motion_notify_event(self, widget, event):
        if self.allow_movement:
            if event.is_hint:
                x, y, state = event.window.get_pointer()
            else:
                x = event.x
                y = event.y
                state = event.state

            # Genom tidskontroll undviker vi oavsiktlig rörelse av kartan,
            # t ex ifall någon råkar nudda skärmen med ett finger eller liknande.
            if time.time() > self.last_movement_timestamp + 0.1:
                lon, lat = self.pixel_to_gps(self.movement_from["x"] - x,
                                             self.movement_from["y"] - y)
                self.mapdata.set_focus(self.origin_position["longitude"] + lon,
                                     self.origin_position["latitude"] - lat)
                self.movement_from["x"] = x
                self.movement_from["y"] = y
            
                # Ritar om kartan
                self.queue_draw()

        return True

    def handle_expose_event(self, widget, event):
        self.context = widget.window.cairo_create()

        # Regionen vi ska rita på
        self.context.rectangle(event.area.x,
                               event.area.y,
                               event.area.width,
                               event.area.height)
        self.context.clip()
        self.draw()

        return False

#    # skicka in skiten här linus, gogo!
#    def set_gps_data(self, gps_data):
#        self.gps_data = gps_data
#        self.queue_draw()

    def draw(self):
        # Hämtar alla tiles för en nivå
        level = self.mapdata.get_level(self.zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self.mapdata.focus)
        self.cols = cols
        self.rows = rows

        self.bounds["min_longitude"] = tiles[0].bounds["min_longitude"]
        self.bounds["min_latitude"] = tiles[0].bounds["min_latitude"]
        self.bounds["max_longitude"] = tiles[-1].bounds["max_longitude"]
        self.bounds["max_latitude"] = tiles[-1].bounds["max_latitude"]

        # Ritar kartan
        for tile in tiles:
            #img = tile.get_picture()
            x, y = self.gps_to_pixel(tile.bounds["min_longitude"],
                                     tile.bounds["min_latitude"])
            tile.picture.draw(self.context, x, y)

        # Ritar ut eventuella objekt

        objects = self.mapdata.objects
            
        for item in objects:
            x, y = self.gps_to_pixel(objects[item].map_object_data.coords[0],
                                     objects[item].map_object_data.coords[1])

            if x != 0 and y != 0:
                objects[item].picture.draw(self.context, x, y)


    def gps_to_pixel(self, lon, lat):
        cols = self.cols
        rows = self.rows
        width = self.bounds["max_longitude"] - self.bounds["min_longitude"]
        height = self.bounds["min_latitude"] - self.bounds["max_latitude"]
      
        # Ger i procent var vi befinner oss på width och height
        where_lon = (lon - self.bounds["min_longitude"]) / width
        where_lat = (self.bounds["min_latitude"] - lat) / height
      
        # Ger i procent var focus befinner sig på width och height
        where_focus_lon = (self.mapdata.focus["longitude"] - \
                           self.bounds["min_longitude"]) / width
        where_focus_lat = (self.bounds["min_latitude"] - \
                           self.mapdata.focus["latitude"]) / height
      
        # Placerar origo i skärmens centrum
        rect = self.get_allocation()
        x = rect.width / 2.0
        y = rect.height / 2.0
      	
        # Räknar ut position:
        x += (where_lon - where_focus_lon) * (cols * 300.0)
        y += (where_lat - where_focus_lat) * (rows * 160.0)
      
        return [round(x), round(y)]
   
    def pixel_to_gps(self, movement_x, movement_y):
        # Hämtar alla tiles för en nivå
        level = self.mapdata.get_level(self.zoom_level)
        # Plockar ur de tiles vi söker från nivån
        tiles, cols, rows = level.get_tiles(self.mapdata.focus)

        # Gps per pixlar
        width = self.bounds["max_longitude"] - self.bounds["min_longitude"]
        height = self.bounds["min_latitude"] - self.bounds["max_latitude"]
        gps_per_pix_width = width / (cols * 300)
        gps_per_pix_height = height / (rows * 160)

        # Observera att kartans GPS-koordinatsystem börjar i vänstra nedre
        # hörnet, medan cairo börjar i vänstra övre hörnet! På grund av detta
        # inverterar vi värdet vi räknar fram så båda koordinatsystemen
        # överensstämmer.
        return [gps_per_pix_width * movement_x,
                gps_per_pix_height * movement_y]
        
    def get_clicked_coord(self, event):
        r = self.get_allocation()        
        x, y, state = event.window.get_pointer()
        (lon,lat) = self.pixel_to_gps(x,y)        
        (m,n) = self.pixel_to_gps(r.width/2, r.height/2)
        self.gps_x = self.origin_position["longitude"] - m + lon
        self.gps_y = self.origin_position["latitude"] + n  - lat
        
    def draw_sign(self):  
        poi_data = shared.data.POIData(self.gps_x, self.gps_y, "goal", datetime.now(), shared.data.POIType.flag)
        self.mapdata.objects["add-sign"] = POI(poi_data)
        self.queue_draw()
        
    def remove_sign(self):
        try:
            del self.mapdata.objects["add-sign"]
            self.queue_draw()  
        except:
            pass

    def draw_clicked_pos(self, event):
        self.get_clicked_coord(event)
        if self.sign:
            self.draw_sign()
