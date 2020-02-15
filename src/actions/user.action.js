import {
  signInWithEmailAndPassword,
  signUpWithEmailAndPassword,
  signOut as logOut,
  getUserData,
  updateUserData as updateUser,
  sendCode,
  verify
} from "../services/user";

export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_ERROR = "LOGIN_ERROR";
export const SIGN_UP_SUCCESS = "SIGN_UP_SUCCESS";
export const SIGN_UP_ERROR = "SIGN_UP_ERROR";
export const SIGN_OUT_SUCCESS = "SIGN_OUT_SUCCESS";
export const GET_CURRENT_USER_SUCCESS = "GET_CURRENT_USER_SUCCESS";
export const TOGGLE_SIGN_IN_MODAL = "TOGGLE_SIGN_IN_MODAL";
export const TOGGLE_SIGN_UP_MODAL = "TOGGLE_SIGN_UP_MODAL";
export const TOGGLE_CONFIRM_NUMBER_MODAL = "TOGGLE_CONFIRM_NUMBER_MODAL";
export const TOGGLE_LOADING = "TOGGLE_LOADING";
export const UPDATE_USER_SUCCESS = "UPDATE_USER_SUCCESS";
export const UPDATE_USER_ERROR = "UPDATE_USER_ERROR";
export const VERIFY_SUCCESS = "VERIFY_SUCCESS";
export const VERIFY_ERROR = "VERIFY_ERROR";

export const toggleLoading = () => {
  return dispatch => {
    dispatch({
      type: TOGGLE_LOADING
    });
  };
};
export const toggleSignInModal = () => {
  return dispatch => {
    dispatch({
      type: TOGGLE_SIGN_IN_MODAL
    });
  };
};
export const toggleSignUpModal = () => {
  return dispatch => {
    dispatch({
      type: TOGGLE_SIGN_UP_MODAL
    });
  };
};
export const toggleConfirmNumberModal = () => {
  return dispatch => {
    dispatch({
      type: TOGGLE_CONFIRM_NUMBER_MODAL
    });
  };
};

export const updateUserData = data => {
  return dispatch => {
    updateUser(data)
      .then(data => {
        dispatch({
          type: UPDATE_USER_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: UPDATE_USER_ERROR,
          payload: error
        });
      });
  };
};

export const getCurrentUser = () => {
  const token = localStorage.getItem("token");
  return dispatch => {
    getUserData(token)
      .then(data => {
        dispatch({
          type: GET_CURRENT_USER_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        console.log(error);
      });
  };
};
export const signIn = signInFormDate => {
  const phone = signInFormDate.get("phone"),
    password = signInFormDate.get("password");

  if (phone === "+7" || password === "") {
    return dispatch => {
      dispatch({
        type: LOGIN_ERROR,
        error: "Заполните поля"
      });
    };
  } else {
    return dispatch => {
      signInWithEmailAndPassword(signInFormDate)
        .then(data => {
          const token = data.data.auth_token;
          localStorage.setItem("token", token);
          dispatch({
            type: LOGIN_SUCCESS,
            payload: data.data
          });
        })
        .catch(error => {
          dispatch({
            type: LOGIN_ERROR,
            error: error.response.data.error_message
          });
        });
    };
  }
};
export const signUp = (params = {}) => {
  return dispatch => {
    signUpWithEmailAndPassword(params)
      .then(data => {
        const token = data.data.auth_token;
        localStorage.setItem("token", token);

        sendCode(data.data.user.phone);
        dispatch({
          type: SIGN_UP_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: SIGN_UP_ERROR,
          error: error.response.data.error_message
        });
      });
  };
};
export const verifyPhone = (phone, code) => {
  return dispatch => {
    verify(phone, code)
      .then(data => {
        dispatch({
          type: VERIFY_SUCCESS,
          payload: data.data
        });
      })
      .catch(error => {
        dispatch({
          type: VERIFY_ERROR,
          error: error.response.data.error_message
        });
      });
  };
};
export const signOut = () => {
  return dispatch => {
    logOut().then(() => {
      dispatch({
        type: SIGN_OUT_SUCCESS
      });
    });
  };
};
