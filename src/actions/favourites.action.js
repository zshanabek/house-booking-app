import { favourites } from "../services/favourites";

export const GET_FAVOURITES_SUCCESS = "GET_FAVOURITES_SUCCESS";
export const GET_FAVOURITES_ERROR = "GET_FAVOURITES_ERROR";

export const getFavourites = () => {
  return dispatch => {
    favourites()
      .then(data => {
        dispatch({
          type: GET_FAVOURITES_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: GET_FAVOURITES_ERROR,
          payload: error
        });
      });
  };
};
