import {
  GET_FAVOURITES_SUCCESS,
  GET_FAVOURITES_ERROR
} from "../actions/favourites.action";

const initState = {
  loading: true,
  results: []
};

export default function(state = initState, action) {
  switch (action.type) {
    case GET_FAVOURITES_SUCCESS:
      return {
        ...state,
        ...action.payload,
        loading: false
      };
    case GET_FAVOURITES_ERROR:
      return {
        ...state,
        loading: false
      };
    default:
      return state;
  }
}
