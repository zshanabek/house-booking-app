import {
  GET_HOUSE_SUCCESS,
  GET_HOUSE_ERROR,
  GET_MY_HOUSES_SUCCESS,
  GET_MY_HOUSES_ERROR,
  EDIT_MYHOUSE_SUCCESS,
  EDIT_MYHOUSE_ERROR,
  DELETE_MYHOUSE_SUCCESS,
  DELETE_MYHOUSE_ERROR,
  EDIT_HOUSE_SUCCESS,
  EDIT_HOUSE_ERROR
} from "../actions/house.action";

const initState = {
  houses: {
    results: []
  },
  myHouses: {
    results: []
  }
};

export default function(state = initState, action) {
  let housesList = [...state.houses.results];
  let myHousesList = [...state.myHouses.results];
  switch (action.type) {
    case GET_HOUSE_SUCCESS:
      return {
        ...state,
        houses: action.payload
      };
    case GET_HOUSE_ERROR:
      return {
        ...state,
        error: action.error
      };
    case GET_MY_HOUSES_SUCCESS:
      return { ...state, myHouses: action.payload };
    case GET_MY_HOUSES_ERROR:
      return {
        ...state,
        error: action.error
      };
    case EDIT_MYHOUSE_SUCCESS:
      myHousesList[action.payload.index] = action.payload.house;
      return {
        ...state,
        myHouses: {
          ...state.myHouses,
          results: [...myHousesList]
        }
      };
    case EDIT_MYHOUSE_ERROR:
      return state;

    case DELETE_MYHOUSE_SUCCESS:
      myHousesList.splice(action.payload, 1);
      return {
        ...state,
        myHouses: {
          ...state.myHouses,
          results: [...myHousesList]
        }
      };
    case DELETE_MYHOUSE_ERROR:
      return state;

    case EDIT_HOUSE_SUCCESS:
      housesList[action.payload.index] = action.payload.house;
      return {
        ...state,
        houses: {
          ...state.houses,
          results: [...housesList]
        }
      };
    case EDIT_HOUSE_ERROR:
      return state;
    default:
      return state;
  }
}
