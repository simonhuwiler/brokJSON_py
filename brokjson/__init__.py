# __init__.py

__version__ = "1.0.0"

def geo2brok(geojson):
    
    global_geometries = []
    global_properties = []
    global_foreign_members = []

    for feature in geojson["features"]:

        if feature["type"].casefold() != "feature":
            continue
            
        if not("geometry" in feature): #Check this
            return

        # Add Properties
        props = []
        if 'properties' in feature:
            for property in feature['properties']:

                # Check if item in List
                if not (property in global_properties):
                    # Add to list
                    global_properties.append(property)

                index = global_properties.index(property)

                # Check if props are long enough. If not, add None values
                if len(props) - 1 < index:
                    props = props + [None] * (index + 1 - len(props))

                # Add to Props
                props[index] = feature['properties'][property]

        # Add Foreign Members
        foreign_members = []
        for item in feature:

            # Excludes
            if item.casefold() in ['type', 'properties', 'geometry']:
                continue

            # Check if item in List
            if not (item in global_foreign_members):
                # Add to list
                global_foreign_members.append(item)

            index = global_foreign_members.index(item)

            # Check if foreign_members is long enough. If not, add None values
            if len(foreign_members) - 1 < index:
                foreign_members = foreign_members + [None] * (index + 1 - len(foreign_members))

            # Add Foreign Members
            foreign_members[index] = feature[item]

        coords = None
        if feature["geometry"]["type"].casefold() == "geometrycollection":
            
            # GeometryCollection detected!
            coords = []
            
            for geom in feature["geometry"]["geometries"]:
                
                # Now check if last item of geometries is same type. If not, add the type
                if ((len(coords) == 0) or
                     (coords[-1]['type'].casefold() != geom['type'].casefold())):

                    # Add new geometry-list
                    coords.append({'type': geom['type'], 'features': []})
                
                # Add feature to geometry list
                coords[len(coords) - 1]['features'].append([geom["coordinates"]])
                
        else: 
            # Add Coords
            coords = feature["geometry"]["coordinates"]
        
        # Create feature-array
        brok_feature = [coords]

        # Add props
        if len(props) > 0:
            brok_feature.append(props)

        # Add foreign members
        if len(foreign_members) > 0:
            if len(brok_feature) < 2:
                brok_feature.append(None)
            brok_feature.append(foreign_members)

        # Now check if last item of geometries is same type. If not, add the type
        if ((len(global_geometries) == 0) or
             (global_geometries[-1]['type'].casefold() != feature['geometry']['type'].casefold())):

            # Add new geometry-list
            global_geometries.append({'type': feature['geometry']['type'], 'features': []})

        # Add feature to geometry list
        global_geometries[len(global_geometries) - 1]['features'].append(brok_feature)    


    # Build BrokJSON
    brok = {}

    # Add Global Properties
    if len(global_properties) > 0:
        brok['properties'] = global_properties

    # Add Foreign Members
    if len(global_foreign_members) > 0:
        brok['foreignMembers'] = global_foreign_members
        
    # Add all unknown members
    for member in geojson:
        
        # Exclude List
        if member in ['type', 'features']:
            continue
            
        brok[member] = geojson[member]
    

    # Add Geometry
    if len(global_geometries) > 0:
        brok['geometries'] = global_geometries
        
    return brok

def brok2geo(brok):
    geo = {
        "type": "FeatureCollection"
    }
    
    # Look for custom properties on root
    for member in brok:
        if not(member in ['properties', 'geometries', 'foreignMembers']):
            geo[member] = brok[member]

    if len(brok['geometries']) > 0:
        geo['features'] = []
    
    # Add Geometries
    geometries = []
    for geometryCollection in brok['geometries']:
        
        for feature in geometryCollection['features']:
            
            # Create Feature
            json_feature = {"type": "Feature"}
            
            # Check and add properties
            properties = {}
            if len(feature) >= 2:
                
                for p in range(0, len(feature[1])):
                    
                    prop = feature[1][p]
                    
                    if(prop == None):
                        continue
                        
                    properties[brok['properties'][p]] = prop
                    
            # Check and add foreign members
            if len(feature) >= 3:
                for m in range(0, len(feature[2])):
                    json_feature[brok['foreignMembers'][m]] = feature[2][m]
            
            # Add props
            if(len(properties) > 0):
                json_feature['properties'] = properties
                
            # Check if Geometry Collection
            if geometryCollection["type"].casefold() == 'geometrycollection':
                
                new_coords = []
                for coordinates in geometryCollection['features']:
                    for geocol in coordinates[0]:
                        for types in geocol['features']:
                            coord = {
                                "type": geocol['type'],
                                "coordinates": types[0]
                            }
                            new_coords.append(coord)

                            
                # Add Geometry
                json_feature['geometry'] = {"type": geometryCollection["type"], "geometries": new_coords}
                
            else:
                # Normal Geometry
                json_feature['geometry'] = {"type": geometryCollection["type"], "coordinates": feature[0]}
            
            geo['features'].append(json_feature)
    
    return geo