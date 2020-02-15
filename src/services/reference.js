import axios from "axios";
import { url } from "./config";

const HOUSE_TYPES_PATH = "/api/house_types";
const CITIES_PATH = "/api/cities";
const REGIONS_PATH = "/api/regions";
const COUNTRIES_PATH = "/api/countries";
const ACCOMMODATIONS_PATH = "/api/accommodations";
const NEAR_BUILDINGS_PATH = "/api/near_buildings";
const RULES_PATH = "/api/rules";

export function houseTypes() {
  return axios({
    method: "GET",
    url: url + HOUSE_TYPES_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}
export function cities() {
  return axios({
    method: "GET",
    url: url + CITIES_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}
export function regions() {
  return axios({
    method: "GET",
    url: url + REGIONS_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}
export function countries() {
  return axios({
    method: "GET",
    url: url + COUNTRIES_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}

export function accommodations() {
  return axios({
    method: "GET",
    url: url + ACCOMMODATIONS_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}
export function nearBuildings() {
  return axios({
    method: "GET",
    url: url + NEAR_BUILDINGS_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}

export function rules() {
  return axios({
    method: "GET",
    url: url + RULES_PATH,
    headers: {
      "Content-Type": "application/json"
    }
  });
}
