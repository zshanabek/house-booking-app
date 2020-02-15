import React, { Component } from "react";

import moment from "moment";

import Month from "./Month";

import "./DatePicker.scss";

class DatePreview extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedDate: moment()
    };
  }
  prevMonth = () => {
    let date = this.state.selectedDate;
    date.subtract(1, "months");
    this.setState({
      selectedDate: date
    });
  };
  nextMonth = () => {
    let date = this.state.selectedDate;
    date.add(1, "months");
    this.setState({
      selectedDate: date
    });
  };
  render() {
    const { reserves, blocked, minBookingDate, maxBookingDate } = this.props;
    const { selectedDate } = this.state;

    const size = window.screen.availWidth;
    let numberOfMonths = size <= 1200 ? 2 : 3;
    const months = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    months.length = numberOfMonths;

    const dateNumber = selectedDate.date();
    const monthNumber = selectedDate.month();
    const yearNumber = selectedDate.year();
    return (
      <div className="DatePreview">
        <button
          className="DatePreview__button DatePreview__button--prev"
          onClick={this.prevMonth}
        >
          {"<"}
        </button>
        <button
          className="DatePreview__button DatePreview__button--next"
          onClick={this.nextMonth}
        >
          {">"}
        </button>
        {months.map((item, index) => (
          <Month
            selectedDate={selectedDate}
            reserves={reserves}
            blocked={blocked}
            minBookingDate={minBookingDate}
            maxBookingDate={maxBookingDate}
            key={index}
            date={dateNumber}
            month={
              monthNumber + index > 11 ? 0 + -1 + index : monthNumber + index
            }
            year={yearNumber}
          />
        ))}
      </div>
    );
  }
}

export default DatePreview;
