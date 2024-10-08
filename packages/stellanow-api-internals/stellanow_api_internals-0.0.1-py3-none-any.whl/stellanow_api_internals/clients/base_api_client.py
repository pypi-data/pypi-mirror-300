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

import json
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import httpx
from loguru import logger

from stellanow_api_internals.auth.keycloak_auth import KeycloakAuth
from stellanow_api_internals.exceptions.api_exceptions import (
    StellaAPIBadRequestError,
    StellaAPIConflictError,
    StellaAPIForbiddenError,
    StellaAPINotFoundError,
    StellaAPIUnauthorisedError,
    StellaAPIWrongCredentialsError,
)

T = TypeVar("T")


class StellanowBaseAPIClient:
    def __init__(
        self, base_url: str, username: str, password: str, organization_id: str, client: Optional[httpx.Client] = None
    ) -> None:
        self.base_url = base_url
        self.username = username
        self.password = password
        self.organization_id = organization_id
        self.auth_token = None
        self.refresh_token = None
        self.client = client or httpx.Client()

        self.keycloak = KeycloakAuth(
            server_url=self._auth_url, client_id="tools-cli", realm_name=self.organization_id, verify=True
        )

        self.authenticate()

    @property
    def _auth_url(self):
        return f"{self.base_url}/auth/"

    def _handle_response(self, response, url, method=None) -> None:
        """
        Handle the API response and raise appropriate exceptions for error status codes.

        :param response: The HTTP response object.
        :param url: The URL that was called.
        :param method: The HTTP method used (optional, for logging purposes).
        """
        try:
            details = response.json().get("details", {})
            if not isinstance(details, dict):
                details = {}
        except json.JSONDecodeError:
            details = {}

        status_code = response.status_code
        error_message = details.get("errorMessage", "No error details provided")
        request_info = f"{method or 'REQUEST'} to {url}"

        if status_code >= HTTPStatus.BAD_REQUEST:
            logger.error(f"API request failed with status {status_code} for {request_info}: {error_message}")

        match status_code:
            case HTTPStatus.BAD_REQUEST:
                raise StellaAPIBadRequestError(f"Bad Request: {error_message}")
            case HTTPStatus.UNAUTHORIZED:
                errors = details.get("errors", [])
                if not isinstance(errors, list):
                    errors = []

                for error in errors:
                    match error.get("errorCode"):
                        case "inactiveAuthToken":
                            self.auth_refresh()
                            return
                        case "wrongUsernameOrPassword":
                            raise StellaAPIWrongCredentialsError()
                        case _:
                            raise StellaAPIUnauthorisedError(f"Unauthorized: {error_message}")
                else:
                    response.raise_for_status()
            case HTTPStatus.FORBIDDEN:
                raise StellaAPIForbiddenError(f"Forbidden: {error_message}")
            case HTTPStatus.NOT_FOUND:
                raise StellaAPINotFoundError(f"Not Found: {error_message}")
            case HTTPStatus.CONFLICT:
                raise StellaAPIConflictError(f"Conflict: {error_message}")
            case _:
                response.raise_for_status()

    def authenticate(self):
        logger.info(f"Authenticating to the {self.__class__.__name__} API ... ")

        if self.refresh_token is not None:
            self.auth_refresh()
        else:
            self.auth_token = None
            self.refresh_token = None

            response = self.keycloak.get_token(self.username, self.password)

            self.auth_token = response.get("access_token")
            self.refresh_token = response.get("refresh_token")

        logger.info("Authentication Successful")

    def auth_refresh(self):
        if self.refresh_token is None:
            self.authenticate()
        else:
            logger.info("API Token Refreshing ...")

            refresh_token = self.refresh_token

            self.auth_token = None
            self.refresh_token = None

            response = self.keycloak.refresh_token(refresh_token)

            self.auth_token = response.get("access_token")
            self.refresh_token = response.get("refresh_token")

            logger.info("API Token Refresh Successful")

    def _make_request(
        self,
        url: str,
        method: str = "GET",
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.client.request(method, url, headers=headers, json=data, params=params)
        self._handle_response(response=response, url=url, method=method)
        return response.json().get("details", {})

    def _get_paginated_results(
        self,
        url_template: str,
        result_class: Type[T],
        page: int = 1,
        page_size: int = 20,
        filter: Optional[str] = None,
        search: Optional[str] = None,
        sorting: Optional[str] = None,
    ) -> List[T]:
        results: List[T] = []
        while True:
            url = url_template

            params = {
                "filter": filter,
                "search": search,
                "sorting": sorting,
                "page": page,
                "pageSize": page_size,
            }
            params = {k: v for k, v in params.items() if v is not None}

            details = self._make_request(url, params=params)

            page_results = details.get("results", [])
            if not page_results:
                break

            results.extend(result_class(**item) for item in page_results)

            page_number = details.get("pageNumber", page)
            number_of_pages = details.get("numberOfPages", 1)

            if page_number >= number_of_pages:
                break

            page += 1

        return results

    def set_project_id(self, project_id: str) -> None:
        self.project_id = project_id

    def _validate_project_id(self) -> None:
        if not self.project_id:
            raise ValueError("Project ID is not set. Please set the project_id before making this request.")

    def _build_url_project_required(self, path: str) -> str:
        """Builds the URL that requires a project ID, using the client-specific base path."""
        self._validate_project_id()
        return f"{self.base_url}{self.base_path}{self.project_id}{path}"

    @property
    def base_path(self) -> str:
        """To be overridden by subclasses to provide the base path for each client."""
        raise NotImplementedError("Subclasses must define 'base_path'.")

    def get(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.get(url, headers=headers, params=params)
        self._handle_response(response=response, url=url, method="GET")
        return response.json()

    def post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.post(url, headers=headers, json=data)
        self._handle_response(response=response, url=url, method="POST")
        return response.json()

    def put(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.put(url, headers=headers, json=data)
        self._handle_response(response=response, url=url, method="PUT")
        return response.json()

    def delete(self, endpoint: str) -> dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = httpx.delete(url, headers=headers)
        self._handle_response(response=response, url=url, method="DELETE")
        return response.json()
