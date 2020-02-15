import React from "react";

export default function Day({
  fullDate,
  isReserved,
  reservedColor,
  isBlocked,
  onMouseEnter,
  onMouseLeave,
  hovering
}) {
  if (fullDate == null) {
    return <div className="EmptyStateDay" />;
  }
  const date = fullDate.getDate();
  let className = "Day";

  if (hovering) {
    className = "Day Day--hovering";
  }
  if (isBlocked) {
    className = "Day Day__blocked";
  }

  return (
    <div
      style={
        isReserved
          ? { backgroundColor: reservedColor, color: "#fff", border: "none" }
          : null
      }
      className={className}
      onMouseEnter={onMouseEnter.bind(this, date)}
      onMouseLeave={onMouseLeave.bind(this, date)}
    >
      {date}
    </div>
  );
}
