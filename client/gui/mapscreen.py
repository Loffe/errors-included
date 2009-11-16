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
    '''
    The visible map screen.
    '''
    # the database holding the objects to show on map.
    db = None

    # the bounds of this map.
    bounds = {"min_latitude":0,
                "max_latitude":0,
                "min_longitude":0,
                "max_longitude":0}

    def __init__(self, db):
        '''
        Constructor. Creates a new map screen.
        @param db:
        '''
        gui.Screen.__init__(self, "Map")
        gtk.DrawingArea.__init__(self)

        # connect database changes to the map screen update function
        self.db = db
        self.db.connect('mapobject-added', self.update_map)

        # create mapdata from xml 
        mapxml = map.map_xml_reader.MapXML("map/data/map.xml")
        self.mapdata = map.mapdata.MapData(mapxml.name, mapxml.levels)

        # queue_draw() inherited from gtk.DrawingArea
        # mapdata call redraw when changed to update the view
        self.mapdata.redraw_function = self.queue_draw

        self.pos = {"x":0, "y":0}
        self.origin_position = None

        # the number of tile-rows and tile-columns
        self.cols = 0
        self.rows = 0

        # variables used for map movement
        self.movement_from = {"x": 0, "y":0}
        self.allow_movement = False
        self.last_movement_timestamp = 0.0

        # the current zoom level
        self.zoom_level = 1
        
        self.dirty = True

        # handle events; connect signals to callback functions
        self.set_flags(gtk.CAN_FOCUS)
        self.connect("expose_event", self.handle_expose_event)
        self.connect("button_press_event", self.handle_button_press_event)
        self.connect("button_release_event", self.handle_button_release_event)
        self.connect("motion_notify_event", self.handle_motion_notify_event)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)

        # add all current objects in db to map
        self.update_map(data = "all")
    
    def update_map(self, database = None, data = None):
        '''
        Callback function. Call to update map view when database changed.
        @param database: 
        @param data: the updated object
        '''

        # add all map objects in database to a dict with objects to draw
        if data == "all":
            mapobjectdata = self.db.get_all_mapobjects()
            for data in mapobjectdata:
                if data.__class__ == shared.data.UnitData:
                    self.mapdata.objects[data.name] = Unit(data)
                elif data.__class__ == shared.data.POIData:
                    self.mapdata.objects[data.name] = POI(data)
        # add a specified object
        else:
            if data.__class__ == shared.data.UnitData:
                self.mapdata.objects[data.name] = Unit(data)
            elif data.__class__ == shared.data.POIData:
                self.mapdata.objects[data.name] = POI(data)

        # redraw
        self.queue_draw()

    def zoom(self, change):
        '''
        Change the zoom-level with specified change (increase or decrease).
        @param change: "+" to increase zoom or "-" to decrease zoom
        '''
        # get the new level (map tiles)
        level = self.mapdata.get_level(self.zoom_level)
        # clear memory by unloading tiles
#        level.unload_tiles("all")

        # change the zoom-level
        if change == "+":
            if self.zoom_level < 3:
                self.zoom_level += 1
        else:
            if self.zoom_level > 1:
                self.zoom_level -= 1

        # redraw
        self.dirty = True
        self.queue_draw()

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
        self.dirty = True
        return True

    def handle_motion_notify_event(self, widget, event):
        if self.allow_movement:
            if event.is_hint:
                x, y, state = event.window.get_pointer()
            else:
                x = event.x
                y = event.y
                state = event.state

            # Avoid accidental map movement by using timestamp
            # Handle map movement
            if time.time() > self.last_movement_timestamp + 0.1:
                lon, lat = self.pixel_to_gps(self.movement_from["x"] - x,
                                             self.movement_from["y"] - y)
                self.mapdata.set_focus(self.origin_position["longitude"] + lon,
                                     self.origin_position["latitude"] - lat)
                self.movement_from["x"] = x
                self.movement_from["y"] = y
            
                # redraw
                self.dirty = True
#                self.queue_draw()

        return True

    def handle_expose_event(self, widget, event):
        self.context = widget.window.cairo_create()

        # the context rect to draw on
        self.context.rectangle(event.area.x, event.area.y,
                               event.area.width, event.area.height)
        self.context.clip()
        if self.dirty:
            self.draw()
            self.dirty = False
        return False

    def draw(self):
        '''
        Draw the tiles and objects of this map.
        '''
        # get all tiles of this level
        level = self.mapdata.get_level(self.zoom_level)
        # select only the needed tiles
        tiles, cols, rows = level.get_tiles(self.mapdata.focus)
        self.cols = cols
        self.rows = rows

        # set bounds
        self.bounds["min_longitude"] = tiles[0].bounds["min_longitude"]
        self.bounds["min_latitude"] = tiles[0].bounds["min_latitude"]
        self.bounds["max_longitude"] = tiles[-1].bounds["max_longitude"]
        self.bounds["max_latitude"] = tiles[-1].bounds["max_latitude"]

        # draw every map tile in tiles
        for tile in tiles:
            x, y = self.gps_to_pixel(tile.bounds["min_longitude"],
                                     tile.bounds["min_latitude"])
            tile.picture.draw(self.context, x, y)

        # get the map objects to draw
        objects = self.mapdata.objects

        # draw objects
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
        x, y, state = event.window.get_pointer()
        (lon,lat) = self.pixel_to_gps(x,y)
#        rect = self.get_allocation()
#        dx = 1.0*x/rect.width
#        dy = 1.0*y/rect.height
#        
#        width = self.bounds["max_longitude"] - self.bounds["min_longitude"]
#        height = self.bounds["max_latitude"] - self.bounds["min_latitude"]
        
        gps_x = self.bounds["min_longitude"] + lon#dx*width
        gps_y = self.bounds["min_latitude"] - lat#dy*height

        print gps_x, gps_y
        return gps_x,gps_y
        
    def draw_clicked_pos(self,event):
        (lon,lat) = self.get_clicked_coord(event)
        print (lon,lat)
