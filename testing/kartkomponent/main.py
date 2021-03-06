# -*- coding: utf-8 -*-
import sys
import data_storage
import map_xml_reader
import gui
import shared.data

# Kartan
print "Läser in kartinformation från kartdata/map.xml"
mapxml = map_xml_reader.MapXML("kartdata/map.xml")

map = data_storage.MapData(mapxml.get_name(),
                           mapxml.get_levels())

# Ställer in vad kartkomponenten ska fokusera på (visa)
# (blir mittenpunkten på skärmen, dvs 50% x-led, 50% y-lyd.
map.set_focus(15.5726, 58.4035)

#Draw a totempole

totem_coordinate = (15.5726, 58.4035)
totem_unit_data = shared.data.UnitData(totem_coordinate, "Totem", 0)
totem_unit_data.type = shared.data.UnitType.commander
totem = data_storage.Unit(totem_unit_data)
map.add_object("totem", totem)

#Draw a tree

tree_coordinate = (15.5726, 58.4050)
tree_obstacle_data = shared.data.ObstacleData(tree_coordinate, "Tree", 0)
tree_obstacle_data.type = shared.data.ObstacleType.tree
tree = data_storage.Obstacle(tree_obstacle_data)
map.add_object("Tree", tree)

# hej

goal_coordinate = (15.5766, 58.3960)
goal_poi_data = shared.data.POIData(goal_coordinate, "goal", 0)
goal = data_storage.POI(goal_poi_data)
goal.map_object_data.type = shared.data.POIType.pasta_wagon
map.add_object("PastaVagnen", goal)

# Ritar ut tre objekt
'''
map.add_object("Ambulans1", data_storage.MapObject({"longitude":15.5726,
                                                    "latitude":58.4035},
                                                   "ikoner/Totem-Pole-32x32.png"))
map.add_object("Brandbil1", data_storage.MapObject({"longitude":15.5729,
                                                    "latitude":58.40193},
                                                   "ikoner/brandbil.png"))
map.add_object("Sjukhus1", data_storage.MapObject({"longitude":15.5629,
                                                   "latitude":58.4093},
                                                  "ikoner/sjukhus.png"))
'''
# Ritar ut en svart cirkel
#
# Nedan används två kommandon för utritningen.
#   arc: Ritar ut en cirkel med centrum i position x - 5 och y - 5, radie 10.
#        0 respektive 2 * math.pi är vinklar. Utritningen börjar vid första
#        vinkeln (0) och fortsätter i riktning mot den andra (2 * math.pi).
#   set_source_rgb: Ställer in cirkelns färg.
# Andra exempel på kommandon finns här:
#   http://www.tortall.net/mu/wiki/CairoTutorial
#   http://www.tortall.net/mu/wiki/PyGTKCairoTutorial
# Övrigt
#   Det kanske upplevs underligt att x, y och math.pi används i uttrycken,
#   var definieras variablerna? x och y räknas ut av objektets draw-funktion
#   och finns tillgängliga när utritning senare sker. Se x och y som samma
#   position som figurens GPS-koordinater, men i pixlar.
#   Förutom x och y finns hela Pythons math-bibliotek tillgängligt för
#   användning i uttrycken nedan.
'''
map.add_object("Shape1", data_storage.MapObject({"longitude":15.5829,
                                                 "latitude":58.4093},
                                                "arc(x - 5, y - 5, 10, 0, 2 * math.pi)",
                                                "set_source_rgb(0, 0, 0)"))
'''
# Skapar grafiska interfacet.
print "Skapar programmets GUI."
app = gui.Gui(map)

# Kör programmet
print "Kör programmet."
app.run()
