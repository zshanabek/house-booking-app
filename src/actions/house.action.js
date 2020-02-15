import { houses, myHouses } from "../services/house";

export const GET_HOUSE_SUCCESS = "GET_HOUSE_MAIN_SUCCESS";
export const GET_HOUSE_ERROR = "GET_HOUSE_MAIN_ERROR";
export const GET_MY_HOUSES_SUCCESS = "GET_MY_HOUSES_SUCCESS";
export const GET_MY_HOUSES_ERROR = "GET_MY_HOUSES_ERROR";
export const EDIT_MYHOUSE_SUCCESS = "EDIT_MYHOUSE_SUCCESS";
export const EDIT_MYHOUSE_ERROR = "EDIT_MYHOUSE_ERROR";
export const DELETE_MYHOUSE_SUCCESS = "DELETE_MYHOUSE_SUCCESS";
export const DELETE_MYHOUSE_ERROR = "DELETE_MYHOUSE_ERROR";

export const EDIT_HOUSE_SUCCESS = "EDIT_HOUSE_SUCCESS";
export const EDIT_HOUSE_ERROR = "EDIT_HOUSE_ERROR";

export const getHouses = params => {
  return dispatch => {
    houses(params)
      .then(data => {
        dispatch({
          type: GET_HOUSE_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_HOUSE_ERROR,
          error
        });
      });
  };
};

export const getMyHouses = () => {
  return dispatch => {
    myHouses()
      .then(data => {
        dispatch({
          type: GET_MY_HOUSES_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_MY_HOUSES_ERROR,
          error
        });
      });
  };
};

export const editActivation = (index, house, isError) => {
  return dispatch => {
    if (!isError) {
      dispatch({
        type: EDIT_MYHOUSE_SUCCESS,
        payload: {
          index,
          house
        }
      });
    } else {
      dispatch({
        type: EDIT_MYHOUSE_ERROR
      });
    }
  };
};

export const deleteMyHouse = (index, isError) => {
  return dispatch => {
    if (!isError) {
      dispatch({
        type: DELETE_MYHOUSE_SUCCESS,
        payload: index
      });
    } else {
      dispatch({
        type: DELETE_MYHOUSE_ERROR
      });
    }
  };
};

export const editFavourite = (index, isError, house = null) => {
  return dispatch => {
    if (!isError) {
      dispatch({
        type: EDIT_HOUSE_SUCCESS,
        payload: {
          index,
          house
        }
      });
    } else {
      dispatch({
        type: EDIT_HOUSE_ERROR
      });
    }
  };
};
