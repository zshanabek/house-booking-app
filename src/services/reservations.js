import axios from "axios";
import { url } from "./config";

const RESERVATIONS_PATH = "/api/reservations/";
const ORDERS_PATH = "/api/orders/";

export function getReservations() {
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + RESERVATIONS_PATH,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function getReservation(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + RESERVATIONS_PATH + id,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function createReservation(params = {}) {
  const token = localStorage.getItem("token");
  return axios({
    method: "POST",
    url: url + RESERVATIONS_PATH,
    data: params,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function deleteReservation(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "DELETE",
    url: url + RESERVATIONS_PATH + id,
    headers: {
      Authorization: "Token " + token
    }
  });
}
export function cancelReservation(id, message) {
  const token = localStorage.getItem("token");
  return axios({
    method: "PATCH",
    url: url + RESERVATIONS_PATH + id + "/cancel/",
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    },
    data: {
      message
    }
  });
}
export function getOrders() {
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + ORDERS_PATH,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function acceptReservation(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "PATCH",
    url: url + ORDERS_PATH + id + "/accept/",
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function rejectReservation(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "PATCH",
    url: url + ORDERS_PATH + id + "/reject/",
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}
