from typing import List, Dict, Any, Optional
import uuid

class LandXMLObject:
    def __init__(self, name: str, attributes: Dict[str, Any]):
        self.id = str(uuid.uuid4())  # Generate a unique ID for each object
        self.name = name
        self.attributes = attributes

class LandXMLHeader(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], project='Unknown Project', application='Unknown Application'):
        super().__init__(name='Header', attributes=attributes)
        self.project = project
        self.application = application
        self.units: List[Dict[str, Any]] = []

class Units(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)

class Point(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], north: float, east: float, elevation: float):
        # Remove 'name', 'north', 'east', and 'elevation' from attributes if they exist
        attributes = {k: v for k, v in attributes.items() if k not in ['name', 'north', 'east', 'elevation']}
        super().__init__(name, attributes)
        self.north = float(north)
        self.east = float(east)
        self.elevation = float(elevation)

class Alignment(LandXMLObject):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)
        self.coord_geom = []
        self.sta_equations = []
        self.profile = None

class Profile(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.elements: List[Any] = []

class ProfAlign(LandXMLObject):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)
        self.elements = []

class ProfSurf(LandXMLObject):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)
        self.points = []

class PVI(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.station = attributes.get('station')
        self.elevation = attributes.get('elevation')

class CircCurve(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.length = attributes.get('length')
        self.radius = attributes.get('radius')
        self.station = attributes.get('station')
        self.elevation = attributes.get('elevation')

class Ptlist2d(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.elements: List[Any] = []

class CoordGeom(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.elements: List[Any] = []

class Line(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], start: Point, end: Point):
        super().__init__(name, attributes)
        self.start = start
        self.end = end

class Curve(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], start: Point, center: Point, end: Point):
        super().__init__(name, attributes)
        self.start = start
        self.center = center
        self.end = end

class Spiral(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], start: Point, pi: Point, end: Point):
        super().__init__(name, attributes)
        self.start = start
        self.pi = pi
        self.end = end

class Surface(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], definition: Dict[str, Any]):
        super().__init__(name, attributes)
        self.definition = definition
        self.features: List[Dict[str, Any]] = []

class SurveyData(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.header: Dict[str, Any] = {}
        self.equipment: List[Dict[str, Any]] = []
        self.cg_points: List[Dict[str, Any]] = []
        self.instrument_setups: List[Dict[str, Any]] = []
        self.observation_groups: List[ObservationGroup] = []

class Backsight(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.circle = attributes.get('circle')
        self.setupID = attributes.get('setupID')
        self.point: Optional[Dict[str, Any]] = None

class RawObservation:
    def __init__(self, targetHeight: str, slopeDistance: str, zenithAngle: str, azimuth: str, horizAngle: str, directFace: str):
        self.targetHeight = targetHeight
        self.slopeDistance = slopeDistance
        self.zenithAngle = zenithAngle
        self.azimuth = azimuth
        self.horizAngle = horizAngle
        self.directFace = directFace
        self.targetPoint: Optional[TargetPoint] = None

class TargetPoint:
    def __init__(self, description: str, pointReference: str):
        self.description = description
        self.pointReference = pointReference
        self.coordinates: Optional[List[float]] = None

class InstrumentSetup(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.instrument_points = str

class ObservationGroup(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.backsight: Optional[Backsight] = None
        self.observations: List[RawObservation] = []

    def add_backsight(self, backsight: Backsight):
        self.backsight = backsight

    def add_observation(self, observation: RawObservation):
        self.observations.append(observation)

class PipeNetworks(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.pipe_networks: List[PipeNetwork] = []
        self.features: List[Feature] = []

class Feature(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)

class PipeNetwork(LandXMLObject):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)
        self.pipes = []
        self.structs = []

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def add_struct(self, struct):
        self.structs.append(struct)

class Pipe(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.refEnd: str = attributes.get('refEnd')
        self.refStart: str = attributes.get('refStart')
        self.length: float = attributes.get('length')
        self.slope: float = attributes.get('slope')

class Pipes(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], pipes: List[Pipe] = None):
        super().__init__(name, attributes)
        self.pipes = pipes or []

class CircPipe(Pipe):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.diameter: float = attributes.get('diameter')
        self.thickness: float = attributes.get('thickness')

class Struct(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any]):
        super().__init__(name, attributes)
        self.desc: str = attributes.get('desc')
        self.center: str = attributes.get('center')
        self.diameter: float = attributes.get('diameter')
        self.thickness: float = attributes.get('thickness')
        self.inverts: List[Dict[str, Any]] = attributes.get('inverts', [])

class Structs(LandXMLObject):
    def __init__(self, name: str, attributes: Dict[str, Any], structs: List[Struct] = None):
        super().__init__(name, attributes)
        self.structs = structs or []