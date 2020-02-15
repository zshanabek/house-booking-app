import React, { Component } from "react";

import DatePreview from "../UIComponents/DatePreview/DatePreview";

import "./Dev.scss";
import { Container } from "react-bootstrap";

export default class Dev extends Component {
  constructor(params) {
    super(params);
    this.state = {};
  }

  render() {
    // color = colors[Math.floor(Math.random() * colors.length)];

    const size = window.screen.availWidth;

    const reserve = [
      {
        check_in: "2020-02-22",
        check_out: "2020-02-27",
        user: {
          id: 118,
          first_name: "WWW",
          last_name: "SSS",
          userpic: null,
          email: "admin123@mail.dd"
        },
        income: 25000,
        color: "#ef5350"
      },
      {
        check_in: "2020-03-13",
        check_out: "2020-03-15",
        user: {
          id: 118,
          first_name: "admin",
          last_name: "wddd",
          userpic: null,
          email: "admin123@mail.dd"
        },
        income: 25000,
        color: "#29B6F6"
      },
      {
        check_in: "2020-03-27",
        check_out: "2020-03-31",
        user: {
          id: 118,
          first_name: "den",
          last_name: "ben",
          userpic: null,
          email: "admin123@mail.dd"
        },
        income: 25000,
        color: "#9CCC65"
      }
    ];
    const blocked = [
      [new Date("2020-02-16"), new Date("2020-02-20")],
      [new Date("2020-02-25"), new Date("2020-03-01")],
      [new Date("2020-03-06"), new Date("2020-03-11")]
    ];
    return (
      <div>
        <Container>
          <br />
          <br />
          <br />
          <br />
          <DatePreview
            reserves={reserve}
            blocked={blocked}
            minBookingDate={new Date()}
            maxBookingDate={
              new Date(new Date().getTime() + 60 * 24 * 60 * 60 * 1000)
            }
            numberOfMonths={3}
          />
        </Container>
      </div>
    );
  }
}
