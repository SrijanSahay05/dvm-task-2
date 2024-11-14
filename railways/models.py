from django.db import models
from datetime import timedelta, datetime


class Station(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Day(models.Model):
    day_name = models.CharField(max_length=10)
    day_code = models.CharField(max_length=3)

    def __str__(self):
        return self.day_name


class Date(models.Model):
    date = models.DateField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="dates")

    def __str__(self):
        return str(self.date)


class HaltStation(models.Model):
    train = models.ForeignKey(
        "Train", on_delete=models.CASCADE, related_name="halt_stations"
    )
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="halt_station_stops"
    )
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    order = models.IntegerField()

    class Meta:
        unique_together = ("train", "station", "order")

    def __str__(self):
        return f"{self.station.name} (Order: {self.order})"


class SeatCategory(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TrainSeatCategory(models.Model):
    train = models.ForeignKey(
        "Train", on_delete=models.CASCADE, related_name="train_seat_categories"
    )
    seat_category = models.ForeignKey(
        SeatCategory, on_delete=models.CASCADE, related_name="train_seat_categories"
    )
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.train.name} - {self.seat_category.name} ({self.available_seats} available)"


class Train(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    departure_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="train_departures"
    )
    arrival_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="train_arrivals"
    )
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    journey_length = models.DurationField(default=timedelta(hours=0))
    days_running = models.ManyToManyField(Day, related_name="running_trains")
    seat_categories = models.ManyToManyField(
        SeatCategory, through="TrainSeatCategory", related_name="trains_with_category"
    )

    def __str__(self):
        return f"{self.name} ({self.number})"

    def calculate_journey_length(self):
        """Calculates the journey length based on departure and arrival times."""
        # Adjust for overnight travel
        if self.arrival_time < self.departure_time:
            journey_length = (
                timedelta(hours=24)
                - timedelta(
                    hours=self.departure_time.hour, minutes=self.departure_time.minute
                )
                + timedelta(
                    hours=self.arrival_time.hour, minutes=self.arrival_time.minute
                )
            )
        else:
            journey_length = timedelta(
                hours=self.arrival_time.hour - self.departure_time.hour,
                minutes=self.arrival_time.minute - self.departure_time.minute,
            )
        return journey_length


class Journey(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="journeys")
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name="journeys")
    total_seats = models.IntegerField()
    booked_seats = models.IntegerField(default=0)

    def __str__(self):
        return f"Journey of {self.train.name} on {self.date.date}"


class JourneySegment(models.Model):
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="segments"
    )
    departure_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="segment_departures"
    )
    arrival_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="segment_arrivals"
    )
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    journey_length = models.DurationField()
    price_segment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Segment from {self.departure_station.name} to {self.arrival_station.name} for Journey on {self.journey.date}"


class JourneySeatCategory(models.Model):
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="journey_seat_categories"
    )
    seat_category = models.ForeignKey(
        SeatCategory, on_delete=models.CASCADE, related_name="journey_seat_categories"
    )
    total_seats = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Seat category {self.seat_category.name} in journey of {self.journey.train.name} on {self.journey.date.date}"


class JourneySegmentSeatCategory(models.Model):
    journey_segment = models.ForeignKey(
        JourneySegment, on_delete=models.CASCADE, related_name="segment_seat_categories"
    )
    seat_category = models.ForeignKey(
        SeatCategory, on_delete=models.CASCADE, related_name="segment_seat_categories"
    )
    total_seats = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Seat category {self.seat_category.name} in segment from {self.journey_segment.departure_station.name} to {self.journey_segment.arrival_station.name}"
