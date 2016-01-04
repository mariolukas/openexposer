import json


class SettingsItem(object):
    TYPE = str

    def __init__(self, name, short, default, description, advanced=False, arg=None):
        self.name = name
        self.short = short
        self.default = default
        self.description = description
        self.advanced = advanced
        self.arg = arg

    def to_dict(self):
        return {
            'name': self.name,
            'short': self.short,
            'default': self.default,
            'description': self.description,
            'advanced': self.advanced}


class RangeSettingFloat(SettingsItem):
    TYPE = float

    def __init__(self, name, short, default, description, low, high, step, advanced=False, arg=None):
        super(RangeSettingFloat, self).__init__(name, short, default, description, advanced, arg)
        self.low = low
        self.high = high
        self.step = step

    def to_dict(self):
        d = super(RangeSettingFloat, self).to_dict()
        d.update({'low': self.low, 'high': self.high, 'step': self.step})
        return d

    @staticmethod
    def convert(val):
        return float(val)


class RangeSettingInt(RangeSettingFloat):
    TYPE = int

    @staticmethod
    def convert(val):
        return int(val)


class BoolSetting(SettingsItem):
    TYPE = bool

    @staticmethod
    def convert(val):
        if isinstance(val, bool):
            return val
        return str(val).upper() in ['TRUE', '1', 'T', 'Y', 'YES']


# All measurements are in mm
def cm(v):
    return v * 10


def um(v):
    return v / 1000.0


