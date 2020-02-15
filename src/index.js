import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";

import { createStore, compose, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { Provider } from "react-redux";
import reducers from "./reducers";

import "bootstrap/dist/css/bootstrap.min.css";
import "./index.scss";

import App from "./components/app/App";

const __DEV__ = process.env.NODE_ENV;

// export const store =
//   __DEV__ === "development"
//     ? createStore(
//         reducers,
//         compose(
//           applyMiddleware(thunk),
//           window.__REDUX_DEVTOOLS_EXTENSION__ &&
//             window.__REDUX_DEVTOOLS_EXTENSION__()
//         )
//       )
//     : createStore(reducers, applyMiddleware(thunk));
export const store = window.__REDUX_DEVTOOLS_EXTENSION__
  ? createStore(
      reducers,
      compose(
        applyMiddleware(thunk),
        window.__REDUX_DEVTOOLS_EXTENSION__ &&
          window.__REDUX_DEVTOOLS_EXTENSION__()
      )
    )
  : createStore(reducers, applyMiddleware(thunk));

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <App />
    </Router>
  </Provider>,
  document.getElementById("root")
);
