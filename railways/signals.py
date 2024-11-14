from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from datetime import date, timedelta
from .models import (
    Day,
    Date,
    Train,
    Journey,
    JourneySegment,
    JourneySeatCategory,
    TrainSeatCategory,
    SeatCategory,
    HaltStation,
)


@receiver(post_save, sender=Day)
def create_upcoming_dates(sender, instance, created, **kwargs):
    if created:
        print(f"[Signal] Creating upcoming dates for {instance.day_name}")
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    for day_offset in range(90):
        target_date = start_of_week + timedelta(days=day_offset)
        if target_date.strftime("%A") == instance.day_name:
            Date.objects.get_or_create(day=instance, date=target_date)
            print(f"[Signal] Created/Updated Date object for {target_date}")


def create_segments_for_all_journeys(journey):
    """
    Helper function to create JourneySegment entries for a given Journey
    based on the Train's HaltStations.
    """
    halts = journey.train.halt_stations.order_by("order")
    for i in range(len(halts) - 1):
        departure_halt = halts[i]
        arrival_halt = halts[i + 1]
        journey_length = timedelta(minutes=30)  # Default segment time
        price_segment = calculate_price_segment(journey_length)

        JourneySegment.objects.get_or_create(
            journey=journey,
            departure_station=departure_halt.station,
            arrival_station=arrival_halt.station,
            departure_time=departure_halt.departure_time,
            arrival_time=arrival_halt.arrival_time,
            journey_length=journey_length,
            price_segment=price_segment,
        )


def calculate_price_segment(journey_length):
    """
    Method to calculate the price of a journey segment based on duration.
    """
    price_per_hour = 10.0
    hours = journey_length.total_seconds() / 3600
    return round(hours * price_per_hour, 2)


def create_or_update_journeys_for_train(train_instance, created=True):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    running_days = train_instance.days_running.all()

    if not created:
        Journey.objects.filter(train=train_instance, date__date__gte=today).delete()

    for day_offset in range(90):
        target_date = start_of_week + timedelta(days=day_offset)
        day_instance = next(
            (day for day in running_days if day.day_name == target_date.strftime("%A")),
            None,
        )

        if day_instance:
            date_instance, _ = Date.objects.get_or_create(
                date=target_date, day=day_instance
            )
            journey, journey_created = Journey.objects.get_or_create(
                train=train_instance,
                date=date_instance,
                defaults={
                    "total_seats": sum(
                        category.available_seats
                        for category in train_instance.train_seat_categories.all()
                    ),
                    "booked_seats": 0,
                },
            )

            if journey_created:
                create_segments_for_all_journeys(journey)
                create_journey_seat_categories_for_train(train_instance)


def create_journey_seat_categories_for_train(train):
    """
    Helper function to create JourneySeatCategory entries for all Journeys of a Train based on TrainSeatCategory entries.
    """
    journeys = train.journeys.all()
    train_seat_categories = train.train_seat_categories.all()

    for journey in journeys:
        for train_seat_category in train_seat_categories:
            JourneySeatCategory.objects.get_or_create(
                journey=journey,
                seat_category=train_seat_category.seat_category,
                defaults={
                    "total_seats": train_seat_category.available_seats,
                    "base_price": train_seat_category.base_price,
                },
            )


@receiver(post_save, sender=TrainSeatCategory)
def create_journey_seat_categories_on_train_seat_category_change(
    sender, instance, created, **kwargs
):
    create_journey_seat_categories_for_train(instance.train)


@receiver(post_save, sender=Train)
def create_journeys_for_new_train(sender, instance, created, **kwargs):
    create_or_update_journeys_for_train(instance, created=created)


@receiver(m2m_changed, sender=Train.days_running.through)
def update_journeys_on_running_days_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        create_or_update_journeys_for_train(instance, created=False)


@receiver(post_save, sender=Journey)
def create_segments_for_journey_on_creation(sender, instance, created, **kwargs):
    """
    Signal to automatically create JourneySegment objects when a new Journey is created.
    """
    if created:
        create_segments_for_all_journeys(instance)
