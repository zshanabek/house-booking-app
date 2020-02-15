import React, { Component } from "react";

import { format } from "date-fns";
import { ru as locale } from "date-fns/locale";

import Weekday from "./Weekday";
import Day from "./Day";
import { weekdays, abbreviationForWeekday, getWeeksForMonth } from "./helpers";
import { getMonthName } from "./helpers";

class Month extends Component {
  constructor(props) {
    super(props);

    this.renderWeek = this.renderWeek.bind(this);
    this.handleMouseEnter = this.handleMouseEnter.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);

    this.state = {
      hoveredDate: null
    };
  }

  render() {
    const { date, month, year } = this.props;

    const week = getWeeksForMonth(month, year);
    const weeksMarkup = week.map((week, index) => {
      return (
        <div role="row" className="Week" key={index}>
          {week.map(this.renderWeek)}
        </div>
      );
    });

    const weekDaysMarkup = weekdays.map(weekday => {
      return (
        <Weekday
          key={weekday}
          title={abbreviationForWeekday(weekday)}
          current={true}
          label={weekday}
        />
      );
    });

    return (
      <div className="MonthContainer">
        <div className="Month__name">
          {format(
            new Date(year + "-" + (month + 1) + "-" + date),
            "yyyy MMMM",
            {
              locale
            }
          )}
        </div>

        <div className="WeekdayContainer">{weekDaysMarkup}</div>
        {weeksMarkup}
      </div>
    );
  }

  isBeforeDay = (a, b) => {
    const aYear = a.getYear();
    const aMonth = a.getMonth();

    const bYear = b.getYear();
    const bMonth = b.getMonth();

    const isSameYear = aYear === bYear;
    const isSameMonth = aMonth === bMonth;

    if (isSameYear && isSameMonth) return a.getDate() < b.getDate();
    if (isSameYear) return aMonth < bMonth;
    return aYear < bYear;
  };
  isDayBetween = (range, day) => {
    const a = range[0],
      b = range[1];

    const aYear = a.getYear();
    const aMonth = a.getMonth();

    const bYear = b.getYear();
    const bMonth = b.getMonth();

    const dayYear = day.getYear();
    const dayMonth = day.getMonth();

    const isSameYear = aYear === dayYear && dayYear === bYear;
    const isSameMonth = aMonth === dayMonth && dayMonth === bMonth;

    if (isSameYear && isSameMonth) {
      return a.getDate() <= day.getDate() && day.getDate() <= b.getDate();
    }

    if (isSameYear) return aMonth < dayMonth && dayMonth < bMonth;
    return aYear < dayYear && dayYear < bYear;
  };
  renderWeek(fullDate, dayIndex) {
    const { minBookingDate, maxBookingDate, reserves, blocked } = this.props;
    const { hoveredDate } = this.state;

    if (fullDate == null) {
      return <Day key={dayIndex} />;
    }

    let isBlocked;

    if (minBookingDate && this.isBeforeDay(fullDate, minBookingDate)) {
      isBlocked = true;
    }
    if (maxBookingDate && maxBookingDate < fullDate) {
      isBlocked = true;
    }
    let minDate, maxDate;
    if (blocked) {
      blocked.forEach(range => {
        minDate = range[0];
        maxDate = range[1];
        if (this.isDayBetween([minDate, maxDate], fullDate)) {
          isBlocked = true;
        }
      });
    }
    let isReserved,
      color = null;

    if (reserves) {
      reserves.forEach(range => {
        minDate = range.check_in;
        maxDate = range.check_out;

        if (
          this.isDayBetween([new Date(minDate), new Date(maxDate)], fullDate)
        ) {
          isBlocked = false;
          isReserved = true;
          color = range.color;
        }
      });
    }

    const date = fullDate.getDate();
    return (
      <Day
        key={dayIndex}
        fullDate={fullDate}
        isReserved={isReserved}
        reservedColor={color}
        isBlocked={isBlocked}
        hovering={date === hoveredDate}
        onMouseEnter={this.handleMouseEnter}
        onMouseLeave={this.handleMouseLeave}
      />
    );
  }

  handleMouseEnter(date) {
    this.setState({
      hoveredDate: date
    });
  }

  handleMouseLeave() {
    this.setState({
      hoveredDate: null
    });
  }
}

export default Month;
