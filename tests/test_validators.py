import unittest
from pyramid import testing
from geozoekdiensten.validators import validate_afbakeningen_param_values, ValidationError, validate_categorie, \
    validate_buffer, validate_geometrie, validate_geometrie_buffer, validate_type, \
    validate_admingrenzen_param_values, validate_geef_geometrie


class ValidateParamsTests(unittest.TestCase):
    def setUp(self):
        self.admingrenzen_types = {
            'gemeente': 'au:au_gemt_vlaa',
            'provincie': 'au:au_prov_vlaa',
            'arrondissement': 'au:au_arron_vlaa',
            'gewest': 'au:au_gew_vlaa'
        }

    def test_validate_type(self):
        errors = []
        validate_type(['gewest', 'arrondissement', 'provincie', 'gemeente'], errors)
        self.assertEqual(len(errors), 0)

    def test_validate_type_invalid(self):
        errors = []
        validate_type(['deelgemeente'], errors)
        self.assertEqual(len(errors), 1)

    def test_validate_geef_geometrie(self):
        errors = []
        validate_geef_geometrie(0, errors)
        self.assertEqual(len(errors), 0)

    def test_validate_geef_geometrie_invalid(self):
        errors = []
        validate_geef_geometrie('test', errors)
        self.assertEqual(len(errors), 1)

    def test_validate_categorie_invalid(self):
        errors = []
        validate_categorie("ongeldige categorie", errors)
        self.assertEquals(errors.__len__(), 1)

    def test_validate_categorie_objecten(self):
        errors = []
        validate_categorie("objecten", errors)
        self.assertEquals(errors.__len__(), 1)

    def test_validate_categorie_erfgoedobjecten(self):
        errors = []
        validate_categorie("erfgoedobjecten", errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_categorie_plannen(self):
        errors = []
        validate_categorie("plannen", errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_categorie_dossiers(self):
        errors = []
        validate_categorie("dossiers", errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_categorie_meerdere(self):
        errors = []
        validate_categorie(["dossiers", "plannen"], errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_categorie_meerdere_fail(self):
        errors = []
        validate_categorie(["dossiers", "test"], errors)
        self.assertEquals(errors.__len__(), 1)

    def test_validate_buffer_valid(self):
        errors = []
        validate_buffer("1", errors)
        validate_buffer("4999", errors)
        validate_buffer("999.9", errors)
        validate_buffer(4999, errors)
        validate_buffer(9.999, errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_buffer_invalid(self):
        errors = []
        validate_buffer("-1", errors)
        validate_buffer("twee", errors)
        validate_buffer(-1, errors)
        validate_buffer(10001, errors)
        validate_buffer("999,9", errors)
        self.assertEquals(errors.__len__(), 5)

    def test_validate_geometrie_valid(self):
        errors = []
        geometrie = {
            "type": "Point",
            "coordinates": [209289.18, 173495.99],
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::31370"
                }
            }
        }
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_geometrie_valid_wgs(self):
        errors = []
        geometrie = {
            "type": "Point",
            "coordinates": [4.7, 50.8]
        }
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 0)

    def test_none_geometrie(self):
        errors = []
        geometrie = None
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 1)

    def test_validate_geometrie_invalid(self):
        errors = []
        geometrie = {
            "type": "InvalidType",
            "coordinates": [10, 20]}
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 1)

    def test_wrong_epsg_geometrie(self):
        errors = []
        geometrie = {
            "type": "MultiPolygon",
            "coordinates": [[[[136331.78223835284, 186530.2666452732], [130146.82902782407, 188039.69512006454],
                              [138258.6594426263, 194548.5469229715], [136331.78223835284, 186530.2666452732]]],
                            [[[132476.42226441827, 192836.11502214056], [141056.8954990197, 189456.52098675352],
                              [134714.03518756485, 195426.7922792174], [132476.42226441827, 192836.11502214056]]]],
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}}
        }

        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 1)

    def test_cleaned_selfintersecting_geometrie(self):
        errors = []
        geometrie = \
            {
                "type": "MultiPolygon",
                "coordinates": [[[[95026.54173062785, 193574.22826667782], [94977.46393065073, 193696.72356663365],
                                  [94949.89243065918, 193666.64306663908], [94920.37773066101, 193634.4423666466],
                                  [94889.90983066578, 193604.45536665153], [94891.43083067038, 193602.3383666519],
                                  [94891.5638306641, 193600.5523666516], [94890.37293066607, 193598.10536665097],
                                  [94880.74053066899, 193587.204466654], [94876.92453067003, 193582.88566665817],
                                  [94889.57673066334, 193569.9624666609], [94896.7246306607, 193562.66156666353],
                                  [94952.89093063647, 193505.29236668907], [95026.54173062785, 193574.22826667782]]], [
                                    [[94977.46393065073, 193696.72356663365], [94976.5141306516, 193699.137666638],
                                     [94894.66573070301, 193907.17046656925], [94892.79903070269, 193908.48286656756],
                                     [94891.70473070099, 193907.6128665628], [94889.90373070227, 193906.18126656674],
                                     [94884.19573070624, 193899.30426656734], [94876.85673070545, 193887.349266571],
                                     [94849.13773070321, 193836.42726658192], [94949.89243065918, 193666.64306663908],
                                     [94977.46393065073, 193696.72356663365]]]],
                "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::31370"}}
            }
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 0)

    def test_geometrie_multipolygon(self):
        errors = []
        geometrie = \
            {
                "type": "MultiPolygon",
                "coordinates": [[[[103827.44321801752, 192484.5100535322], [103826.65621839411, 192565.57026445214],
                                  [103839.2000972359, 192622.4958831761], [103877.27257229008, 192673.1911981115],
                                  [103981.90807816133, 192592.71585010737], [104050.62835409257, 192535.07265175506],
                                  [104119.78606355426, 192526.95860514138], [104157.5529127745, 192543.1371434061],
                                  [104163.33481632298, 192516.068607972], [104043.86794770884, 192451.07658289373],
                                  [103839.39232099024, 192304.2814310426], [103825.49962980268, 192434.99411542248],
                                  [103827.44321801752, 192484.5100535322]]]],
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": "urn:ogc:def:crs:EPSG::31370"}}}
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 0)

    def test_validate_geometrie_outside_flanders(self):
        errors = []
        geometrie = {
            "type": "Point",
            "coordinates": [2.7, 50.3]}
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 1)

    def test_validate_geometrie_buffer_out_of_range(self):
        errors = []
        geometrie_buffer = {
            "type": "Polygon",
            "coordinates": [[[209289.18, 173495.99], [209289.18, 186116.7], [223498.88, 186116.7],
                             [223498.88, 173495.99], [209289.18, 173495.99]]],
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::31370"
                }
            }
        }
        validate_geometrie_buffer(geometrie_buffer, errors)
        self.assertEquals(errors.__len__(), 1)

    def test_validate_geometrycollection(self):
        errors = []
        geometrie = {"type": "GeometryCollection",
                     "geometries": [
                         {"type": "Point",
                          "coordinates": [100.0, 0.0]
                          },
                         {"type": "LineString",
                          "coordinates": [[101.0, 0.0], [102.0, 1.0]]
                          }
                     ]
                     }
        validate_geometrie(geometrie, errors)
        self.assertEquals(errors.__len__(), 1)

    def test_search_error_test2(self):
        from geozoekdiensten.validators import ValidationError

        errors = []
        errors.append({'info': 'error info', 'detail': 'error detail'})
        validation_error = ValidationError('error value', errors)
        self.assertEqual(validation_error.__str__(), repr('error value'))
        self.assertEqual(validation_error.__json__(testing.DummyRequest()),
                         {'value': 'error value', 'errors': ['error info']})

    def test_validate_params_no_geometrie(self):
        params = {}
        self.assertRaises(ValidationError, validate_afbakeningen_param_values, params)
        self.assertRaises(ValidationError, validate_admingrenzen_param_values, params, self.admingrenzen_types)

    def test_validate_admingrenzen(self):
        params = {'type': 'gemeente'}
        self.assertRaises(ValidationError, validate_admingrenzen_param_values, params, self.admingrenzen_types)
        params = {
            'type': 'gemeente',
            'buffer': 1,
            'geometrie': {
                "type": "Point",
                "coordinates": [4.7, 50.8]
            }
        }
        searchparams = validate_admingrenzen_param_values(params, self.admingrenzen_types)
        self.assertIn('type', searchparams)
        self.assertIn('buffer', searchparams)
        self.assertIn('geef_geometrie', searchparams)
        self.assertIn('geometrie', searchparams)
        params = {
            'buffer': 1,
            'geometrie': {
                "type": "Point",
                "coordinates": [4.7, 50.8]
            }
        }
        searchparams = validate_admingrenzen_param_values(params, self.admingrenzen_types)
        self.assertIn('type', searchparams)
        self.assertIn('buffer', searchparams)
        self.assertIn('geometrie_buffer', searchparams)
        self.assertIn('geef_geometrie', searchparams)
        self.assertIn('geometrie', searchparams)
        params = {
            'geef_geometrie': 0,
            'geometrie': {
                "type": "MultiPolygon",
                "coordinates": [[[[103827.44321801752, 192484.5100535322], [103826.65621839411, 192565.57026445214],
                                  [103839.2000972359, 192622.4958831761], [103877.27257229008, 192673.1911981115],
                                  [103981.90807816133, 192592.71585010737], [104050.62835409257, 192535.07265175506],
                                  [104119.78606355426, 192526.95860514138], [104157.5529127745, 192543.1371434061],
                                  [104163.33481632298, 192516.068607972], [104043.86794770884, 192451.07658289373],
                                  [103839.39232099024, 192304.2814310426], [103825.49962980268, 192434.99411542248],
                                  [103827.44321801752, 192484.5100535322]]]],
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": "urn:ogc:def:crs:EPSG::31370"}}}
        }
        searchparams = validate_admingrenzen_param_values(params, self.admingrenzen_types)
        self.assertIn('type', searchparams)
        self.assertIn('buffer', searchparams)
        self.assertIn('geometrie_buffer', searchparams)
        self.assertIn('geef_geometrie', searchparams)
        self.assertIn('geometrie', searchparams)
