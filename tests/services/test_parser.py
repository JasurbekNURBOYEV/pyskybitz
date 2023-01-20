"""Parser tests."""
import datetime

import pyskybitz.services.parser as under_testing
from tests.sample_data_loader import load_sample_data

QUERY_POSITIONS_SAMPLE_DATA = load_sample_data(
    "query-positions-response.xml", as_bytes=True
)


class TestParser:
    """All-in-one tester for Parser service."""

    def test_parsed_object_should_include_all_vehicles(self):
        """All vehicles/assets should be included in parsed object."""
        sample_data = QUERY_POSITIONS_SAMPLE_DATA
        parsed = under_testing.Parser().parse_string(sample_data, silence=True)

        assert len(parsed.gls) == 10

    def test_order_is_kept_while_parsing(self):
        """Order which was given in the original XML should be kept after parsing."""
        sample_data = QUERY_POSITIONS_SAMPLE_DATA
        parsed = under_testing.Parser().parse_string(sample_data, silence=True)

        # Asset IDs in sample data are stored in incremental order, starting with 1
        for index, gls in enumerate(parsed.gls):
            assert str(index + 1) == gls.asset.assetid.value

    def test_should_parse_time_correctly(self):
        """Time fields should be parsed into datetime, ISO fields should be strings."""
        sample_data = QUERY_POSITIONS_SAMPLE_DATA
        parsed = under_testing.Parser().parse_string(sample_data, silence=True)

        gls = parsed.gls[0]
        assert gls.time == datetime.datetime(2022, 12, 28, 12, 23, 4)
        assert gls.time_iso8601.value == "2022-12-28T12:23:04Z"
        assert gls.messagereceivedtime == datetime.datetime(2022, 12, 28, 12, 24, 51)

    def test_should_parse_locations_correctly(self):
        """Locations should be parsed as strings, ISO versions should follow the standard."""
        sample_data = QUERY_POSITIONS_SAMPLE_DATA
        parsed = under_testing.Parser().parse_string(sample_data, silence=True)

        gls = parsed.gls[0]
        assert gls.longitude.value == "-94.78069"
        assert gls.longitude_iso6709.value == "94°46'50\"W"
        assert gls.latitude.value == "38.92067"
        assert gls.latitude_iso6709.value == "38°55'14\"N"

    def test_should_include_all_fields(self):
        """Parsed object should include all fields given in the original XML."""
        sample_data = QUERY_POSITIONS_SAMPLE_DATA
        parsed = under_testing.Parser().parse_string(sample_data, silence=True)

        fields = [
            "mtsn",
            "asset",
            "messagetype",
            "extpwr",
            "serial",
            "latitude",
            "latitude_iso6709",
            "longitude",
            "longitude_iso6709",
            "speed",
            "heading",
            "headingindegrees",
            "battery",
            "time",
            "time_iso8601",
            "quality",
            "landmark",
            "address",
            "skyfence",
            "idle",
            "epmflag",
            "messagereceivedtime",
            "messagereceivedtime_iso8601",
            "devicetype",
        ]

        gls = parsed.gls[0]
        for field in fields:
            assert getattr(gls, field) is not None
