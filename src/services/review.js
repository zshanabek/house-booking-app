import axios from "axios";
import { url } from "./config";

const HOUSES_PATH = "/api/houses/";
const REVIEWS_PATH = "/reviews/";

export function getReviews(houseId) {
  return axios({
    method: "get",
    url: url + HOUSES_PATH + houseId + REVIEWS_PATH
  });
}

export function getReview(houseId, reviewId) {
  return axios({
    method: "get",
    url: url + HOUSES_PATH + houseId + REVIEWS_PATH + reviewId
  });
}

export function createReview(token, houseId, body, rating) {
  return axios({
    method: "post",
    url: url + HOUSES_PATH + houseId + REVIEWS_PATH,
    data: {
      body: "asdasdasd"
    },
    headers: {
      Authorization: "token " + token
    }
  });
}

export function deleteReview(token, houseId) {
  return axios({
    method: "delete",
    url: url + HOUSES_PATH + houseId + REVIEWS_PATH,
    headers: {
      Authorization: "token " + token
    }
  });
}

export function updateReview(houseId, reviewId) {
  return axios({
    method: "put",
    url: url + HOUSES_PATH + houseId + REVIEWS_PATH + reviewId,
    data: {
      body: "ok"
    }
  });
}
