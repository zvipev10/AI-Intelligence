import unittest
import json
import threading
from http.server import ThreadingHTTPServer
from urllib.request import urlopen
from urllib.parse import quote, urlencode
from urllib.error import HTTPError
from unittest.mock import patch

from mcp_server.catalog_layers import resolve_layer, validate_filters, filter_rows
from test_catalog_layer_actions import load_module, ROOT


UAV = {'id': 'events:וידאו מכטב"מ', 'label': 'וידאו מכטב"מ', 'kind': 'events'}
CATALOG = [UAV, {'id': 'events:Telegram', 'label': 'Telegram', 'kind': 'events', 'aliases': ['טלגרם']}]


class CatalogRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mcp = load_module('recovery_mcp', ROOT / 'mcp_server/server.py')
        cls.gateway = load_module('recovery_gateway', ROOT / 'server.py')

    def test_incident_hebrew_final_letter_and_quotes(self):
        for name in ['events:וידאו מכטב"ם', 'וידאו מכטב״ם', '  וידאו מכטב"מ  ']:
            self.assertEqual(resolve_layer(name, CATALOG)['layer']['id'], UAV['id'])

    def test_exact_and_explicit_alias(self):
        self.assertEqual(resolve_layer('events:Telegram', CATALOG)['match'], 'exact')
        self.assertEqual(resolve_layer('טלגרם', CATALOG)['layer']['id'], 'events:Telegram')

    def test_typo_and_ambiguity(self):
        self.assertEqual(resolve_layer('Telegrm', CATALOG)['layer']['id'], 'events:Telegram')
        catalog = [{'id': 'events:Video north', 'label': 'Video north'}, {'id': 'events:Video south', 'label': 'Video south'}]
        self.assertEqual(resolve_layer('Video orth', catalog)['status'], 'ambiguous')
        self.assertEqual(resolve_layer('Video outh', catalog)['status'], 'ambiguous')
        duplicates = CATALOG + [{'id': 'events:other', 'label': 'Telegram'}]
        self.assertEqual(resolve_layer('Telegram', duplicates)['status'], 'ambiguous')
        self.assertEqual(resolve_layer('events:Telegram', duplicates)['match'], 'exact')

    def test_unrelated_and_explicit_family_not_guessed(self):
        for value in ['', 'radar stations', 'entities:Telegram']:
            self.assertEqual(resolve_layer(value, CATALOG)['status'], 'not_found')

    def test_tool_returns_canonical_action_and_preserves_scope(self):
        with patch.object(self.mcp, 'load_ui_catalog', return_value=CATALOG):
            result = self.mcp.open_catalog_layers({'catalog_layer_ids': ['events:וידאו מכטב"ם'], 'view': 'evidence',
                'filters': {'location_ids': ['LOC-V2-001', 'LOC-V2-003']}})
        self.assertEqual(result['status'], 'pending_ui')
        self.assertEqual(result['catalog_layer_actions'][0]['catalog_layer_id'], UAV['id'])
        self.assertEqual(result['catalog_layer_actions'][0]['filters']['location_ids'], ['LOC-V2-001', 'LOC-V2-003'])

    def test_unknown_or_unavailable_does_not_queue(self):
        for catalog, expected in [(CATALOG, 'clarification_required'), (OSError('offline'), 'catalog_unavailable')]:
            with patch.object(self.mcp, 'load_ui_catalog', **({'side_effect': catalog} if isinstance(catalog, Exception) else {'return_value': catalog})):
                result = self.mcp.open_catalog_layers({'catalog_layer_ids': ['unknown'], 'view': 'map'})
            self.assertEqual(result['status'], expected)
            self.assertEqual(result['catalog_layer_actions'], [])

    def test_invalid_filters_fail_instead_of_broadening(self):
        for value in [{'location_ids': []}, {'location_ids': 'LOC-1'}, {'other': 'x'}, {'start_time': 'bad'},
                      {'start_time': '2026-09-17', 'end_time': '2026-09-16'}]:
            with self.assertRaises(ValueError):
                validate_filters(value)

    def test_location_entity_time_and_record_intersection(self):
        rows = [{'event_id': str(i), 'location_id': loc, 'entity_id': 'ENT-1', 'timestamp_utc': when}
                for i, loc, when in [(1, 'LOC-1', '2026-09-16T10:00:00Z'), (2, 'LOC-2', '2026-09-16T10:00:00Z'),
                                     (3, 'LOC-1', '2026-09-15T10:00:00Z'), (4, 'LOC-1', '')]]
        filters = {'location_ids': ['LOC-1'], 'entity_ids': ['ENT-1'], 'event_ids': ['1', '2', '3', '4'],
                   'start_time': '2026-09-16T10:00:00Z', 'end_time': '2026-09-16T12:00:00Z'}
        self.assertEqual([r['event_id'] for r in filter_rows(rows, filters)], ['1'])

    def test_tool_gateway_and_http_preserve_scope(self):
        scope = {'location_ids': ['LOC-1', 'LOC-3']}
        rows = [{'event_id': str(i), 'location_id': loc, 'source_type': UAV['label']}
                for i, loc in enumerate(['LOC-1', 'LOC-2', 'LOC-3'])]
        with patch.object(self.mcp, 'load_ui_catalog', return_value=CATALOG), \
             patch.object(self.gateway, 'list_ui_layers', return_value=CATALOG), \
             patch.object(self.gateway, 'ui_layer_data', return_value=(rows, {}, {})):
            action = self.mcp.open_catalog_layers({'catalog_layer_ids': ['events:וידאו מכטב"ם'],
                                                  'view': 'map', 'filters': scope})['catalog_layer_actions']
            accepted, errors = self.gateway.validate_catalog_layer_actions(action, 'he')
            self.assertEqual(errors, [])
            self.assertEqual(accepted[0]['filters'], scope)
            httpd = ThreadingHTTPServer(('127.0.0.1', 0), self.gateway.Handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                url = f'http://127.0.0.1:{httpd.server_port}/api/layers/{quote(UAV["id"], safe="")}/rows?'
                with urlopen(url + urlencode({'filters': json.dumps(scope)})) as response:
                    data = json.load(response)
                self.assertEqual([r['location_id'] for r in data['rows']], ['LOC-1', 'LOC-3'])
                self.assertEqual(data['layer']['catalog_filters'], scope)
                with self.assertRaises(HTTPError) as error:
                    urlopen(url + urlencode({'filters': '{"unsupported": true}'}))
                self.assertEqual(error.exception.code, 400)
            finally:
                httpd.shutdown()
                httpd.server_close()
                thread.join()


if __name__ == '__main__':
    unittest.main()
