import axios from "axios";
import { url } from "./config";

const HOUSES_PATH = "/api/houses/";
const MY_HOUSES_PATH = "/api/my_houses/";
const DEACTIVATE_HOUSE_PATH = "/deactivate/";
const ACTIVATE_HOUSE_PATH = "/activate/";
const BLOCKED_DATS_PATH = "/blocked_dates/";

export function houses(params = {}) {
  const token = localStorage.getItem("token");
  let headers = {};
  if (token !== null) {
    headers = {
      Authorization: "token " + token,
      "Content-Type": "application/x-www-form-urlencoded"
    };
  }
  return axios({
    method: "get",
    url: url + HOUSES_PATH,
    headers,
    params
  });
}
export function myHouses() {
  const token = localStorage.getItem("token");
  return axios({
    method: "get",
    url: url + MY_HOUSES_PATH,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function getBlockedDates(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + HOUSES_PATH + id + BLOCKED_DATS_PATH,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}
export function deactivateHouse(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "POST",
    url: url + HOUSES_PATH + id + DEACTIVATE_HOUSE_PATH,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}
export function activateHouse(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "POST",
    url: url + HOUSES_PATH + id + ACTIVATE_HOUSE_PATH,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function getHouse(id) {
  return axios({
    method: "GET",
    url: url + HOUSES_PATH + id
  });
}
export function createHouse(params = {}) {
  const token = localStorage.getItem("token");
  return axios({
    method: "POST",
    url: url + HOUSES_PATH,
    data: params,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: "Token " + token
    }
  });
}
export function deleteHouse(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "DELETE",
    url: url + HOUSES_PATH + id,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: "Token " + token
    }
  });
}
export function updateHouse(id, params) {
  const token = localStorage.getItem("token");

  return axios({
    method: "PUT",
    url: url + HOUSES_PATH + id + "/",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: "Token " + token
    },
    data: params
  });
}
