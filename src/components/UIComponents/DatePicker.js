import React, { Component } from "react";
import { format } from "date-fns";
import { ru as locale } from "date-fns/locale";
import { ThemeProvider } from "styled-components";
import { phraseOverrides } from "../../services/config";
import { Datepicker } from "@datepicker-react/styled";
import { DateSingleInput as DSI } from "@datepicker-react/styled";

export class DatePicker extends Component {
  render() {
    const size = window.screen.availWidth;
    // const size = window.screen.availWidth <= 450 ? "sm" : "";

    return (
      <div>
        <ThemeProvider
          theme={{
            breakpoints: ["32em", "48em", "64em"],
            reactDatepicker: {
              // datepickerWidth: "100%",
              // dayBackground: "#000",

              daySize: [26, 31],
              fontFamily: "system-ui, -apple-system",
              colors: {
                accessibility: "#D80249",
                selectedDay: "#F85E6F",
                selectedDayHover: "#F85E6F",
                primaryColor: "#CD3232"
              }
            }
          }}
        >
          <Datepicker
            onClose={this.props.onClose}
            onDatesChange={this.props.onDatesChange}
            startDate={this.props.startDate}
            endDate={this.props.endDate}
            focusedInput={this.props.focusedInput}
            vertical={size <= 450}
            numberOfMonths={
              this.props.numberOfMonths !== 2 ? this.props.numberOfMonths : 2
            }
            isDateBlocked={date => {
              let isBlocked = false;
              this.props.blockedDateRanges &&
                this.props.blockedDateRanges.forEach(item => {
                  let start = new Date(item.check_in),
                    end = new Date(item.check_out);
                  start.setDate(start.getDate() - 1);
                  if (date >= start && date < end) {
                    isBlocked = true;
                  }
                });
              return isBlocked;
            }}
            minBookingDate={new Date()}
            maxBookingDate={
              new Date(new Date().getTime() + 60 * 24 * 60 * 60 * 1000)
            }
            showClose={this.props.showClose === false ? false : true}
            showResetDates={this.props.showResetDates === false ? false : true}
            showSelectedDates={
              this.props.showSelectedDates === false ? false : true
            }
            placement="top"
            phrases={phraseOverrides}
            dayLabelFormat={date => format(date, "dd", { locale })}
            // dayLabelFormat={date => (
            //   <div className="Day">{format(date, "dd", { locale })}</div>
            // )}
            weekdayLabelFormat={date => format(date, "eeeeee", { locale })}
            monthLabelFormat={date => format(date, "yyyy MMMM", { locale })}
          />
        </ThemeProvider>
      </div>
    );
  }
}

export class DateSingleInput extends Component {
  render() {
    return (
      <ThemeProvider
        theme={{
          breakpoints: ["32em", "48em", "64em"],

          reactDatepicker: {
            inputBorder: "none",

            daySize: [26, 31],
            fontFamily: "system-ui, -apple-system",
            colors: {
              accessibility: "#D80249",
              selectedDay: "#F85E6F",
              selectedDayHover: "#F85E6F",
              primaryColor: "#CD3232"
            }
          }
        }}
      >
        <DSI
          placement="top"
          phrases={phraseOverrides}
          dayLabelFormat={date => format(date, "dd", { locale })}
          weekdayLabelFormat={date => format(date, "eeeeee", { locale })}
          monthLabelFormat={date => format(date, "yyyy MMMM", { locale })}
          onDateChange={this.props.onDateChange}
          focusedInput={this.props.focusedInput}
          onFocusChange={this.props.onFocusChange}
          date={this.props.date}
          showDatepicker={this.props.showDatepicker}
        />
      </ThemeProvider>
    );
  }
}
