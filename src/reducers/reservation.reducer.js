import {
  GET_RESERVATIONS_SUCCESS,
  GET_RESERVATIONS_ERROR,
  GET_ORDERS_SUCCESS,
  GET_ORDERS_ERROR
} from "../actions/reservation.action";

const initState = {};

export default function(state = initState, action) {
  switch (action.type) {
    case GET_RESERVATIONS_SUCCESS:
      return {
        reservations: action.payload
      };
    case GET_RESERVATIONS_ERROR:
      return {
        state
      };
    case GET_ORDERS_SUCCESS:
      return {
        orders: action.payload
      };
    case GET_ORDERS_ERROR:
      return {
        state
      };
    default:
      return state;
  }
}
