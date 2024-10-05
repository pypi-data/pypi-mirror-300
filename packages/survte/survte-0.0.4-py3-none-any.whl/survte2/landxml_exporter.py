import xml.etree.ElementTree as ET
import copy
import logging
from landxml_objects import SurveyData, LandXMLHeader, Point, Alignment

class LandXMLExporter:
    def __init__(self, original_tree, modified_elements):
        self.original_tree = original_tree
        self.modified_elements = modified_elements
        self.root = copy.deepcopy(self.original_tree.getroot())

    def update_modified_elements(self, objects):
        for obj in objects:
            if isinstance(obj, LandXMLHeader):
                self.update_header(obj)
            elif hasattr(obj, 'id') and obj.id in self.modified_elements:
                self.update_element(obj)

    def update_header(self, header):
        # Update root attributes
        for key, value in header.attributes.items():
            self.root.set(key, str(value))

        # Update Units
        units = self.root.find('landxml:Units', namespaces={'landxml': self.root.tag.split('}')[0][1:]})
        if units is not None and header.units:
            imperial = units.find('landxml:Imperial', namespaces={'landxml': self.root.tag.split('}')[0][1:]})
            if imperial is not None:
                for key, value in header.units.items():
                    imperial.set(key, str(value))

        # Update Project
        project = self.root.find('landxml:Project', namespaces={'landxml': self.root.tag.split('}')[0][1:]})
        if project is not None and header.project:
            for key, value in header.project.items():
                project.set(key, str(value))

        # Update Application
        application = self.root.find('landxml:Application', namespaces={'landxml': self.root.tag.split('}')[0][1:]})
        if application is not None and header.application:
            for key, value in header.application.items():
                application.set(key, str(value))

    def update_element(self, obj):
        if isinstance(obj, SurveyData):
            self.update_survey_data(obj)
        elif isinstance(obj, Point):
            self.update_point(obj)
        elif isinstance(obj, Alignment):
            self.update_alignment(obj)
        # ... (add other object types as needed)

    def update_point(self, point):
        point_elem = self.root.find(f".//landxml:CgPoint[@name='{point.name}']", namespaces={'landxml': self.root.tag.split('}')[0][1:]})
        if point_elem is not None:
            point_elem.text = f"{point.east} {point.north} {point.elevation}"
            for key, value in point.attributes.items():
                point_elem.set(key, str(value))

    def update_alignment(self, alignment):
        # Implement alignment update logic
        pass

    def update_survey_data(self, survey_data):
        survey = self.root.find(f".//landxml:Survey[@id='{survey_data.id}']", namespaces={'landxml': self.root.tag.split('}')[0][1:]})
        if survey is not None:
            self.add_attributes(survey, survey_data.attributes)
            
            for child in survey_data.children:
                if child.name == "SurveyHeader":
                    self.add_survey_header(survey, child)
                elif child.name == "InstrumentSetup":
                    self.add_instrument_setup(survey, child)
                # Add other child types as needed

    def add_survey_header(self, parent, header):
        survey_header = ET.SubElement(parent, "SurveyHeader")
        self.add_attributes(survey_header, header.attributes)

    def add_instrument_setup(self, parent, setup):
        instrument_setup = ET.SubElement(parent, "InstrumentSetup")
        self.add_attributes(instrument_setup, setup.attributes)
        
        for child in setup.children:
            if child.name == "InstrumentPoint":
                self.add_instrument_point(instrument_setup, child)
            elif child.name == "ObservationGroup":
                self.add_observation_group(instrument_setup, child)

    def add_instrument_point(self, parent, point):
        instrument_point = ET.SubElement(parent, "InstrumentPoint")
        self.add_attributes(instrument_point, point.attributes)

    def add_observation_group(self, parent, obs_group):
        observation_group = ET.SubElement(parent, "ObservationGroup")
        self.add_attributes(observation_group, obs_group.attributes)
        
        for child in obs_group.children:
            if child.name == "Backsight":
                self.add_backsight(observation_group, child)
            elif child.name == "RawObservation":
                self.add_raw_observation(observation_group, child)

    def add_backsight(self, parent, backsight):
        backsight_elem = ET.SubElement(parent, "Backsight")
        self.add_attributes(backsight_elem, backsight.attributes)
        
        for child in backsight.children:
            if child.name == "BacksightPoint":
                self.add_backsight_point(backsight_elem, child)

    def add_backsight_point(self, parent, point):
        backsight_point = ET.SubElement(parent, "BacksightPoint")
        self.add_attributes(backsight_point, point.attributes)

    def add_raw_observation(self, parent, observation):
        raw_observation = ET.SubElement(parent, "RawObservation")
        self.add_attributes(raw_observation, observation.attributes)
        
        for child in observation.children:
            if child.name == "TargetPoint":
                self.add_target_point(raw_observation, child)

    def add_target_point(self, parent, point):
        target_point = ET.SubElement(parent, "TargetPoint")
        self.add_attributes(target_point, point.attributes)

    def add_attributes(self, element, attributes):
        for key, value in attributes.items():
            element.set(key, str(value))

    def export_to_file(self, filename):
        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        logging.info(f"LandXML file exported to {filename}")
