const months = [
  "Январь",
  "Февраль",
  "Март",
  "Апрель",
  "May",
  "Июнь",
  "Июль",
  "Август",
  "Сентябрь",
  "Октябрь",
  "Ноябрь",
  "Декабрь"
];
export const colors = [
  "#ef5350",
  "#EC407A",
  "#AB47BC",
  "#7E57C2",
  "#5C6BC0",
  "#42A5F5",
  "#29B6F6",
  "#26C6DA",
  "#26A69A",
  "#66BB6A",
  "#9CCC65",
  "#D4E157",
  "#FFCA28",
  "#FFA726",
  "#FF7043"
];
export function getMonthName(index) {
  return months[index];
}

export const weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];

export function abbreviationForWeekday(weekday) {
  return weekday.substring(0, 2);
}

const WEEK_LENGTH = 7;

export function getWeeksForMonth(month, year) {
  const firstOfMonth = new Date(year, month, 1);
  const firstDayOfWeek =
    firstOfMonth.getDay() - 1 === -1 ? 6 : firstOfMonth.getDay() - 1;
  const weeks = [[]];

  let currentWeek = weeks[0];
  let currentDate = firstOfMonth;

  for (let i = 0; i < firstDayOfWeek; i++) {
    currentWeek.push(null);
  }

  while (currentDate.getMonth() === month) {
    if (currentWeek.length === WEEK_LENGTH) {
      currentWeek = [];
      weeks.push(currentWeek);
    }

    currentWeek.push(currentDate);
    currentDate = new Date(year, month, currentDate.getDate() + 1);
  }

  while (currentWeek.length < 7) {
    currentWeek.push(null);
  }

  return weeks;
}
