import axios from "axios";
import { url } from "./config";

const HOUSES_PATH = "/api/houses/";
const FAVOURITES_PATH = "/api/favourites/";
const CREATE_FAVOURITES_PATH = "/save_favourite/";
const CANCEL_FAVOURITES_PATH = "/cancel_favourite/";

export function toggleFavourite(liked, id, callback) {
  if (!liked) {
    return createFavourite(id);
  } else {
    return deleteFavourite(id);
  }
}

export function favourites() {
  const token = localStorage.getItem("token");

  return axios({
    method: "GET",
    url: url + FAVOURITES_PATH,
    headers: {
      Authorization: "token " + token,
      "Content-Type": "application/x-www-form-urlencoded"
    }
  });
}

export function createFavourite(id) {
  const token = localStorage.getItem("token");
  return axios({
    method: "POST",
    url: url + HOUSES_PATH + id + CREATE_FAVOURITES_PATH,
    headers: {
      Authorization: "token " + token,
      "Content-Type": "application/x-www-form-urlencoded"
    }
  });
}
export function deleteFavourite(id) {
  const token = localStorage.getItem("token");

  return axios({
    method: "DELETE",
    url: url + HOUSES_PATH + id + CANCEL_FAVOURITES_PATH,
    headers: {
      Authorization: "token " + token,
      "Content-Type": "application/x-www-form-urlencoded"
    }
  });
}
