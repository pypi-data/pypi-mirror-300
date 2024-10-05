import logging
import xml.etree.ElementTree as ET
from landxml_objects import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from landxml_exporter import LandXMLExporter  # Adjust the import path as needed


class LandXMLParser:
    def __init__(self, xml_content=None):
        self.namespaces = {'landxml': 'http://www.landxml.org/schema/LandXML-1.2'}
        if xml_content:
            self.root = ET.fromstring(xml_content)
        else:
            self.root = None
        self.original_tree = None
        self.modified_elements = set()
        
    def export_landxml(self):
        if not self.objects:
            QMessageBox.warning(self, "Export Error", "No data to export. Please import a LandXML file first.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save LandXML File", "", "LandXML Files (*.xml)")
        if file_name:
            try:
                exporter = LandXMLExporter()
                exporter.create_landxml(self.objects)
                exporter.export_to_file(file_name)
                QMessageBox.information(self, "Export Successful", f"LandXML file exported to {file_name}")
            except Exception as e:
                logging.error(f"Error exporting file: {str(e)}")
                QMessageBox.critical(self, "Export Error", f"An error occurred while exporting the file: {str(e)}")

    def parse(self, file_name):
        self.original_tree = ET.parse(file_name)
        self.root = self.original_tree.getroot()
        logging.info(f"Root tag: {self.root.tag}")
        logging.info(f"Root attributes: {self.root.attrib}")
        
        # Extract namespace from the root tag
        self.xmlns = self.root.tag.split('}')[0][1:]
        self.namespaces = {'landxml': self.xmlns}
        logging.info(f"Namespaces: {self.namespaces}")

        parsed_objects = []
        logging.info("Parsing header")
        parsed_objects.append(self.parse_header())
        
        points = self.parse_points()
        logging.info(f"Parsed {len(points)} valid points")
        parsed_objects.extend(points)
        
        alignments = self.parse_alignments()
        logging.info(f"Parsed {len(alignments)} alignments")
        parsed_objects.extend(alignments)
        
        surfaces = self.parse_surfaces()
        logging.info(f"Parsed {len(surfaces)} surfaces")
        parsed_objects.extend(surfaces)
        
        survey_data = self.parse_survey_data()
        logging.info(f"Parsed {len(survey_data)} survey data objects")
        parsed_objects.extend(survey_data)
        
        pipe_networks = self.parse_pipe_networks()
        logging.info(f"Parsed {len(pipe_networks)} pipe networks")
        parsed_objects.extend(pipe_networks)

        logging.info(f"Parsed {len(parsed_objects)} objects in total")
        return parsed_objects

    def parse_header(self):
        root_attributes = dict(self.root.attrib)

        units = self.root.find('landxml:Units', self.namespaces)
        if units is not None:
            units_dict = {}
            
            # Check for Metric units
            metric = units.find('landxml:Metric', self.namespaces)
            if metric is not None:
                units_dict['metric'] = dict(metric.attrib)
            
            # Check for Imperial units
            imperial = units.find('landxml:Imperial', self.namespaces)
            if imperial is not None:
                units_dict['imperial'] = dict(imperial.attrib)
            
            # If neither Metric nor Imperial is found, store any direct attributes of Units
            if not units_dict:
                units_dict = dict(units.attrib)
        else:
            units_dict = {}

        project = 'Unknown Project'
        project_element = self.root.find('landxml:Project', self.namespaces)
        if project_element is not None:
            project = project_element.get('name', project)
        
        application = 'Unknown Application'
        application_element = self.root.find('landxml:Application', self.namespaces)
        if application_element is not None: 
            application = application_element.get('name', application)
        
        header = LandXMLHeader(name='LandXMLHeader', attributes=root_attributes, project=project, application=application)
        header.units.append(units_dict)
        
        return header

    def parse_surfaces(self):
        logging.info("Parsing surfaces")
        surfaces = []
        try:
            surface_elements = self.root.findall('.//landxml:Surfaces/landxml:Surface', self.namespaces)
            if not surface_elements:
                logging.warning("No surfaces found")
                return surfaces
            logging.info(f"Found {len(surface_elements)} surfaces")
            for surface in surface_elements:
                name = surface.get('name')
                attributes = dict(surface.attrib)
                
                source_data = self.parse_source_data(surface)
                definition = self.parse_definition(surface)
                
                if definition:
                    surface_obj = Surface(name, attributes, definition)
                    surface_obj.source_data = source_data
                    surfaces.append(surface_obj)
                else:
                    logging.warning(f"Surface {name} has no definition, skipping")
        except Exception as e:
            logging.error(f"Error parsing surfaces: {str(e)}", exc_info=True)
        return surfaces

    def parse_source_data(self, surface):
        source_data_elem = surface.find('landxml:SourceData', self.namespaces)
        if source_data_elem is not None:
            return {'content': source_data_elem.text}
        return None

    def parse_definition(self, surface):
        definition_elem = surface.find('landxml:Definition', self.namespaces)
        if definition_elem is not None:
            definition = {
                'surfType': definition_elem.get('surfType'),
                'area2DSurf': definition_elem.get('area2DSurf'),
                'area3DSurf': definition_elem.get('area3DSurf'),
                'elevMax': definition_elem.get('elevMax'),
                'elevMin': definition_elem.get('elevMin'),
                'points': self.extract_surface_points(definition_elem),
                'faces': self.extract_surface_faces(definition_elem)
            }
            return definition
        return None

    def parse_features(self, surface):
        features = []
        feature_elements = surface.findall('LandXML.Feature', self.namespaces)
        if feature_elements is None:
            logging.warning("No features found")
            return features
        for feature in feature_elements:
            features.append(dict(feature.attrib))
        return features

    def extract_coordinates(self, element):
        coords = []
        for coord in element.findall('LandXML.Coord', self.namespaces):
            coords.append(tuple(map(float, coord.text.split())))
        return coords

    def extract_surface_points(self, element):
        points = []
        pnts_elem = element.find('landxml:Pnts', self.namespaces)
        if pnts_elem is not None:
            for p in pnts_elem.findall('landxml:P', self.namespaces):
                coords = p.text.split()
                if len(coords) == 3:
                    points.append({
                        'id': p.get('id'),
                        'x': float(coords[0]),
                        'y': float(coords[1]),
                        'z': float(coords[2])
                    })
                else:
                    logging.warning(f"Invalid point data: {p.text}")
        return points

    def extract_surface_faces(self, element):
        faces = []
        faces_elem = element.find('landxml:Faces', self.namespaces)
        if faces_elem is not None:
            for f in faces_elem.findall('landxml:F', self.namespaces):
                face_data = f.text.split()
                if len(face_data) >= 3:
                    faces.append({
                        'vertices': [int(i) for i in face_data[:3]],
                        'n': f.get('n')
                    })
                else:
                    logging.warning(f"Invalid face data: {f.text}")
        return faces

    def parse_survey_data(self):
        logging.info("Parsing survey data")
        survey_data = []
        try:
            survey_elements = self.root.findall('.//landxml:Survey', self.namespaces)
            logging.info(f"Found {len(survey_elements)} Survey elements")
            for survey in survey_elements:
                survey_item = SurveyData(survey.get('name', 'Unnamed Survey'), dict(survey.attrib))
                self.parse_survey_header(survey, survey_item)
                self.parse_equipment(survey, survey_item)
                self.parse_cg_points(survey, survey_item)
                self.parse_instrument_setups(survey, survey_item)
                self.parse_observation_groups(survey, survey_item)
                survey_data.append(survey_item)
            logging.info(f"Parsed {len(survey_data)} survey data objects")
        except Exception as e:
            logging.error(f"Error parsing survey data: {str(e)}", exc_info=True)
        return survey_data

    def parse_survey_header(self, survey, survey_item):
        header = survey.find('landxml:SurveyHeader', self.namespaces)
        if header is not None:
            survey_item.header = dict(header.attrib)

    def parse_equipment(self, survey, survey_item):
        equipment = survey.find('landxml:Equipment', self.namespaces)
        if equipment is not None:
            survey_item.equipment = []
            for instrument in equipment.findall('landxml:InstrumentDetails', self.namespaces):
                survey_item.equipment.append(dict(instrument.attrib))

    def parse_cg_points(self, survey, survey_item):
        cg_points = survey.find('landxml:CgPoints', self.namespaces)
        if cg_points is not None:
            survey_item.cg_points = []
            for point in cg_points.findall('landxml:CgPoint', self.namespaces):
                coords = point.text.strip().split()
                survey_item.cg_points.append({
                    'pntRef': point.get('pntRef'),
                    'coordinates': [float(coord) for coord in coords]
                })

    def parse_instrument_setups(self, survey, survey_item):
        survey_item.instrument_setups = []
        for setup in survey.findall('landxml:InstrumentSetup', self.namespaces):
            setup_item = {
                'id': setup.get('id'),
                'stationName': setup.get('stationName'),
                'instrumentHeight': setup.get('instrumentHeight'),
                'instrumentPoint': None
            }
            instrument_point = setup.find('landxml:InstrumentPoint', self.namespaces)
            if instrument_point is not None:
                setup_item['instrumentPoint'] = instrument_point.get('pntRef')
            survey_item.instrument_setups.append(setup_item)

    def parse_observation_groups(self, survey, survey_item):
        for obs_group in survey.findall('landxml:ObservationGroup', self.namespaces):
            group = ObservationGroup(obs_group.get('id', 'Unnamed Group'), dict(obs_group.attrib))
            self.parse_backsight(obs_group, group)
            self.parse_observations(obs_group, group)
            survey_item.observation_groups.append(group)

    def parse_backsight(self, obs_group, group):
        backsight = obs_group.find('landxml:Backsight', self.namespaces)
        if backsight is not None:
            backsight_obj = Backsight(backsight.get('id', 'Unnamed Backsight'), dict(backsight.attrib))
            backsight_point = backsight.find('landxml:BacksightPoint', self.namespaces)
            if backsight_point is not None:
                backsight_obj.point = dict(backsight_point.attrib)
                if backsight_point.text:
                    backsight_obj.point['coordinates'] = [float(coord) for coord in backsight_point.text.strip().split()]
            group.add_backsight(backsight_obj)

    def parse_observations(self, obs_group, group):
        for observation in obs_group.findall('landxml:RawObservation', self.namespaces):
            obs_attrs = dict(observation.attrib)
            raw_obs = RawObservation(
                targetHeight=obs_attrs.get('targetHeight'),
                slopeDistance=obs_attrs.get('slopeDistance'),
                zenithAngle=obs_attrs.get('zenithAngle'),
                azimuth=obs_attrs.get('azimuth'),
                horizAngle=obs_attrs.get('horizAngle'),
                directFace=obs_attrs.get('directFace')
            )
            target_point = observation.find('landxml:TargetPoint', self.namespaces)
            if target_point is not None:
                raw_obs.targetPoint = TargetPoint(
                    description=target_point.get('desc'),
                    pointReference=target_point.get('pntRef')
                )
                if target_point.text:
                    raw_obs.targetPoint.coordinates = [float(coord) for coord in target_point.text.strip().split()]
            group.add_observation(raw_obs)

    def parse_points(self):
        logging.info("Parsing points")
        points = []
        try:
            # Parse points at the root level
            root_point_elements = self.root.findall('./landxml:CgPoints/landxml:CgPoint', self.namespaces)
            logging.info(f"Found {len(root_point_elements)} points at root level")
            points.extend(self.create_point_objects(root_point_elements))

            # Parse points within the Survey section
            survey_point_elements = self.root.findall('./landxml:Survey/landxml:CgPoints/landxml:CgPoint', self.namespaces)
            logging.info(f"Found {len(survey_point_elements)} points in Survey section")
            points.extend(self.create_point_objects(survey_point_elements))

            logging.info(f"Successfully parsed {len(points)} points in total")
        except Exception as e:
            logging.error(f"Error parsing points: {str(e)}", exc_info=True)
        return points

    def create_point_objects(self, point_elements):
        point_objects = []
        for point in point_elements:
            name = point.get('name')
            coords = point.text.strip().split()
            if len(coords) == 3:
                north, east, elevation = map(float, coords)
                point_obj = Point(name, dict(point.attrib), north, east, elevation)
                point_objects.append(point_obj)
            else:
                logging.warning(f"Invalid coordinate data for point {name}: {point.text}")
        return point_objects

    def parse_pipe_networks(self):
            pipe_networks = []
            try:
                pipe_network_elements = self.root.findall('.//landxml:PipeNetworks/landxml:PipeNetwork', self.namespaces)
                logging.info(f"Found {len(pipe_network_elements)} pipe networks")
                for pipe_network in pipe_network_elements:
                    name = pipe_network.get('name')
                    
                    pipes = self.parse_pipes(pipe_network)
                    structs = self.parse_structs(pipe_network)
                    features = self.parse_features(pipe_network)
                    
                    network = PipeNetwork(name, dict(pipe_network.attrib))
                    network.pipes = pipes
                    network.structs = structs
                    network.features = features
                    
                    pipe_networks.append(network)
                logging.info(f"Parsed {len(pipe_networks)} pipe networks")
            except Exception as e:
                logging.error(f"Error parsing pipe networks: {str(e)}", exc_info=True)
            return pipe_networks

    def parse_pipes(self, pipe_network):
        pipes = []
        pipe_elements = pipe_network.findall('.//landxml:Pipe', self.namespaces)
        logging.info(f"Found {len(pipe_elements)} pipes")
        for pipe in pipe_elements:
            name = pipe.get('name')
            attributes = dict(pipe.attrib)
            
            # Parse the CircPipe element
            circ_pipe_elem = pipe.find('landxml:CircPipe', self.namespaces)
            if circ_pipe_elem is not None:
                attributes['diameter'] = circ_pipe_elem.get('diameter')
                attributes['thickness'] = circ_pipe_elem.get('thickness')
            
            pipe_obj = Pipe(name, attributes)
            pipes.append(pipe_obj)
        return pipes

    def parse_structs(self, pipe_network):
        structs = []
        struct_elements = pipe_network.findall('.//landxml:Struct', self.namespaces)
        logging.info(f"Found {len(struct_elements)} structs")
        for struct in struct_elements:
            name = struct.get('name')
            attributes = dict(struct.attrib)
            
            # Parse the Center element
            center_elem = struct.find('landxml:Center', self.namespaces)
            if center_elem is not None:
                attributes['center'] = center_elem.text.strip()
            
            # Parse the CircStruct element
            circ_struct_elem = struct.find('landxml:CircStruct', self.namespaces)
            if circ_struct_elem is not None:
                attributes['diameter'] = circ_struct_elem.get('diameter')
                attributes['thickness'] = circ_struct_elem.get('thickness')
            
            # Parse Invert elements
            invert_elements = struct.findall('landxml:Invert', self.namespaces)
            attributes['inverts'] = []
            for invert in invert_elements:
                invert_data = {
                    'elev': invert.get('elev'),
                    'flowDir': invert.get('flowDir'),
                    'refPipe': invert.get('refPipe')
                }
                attributes['inverts'].append(invert_data)
            
            struct_obj = Struct(name, attributes)
            structs.append(struct_obj)
        return structs

    def parse_features(self, pipe_network):
        features = []
        feature_elements = pipe_network.findall('.//landxml:Feature', self.namespaces)
        logging.info(f"Found {len(feature_elements)} features")
        for feature in feature_elements:
            name = feature.get('name')
            feature_obj = Feature(name, dict(feature.attrib))
            features.append(feature_obj)
        return features

    def parse_features(self, pipe_network):
        features = []
        feature_elements = pipe_network.findall('.//landxml:Feature', self.namespaces)
        logging.info(f"Found {len(feature_elements)} features")
        for feature in feature_elements:
            name = feature.get('name')
            feature_obj = Feature(name, dict(feature.attrib))
            features.append(feature_obj)
        return features

    def parse_alignments(self):
        logging.info("Parsing alignments")
        alignments = []
        try:
            alignment_elements = self.root.findall('.//landxml:Alignments/landxml:Alignment', self.namespaces)
            logging.info(f"Found {len(alignment_elements)} alignments")
            for alignment in alignment_elements:
                name = alignment.get('name')
                length = alignment.get('length')
                sta_start = alignment.get('staStart')
                
                coord_geom = self.parse_coord_geom(alignment)
                sta_equations = self.parse_sta_equations(alignment)
                profile = self.parse_profile(alignment)
                
                alignment_obj = Alignment(name, {
                    'name': name,
                    'length': length,
                    'staStart': sta_start
                })

                alignment_obj.coord_geom = coord_geom
                alignment_obj.sta_equations = sta_equations
                alignment_obj.profile = profile

                alignments.append(alignment_obj)
        except Exception as e:
            logging.error(f"Error parsing alignments: {str(e)}", exc_info=True)
        return alignments

    def parse_coord_geom(self, alignment):
        coord_geom = []
        coord_geom_elem = alignment.find('landxml:CoordGeom', self.namespaces)
        if coord_geom_elem is not None:
            for element in coord_geom_elem:
                if element.tag.endswith('Line'):
                    coord_geom.append(self.parse_line(element))
                elif element.tag.endswith('Curve'):
                    coord_geom.append(self.parse_curve(element))
                elif element.tag.endswith('Spiral'):
                    coord_geom.append(self.parse_spiral(element))
        return coord_geom

    def parse_line(self, line_elem):
        return {
            'type': 'Line',
            'staStart': line_elem.get('staStart'),
            'length': line_elem.get('length'),
            'dir': line_elem.get('dir'),
            'start': self.parse_point(line_elem.find('landxml:Start', self.namespaces)),
            'end': self.parse_point(line_elem.find('landxml:End', self.namespaces))
        }

    def parse_curve(self, curve_elem):
        return {
            'type': 'Curve',
            'staStart': curve_elem.get('staStart'),
            'rot': curve_elem.get('rot'),
            'start': self.parse_point(curve_elem.find('landxml:Start', self.namespaces)),
            'center': self.parse_point(curve_elem.find('landxml:Center', self.namespaces)),
            'end': self.parse_point(curve_elem.find('landxml:End', self.namespaces))
        }

    def parse_spiral(self, spiral_elem):
        return {
            'type': 'Spiral',
            'staStart': spiral_elem.get('staStart'),
            'length': spiral_elem.get('length'),
            'rot': spiral_elem.get('rot'),
            'radiusStart': spiral_elem.get('radiusStart'),
            'radiusEnd': spiral_elem.get('radiusEnd'),
            'spiType': spiral_elem.get('spiType'),
            'start': self.parse_point(spiral_elem.find('landxml:Start', self.namespaces)),
            'PI': self.parse_point(spiral_elem.find('landxml:PI', self.namespaces)),
            'end': self.parse_point(spiral_elem.find('landxml:End', self.namespaces))
        }

    def parse_point(self, point_elem):
        if point_elem is not None:
            coords = point_elem.text.split()
            return {
                'name': point_elem.get('name'),
                'x': float(coords[0]),
                'y': float(coords[1])
            }
        return None

    def parse_sta_equations(self, alignment):
        sta_equations = []
        for sta_eq in alignment.findall('landxml:StaEquation', self.namespaces):
            sta_equations.append({
                'staAhead': sta_eq.get('staAhead'),
                'staBack': sta_eq.get('staBack'),
                'staInternal': sta_eq.get('staInternal')
            })
        return sta_equations

    def parse_coord_geom(self, alignment):
        coord_geom = []
        coord_geom_elem = alignment.find('landxml:CoordGeom', self.namespaces)
        if coord_geom_elem is not None:
            for element in coord_geom_elem:
                if element.tag.endswith('Line'):
                    coord_geom.append(self.parse_line(element))
                elif element.tag.endswith('Curve'):
                    coord_geom.append(self.parse_curve(element))
                elif element.tag.endswith('Spiral'):
                    coord_geom.append(self.parse_spiral(element))
        return coord_geom
    
    def parse_profile(self, alignment):
        profile = {'elements': []}
        profile_elem = alignment.find('landxml:Profile', self.namespaces)
        if profile_elem is not None:
            prof_align_elem = profile_elem.find('landxml:ProfAlign', self.namespaces)
            if prof_align_elem is not None:
                profile['elements'].extend(self.parse_profAlign(prof_align_elem))
            
            prof_surf_elements = profile_elem.findall('landxml:ProfSurf', self.namespaces)
            if prof_surf_elements:
                for prof_surf in prof_surf_elements:
                    profile['elements'].extend(self.parse_profSurf(prof_surf))
        
        return profile

    def parse_profAlign(self, prof_align_elem):
        elements = []
        for element in prof_align_elem:
            if element.tag.endswith('PVI'):
                elements.append(self.parse_PVI(element))
            elif element.tag.endswith('CircCurve'):
                elements.append(self.parse_CircCurve(element))
        return elements

    def parse_PVI(self, pvi_elem):
        station, elevation = map(float, pvi_elem.text.split())
        return {'type': 'PVI', 'station': station, 'elevation': elevation, 'source': 'ProfAlign'}

    def parse_CircCurve(self, circ_curve_elem):
        length = float(circ_curve_elem.get('length'))
        radius = float(circ_curve_elem.get('radius'))
        return {'type': 'CircCurve', 'length': length, 'radius': radius, 'source': 'ProfAlign'}

    def parse_profSurf(self, prof_surf_elem):
        name = prof_surf_elem.get('name')
        points = []
        for point_elem in prof_surf_elem.findall('landxml:PntList2D', self.namespaces):
            point_data = point_elem.text.split()
            for i in range(0, len(point_data), 2):
                points.append({
                    'type': 'PVI',
                    'station': float(point_data[i]),
                    'elevation': float(point_data[i+1]),
                    'source': f'ProfSurf:{name}'
                })
        return points

    def parse_ptlist2d(self, ptlist2d_elem):
        points = []
        coords = ptlist2d_elem.text.strip().split()
        for i in range(0, len(coords), 2):
            points.append({'x': float(coords[i]), 'y': float(coords[i+1])})
        return points
    


    

    
