import axios from "axios";
import { url } from "./config";

const ALL_CHATS = "/api/chat_sessions/";
const CONVERSATION = "/api/messages/";

export function getAllChats() {
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + ALL_CHATS,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    }
  });
}

export function getConversation(params) {
  console.log(params);
  const token = localStorage.getItem("token");
  return axios({
    method: "GET",
    url: url + CONVERSATION,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    },
    params
  });
}

export function sendMessage(data) {
  const token = localStorage.getItem("token");
  return axios({
    method: "POST",
    url: url + CONVERSATION,
    headers: {
      Authorization: "Token " + token,
      "Content-Type": "application/json"
    },
    data
  });
}
