from django.contrib import admin
from .models import (
    Day,
    Date,
    Station,
    HaltStation,
    SeatCategory,
    TrainSeatCategory,
    Train,
    Journey,
    JourneySegment,
    JourneySeatCategory,
    JourneySegmentSeatCategory,
)


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ("day_name", "day_code")
    search_fields = ("day_name", "day_code")


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ("date", "day")
    list_filter = ("day",)
    search_fields = ("date",)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(HaltStation)
class HaltStationAdmin(admin.ModelAdmin):
    list_display = ("train", "station", "arrival_time", "departure_time", "order")
    list_filter = ("train", "station")
    search_fields = ("train__name", "station__name")
    ordering = ("train", "order")


@admin.register(SeatCategory)
class SeatCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


class HaltStationInline(admin.TabularInline):
    model = HaltStation
    extra = 1
    fields = ("station", "arrival_time", "departure_time", "order")
    ordering = ("order",)


class TrainSeatCategoryInline(admin.TabularInline):
    model = TrainSeatCategory
    extra = 1
    fields = ("seat_category", "total_seats", "available_seats", "base_price")


@admin.register(TrainSeatCategory)
class TrainSeatCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "train",
        "seat_category",
        "total_seats",
        "available_seats",
        "base_price",
    )
    list_filter = ("train", "seat_category")
    search_fields = ("train__name", "seat_category__name")
    ordering = ("train", "seat_category")


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "number",
        "departure_station",
        "arrival_station",
        "departure_time",
        "arrival_time",
    )
    list_filter = ("departure_station", "arrival_station", "days_running")
    search_fields = ("name", "number")
    inlines = [HaltStationInline, TrainSeatCategoryInline]
    ordering = ("number",)


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("train", "date", "total_seats", "booked_seats")
    list_filter = ("train", "date")
    search_fields = ("train__name", "date__date")
    ordering = ("date",)
    readonly_fields = ("booked_seats",)


class JourneySegmentInline(admin.TabularInline):
    model = JourneySegment
    extra = 1
    fields = (
        "departure_station",
        "arrival_station",
        "departure_time",
        "arrival_time",
        "journey_length",
        "price_segment",
    )
    readonly_fields = ("journey_length", "price_segment")


@admin.register(JourneySegment)
class JourneySegmentAdmin(admin.ModelAdmin):
    list_display = (
        "journey",
        "departure_station",
        "arrival_station",
        "departure_time",
        "arrival_time",
        "journey_length",
        "price_segment",
    )
    list_filter = ("journey", "departure_station", "arrival_station")
    search_fields = (
        "journey__train__name",
        "departure_station__name",
        "arrival_station__name",
    )
    ordering = ("journey", "departure_station", "arrival_station")


@admin.register(JourneySeatCategory)
class JourneySeatCategoryAdmin(admin.ModelAdmin):
    list_display = ("journey", "seat_category", "total_seats", "base_price")
    list_filter = ("journey", "seat_category")
    search_fields = ("journey__train__name", "seat_category__name")
    ordering = ("journey", "seat_category")


@admin.register(JourneySegmentSeatCategory)
class JourneySegmentSeatCategoryAdmin(admin.ModelAdmin):
    list_display = ("journey_segment", "seat_category", "total_seats", "base_price")
    list_filter = ("journey_segment", "seat_category")
    search_fields = ("journey_segment__journey__train__name", "seat_category__name")
    ordering = ("journey_segment", "seat_category")
