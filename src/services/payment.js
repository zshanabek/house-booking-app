import axios from "axios";
import { url } from "./config";

const PAYMENT = "/api/pay";
const MY_PAYMENTS = "/api/payments/";

export function createPayment(id) {
  return axios({
    method: "POST",
    url: url + PAYMENT,
    headers: {
      "Content-Type": "application/json"
    },
    data: { reservation_id: id }
  });
}

export function getMyPayments() {
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + MY_PAYMENTS,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}
