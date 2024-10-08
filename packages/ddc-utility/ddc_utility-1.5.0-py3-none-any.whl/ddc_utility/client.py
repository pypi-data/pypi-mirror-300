import os
import platform
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from importlib.metadata import version

import pandas as pd
import requests
import s3fs
import xarray as xr
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon

from ddc_utility.auth import OAuth2BearerHandler
from ddc_utility.constants import (DEFAULT_AOI_BUCKET, DEFAULT_DDC_BUCKET,
                                   DEFAULT_DDC_HOST)
from ddc_utility.cube import open_cube
from ddc_utility.errors import (BadRequest, DdcClientError, DdcException,
                                DdcRequestError, Forbidden, HTTPException,
                                NotFound, ServerError, TooManyRequests,
                                Unauthorized)
from ddc_utility.utils import Geometry, IrrigationSchedule, TimeRange
from ddc_utility.logger import log

try:
    package_version = version("ddc-utility")
except Exception:
    package_version = ""


def authorize_request(method):
    def wrapper(self, *args, **kwargs):
        now = round(time.time())
        if self.auth is None or (self.auth.expires_at - now < 60):
            token = self.fetch_token()
            self.auth = OAuth2BearerHandler(
                token.get('access_token'), token.get('expires_at'))

        return method(self, *args, **kwargs)
    return wrapper


def authorize_s3_access(method):
    def wrapper(self, *args, **kwargs):
        now = round(time.time())

        if self.aws_s3 is None or (self.aws_session_exp - now < 60):
            temp_cred = self.fetch_temporary_credentials()
            self.aws_s3 = s3fs.S3FileSystem(
                key=temp_cred["AccessKeyId"],
                secret=temp_cred["SecretKey"],
                token=temp_cred["SessionToken"])
            self.aws_session_exp = temp_cred["expires_at"]

        return method(self, *args, **kwargs)
    return wrapper


class BaseClient:

    def __init__(
            self,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None,
            host: Optional[str] = None,
            wait_on_rate_limit: Optional[bool] = False) -> None:

        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host

        self.wait_on_rate_limit = wait_on_rate_limit

        self.session = requests.Session()
        self.user_agent = (
            f"Python/{platform.python_version()} "
            f"Requests/{requests.__version__} "
            f"ddc_cube/{package_version}"
        )

    def request(self, method: str, route: str, params: Optional[Dict] = None,
                json_data: Optional[Dict] = None, auth: requests.auth.AuthBase = None, content_type: Optional[str] = None, accept: Optional[str] = None):

        headers = {
            "User-Agent": self.user_agent,
            "client_id": self.client_id
        }
        if content_type is not None:
            headers["Content-Type"] = content_type
        if accept is not None:
            headers["Accept"] = accept

        url = self.host + route

        log.debug(
            f"\nMaking API request: {method} {url}\n"
            f"Parameters: {params}\n"
            f"Headers: {headers}\n"
            f"Body: {json_data}"
        )

        with self.session.request(
                method, url, params=params, json=json_data, headers=headers, auth=auth) as response:

            if isinstance(response.content, bytes):
                log.debug(
                    "\nReceived API response: "
                    f"{response.status_code} {response.reason}\n"
                    f"Headers: {response.headers}\n"
                    f"Content: 'bytes content'"
                )

            else:
                log.debug(
                    "\nReceived API response: "
                    f"{response.status_code} {response.reason}\n"
                    f"Headers: {response.headers}\n"
                    f"Content: {response.content}"
                )

            if response.status_code == 400:
                raise BadRequest(response)
            if response.status_code == 401:
                raise Unauthorized(response)
            if response.status_code == 403:
                raise Forbidden(response)
            if response.status_code == 404:
                raise NotFound(response)
            if response.status_code == 429:
                if self.wait_on_rate_limit:
                    reset_time = int(response.headers["x-rate-limit-reset"])
                    sleep_time = reset_time - int(time.time()) + 1
                    if sleep_time > 0:
                        log.warning(
                            "Rate limit exceeded. "
                            f"Sleeping for {sleep_time} seconds."
                        )
                        time.sleep(sleep_time)
                    return self.request(method, route, params, json_data, auth, content_type, accept)
                else:
                    raise TooManyRequests(response)
            if response.status_code >= 500:
                raise ServerError(response)
            if not 200 <= response.status_code < 300:
                raise HTTPException(response)

            return response

    def _make_request(self, method, route, params={},
                      json_data=None, auth=None, content_type=None, accept=None):

        response = self.request(method, route, params=params,
                                json_data=json_data, auth=auth, content_type=content_type, accept=accept)

        # if return_type is dict and accept == "application/json":
        return response.json()
        # else:
        #    return response