DEFAULT_SETTINGS = [
    ('Geometry',
     [
         RangeSettingFloat('scale', 'Scale', 1.0, low=0.1, high=10.0, step=0.1,
                           description='Scaling factor for input geometry', arg='s'),
         RangeSettingFloat('roundOffError', 'Round-off error', um(20), low=um(1), high=um(100), step=um(1),
                           description='Merging area of vertices', advanced=True, arg='roe'),
         # RangeSettingInt('positionMinX', 'Min X', 0, low=0, high=500, step=1,
         # description='Min X position on plate'),
         # RangeSettingInt('positionMinY', 'Min Y', 0, low=0, high=500, step=1, description='Min Y position on plate')
     ]
     ),
    ('Printer',
     [
         RangeSettingInt('printPlateWidth', 'Plate width', 200, low=0, high=500, step=1, description='Plate width',
                         arg='w'),
         RangeSettingInt('printPlateLength', 'Plate length', 200, low=0, high=500, step=1, description='Plate length',
                         arg='l'),
         RangeSettingFloat('nozzleDiameter', 'Nozzle diameter', default=0.35, low=0.1, high=1.0, step=0.01,
                           description='Nozzle diameter', arg='nd'),
         RangeSettingFloat('filamentDiameter', 'Filament diameter', default=3.0, low=0.1, high=5.0, step=0.01,
                           description='Filament diameter', arg='fd'),
         RangeSettingInt('nozzleTemperature', 'Nozzle temperature', default=236, low=0, high=300, step=1,
                         description='Nozzle temperature', arg='nt'),
         RangeSettingInt('bedTemperature', 'Bed temperature', 90, low=0, high=150, step=1,
                         description='Bed temperature', arg='bt'),
         RangeSettingFloat('layerHeight', 'Layer height', 0.30, low=0.1, high=1.0, step=0.01,
                           description='Layer height', arg='lh'),
         RangeSettingFloat('extrusionWidth', 'Exstrusion width', 0.35, low=0.1, high=1.0, step=0.01,
                           description='Extrusion width', arg='ew'),
         RangeSettingFloat('correctionZ', 'Z correction', 0, low=0, high=10, step=0.01, description='Z correction',
                           arg='zc'),
     ]
     ),
    ('Infill',
     [
         # includes contour
         RangeSettingInt('offsetsNr', 'Offsets nr', default=3, low=0, high=10, step=1,
                         description='Number of offsets (including perimeter)', arg='onr'),  # infill
         RangeSettingFloat('offsetsDelta', 'Offsets delta', default=0, low=0, high=1.0, step=0.01,
                           description='Empty space between offsets', arg='odel'),  # infill; + extrusionWidth
         # number of offsets that have to be feasible inside of contour so that line infill is performed
         RangeSettingInt('offsetsMinNrForLines', 'Min nr offsets for lines', default=2, low=1, high=10, step=1,
                         description='Minimum amount of offsets that has to fit into the most inner offset to create a line infill inside it',
                         advanced=True, arg='omnrl'),
         # infill

         BoolSetting('linesEnable', 'Enable line infill', default=True, description='Enable lines inner pattern',
                     arg='eli'),
         # infll
         # extra spacing between tvo extrusion lines
         RangeSettingFloat('linesDelta', 'Lines delta', default=0.2, low=0.0, high=5.0, step=0.1,
                           description='Spacing between lines', arg='ldel'),  # + extrusionWidth # infll
         # When connecting lines of line infill - how long is max acceptable connection (factor * lineInfillSpacing)
         RangeSettingFloat('linesConnectionDistFactor', 'Lines connection distance factor', default=2.0, low=0.0,
                           high=5.0, step=0.1,
                           description='Factor of line spacing between two consecutive lines are connected with extruded filament',
                           arg='lconf'),
         # infll
         # 0 - never rotate, 1 - rotate every layer
         RangeSettingInt('linesNrLayersForRotation', 'Nr layers for lines rotation', default=2, low=0, high=10,
                         step=1,
                         description='How many consecutive layers have the same rotation',
                         arg='lnrr'),
         # infll
         RangeSettingInt('linesRotationTheta', 'Lines rotation degrees', default=30, low=0, high=180, step=1,
                         description='The degree of rotation', arg='lrt'),  # infll
     ]
     ),
    ('Support',
     [
         RangeSettingFloat('skirtsInitialDelta', 'Skirts initial delta', default=7, low=0, high=30, step=0.1,
                           description='Spacing between skirts and AABB of the model', arg='sidel'),
         RangeSettingInt('skirtsOffsetsNr', 'Skirts nr of offsets', default=2, low=0, high=5, step=1,
                         description='Number of skirt offsets', arg='sonr'),
         RangeSettingInt('skirtsLayers', 'Skirts nr layers', default=1, low=0, high=5, step=1,
                         description='How high should skirts be', arg='sly'),
     ]
     ),
    ('G-Code',
     [
         RangeSettingFloat('extrusionMultiplier', 'Exstrusion multiplier', default=1.0, low=0.1, high=2.0,
                           step=0.01,
                           description='By how much should the calculated extruded filament be multiplied', arg='em'),
         RangeSettingInt('speedOffsets', 'Speed offsets', default=1260, low=100, high=10000, step=1,
                         description='Speed of printing offsets', arg='so'),
         RangeSettingInt('speedContours', 'Speed contours', default=1800, low=100, high=10000, step=1,
                         description='Speed of printing contours', arg='sc'),
         RangeSettingInt('speedLines', 'Speed lines', default=3600, low=100, high=10000, step=1,
                         description='Speed of printing lines', arg='sl'),
         RangeSettingInt('speedTravel', 'Speed travel', default=7800, low=100, high=10000, step=1,
                         description='Speed of travel', arg='st'),
         RangeSettingInt('speedSupports', 'Speed supports', default=3600, low=100, high=10000, step=1,
                         description='Speed of printing supports', arg='ss'),
         RangeSettingFloat('speedModifierLayers', 'Speed modifier layers', default=1.0, low=0.01, high=10.0,
                           step=0.1,
                           description='For how many layers should speed modifier be used', arg='sml'),
         RangeSettingFloat('speedModifier', 'Speed modifier', default=0.70, low=0.1, high=1.0, step=0.1,
                           description='Speed modifier', arg='sm'),

         # 0 - no retracts
         RangeSettingFloat('retractLength', 'Retract length', default=0.2, low=0.0, high=5.0, step=0.1,
                           description='Length of retraction', arg='lr'),
         RangeSettingFloat('spitLength', 'Spit length', default=0.01, low=0.0, high=5.0, step=0.1,
                           description='Length of contra retraction', arg='lcr'),

         BoolSetting('retractEachLayer', 'Retract each layer', default=True,
                     description='Should retract on the beggining of each layer', arg='rel'),
         BoolSetting('retractEachPath', 'Retract each path', default=False,
                     description='Should retract for each path', arg='rep'),
         BoolSetting('retractFirstPath', 'Retract first path', default=False,
                     description='Should retract for the first path of pattern', arg='rfp'),
         BoolSetting('verbose', 'Verbose', default=True,
                     description='Add comments to commands', arg='v'),
     ]
     ),
    ('Scanline',
     [
         RangeSettingFloat('scanlineSpacing', 'Scanline distance', default=0.1, low=0.001, high=1, step=0.001,
                           description='Spacing between the individual scanlines', arg='scanline_spacing'),
         RangeSettingInt('exposingCycles', 'Exposing cycles', default=10, low=1, high=100, step=1,
                         description='Number of exposing cycles for each line', arg='scanline_cycles'),
     ]
     )
]


