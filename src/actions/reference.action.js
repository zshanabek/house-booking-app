import {
  cities,
  regions,
  countries,
  nearBuildings,
  accommodations,
  houseTypes,
  rules
} from "../services/reference";

export const GET_CITY_SUCCESS = "GET_CITY_SUCCESS";
export const GET_CITY_ERROR = "GET_CITY_ERROR";
export const GET_REGION_SUCCESS = "GET_REGION_SUCCESS";
export const GET_REGION_ERROR = "GET_REGION_ERROR";
export const GET_COUNTRY_SUCCESS = "GET_COUNTRY_SUCCESS";
export const GET_COUNTRY_ERROR = "GET_COUNTRY_ERROR";
export const GET_NEAR_BUILDINGS_SUCCESS = "GET_NEAR_BUILDINGS_SUCCESS";
export const GET_NEAR_BUILDINGS_ERROR = "GET_NEAR_BUILDINGS_ERROR";
export const GET_HOUSE_TYPES_SUCCESS = "GET_HOUSE_TYPES_SUCCESS";
export const GET_HOUSE_TYPES_ERROR = "GET_HOUSE_TYPES_ERROR";
export const GET_ACCOMMODATIONS_SUCCESS = "GET_ACCOMMODATIONS_SUCCESS";
export const GET_ACCOMMODATIONS_ERROR = "GET_ACCOMMODATIONS_ERROR";
export const GET_RULES_SUCCESS = "GET_RULES_SUCCESS";
export const GET_RULES_ERROR = "GET_RULES_ERROR";

export const getCities = () => {
  return dispatch => {
    cities()
      .then(data => {
        dispatch({
          type: GET_CITY_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_CITY_ERROR,
          payload: error
        });
      });
  };
};
export const getRegions = () => {
  return dispatch => {
    regions()
      .then(data => {
        dispatch({
          type: GET_REGION_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_REGION_ERROR,
          payload: error
        });
      });
  };
};
export const getCountries = () => {
  return dispatch => {
    countries()
      .then(data => {
        dispatch({
          type: GET_COUNTRY_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_COUNTRY_ERROR,
          payload: error
        });
      });
  };
};
export const getNearBuildings = () => {
  return dispatch => {
    nearBuildings()
      .then(data => {
        dispatch({
          type: GET_NEAR_BUILDINGS_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_NEAR_BUILDINGS_ERROR,
          payload: error
        });
      });
  };
};
export const getHouseTypes = () => {
  return dispatch => {
    houseTypes()
      .then(data => {
        dispatch({
          type: GET_HOUSE_TYPES_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_HOUSE_TYPES_ERROR,
          payload: error
        });
      });
  };
};
export const getAccommodations = () => {
  return dispatch => {
    accommodations()
      .then(data => {
        dispatch({
          type: GET_ACCOMMODATIONS_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_ACCOMMODATIONS_ERROR,
          payload: error
        });
      });
  };
};
export const getRules = () => {
  return dispatch => {
    rules()
      .then(data => {
        dispatch({
          type: GET_RULES_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_RULES_ERROR,
          payload: error
        });
      });
  };
};
