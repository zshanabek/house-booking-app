import axios from "axios";
import { url } from "./config";

const SIGN_IN_PATH = "/api/auth/token/login/";
const CURRENT_USER_PATH = "/api/auth/users/me/";
const SIGN_UP_PATH = "/api/auth/users/";
const LOG_OUT_PATH = "/api/auth/token/logout/";
const SEND_CODE_PATH = "/api/auth/send_code";
const VERIFY_CODE_PATH = "/api/auth/verify";
const RESET_PASSWORD_PATH = "/api/auth/users/reset_password/";
const RESET_PASSWORD_CONFIRM_PATH = "/api/auth/users/reset_password_confirm/";

export function getUserData(token) {
  return axios({
    method: "GET",
    url: url + CURRENT_USER_PATH,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Token " + token
    }
  });
}
export function signInWithEmailAndPassword(signInFormDate) {
  return axios({
    method: "POST",
    url: url + SIGN_IN_PATH,
    data: signInFormDate
  });
}
export function signUpWithEmailAndPassword(params) {
  return axios({
    method: "POST",
    url: url + SIGN_UP_PATH,
    data: params
  });
}
export function signOut() {
  const token = localStorage.getItem("token");
  localStorage.removeItem("token");

  return axios({
    method: "POST",
    url: url + LOG_OUT_PATH,
    headers: {
      "Content-Type": "application/json",
      Authorization: "token " + token
    }
  });
}
export function updateUserData(data) {
  const token = localStorage.getItem("token");
  return axios({
    method: "PATCH",
    url: url + CURRENT_USER_PATH,
    headers: {
      Authorization: "token " + token,
      "Content-Type": "application/x-www-form-urlencoded"
    },
    data
  });
}
export function sendCode(phone) {
  return axios({
    method: "POST",
    url: url + SEND_CODE_PATH,
    headers: {
      "Content-Type": "application/json"
    },
    data: {
      phone
    }
  });
}
export function verify(phone, code) {
  return axios({
    method: "POST",
    url: url + VERIFY_CODE_PATH,
    headers: {
      "Content-Type": "application/json"
    },
    data: {
      phone,
      code
    }
  });
}

export function resetPassword(email) {
  return axios({
    method: "POST",
    url: url + RESET_PASSWORD_PATH,
    headers: {
      "Content-Type": "application/json"
    },
    data: {
      email
    }
  });
}
export function resetPasswordConfirm(data) {
  return axios({
    method: "POST",
    url: url + RESET_PASSWORD_CONFIRM_PATH,
    headers: {
      "Content-Type": "application/json"
    },
    data: data
  });
}
