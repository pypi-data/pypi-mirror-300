import pytest
from aioresponses import aioresponses

from appartme_paas import AppartmePaasClient, DeviceOfflineError, ApiError


@pytest.mark.asyncio
async def test_fetch_devices():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)

    # Sample response for fetch_devices
    devices_response = [
        {
            "deviceId": "26575d16-92fc-476e-8fe0-b53ddfc5ace6",
            "name": "MM",
            "spaceId": "2b1b2df6-5122-4d5f-9bb8-d44694bb377a",
            "type": "mm"
        }
    ]

    with aioresponses() as mocked:
        mocked.get(
            f"{client.base_url}/devices",
            payload=devices_response,
            status=200,
        )

        devices = await client.fetch_devices()
        assert devices == devices_response

    await client.close()


@pytest.mark.asyncio
async def test_fetch_device_details():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)
    device_id = "26575d16-92fc-476e-8fe0-b53ddfc5ace6"

    # Sample response for fetch_device_details
    device_details_response = {
        "deviceId": device_id,
        "spaceId": "2b1b2df6-5122-4d5f-9bb8-d44694bb377a",
        "name": "MM",
        "type": "mm",
        "properties": [
            {
                "propertyId": "water",
                "type": "boolean",
                "mode": "readwrite"
            },
        ]
    }

    with aioresponses() as mocked:
        mocked.get(
            f"{client.base_url}/devices/{device_id}",
            payload=device_details_response,
            status=200,
        )

        device_details = await client.fetch_device_details(device_id)
        assert device_details == device_details_response

    await client.close()


@pytest.mark.asyncio
async def test_get_device_property_value():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)
    device_id = "26575d16-92fc-476e-8fe0-b53ddfc5ace6"
    property_id = "water"

    # Sample response for get_device_property_value
    property_value_response = {
        "propertyId": "water",
        "type": "boolean",
        "mode": "readwrite",
        "value": False
    }

    with aioresponses() as mocked:
        mocked.get(
            f"{client.base_url}/devices/{device_id}/property/{property_id}/value",
            payload=property_value_response,
            status=200,
        )

        property_value = await client.get_device_property_value(device_id, property_id)
        assert property_value == property_value_response

    await client.close()


@pytest.mark.asyncio
async def test_get_device_properties():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)
    device_id = "26575d16-92fc-476e-8fe0-b53ddfc5ace6"

    # Sample response for get_device_properties
    device_properties_response = {
        "values": [
            {
                "value": 0,
                "propertyId": "phase_1_current",
                "type": "number",
                "mode": "read"
            },
        ]
    }

    with aioresponses() as mocked:
        mocked.get(
            f"{client.base_url}/devices/{device_id}/property",
            payload=device_properties_response,
            status=200,
        )

        properties = await client.get_device_properties(device_id)
        assert properties == device_properties_response

    await client.close()


@pytest.mark.asyncio
async def test_set_device_property_value():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)
    device_id = "26575d16-92fc-476e-8fe0-b53ddfc5ace6"
    property_id = "water"
    value_to_set = True

    # Sample response for set_device_property_value
    set_property_response = {
        "propertyId": property_id,
        "type": "boolean",
        "mode": "readwrite",
        "value": value_to_set
    }

    with aioresponses() as mocked:
        mocked.patch(
            f"{client.base_url}/devices/{device_id}/property/{property_id}/value",
            payload=set_property_response,
            status=200,
        )

        result = await client.set_device_property_value(device_id, property_id, value_to_set)
        assert result == set_property_response

    await client.close()


@pytest.mark.asyncio
async def test_device_offline_error():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)
    device_id = "offline_device_id"
    property_id = "water"

    with aioresponses() as mocked:
        mocked.get(
            f"{client.base_url}/devices/{device_id}/property/{property_id}/value",
            status=504,  # Device offline
        )

        with pytest.raises(DeviceOfflineError):
            await client.get_device_property_value(device_id, property_id)

    await client.close()


@pytest.mark.asyncio
async def test_api_error():
    access_token = "test_access_token"
    client = AppartmePaasClient(access_token)
    device_id = "invalid_device_id"
    property_id = "water"

    with aioresponses() as mocked:
        mocked.get(
            f"{client.base_url}/devices/{device_id}/property/{property_id}/value",
            status=404,
            body='{"error": "Device not found"}',
        )

        with pytest.raises(ApiError):
            await client.get_device_property_value(device_id, property_id)

    await client.close()
