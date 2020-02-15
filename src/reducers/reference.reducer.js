import {
  GET_CITY_SUCCESS,
  GET_CITY_ERROR,
  GET_REGION_SUCCESS,
  GET_REGION_ERROR,
  GET_COUNTRY_SUCCESS,
  GET_COUNTRY_ERROR,
  GET_ACCOMMODATIONS_SUCCESS,
  GET_ACCOMMODATIONS_ERROR,
  GET_HOUSE_TYPES_SUCCESS,
  GET_HOUSE_TYPES_ERROR,
  GET_NEAR_BUILDINGS_SUCCESS,
  GET_NEAR_BUILDINGS_ERROR,
  GET_RULES_SUCCESS,
  GET_RULES_ERROR
} from "../actions/reference.action";

const initState = {};

export default function(state = initState, action) {
  switch (action.type) {
    case GET_CITY_SUCCESS:
      return {
        ...state,
        cities: action.payload
      };
    case GET_CITY_ERROR:
      return {
        state
      };
    case GET_REGION_SUCCESS:
      return {
        ...state,
        regions: action.payload
      };
    case GET_REGION_ERROR:
      return {
        state
      };
    case GET_COUNTRY_SUCCESS:
      return {
        ...state,
        countries: action.payload
      };
    case GET_COUNTRY_ERROR:
      return {
        state
      };
    case GET_ACCOMMODATIONS_SUCCESS:
      return {
        ...state,
        accommodations: action.payload
      };
    case GET_ACCOMMODATIONS_ERROR:
      return {
        state
      };
    case GET_HOUSE_TYPES_SUCCESS:
      return {
        ...state,
        houseTypes: action.payload
      };
    case GET_HOUSE_TYPES_ERROR:
      return {
        state
      };
    case GET_NEAR_BUILDINGS_SUCCESS:
      return {
        ...state,
        nearBuildings: action.payload
      };
    case GET_NEAR_BUILDINGS_ERROR:
      return {
        state
      };
    case GET_RULES_SUCCESS:
      return {
        ...state,
        rules: action.payload
      };
    case GET_RULES_ERROR:
      return {
        state
      };

    default:
      return state;
  }
}
