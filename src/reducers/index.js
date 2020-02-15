import { combineReducers } from "redux";
import userReducer from "./user.reducer";
import referenceReducer from "./reference.reducer";
import houseReducer from "./house.reducer";
import reservationReducer from "./reservation.reducer";
import favouritesReducer from "./favourites.reducer";

const appReducer = combineReducers({
  auth: userReducer,
  reference: referenceReducer,
  house: houseReducer,
  reservations: reservationReducer,
  favourites: favouritesReducer
});

export default appReducer;
