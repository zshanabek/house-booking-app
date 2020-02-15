import {
  LOGIN_SUCCESS,
  LOGIN_ERROR,
  SIGN_UP_SUCCESS,
  SIGN_UP_ERROR,
  SIGN_OUT_SUCCESS,
  GET_CURRENT_USER_SUCCESS,
  TOGGLE_SIGN_IN_MODAL,
  TOGGLE_SIGN_UP_MODAL,
  TOGGLE_CONFIRM_NUMBER_MODAL,
  TOGGLE_LOADING,
  UPDATE_USER_SUCCESS,
  UPDATE_USER_ERROR,
  VERIFY_SUCCESS,
  VERIFY_ERROR
} from "../actions/user.action";

const initState = {
  authError: null,
  loading: false,
  signInModal: false,
  signUpModal: false,
  confirmNumberModal: false,
  isAuthenticated: false,
  user: null
};

export default function(state = initState, action) {
  switch (action.type) {
    case TOGGLE_LOADING:
      return {
        ...state,
        loading: !state.loading
      };
    case TOGGLE_SIGN_IN_MODAL:
      return {
        ...state,
        signInModal: !state.signInModal,
        loading: false,
        authError: false
      };
    case TOGGLE_SIGN_UP_MODAL:
      return {
        ...state,
        signUpModal: !state.signUpModal,
        loading: false,
        authError: false
      };
    case TOGGLE_CONFIRM_NUMBER_MODAL:
      return {
        ...state,
        confirmNumberModal: !state.confirmNumberModal,
        loading: false,
        authError: false
      };
    case LOGIN_SUCCESS:
      return {
        ...state,
        authError: null,
        isAuthenticated: true,
        loading: false,
        signInModal: false,
        ...action.payload
      };
    case LOGIN_ERROR:
      return {
        ...state,
        authError: action.error,
        loading: false
      };
    case VERIFY_SUCCESS:
      return {
        ...state,
        confirmNumberModal: false,
        ...action.payload
      };
    case VERIFY_ERROR:
      return state;
    case SIGN_UP_SUCCESS:
      return {
        ...state,
        authError: null,
        loading: false,
        isAuthenticated: true,
        signUpModal: false,
        confirmNumberModal: true,
        ...action.payload
      };
    case SIGN_UP_ERROR:
      return {
        ...state,
        authError: action.error,
        loading: false
      };
    case GET_CURRENT_USER_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload
      };
    case UPDATE_USER_SUCCESS:
      return {
        ...state,
        user: action.payload
      };
    case UPDATE_USER_ERROR:
      return state;
    case SIGN_OUT_SUCCESS:
      return {
        ...state,
        isAuthenticated: false,
        loading: false,
        user: null
      };
    default:
      return state;
  }
}