def settings_iter():
    for group in DEFAULT_SETTINGS:
        for prop in group[1]:
            yield group[0], prop


def create_reverse_map():
    d = {}
    for group_key, prop in settings_iter():
        d[prop.name] = group_key
    return d


def create_settings_dict():
    d = {}
    for group_key, prop in settings_iter():
        d.setdefault(group_key, {})
        d[group_key][prop.name] = prop
    return d


DEFAULT_SETTINGS_GROUPS_REVERSE = create_reverse_map()
DEFAULT_SETTINGS_DICT = create_settings_dict()

DEFAULT_SETTINGS_CONFIG = [(group[0], [prop.to_dict() for prop in group[1]]) for group in DEFAULT_SETTINGS]


class SlicerSettings(object):
    def __init__(self, file_name=None, flat_settings_dict=None):
        self._settings = {}

        for group_key, prop in settings_iter():
            self._settings[prop.name] = prop.convert(prop.default)

        if file_name is not None:
            self.load_file(file_name)

        if flat_settings_dict:
            self.from_flat_dict(flat_settings_dict)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if key in DEFAULT_SETTINGS_GROUPS_REVERSE:
            self[key] = value
        else:
            return object.__setattr__(self, key, value)

    def __getitem__(self, item):
        return self._settings[item]

    def __setitem__(self, key, value):
        prop = DEFAULT_SETTINGS_DICT[DEFAULT_SETTINGS_GROUPS_REVERSE[key]][key]
        self._settings[key] = prop.convert(value)

    def load(self, form, form_key_str='{group}[{key}]'):
        for name, group_key in DEFAULT_SETTINGS_GROUPS_REVERSE.items():
            form_key = form_key_str.format(group=group_key, key=name)
            f_val = form.get(form_key)
            if f_val is not None:
                self[name] = f_val

    def to_dict(self):
        d = {}
        for group_key, prop in settings_iter():
            d.setdefault(group_key, {})
            d[group_key].setdefault(prop.name, {})
            d[group_key][prop.name] = self[prop.name]
        return d

    def from_dict(self, d):
        for group_key, group in d.items():
            for prop_name, value in group.items():
                self[prop_name] = value

    def from_flat_dict(self, d):
        self.load(d, '{key}')

    def load_file(self, file_name):
        with open(file_name) as fs:
            d = json.load(fs)

        self.from_dict(d)

    def write_file(self, file_name):
        with open(file_name, mode='w') as fs:
            json.dump(self.to_dict(), fs, indent=4)

    def __repr__(self):
        return self._settings.__repr__()
