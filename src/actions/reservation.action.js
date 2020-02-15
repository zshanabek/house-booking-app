import {
  getReservations as reservations,
  getOrders as orders
} from "../services/reservations";

export const GET_RESERVATIONS_SUCCESS = "GET_RESERVATIONS_SUCCESS";
export const GET_RESERVATIONS_ERROR = "GET_RESERVATIONS_ERROR";
export const GET_ORDERS_SUCCESS = "GET_ORDERS_SUCCESS";
export const GET_ORDERS_ERROR = "GET_ORDERS_ERROR";

export const getReservations = () => {
  return dispatch => {
    reservations()
      .then(data => {
        dispatch({
          type: GET_RESERVATIONS_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_RESERVATIONS_ERROR,
          payload: error
        });
      });
  };
};

export const getOrders = () => {
  return dispatch => {
    orders()
      .then(data => {
        dispatch({
          type: GET_ORDERS_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_ORDERS_ERROR,
          payload: error
        });
      });
  };
};
