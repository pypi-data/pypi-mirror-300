import logging
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRegExp, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from landxml_parser import LandXMLParser
from landxml_objects import *
from landxml_exporter import LandXMLExporter
import math
from matplotlib.patches import Arc
import numpy as np

def setup_logging():
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    
    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # File handler
    file_handler = logging.FileHandler('landxml_viewer.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Call this function before creating your QApplication
setup_logging()

class LandXMLViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("Initializing LandXMLViewer")
        self.setWindowTitle("LandXML Viewer")
        self.setGeometry(100, 100, 1440, 900)

        self.setup_ui()
        self.setup_toolbar()
        self.setup_statusbar()
        self.setup_connections()
        self.setup_tree_buttons()  

        self.objects = []
        self.scatter = None
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.is_new_import = True

        self.parser = LandXMLParser()
        self.modified_elements = set()

        self.current_view = 'map'  # Track current view

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Main splitter
        main_splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(main_splitter)

        # Top splitter for tree view and map view
        top_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(top_splitter)

        # Add your content to top_splitter here
        # ...

        # Set the sizes of the main splitter to use full height for the top section
        main_splitter.setSizes([self.height(), 0])

        # Make the splitter handles easier to grab (optional)
        main_splitter.setHandleWidth(10)
        top_splitter.setHandleWidth(10)

        # Set the sizes of the top splitter (adjust as needed)
        top_splitter.setSizes([self.width() * 5, self.width() * 5])
        
        # Left panel (Map view)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.figure = Figure(figsize=(5, 16), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        left_layout.addWidget(self.toolbar)
        left_layout.addWidget(self.canvas)

        # Right panel (Tree view)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.filter_tree)
        right_layout.addWidget(self.search_box)

        self.tree_view = QTreeView()
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setAnimated(True)
        self.tree_view.setEditTriggers(QTreeView.DoubleClicked | QTreeView.EditKeyPressed)
        right_layout.addWidget(self.tree_view)

        # Add expand and collapse buttons
        button_layout = QHBoxLayout()
        self.expand_all_button = QPushButton("Expand All")
        self.expand_all_button.clicked.connect(self.expand_all_nodes)
        self.collapse_all_button = QPushButton("Collapse All")
        self.collapse_all_button.clicked.connect(self.collapse_all_nodes)
        button_layout.addWidget(self.expand_all_button)
        button_layout.addWidget(self.collapse_all_button)
        right_layout.addLayout(button_layout)

        # Set up the model and proxy model
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Value"])
        self.proxy_model = QSortFilterProxyModel(self.tree_view)
        self.proxy_model.setSourceModel(self.tree_model)
        self.proxy_model.setRecursiveFilteringEnabled(True)
        self.tree_view.setModel(self.proxy_model)

        # Set column widths
        self.tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree_view.header().setSectionResizeMode(1, QHeaderView.Stretch)

        top_splitter.addWidget(left_panel)
        top_splitter.addWidget(right_panel)

        # Object info
        self.object_info_scroll = QScrollArea()
        self.object_info_widget = QWidget()
        self.object_info_layout = QFormLayout(self.object_info_widget)
        self.object_info_scroll.setWidget(self.object_info_widget)
        self.object_info_scroll.setWidgetResizable(True)
        main_splitter.addWidget(self.object_info_scroll)

        # Set initial sizes
        main_splitter.setSizes([self.height() * 100, self.height() * 0])

        # Connect the model's data change signal to update the underlying objects
        self.tree_model.itemChanged.connect(self.update_object_from_model)

    def filter_tree(self, text):
        self.proxy_model.setFilterRegExp(QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

    def customize_toolbar(self, toolbar):
        # Remove unwanted actions
        unwanted_actions = ["Subplots", "Edit", "Save"]
        for action in toolbar.actions():
            if action.text() in unwanted_actions:
                toolbar.removeAction(action)

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        import_action = QAction(QIcon("icons/import.png"), "Import", self)
        import_action.triggered.connect(self.import_landxml)
        toolbar.addAction(import_action)

        export_action = QAction(QIcon("icons/export.png"), "Export", self)
        export_action.triggered.connect(self.export_landxml)
        toolbar.addAction(export_action)

        toggle_view_action = QAction(QIcon("icons/toggle.png"), "Toggle View", self)
        toggle_view_action.triggered.connect(self.toggle_view)
        toolbar.addAction(toggle_view_action)

        # Set text beside icons
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

    def setup_tree_view(self):
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Value"])
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.tree_model.itemChanged.connect(self.update_object_from_model)

    def toggle_view(self):
        if self.current_view == 'map':
            self.current_view = 'profile'
            self.plot_profiles()
        else:
            self.current_view = 'map'
            self.plot_objects()

    def get_item_attribute(self, item, attribute_name):
        for i in range(item.rowCount()):
            child = item.child(i)
            if child.text().startswith(f"{attribute_name}:"):
                return child.text().split(":", 1)[1].strip()
        return None

    def plot_objects(self):
        logging.info("Plotting objects")
        self.ax.clear()
        if not self.objects:
            logging.warning("No objects to plot")
            return

        north_coords = []
        east_coords = []
        heights = []
        names = []

        for obj in self.objects:
            if isinstance(obj, Point):
                north_coords.append(obj.north)
                east_coords.append(obj.east)
                heights.append(obj.elevation)
                names.append(obj.name)
            elif isinstance(obj, Alignment):
                self.plot_alignment(obj)
            elif isinstance(obj, Surface):
                self.plot_surface_points(obj)

        if north_coords and east_coords:
            self.scatter = self.ax.scatter(east_coords, north_coords, c=heights, 
                                           cmap='viridis', picker=True, pickradius=5)
            for i, name in enumerate(names):
                self.ax.annotate(name, (east_coords[i], north_coords[i]), xytext=(5, 5), 
                                 textcoords='offset points', fontsize=8)

        if self.ax.get_legend_handles_labels()[0]:  # Check if there are any labels
            self.ax.legend()
        self.ax.grid(True)
        self.ax.set_xlabel('East')
        self.ax.set_ylabel('North')
        self.ax.set_title('Map View')

        # Remove coordinate numbers
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.names = names  # Store names for use in on_pick method

        self.canvas.draw()

    def plot_surface_points(self, surface):
        if surface.definition and 'points' in surface.definition:
            points = surface.definition['points']
            x = [p['x'] for p in points]
            y = [p['y'] for p in points]
            z = [p['z'] for p in points]
            self.ax.scatter(x, y, c=z, cmap='viridis', s=1, alpha=0.5, label=f'Surface: {surface.name}')

    def plot_profiles(self):
        self.ax.clear()
        alignments_with_profiles = [obj for obj in self.objects if isinstance(obj, Alignment) and (obj.profile or hasattr(obj, 'profsurf'))]

        if not alignments_with_profiles:
            self.plot_east_elevation()
        else:
            for alignment in alignments_with_profiles:
                if alignment.profile:
                    self.plot_alignment_profile(alignment)
                if hasattr(alignment, 'profsurf') and alignment.profsurf:
                    self.plot_profsurf(alignment)

        self.ax.set_xlabel('Station')
        self.ax.set_ylabel('Elevation')
        self.ax.set_title('Profile View')
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def plot_profsurf(self, alignment):
        if hasattr(alignment, 'profsurf') and alignment.profsurf:
            for surf in alignment.profsurf:
                stations, elevations = zip(*surf['points'])
                self.ax.plot(stations, elevations, label=f"ProfSurf: {surf['name']}")

    def plot_alignment_profile(self, alignment):
        profile = alignment.profile
        stations = []
        elevations = []

        for i, element in enumerate(profile['elements']):
            if element['type'] == 'PVI':
                station = float(element['station'])
                elevation = float(element['elevation'])
                stations.append(station)
                elevations.append(elevation)
                
                if i > 0:
                    prev_element = profile['elements'][i-1]
                    if prev_element['type'] == 'PVI':
                        # Only draw straight line if there's no curve between PVIs
                        prev_station = float(prev_element['station'])
                        prev_elevation = float(prev_element['elevation'])
                        self.ax.plot([prev_station, station], [prev_elevation, elevation], 'b-')
                    elif prev_element['type'] == 'CircCurve':
                        if i > 1 and i < len(profile['elements']) - 1:
                            self.plot_profile_curve(
                                profile['elements'][i-2],  # PVI before curve
                                prev_element,              # Curve element
                                element,                   # PVI after curve
                                profile['elements'][i+1]   # Next PVI for outgoing slope
                            )
        
        # Plot PVI points
        self.ax.plot(stations, elevations, 'ro', label=f"{alignment.name} PVIs")
        self.ax.legend()

    def plot_profile_curve(self, pvi1, curve_element, pvi2, pvi3):
        # Calculate slopes
        incoming_slope = (float(pvi2['elevation']) - float(pvi1['elevation'])) / (float(pvi2['station']) - float(pvi1['station']))
        outgoing_slope = (float(pvi3['elevation']) - float(pvi2['elevation'])) / (float(pvi3['station']) - float(pvi2['station']))

        start_station = float(pvi1['station'])
        start_elevation = float(pvi1['elevation'])
        end_station = float(pvi2['station'])
        end_elevation = float(pvi2['elevation'])
        
        radius = float(curve_element['radius'])
        length = float(curve_element['length'])

        # Determine if the curve is concave up or down based on slope change
        is_concave_up = outgoing_slope < incoming_slope

        # Calculate curve points
        num_points = 100
        stations = np.linspace(start_station, end_station, num_points)
        
        # Calculate the chord slope
        chord_length = end_station - start_station
        chord_slope = (end_elevation - start_elevation) / chord_length
        
        # Calculate the middle ordinate (height of the curve at its midpoint)
        middle_ordinate = (length**2) / (8 * abs(radius))

        # Calculate elevations along the curve
        elevations = []
        for station in stations:
            t = (station - start_station) / length
            y = middle_ordinate * (4 * t * (1 - t))
            
            if not is_concave_up:
                y = -y
            
            chord_elevation = start_elevation + chord_slope * (station - start_station)
            curve_elevation = chord_elevation + y
            elevations.append(curve_elevation)

        # Plot the curve
        self.ax.plot(stations, elevations, 'r-')



    def plot_east_elevation(self):
        points = [obj for obj in self.objects if isinstance(obj, Point)]
        if points:
            east_coords = [point.east for point in points]
            elevations = [point.elevation for point in points]
            self.ax.plot(east_coords, elevations, 'o', label='Points')
            for point in points:
                self.ax.annotate(point.name, 
                                         (point.east, point.elevation),
                                         xytext=(5, 5), textcoords='offset points', fontsize=5)
            self.ax.set_xlabel('East')
            self.ax.legend()

    def plot_alignment(self, alignment):
        for element in alignment.coord_geom:
            if element['type'] == 'Line':
                start = element['start']
                end = element['end']
                self.ax.plot([start['x'], end['x']], [start['y'], end['y']], 'b-')
            elif element['type'] == 'Curve':
                self.plot_curve(element)
            elif element['type'] == 'Spiral':
                start = element['start']
                end = element['end']
                # For spirals, we still use a simplified representation
                self.ax.plot([start['x'], end['x']], [start['y'], end['y']], 'g-')
    
    def add_survey_data_to_tree(self, survey_data, parent_item):
        # Add SurveyHeader
        if survey_data.header:
            header_item = QStandardItem("SurveyHeader")
            parent_item.appendRow([header_item, QStandardItem("")])
            for key, value in survey_data.header.items():
                child = QStandardItem(key)
                value_item = QStandardItem(str(value))
                header_item.appendRow([child, value_item])
        
        # Add Equipment
        if survey_data.equipment:
            equipment_item = QStandardItem("Equipment")
            parent_item.appendRow([equipment_item, QStandardItem("")])
            for equip in survey_data.equipment:
                equip_child = QStandardItem("InstrumentDetails")
                equipment_item.appendRow([equip_child, QStandardItem("")])
                for key, value in equip.items():
                    child = QStandardItem(key)
                    value_item = QStandardItem(str(value))
                    equip_child.appendRow([child, value_item])
        
        # Add CgPoints
        if survey_data.cg_points:
            cg_points_item = QStandardItem("CgPoints")
            parent_item.appendRow([cg_points_item, QStandardItem("")])
            for point in survey_data.cg_points:
                point_child = QStandardItem(f"CgPoint: {point['pntRef']}")
                cg_points_item.appendRow([point_child, QStandardItem("")])
                coords = QStandardItem("Coordinates")
                coords_value = QStandardItem(str(point['coordinates']))
                point_child.appendRow([coords, coords_value])
        
        # Add InstrumentSetups
        if survey_data.instrument_setups:
            setups_item = QStandardItem("InstrumentSetups")
            parent_item.appendRow([setups_item, QStandardItem("")])
            for setup in survey_data.instrument_setups:
                setup_child = QStandardItem(f"Setup: {setup['id']}")
                setups_item.appendRow([setup_child, QStandardItem("")])
                for key, value in setup.items():
                    child = QStandardItem(key)
                    value_item = QStandardItem(str(value))
                    setup_child.appendRow([child, value_item])
        
        # Add ObservationGroups
        if survey_data.observation_groups:
            obs_groups_item = QStandardItem("ObservationGroups")
            parent_item.appendRow([obs_groups_item, QStandardItem("")])
            for group in survey_data.observation_groups:
                group_child = QStandardItem(f"Group: {group.name}")
                obs_groups_item.appendRow([group_child, QStandardItem("")])
                
                # Add Backsight
                if group.backsight:
                    backsight_item = QStandardItem("Backsight")
                    group_child.appendRow([backsight_item, QStandardItem("")])
                    for key, value in group.backsight.attributes.items():
                        child = QStandardItem(key)
                        value_item = QStandardItem(str(value))
                        backsight_item.appendRow([child, value_item])
                    if group.backsight.point:
                        point_item = QStandardItem("BacksightPoint")
                        backsight_item.appendRow([point_item, QStandardItem("")])
                        for key, value in group.backsight.point.items():
                            child = QStandardItem(key)
                            value_item = QStandardItem(str(value))
                            point_item.appendRow([child, value_item])
                
                # Add Observations
                observations_item = QStandardItem("Observations")
                group_child.appendRow([observations_item, QStandardItem("")])
                for obs in group.observations:
                    obs_child = QStandardItem("RawObservation")
                    observations_item.appendRow([obs_child, QStandardItem("")])
                    for attr, value in vars(obs).items():
                        if attr != 'targetPoint':
                            child = QStandardItem(attr)
                            value_item = QStandardItem(str(value))
                            obs_child.appendRow([child, value_item])
                    if obs.targetPoint:
                        target_item = QStandardItem("TargetPoint")
                        obs_child.appendRow([target_item, QStandardItem("")])
                        for attr, value in vars(obs.targetPoint).items():
                            child = QStandardItem(attr)
                            value_item = QStandardItem(str(value))
                            target_item.appendRow([child, value_item])

    def add_pipe_network_to_tree(self, pipe_network, parent_item=None):
        if parent_item is None:
            parent_item = self.tree_model.invisibleRootItem()

        network_item = QStandardItem(f"PipeNetwork: {pipe_network.name}")
        parent_item.appendRow([network_item, QStandardItem("")])

        # Add attributes
        for key, value in pipe_network.attributes.items():
            attr_item = QStandardItem(key)
            value_item = QStandardItem(str(value))
            network_item.appendRow([attr_item, value_item])

        # Add Structs
        structs_item = QStandardItem("Structs")
        network_item.appendRow([structs_item, QStandardItem("")])
        for struct in pipe_network.structs:
            struct_item = QStandardItem(f"Struct: {struct.name}")
            structs_item.appendRow([struct_item, QStandardItem("")])
            for key, value in struct.attributes.items():
                attr_item = QStandardItem(key)
                value_item = QStandardItem(str(value))
                struct_item.appendRow([attr_item, value_item])

        # Add Pipes
        pipes_item = QStandardItem("Pipes")
        network_item.appendRow([pipes_item, QStandardItem("")])
        for pipe in pipe_network.pipes:
            pipe_item = QStandardItem(f"Pipe: {pipe.name}")
            pipes_item.appendRow([pipe_item, QStandardItem("")])
            for key, value in pipe.attributes.items():
                attr_item = QStandardItem(key)
                value_item = QStandardItem(str(value))
                pipe_item.appendRow([attr_item, value_item])

    def plot_surface(self, surface):
        if surface.definition and 'points' in surface.definition and 'faces' in surface.definition:
            points = surface.definition['points']
            faces = surface.definition['faces']
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            z = [p[2] for p in points]
            self.ax.plot_trisurf(x, y, z, triangles=faces, cmap='viridis', alpha=0.7)
            self.ax.set_zlabel('Elevation')

    def plot_curve(self, curve):
        start = curve['start']
        center = curve['center']
        end = curve['end']

        # Calculate radius
        radius = math.sqrt((start['x'] - center['x'])**2 + (start['y'] - center['y'])**2)

        # Calculate start and end angles
        start_angle = math.atan2(start['y'] - center['y'], start['x'] - center['x'])
        end_angle = math.atan2(end['y'] - center['y'], end['x'] - center['x'])

        # Convert angles to degrees
        start_angle_deg = math.degrees(start_angle)
        end_angle_deg = math.degrees(end_angle)

        # Determine if the curve is clockwise or counterclockwise
        dx = end['x'] - start['x']
        dy = end['y'] - start['y']
        cross_product = dx * (center['y'] - start['y']) - dy * (center['x'] - start['x'])

        if cross_product > 0:  # Clockwise
            if end_angle_deg < start_angle_deg:
                end_angle_deg += 360
            theta1, theta2 = start_angle_deg, end_angle_deg
        else:  # Counterclockwise
            if start_angle_deg < end_angle_deg:
                start_angle_deg += 360
            theta1, theta2 = end_angle_deg, start_angle_deg

        # Create and add the arc patch
        arc = Arc((center['x'], center['y']), 2*radius, 2*radius,
                  angle=0, theta1=theta1, theta2=theta2,
                  color='r')
        self.ax.add_patch(arc)

        # Plot start and end points for reference
        self.ax.plot(start['x'], start['y'], 'ro', markersize=5)
        self.ax.plot(end['x'], end['y'], 'ro', markersize=5)

    def display_all_objects(self):
        logging.info("Displaying all objects")
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Attributes"])
        for obj in self.objects:
            self.add_object_to_tree(obj, self.tree_model.invisibleRootItem())

    def add_object_to_tree(self, obj, parent):
        item = QStandardItem(f"{obj.__class__.__name__}: {obj.name}")
        value_item = QStandardItem("")  # Empty value for the main object
        item.setData(obj, Qt.UserRole)  # Store the entire object in the item's data
        parent.appendRow([item, value_item])
        
        if isinstance(obj, SurveyData):
            self.add_survey_data_to_tree(obj, item)
        elif isinstance(obj, PipeNetwork):
            self.add_pipe_network_to_tree(obj, item)
        elif isinstance(obj, Alignment):
            self.add_alignment_to_tree(obj, item)
        else:
            # For other objects, add attributes as before
            for key, value in obj.__dict__.items():
                if key not in ['children', 'coord_geom', 'sta_equations', 'profile']:
                    child = QStandardItem(key)
                    value_item = QStandardItem(str(value))
                    item.appendRow([child, value_item])
            
            if hasattr(obj, 'attributes'):
                for key, value in obj.attributes.items():
                    child = QStandardItem(key)
                    value_item = QStandardItem(str(value))
                    item.appendRow([child, value_item])
        
        if hasattr(obj, 'children'):
            for child in obj.children:
                self.add_object_to_tree(child, item)

    
    def add_alignment_to_tree(self, alignment, parent_item):
        # Add Alignment attributes
        for key, value in alignment.attributes.items():
            attr_item = QStandardItem(key)
            value_item = QStandardItem(str(value))
            parent_item.appendRow([attr_item, value_item])
        
        # Add CoordGeom
        if alignment.coord_geom:
            coord_geom_item = QStandardItem("CoordGeom")
            parent_item.appendRow([coord_geom_item, QStandardItem("")])
            for element in alignment.coord_geom:
                element_item = QStandardItem(element['type'])
                coord_geom_item.appendRow([element_item, QStandardItem("")])
                for key, value in element.items():
                    if key != 'type':
                        child = QStandardItem(key)
                        value_item = QStandardItem(str(value))
                        element_item.appendRow([child, value_item])
        
        # Add StaEquations
        if alignment.sta_equations:
            sta_equations_item = QStandardItem("StaEquations")
            parent_item.appendRow([sta_equations_item, QStandardItem("")])
            for equation in alignment.sta_equations:
                equation_item = QStandardItem("Equation")
                sta_equations_item.appendRow([equation_item, QStandardItem("")])
                for key, value in equation.items():
                    child = QStandardItem(key)
                    value_item = QStandardItem(str(value))
                    equation_item.appendRow([child, value_item])
        
        # Add Profile
        if alignment.profile:
            profile_item = QStandardItem("Profile")
            parent_item.appendRow([profile_item, QStandardItem("")])
            for element in alignment.profile['elements']:
                element_item = QStandardItem(element['type'])
                profile_item.appendRow([element_item, QStandardItem("")])
                for key, value in element.items():
                    if key != 'type':
                        child = QStandardItem(key)
                        value_item = QStandardItem(str(value))
                        element_item.appendRow([child, value_item])
        
        # Add ProfSurf if it exists
        if hasattr(alignment, 'profsurf') and alignment.profsurf:
            profsurf_item = QStandardItem("ProfSurf")
            parent_item.appendRow([profsurf_item, QStandardItem("")])
            for surf in alignment.profsurf:
                surf_item = QStandardItem(surf['name'])
                profsurf_item.appendRow([surf_item, QStandardItem("")])
                for key, value in surf.items():
                    if key != 'name' and key != 'points':
                        child = QStandardItem(key)
                        value_item = QStandardItem(str(value))
                        surf_item.appendRow([child, value_item])
                
                # Add points
                points_item = QStandardItem("Points")
                surf_item.appendRow([points_item, QStandardItem("")])
                for point in surf['points']:
                    point_item = QStandardItem(f"Point ({point[0]}, {point[1]})")
                    points_item.appendRow([point_item, QStandardItem("")])

    def add_surface_to_tree(self, surface, parent):
        if surface.source_data:
            source_data_item = QStandardItem("SourceData")
            source_data_item.setEditable(False)
            parent.appendRow([source_data_item])
            self.add_points_to_tree(surface.source_data['points'], source_data_item)

        if surface.definition:
            definition_item = QStandardItem("Definition")
            definition_item.setEditable(False)
            parent.appendRow([definition_item])
            
            # Add surface attributes
            for key, value in surface.definition.items():
                if key not in ['points', 'faces']:
                    attr_item = QStandardItem(f"{key}: {value}")
                    definition_item.appendRow(attr_item)
            
            # Add points
            points_item = QStandardItem("Points")
            definition_item.appendRow(points_item)
            for point in surface.definition['points']:
                point_item = QStandardItem(f"Point {point['id']}")
                points_item.appendRow(point_item)
                for coord, value in [('x', point['x']), ('y', point['y']), ('z', point['z'])]:
                    coord_item = QStandardItem(f"{coord}: {value}")
                    point_item.appendRow(coord_item)
            
            # Add faces
            if 'faces' in surface.definition:
                self.add_faces_to_tree(surface.definition['faces'], definition_item)

        if surface.watersheds:
            watersheds_item = QStandardItem("Watersheds")
            watersheds_item.setEditable(False)
            parent.appendRow([watersheds_item])
            # Add watershed information here if needed

        if surface.features:
            features_item = QStandardItem("Features")
            features_item.setEditable(False)
            parent.appendRow([features_item])
            for feature in surface.features:
                feature_item = QStandardItem(feature.get('name', 'Unnamed Feature'))
                feature_item.setEditable(False)
                features_item.appendRow([feature_item])
                for key, value in feature.items():
                    child = QStandardItem(key)
                    child.setEditable(False)
                    value_item = QStandardItem(str(value))
                    value_item.setEditable(True)
                    feature_item.appendRow([child, value_item])

    def add_points_to_tree(self, points, parent):
        points_item = QStandardItem("Points")
        points_item.setEditable(False)
        parent.appendRow([points_item])
        for i, point in enumerate(points):
            point_item = QStandardItem(f"Point {i+1}")
            point_item.setEditable(False)
            points_item.appendRow([point_item])
            for j, coord in enumerate(['N', 'E', 'Z']):
                coord_item = QStandardItem(coord)
                coord_item.setEditable(False)
                value_item = QStandardItem(str(point[j]))
                value_item.setEditable(True)
                point_item.appendRow([coord_item, value_item])

    def add_faces_to_tree(self, faces, parent):
        faces_item = QStandardItem("Faces")
        faces_item.setEditable(False)
        parent.appendRow([faces_item])
        for i, face in enumerate(faces):
            face_item = QStandardItem(f"Face {i+1}")
            face_item.setEditable(False)
            faces_item.appendRow([face_item])
            for j, point_index in enumerate(face):
                index_item = QStandardItem(f"Point {j+1}")
                index_item.setEditable(False)
                value_item = QStandardItem(str(point_index))
                value_item.setEditable(True)
                face_item.appendRow([index_item, value_item])

    def update_display(self):
        # Update the tree view
        self.tree_model.layoutChanged.emit()
        
        # Replot the objects
        self.plot_objects()

    def update_object_from_model(self, item):
        if item.column() != 1:  # Only process changes in the Value column
            return

        parent_item = item.parent()
        if parent_item is None:
            logging.warning("Invalid parent item when updating object from model")
            return

        obj_id = parent_item.data(Qt.UserRole)
        if obj_id is None:
            logging.warning("Unable to retrieve object ID when updating from model")
            return

        attr_name = self.tree_model.item(item.row(), 0).text()
        new_value = item.text()

        logging.debug(f"Attempting to update {attr_name} to {new_value} for object with ID {obj_id}")

        obj_updated = False
        for obj in self.objects:
            if obj.id == obj_id:
                logging.debug(f"Found matching object: {obj.__class__.__name__} {obj.name}")
                if attr_name in ['north', 'east', 'elevation'] and isinstance(obj, Point):
                    try:
                        old_value = getattr(obj, attr_name)
                        setattr(obj, attr_name, float(new_value))
                        obj_updated = True
                        logging.info(f"Updated {attr_name} of Point {obj.name} from {old_value} to {new_value}")
                    except ValueError:
                        logging.warning(f"Invalid value '{new_value}' for {attr_name} of Point {obj.name}")
                elif hasattr(obj, attr_name):
                    try:
                        old_value = getattr(obj, attr_name)
                        setattr(obj, attr_name, type(old_value)(new_value))
                        obj_updated = True
                        logging.info(f"Updated {attr_name} of {obj.__class__.__name__} {obj.name} from {old_value} to {new_value}")
                    except ValueError:
                        logging.warning(f"Invalid value '{new_value}' for {attr_name} of {obj.__class__.__name__} {obj.name}")
                elif attr_name in obj.attributes:
                    old_value = obj.attributes[attr_name]
                    obj.attributes[attr_name] = new_value
                    obj_updated = True
                    logging.info(f"Updated attribute {attr_name} of {obj.__class__.__name__} {obj.name} from {old_value} to {new_value}")
                else:
                    logging.warning(f"Attribute {attr_name} not found in {obj.__class__.__name__} {obj.name}")
                if obj_updated:
                    self.modified_elements.add(obj)
                break
        
        if not obj_updated:
            logging.warning(f"Object with ID {obj_id} not found or not updated when updating from model")
            logging.debug(f"Available objects: {[(obj.__class__.__name__, obj.name, obj.id) for obj in self.objects]}")

        # Update the display if necessary
        self.update_display()

    def update_object_attribute(self, object_name, attribute_name, new_value):
        obj = next((obj for obj in self.objects if obj.name == object_name), None)
        if obj:
            if hasattr(obj, attribute_name):
                setattr(obj, attribute_name, new_value)
            elif hasattr(obj, 'attributes') and attribute_name in obj.attributes:
                obj.attributes[attribute_name] = new_value
            self.modified_elements.add(obj)

    def update_object_name(self, old_name, new_name):
        obj = next((obj for obj in self.objects if obj.name == old_name), None)
        if obj:
            obj.name = new_name
            self.modified_elements.add(obj)

    def on_pick(self, event):
        if event.artist == self.scatter:
            ind = event.ind[0]
            point = next((obj for obj in self.objects if isinstance(obj, Point) and obj.name == self.names[ind]), None)
            if point:
                self.display_object_info(point)

    def display_object_info(self, item):
        # Clear previous info
        for i in reversed(range(self.object_info_layout.count())): 
            self.object_info_layout.itemAt(i).widget().setParent(None)

        # Add new info
        self.object_info_layout.addRow(QLabel("Element:"), QLabel(item.text()))
        
        obj = item.data(Qt.UserRole)
        if obj:
            if isinstance(obj, PipeNetwork):
                for key, value in obj.attributes.items():
                    self.object_info_layout.addRow(QLabel(key), QLabel(str(value)))
            elif isinstance(obj, Alignment):
                for key, value in obj.__dict__.items():
                    if key not in ['coord_geom', 'sta_equations', 'profile']:
                        self.object_info_layout.addRow(QLabel(key), QLabel(str(value)))
            else:
                for key, value in obj.__dict__.items():
                    if key not in ['children', 'coord_geom', 'sta_equations', 'profile']:
                        self.object_info_layout.addRow(QLabel(key), QLabel(str(value)))
                
                if hasattr(obj, 'attributes'):
                    for key, value in obj.attributes.items():
                        self.object_info_layout.addRow(QLabel(key), QLabel(str(value)))
        else:
            for i in range(item.rowCount()):
                child = item.child(i)
                key = child.text().split(":")[0].strip()
                value = child.text().split(":", 1)[1].strip() if ":" in child.text() else ""
                self.object_info_layout.addRow(QLabel(key), QLabel(value))

        logging.info(f"Object info layout row count: {self.object_info_layout.rowCount()}")

    def export_landxml(self):
        logging.info("Export button clicked")
        file_name, _ = QFileDialog.getSaveFileName(self, "Save LandXML File", "", "LandXML Files (*.xml)")
        if file_name:
            logging.info(f"Selected file: {file_name}")
            try:
                exporter = LandXMLExporter(self.objects, self.modified_elements)
                exporter.export_to_file(file_name)
                self.statusBar.showMessage(f"Exported to {file_name}", 5000)
            except Exception as e:
                logging.error(f"Error exporting file: {str(e)}")
                self.statusBar.showMessage(f"Error exporting file: {str(e)}", 5000)
        else:
            logging.info("No file selected")

    def setup_statusbar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def format_coord(self, x, y):
        return f'North: {y:.3f}, East: {x:.3f}'

    def import_landxml(self):
        logging.info("Import button clicked")
        file_name, _ = QFileDialog.getOpenFileName(self, "Open LandXML File", "", "LandXML Files (*.xml)")
        if file_name:
            logging.info(f"Selected file: {file_name}")
            try:
                self.objects = []
                self.is_new_import = True
                self.objects = self.parser.parse(file_name)
                self.plot_objects()
                self.display_all_objects()
                self.statusBar.showMessage(f"Imported {len(self.objects)} objects from {file_name}", 5000)
            except Exception as e:
                logging.error(f"Error processing file: {str(e)}")
                self.statusBar.showMessage(f"Error importing file: {str(e)}", 5000)
        else:
            logging.info("No file selected")

    def load_objects(self, objects):
        self.objects = objects
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Attributes"])
        
        for obj in self.objects:
            if isinstance(obj, PipeNetwork):
                self.add_pipe_network_to_tree(obj)
            elif isinstance(obj, SurveyData):
                self.add_survey_data_to_tree(obj)
            else:
                self.add_object_to_tree(obj, self.tree_model.invisibleRootItem())
        
        self.tree_view.expandAll()
        self.plot_objects()

    def setup_connections(self):
        self.tree_view.selectionModel().selectionChanged.connect(self.on_tree_item_selected)

    def on_tree_item_selected(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            item = self.tree_model.itemFromIndex(self.proxy_model.mapToSource(indexes[0]))
            self.display_object_info(item)
            logging.info(f"Selected item: {item.text()}")

    def setup_tree_buttons(self):
        # This method is optional if you want to add the buttons to the toolbar instead
        expand_action = QAction(QIcon("icons/expand.png"), "Expand All", self)
        expand_action.triggered.connect(self.expand_all_nodes)
        self.toolbar.addAction(expand_action)

        collapse_action = QAction(QIcon("icons/collapse.png"), "Collapse All", self)
        collapse_action.triggered.connect(self.collapse_all_nodes)
        self.toolbar.addAction(collapse_action)

    def expand_all_nodes(self):
        self.tree_view.expandAll()

    def collapse_all_nodes(self):
        self.tree_view.collapseAll()