class DdcClient(BaseClient):
    """
    Represents a Danube Data Cube client.

    Args:
        client_id (str): Danube Data Cube client id. Defaults to None. If None, it will use DDC_CLIENT_ID env variable.
        client_secret (str): Danube Data Cube client secret. Defaults to None. If None, it will use DDC_CLIENT_SECRET env variable.
        host (Optional[str] ): Alternative Danube Data Cube host url. Defaults to None. If None, it will use DEFAULT_DDC_HOST constant.

    Examples:
        # Create a DDC Client object for interacting with the DDC service
        >>> client = DdcClient(<client_id>, <client_secret>)
    """

    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 host: Optional[str] = None) -> None:

        client_id = client_id or os.environ.get('DDC_CLIENT_ID')
        client_secret = client_secret or os.environ.get('DDC_CLIENT_SECRET')
        host = host or DEFAULT_DDC_HOST

        if not client_id or not client_secret:
            raise DdcException(
                'both `client_id` and `client_secret` must be provided, '
                'consider setting environment variables '
                'DDC_CLIENT_ID and DDC_CLIENT_SECRET.'
            )

        self.auth = None
        self.aws_s3 = None
        self.aws_session_exp = 0
        
        super().__init__(client_id, client_secret, host, False)

    @authorize_request
    def get_all_aoi(self, with_geometry: bool = True, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get user's all area of interests (AOI).

        Args:
            with_geometry (bool, optional): Whether to retrieve geometry values.
                Defaults to True.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as list of dictionaries (2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, List[Dict]]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a list of dictionary containing AOI information.

        Raises:
            DdcRequestError: If an error occurs during the process of requesting AOIs.
        """

        params = {'user_id': self.client_id,
                  'with_geometry': with_geometry}

        route = "/aoi_manager/get_aoi"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting all aoi with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def get_aoi_by_id(self, aoi_id: int, output_data_type: int = 1) -> Union[pd.DataFrame, Dict]:
        """
        Get user's area of interests (AOI) by ID.

        Args:
            aoi_id (int): ID of the AOI.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing AOI information.

        Raises:
            DdcRequestError: If an error occurs during the process of requesting the AOI.
        """

        params = {'user_id': self.client_id,
                  'aoi_id': aoi_id}

        route = "/aoi_manager/get_aoi"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting all aoi with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def create_aoi(self,
                   name: str,
                   geometry: Union[Geometry, Polygon, MultiPolygon, str],
                   time_range: Union[TimeRange, Tuple[pd.Timestamp, pd.Timestamp], Tuple[str, str]],
                   layer_selection_id:  Optional[int] = None,
                   layer_ids: Optional[List[int]] = None,
                   is_dynamic: bool = False,
                   output_data_type: int = 1
                   ) -> Union[pd.DataFrame, Dict]:
        """
        Create an area of interests (AOI).

        Args:
            name (str): The name of the area of interest.
            geometry (Union[Geometry, Polygon, MultiPolygon, str]): The geometry of the area of interest in WGS84 coordinate system.
                This can be provided as a `ddc_utility.Geometry` object, a `shapely.Polygon`, a `shapely.MultiPolygon`, or as a WKT string.
            time_range (Union[TimeRange, Tuple[pd.Timestamp, pd.Timestamp], Tuple[str, str]]):
                The time range for which the area of interest is defined.
                This can be provided as a `ddc_utility.TimeRange` object, a tuple of two `pandas.Timestamp` objects,
                or a tuple of two strings representing dates.
            layer_selection_id (Optional[int]): Layer selection ID. Defaults to None. If both, layer_selection_id and layer_ids are provided, only layer_selection_id will be use.
            layer_ids (Optional[List[int]]): List of layer IDs. Defaults to None. If both, layer_selection_id and layer_ids are provided, only layer_selection_id will be use.
            is_dynamic (bool, optional): Whether the AOI is dynamic (True) or static (False).
                Defaults to False.
            output_data_type (int, optional): Whether to return the result as a pandas.DataFrame (1) or as a dictionary (2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing AOI information.

        Raises:
            DdcRequestError: If an error occurs during the process of creating the AOI.

        """
        if not isinstance(time_range, TimeRange):
            time_range = TimeRange(*time_range)
        time_range_str = time_range.to_string(only_date=True)

        if not isinstance(geometry, Geometry):
            geometry = Geometry(geometry)
        geometry_str = geometry.to_string()

        if layer_ids:
            layer_ids_str = ','.join(str(x) for x in layer_ids)

        json_data = {
            "user_id": self.client_id,
            "name": name,
            "geometry": geometry_str,
            "start_date": time_range_str[0],
            "end_date": time_range_str[1],
            "is_dynamic": is_dynamic
        }

        if layer_selection_id:
            json_data["layer_selection_id"] = layer_selection_id
        else:
            json_data["layer_ids"] = layer_ids_str

        route = "/aoi_manager/create_aoi"
        accept = "application/json"
        content_type = "application/json"

        try:
            response = self._make_request(
                "POST", route, json_data=json_data, auth=self.auth, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during creating aoi with body {json_data} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def get_data_layers(self, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get available data layers.

        Args:
            output_data_type (int, optional): Whether to return the result as a pandas.DataFrame (1) or as a dictionary (2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing data layer information.
        """

        params = {'user_id': self.client_id}

        route = "/aoi_manager/data_layers"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting data layers with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def get_data_selections(self, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get available data selections.

        Args:
            output_data_type (int, optional): Whether to return the result as a pandas.DataFrame (1) or as a dictionary (2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing data selections information.
        """

        params = {'user_id': self.client_id}

        route = "/aoi_manager/data_selections"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting data selections with params {params} from {route}"
            ) from error

        return self._process_response(response['data_selections'], output_data_type)
    
    @authorize_request
    def get_crop_types(self, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get available crop types.

        Args:
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, List[Dict]]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a list of dictionary containing crop type information.

        Raises:
            DdcRequestError: If an error occurs during the process of requesting crop types.
        """

        params = {'user_id': self.client_id}

        route = "/crop/get_type"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting crop types with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def create_crop_type(self,
                         crop_type_name: str,
                         output_data_type: int = 1
                         ) -> Union[pd.DataFrame, Dict]:
        """
        Create crop type.

        Args:
            crop_type_name (str): Name of the crop type.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing crop type information.

        Raises:
            DdcRequestError: If an error occurs during the process of creating the crop type.

        """

        json_data = {
            "user_id": self.client_id,
            "crop_type_name": crop_type_name
        }

        route = "/crop/create_type"
        accept = "application/json"
        content_type = "application/json"

        try:
            response = self._make_request(
                "POST", route, json_data=json_data, auth=self.auth, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during creating crop type with body {json_data} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def get_crop_variety(self, crop_type_id: int, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get available crop varieties.

        Args:
            crop_type_id (int): ID of crop type.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, List[Dict]]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a list of dictionary containing crop variety information.

        Raises:
            DdcRequestError: If an error occurs during the process of requesting crop variety.
        """

        params = {'user_id': self.client_id,
                  'crop_type_id': crop_type_id}

        route = "/crop/get_variety"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting crop variety with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def create_crop_variety(self,
                            crop_type_id: id,
                            crop_variety_name: str,
                            output_data_type: int = 1
                            ) -> Union[pd.DataFrame, Dict]:
        """
        Create crop variety.

        Args:
            crop_type_id (id): ID of crop type.
            crop_variety_name (str): Name of the crop variety.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing crop variety information.

        Raises:
            DdcRequestError: If an error occurs during the process of creating the crop variety.

        """

        json_data = {
            "user_id": self.client_id,
            "crop_type_id": crop_type_id,
            "crop_variety_name": crop_variety_name
        }

        route = "/crop/create_variety"
        accept = "application/json"
        content_type = "application/json"

        try:
            response = self._make_request(
                "POST", route, json_data=json_data, auth=self.auth, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during creating crop variety with body {json_data} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def get_crop_models(self, crop_type_id: int, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get available crop model list.

        Args:
            crop_type_id (int): ID of crop type.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, List[Dict]]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a list of dictionary containing crop model information.

        Raises:
            DdcRequestError: If an error occurs during the process of requesting crop models.
        """

        params = {'user_id': self.client_id,
                  'crop_type_id': crop_type_id}

        route = "/crop/get_model"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting crop models with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def run_crop_model(self,
                       aoi_id: int,
                       time_range: Union[TimeRange, Tuple[pd.Timestamp, pd.Timestamp], Tuple[str, str]],
                       sowing_date: Union[pd.Timestamp, str],
                       irrigation: List[Union[IrrigationSchedule, Tuple[Union[pd.Timestamp, str], float]]],
                       init_water_content: float,
                       growing_season_id: int,
                       crop_model_name: str,
                       seasonal_trajectory: bool,
                       soil_type: str,
                       output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Run crop model.

        Args:
            aoi_id (int): ID of the AOI.
            time_range (Union[TimeRange, Tuple[pd.Timestamp, pd.Timestamp], Tuple[str, str]]): Time range for the simulation.
            sowing_date (Union[pd.Timestamp, str]): Sowing date for the simulation.
            irrigation (List[Union[IrrigationSchedule, Tuple[Union[pd.Timestamp, str], float]]]): Irrigation schedule for the simulation.
            init_water_content (float): Initial water content for the simulation.
            growing_season_id (int): ID of the growing season.
            crop_model_name (str): Name of the crop model.
            seasonal_trajectory (bool): Flag for utilization of CLMS PPI ST in the modelling process
            soil_type (str): USDA soil type definition  
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, List[Dict]]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a list of dictionary containing crop model information.

        Raises:
            DdcRequestError: If an error occurs during the process of running crop model.

        """

        if not isinstance(time_range, TimeRange):
            time_range = TimeRange(*time_range)
        time_range_str = time_range.to_string(only_date=True)

        if not isinstance(sowing_date, pd.Timestamp):
            sowing_date = pd.Timestamp(sowing_date)
        sowing_date_str = sowing_date.isoformat(sep='T').split('T')[0]

        irrigation_str = []
        for irr in irrigation:
            if not isinstance(irr, IrrigationSchedule):
                irr = IrrigationSchedule(*irr)
            irrigation_str.append(irr.to_string(only_date=True))

        params = {
            "user_id": self.client_id,
            "aoi_id": aoi_id,
            "start_date": time_range_str[0],
            "end_date": time_range_str[1],
            "sowing_date": sowing_date_str,
            "irrigation": irrigation_str,
            "init_water_content": init_water_content,
            "growing_season_id": growing_season_id,
            "crop_model_name": crop_model_name,
            "seasonal_trajectory": seasonal_trajectory,
            "soil_type": soil_type
        }

        route = "/crop_model/run"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during running crop modle with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def get_growing_season(self, aoi_id: int, output_data_type: int = 1) -> Union[pd.DataFrame, List[Dict]]:
        """
        Get growing seasons for AOI.

        Args:
            aoi_id (int): ID of the AOI.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, List[Dict]]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a list of dictionary containing growing season information.

        Raises:
            DdcRequestError: If an error occurs during the process of requesting growing seasons.
        """

        params = {'user_id': self.client_id,
                  'aoi_id': aoi_id}

        route = "/growing_season/get_season"
        accept = "application/json"

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during getting growing seasons with params {params} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_request
    def create_growing_season(self,
                              aoi_id: int,
                              time_range: Union[TimeRange, Tuple[pd.Timestamp, pd.Timestamp], Tuple[str, str]],
                              sowing_date: Union[pd.Timestamp, str],
                              crop_type_id: int,
                              crop_variety_id: int,
                              crop_model_id: int,
                              output_data_type: int = 1
                              ) -> Union[pd.DataFrame, Dict]:
        """
        Create growing season for AOI.

        Args:
            aoi_id (int): ID of the AOI.
            time_range (Union[TimeRange, Tuple[pd.Timestamp, pd.Timestamp], Tuple[str, str]]):
                The time range for which the growing season is defined.
                This can be provided as a `ddc_utility.TimeRange` object, a tuple of two `pandas.Timestamp` objects,
                or a tuple of two strings representing dates.
            sowing_date (Union[pd.Timestamp, str]): The date when the crop is sown.
            crop_type_id (int): ID of crop type.
            crop_variety_id (int): ID of crop variety.
            crop_model_id (int): ID of crop model.
            output_data_type (int, optional): Whether to return the result as pandas.DataFrame (1) or as a dictionary(2).
                Defaults to 1.

        Returns:
            Union[pd.DataFrame, Dict]: Depending on the `output_data_type` parameter,
            this function returns either a pandas.DataFrame or a dictionary containing growing season information.

        Raises:
            DdcRequestError: If an error occurs during the process of creating the growing season.

        """

        if not isinstance(time_range, TimeRange):
            time_range = TimeRange(*time_range)
        time_range_str = time_range.to_string(only_date=True)

        if not isinstance(sowing_date, pd.Timestamp):
            sowing_date = pd.Timestamp(sowing_date)
        sowing_date_str = sowing_date.isoformat(sep='T').split('T')[0]

        json_data = {
            "user_id": self.client_id,
            "aoi_id": aoi_id,
            "start_date": time_range_str[0],
            "end_date": time_range_str[1],
            "sowing_date": sowing_date_str,
            "crop_type_id": crop_type_id,
            "crop_variety_id": crop_variety_id,
            "crop_model_id": crop_model_id
        }

        route = "/growing_season/create_season"
        accept = "application/json"
        content_type = "application/json"

        try:
            response = self._make_request(
                "POST", route, json_data=json_data, auth=self.auth, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during creating growing season with body {json_data} from {route}"
            ) from error

        return self._process_response(response, output_data_type)

    @authorize_s3_access
    def open_aoi_cube(self, aoi_id: int, bucket_name: Optional[str] = DEFAULT_AOI_BUCKET) -> xr.Dataset:
        """
        Open AOI cube as an xarray.Dataset.

        Args:
            aoi_id (int): ID of the AOI.
            bucket_name (Optional[str]): Name of the S3 bucket where the zarr cube is stored.
                Defaults to `DEFAULT_AOI_BUCKET`.

        Returns:
            xr.Dataset: AOI cube.

        Raises:
            DdcClientError: If user don't have access to the bucket.
            DdcRequestError: If an error occurs during opening the cube.

        """

        zarr_path = f"s3://{bucket_name}/{aoi_id}_{self.client_id}.zarr"

        try:
            cube = open_cube(path=zarr_path, fs=self.aws_s3)
        except PermissionError as error:
            raise DdcClientError(
                "User don't have access for this operation") from error
        except FileNotFoundError as error:
            raise DdcRequestError(
                f"Invalid aoi_id - no such aoi cube under {zarr_path}") from error
        except Exception as error:
            raise DdcRequestError(
                f"Error during getting AOI cube from {zarr_path}"
            ) from error
        return cube

    @authorize_s3_access
    def open_ddc_cube(self, zarr_path: str, zarr_group: Optional[str] = None, bucket_name: str = DEFAULT_DDC_BUCKET) -> xr.Dataset:
        """
        Open DDC dataset as an xarray.Dataset.

        Args:
            zarr_path (str): Zarr path to the dataset.
            zarr_group (Optional[str]): Zarr group of the dataset.
            bucket_name (Optional[str]): Name of the S3 bucket where the zarr cube is stored.
                Defaults to `DEFAULT_AOI_BUCKET`.

        Returns:
            xr.Dataset: DDC cube.

        Raises:
            DdcClientError: If user don't have access to the bucket.
            DdcRequestError: If an error occurs during opening the cube.

        """

        zarr_path = f"s3://{bucket_name}/{zarr_path}"

        try:
            cube = open_cube(path=zarr_path,
                             fs=self.aws_s3,
                             group=zarr_group)
        except PermissionError as error:
            raise DdcClientError(
                "User don't have access for this operation") from error
        except Exception as error:
            raise DdcRequestError(
                f"Error during getting DDC cube from {zarr_path}"
            ) from error
        return cube

    
    def _process_response(self, data: Any, output_data_type: int = None):
        if output_data_type == 1:
            if isinstance(data, list):
                return pd.DataFrame(data)
            if isinstance(data, dict):
                return pd.DataFrame([data])
            else:
                raise ValueError(
                    f"Can't post-process API response -- {type(data)} is invalid with output_data_type of {output_data_type}")
        else:
            return data

    def fetch_token(self) -> Dict:
        """Fetch token from a remote token endpoint."""

        route = "/get_token"
        accept = "application/json"
        content_type = "application/json"
        json_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        now = time.time()

        try:
            response = self._make_request(
                "POST", route, json_data=json_data, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during fetching token from {route}"
            ) from error

        if "Error" in response:
            raise DdcClientError(
                f"Error during fetching token for user: {response['Error']}")

        if response['token_type'].lower() != 'bearer':
            raise DdcRequestError(
                f"Expected token_type to equal 'bearer',but got {response['token_type']} instead")

        response['expires_at'] = now + int(response.pop('expires_in'))

        return response

    @authorize_request
    def fetch_temporary_credentials(self) -> Dict:
        """Fetch token from a remote token endpoint."""

        route = "/get_temp_cred"
        accept = "application/json"
        params = {'user_id': self.client_id}

        try:
            response = self._make_request(
                "GET", route, params=params, auth=self.auth, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Error during fetching temporary credential from {route}"
            ) from error

        response = response["Credentials"]

        response["expires_at"] = int(time.mktime(time.strptime(
            response.pop("Expiration"), "%Y-%m-%dT%H:%M:%SZ")))

        return response
