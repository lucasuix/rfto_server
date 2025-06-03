from datetime import datetime, timedelta

class WorkTimeCalculator:
    
    @staticmethod
    def time_remaining(time: datetime) -> int:
        """Minutes left in the workday from a given datetime."""
        end_hour = 16 if time.weekday() == 4 else 17
        return max(0, (end_hour * 60) - (time.hour * 60 + time.minute))

    @staticmethod
    def to_minutes(delta: timedelta) -> float:
        return delta.total_seconds() / 60
    
    @staticmethod
    def to_hour_decimal(time: datetime) -> float:
        return time.hour + (time.minute / 60)

    @staticmethod
    def calculate_breaks(starttime: datetime, endtime: datetime) -> int:
        """Calculate total break time (lunch and coffee) within a range."""
        total = 0
        start_hr = WorkTimeCalculator.to_hour_decimal(starttime)
        end_hr = WorkTimeCalculator.to_hour_decimal(endtime)

        if start_hr < 11.5 and end_hr > 12.5:
            total += 60  # Lunch
            # print("Lunch!")
        if start_hr < 15.5 and end_hr > 15.75:
            total += 15  # Coffee
            # print("Coffee!")
        return total

    @staticmethod
    def calculate_total_minutes(start_time: datetime, end_time: datetime) -> float:
        """Main method to calculate total time spent between two datetimes with breaks and work hours."""
        delta = end_time - start_time
        total_minutes = WorkTimeCalculator.to_minutes(delta)
        first_day_minutes = WorkTimeCalculator.time_remaining(start_time)

        print(total_minutes)

        time_spent_array = []

        # ---------- FIRST DAY ----------
        if total_minutes > first_day_minutes:
            first_day_end = start_time.replace(
                hour=17 if start_time.weekday() != 4 else 16,
                minute=0, second=0
            )
            first_day_breaks = WorkTimeCalculator.calculate_breaks(start_time, first_day_end)
            time_spent_array.append(840 if start_time.weekday() !=4 else 480 + first_day_breaks)
            # print("Time on the first day exceeded normal hours")
        else:
            first_day_breaks = WorkTimeCalculator.calculate_breaks(start_time, end_time)
            time_spent_array.append(first_day_breaks)
            print(time_spent_array)
            # print("Only one day used")
            return total_minutes - sum(time_spent_array)

        # ---------- BETWEEN DAYS ----------
        weekday = (start_time.weekday() + 1) % 7
        between_days_time = 0
        current_date = start_time + timedelta(days=1)
        goal_date = end_time.replace(hour=7, minute=0, second=0)

        while current_date < goal_date:
            if weekday == 5:  # Saturday
                between_days_time += 3300  # Full weekend
                current_date += timedelta(days=2)
                weekday = 0
            else:
                between_days_time += 840 + 60 + 15  # Work hours + breaks
                current_date += timedelta(days=1)
                weekday = (weekday + 1) % 7

        time_spent_array.append(between_days_time)

        # ---------- LAST DAY ----------
        last_day_start = end_time.replace(hour=7, minute=0, second=0)
        if end_time > last_day_start:
            # last_day_minutes = (end_time - last_day_start).total_seconds() / 60
            last_day_breaks = WorkTimeCalculator.calculate_breaks(last_day_start, end_time)
            time_spent_array.append(last_day_breaks)
            # print("Partial last day counted")

        print(time_spent_array)
        return (total_minutes - sum(time_spent_array))
