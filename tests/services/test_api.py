"""Test API client."""
from unittest.mock import MagicMock

import pytest
import requests

import src.services.api as under_testing


@pytest.fixture()
def connection_config():
    """Dummy connection configuration."""
    return under_testing.ConnectionConfig(
        customer="fake-username",
        password="fake-password",
        version="2.74",
        port=1111,
        base_domain="example.com",
    )


@pytest.fixture()
def http_client_session():
    """Mocked version of Session."""
    return MagicMock(spec_set=requests.Session)


@pytest.fixture()
def parser_service():
    """Mocked version of Parser service."""
    return MagicMock(spec_set=under_testing.Parser)


@pytest.fixture()
def api_service(parser_service, http_client_session, connection_config):
    """API service with mocked properties."""
    return under_testing.API(
        parser_service=parser_service,
        http_client_session=http_client_session,
        connection_config=connection_config,
    )


class TestAPI:
    """Tests for API client service."""

    def test_credentials_for_url_should_be_correct(self, api_service):
        """Result returned from _credentials_for_url should be correct."""
        assert api_service._credentials_for_url() == {
            "customer": "fake-username",
            "password": "fake-password",
            "version": "2.74",
        }

    def test_base_url_should_be_correct(self, api_service):
        """Result returned from _credentials_for_url should be correct."""
        assert api_service._base_url() == "https://example.com:1111"

    def test_api_call_url_should_be_correct(self, api_service):
        """Result returned from _credentials_for_url should be correct."""
        api_method_name = "MyCoolMethod"
        assert (
            api_service._api_call_url(api_service._base_url(), api_method_name)
            == f"https://example.com:1111/{api_method_name}"
        )

    def test_prepare_kwargs_for_method_call_should_be_correct(self, api_service):
        """Payload data should be correct when HTTP method changes."""
        payload = {"key": "value"}
        assert api_service._prepare_kwargs_for_method_call(
            under_testing.HTTPMethod.GET, payload
        ) == {"params": payload}
        assert api_service._prepare_kwargs_for_method_call(
            under_testing.HTTPMethod.POST, payload
        ) == {"data": payload}


class TestAPIQueryPositions:
    """Tests for QueryPositions method."""

    def test_http_client_should_be_called_with_correct_values(
        self, api_service, http_client_session
    ):
        """HTTP client should be called with proper values."""
        api_service.query_positions(under_testing.AssetIdPreset.RETURN_ALL_ASSETS)
        http_client_session.request.assert_called_once_with(
            method=under_testing.HTTPMethod.GET,
            url="https://example.com:1111/QueryPositions",
            params={
                "assetid": under_testing.AssetIdPreset.RETURN_ALL_ASSETS,
                "customer": "fake-username",
                "password": "fake-password",
                "version": "2.74",
                "sortby": under_testing.SortingOptions.ASSET_ID_ASCENDING,
            },
        )

    @pytest.mark.parametrize(
        "asset_id, sort_by",
        [
            ("asset-6523", under_testing.SortingOptions.ASSET_ID_ASCENDING),
            ("asset-2365", under_testing.SortingOptions.OBSERVATION_TIME_ASCENDING),
            ("asset-cool", under_testing.SortingOptions.ASSERT_ID_DESCENDING),
            ("asset-crap", under_testing.SortingOptions.OBSERVATION_TIME_DESCENDING),
        ],
    )
    def test_should_carry_arguments_correctly(
        self, api_service, http_client_session, asset_id, sort_by
    ):
        """All arguments passed from API method should be carried correctly to HTTP client."""
        api_service.query_positions(asset_id=asset_id, sort_by=sort_by)
        http_client_session.request.assert_called_once_with(
            method=under_testing.HTTPMethod.GET,
            url="https://example.com:1111/QueryPositions",
            params={
                "assetid": asset_id,
                "customer": "fake-username",
                "password": "fake-password",
                "version": "2.74",
                "sortby": sort_by,
            },
        )
