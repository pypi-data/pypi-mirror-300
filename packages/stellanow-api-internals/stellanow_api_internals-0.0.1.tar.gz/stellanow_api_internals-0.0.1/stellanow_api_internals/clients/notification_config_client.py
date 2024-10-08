"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from typing import List, Optional

import httpx

from stellanow_api_internals.clients.base_api_client import StellanowBaseAPIClient
from stellanow_api_internals.datatypes.notification_config import (
    StellaChannel,
    StellaChannelCreate,
    StellaChannelDetailed,
    StellaDestination,
    StellaDestinationCreate,
    StellaDestinationDetailed,
    StellaNotificationService,
    StellaNotificationServiceDetailed,
    StellaNotificationServiceList,
)

NOTIFICATION_CONFIG_API_BASE = "/notification-config/"
NOTIFICATION_CONFIG_API_PROJECT_CONTEXT = "/notification-config/projects/"


class NotificationConfigClient(StellanowBaseAPIClient):
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        organization_id: str,
        project_id: Optional[str] = None,
        client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(base_url, username, password, organization_id, client)
        self.project_id = project_id

    @property
    def base_path(self) -> str:
        return NOTIFICATION_CONFIG_API_PROJECT_CONTEXT

    @property
    def _services_url(self):
        return f"{self.base_url}{NOTIFICATION_CONFIG_API_BASE}services"

    @property
    def _service_url(self):
        return f"{self.base_url}{NOTIFICATION_CONFIG_API_BASE}services/{{serviceId}}"

    @property
    def _channels_url(self):
        return self._build_url_project_required("/channels")

    @property
    def _channel_url(self):
        return self._build_url_project_required("/channels/{channelId}")

    @property
    def _destinations_url(self):
        return self._build_url_project_required("/channels/{channelId}/destinations")

    @property
    def _destination_url(self):
        return self._build_url_project_required("/channels/{channelId}/destinations/{destinationId}")

    def create_channel(self, channel_data: dict) -> StellaChannelDetailed:
        url = self._channels_url
        channel_data_model = StellaChannelCreate(**channel_data)
        details = self._make_request(url=url, method="POST", data=channel_data_model.model_dump())
        return StellaChannelDetailed(**details)

    def create_destination(self, destination_data: dict, channel_id: str) -> StellaDestination:
        url = self._destinations_url.format(channelId=channel_id)
        destination_data_model = StellaDestinationCreate(**destination_data)
        details = self._make_request(url=url, method="POST", data=destination_data_model.model_dump())
        return StellaDestination(**details)

    def get_services(self) -> StellaNotificationServiceList:
        url = self._services_url
        services_data = self._make_request(url)
        services_list = [StellaNotificationService(**service) for service in services_data]
        return StellaNotificationServiceList(root=services_list)

    def get_service_details(self, service_id: str) -> StellaNotificationServiceDetailed:
        url = self._service_url.format(serviceId=service_id)
        details = self._make_request(url)
        return StellaNotificationServiceDetailed(**details)

    def get_channels(self) -> List[StellaChannel]:
        url = self._channels_url
        channels_list = self._make_request(url)
        return [StellaChannel(**channel) for channel in channels_list.get("channels")]

    def get_channel_details(self, channel_id: str) -> StellaChannelDetailed:
        url = self._channel_url.format(channelId=channel_id)
        details = self._make_request(url)
        return StellaChannelDetailed(**details)

    def get_destinations(self, channel_id: str) -> List[StellaDestination]:
        url = self._destinations_url.format(channelId=channel_id)
        destination_list = self._make_request(url)
        return [StellaDestination(**destination) for destination in destination_list]

    def get_destination_details(self, channel_id: str, destination_id: str) -> StellaDestinationDetailed:
        url = self._destination_url.format(channelId=channel_id, destinationId=destination_id)
        details = self._make_request(url)
        return StellaDestinationDetailed(**details)
