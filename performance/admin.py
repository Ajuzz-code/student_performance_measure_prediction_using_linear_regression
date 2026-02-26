from django.contrib import admin
from django.utils.html import format_html
from .models import Course, StudentProfile, Prediction


# ⭐ PROFESSIONAL ADMIN TITLES
admin.site.site_header = "🎓 Student Performance Prediction Admin"
admin.site.site_title = "AI Prediction Dashboard"
admin.site.index_title = "Linear Regression Control Panel"


# ======================
# Course Admin
# ======================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


# ======================
# Student Profile Admin
# ======================
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_no", "course", "year", "contact")
    list_filter = ("course", "year")
    search_fields = ("user__username", "roll_no", "contact")
    autocomplete_fields = ("user", "course")


# ======================
# Prediction Admin (PROFESSIONAL)
# ======================
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "attendance",
        "previous_marks",
        "assignments",
        "absences",
        "grade_badge",
        "probability_bar",
        "date",
    )

    list_filter = ("date",)
    search_fields = ("student__username",)
    ordering = ("-date",)

    # 🎯 Professional Grade Badge
    def grade_badge(self, obj):
        grade = obj.grade()

        if grade == "Distinction":
            color = "#28a745"
        elif grade == "First Class":
            color = "#17a2b8"
        elif grade == "Pass":
            color = "#ffc107"
        else:
            color = "#dc3545"

        return format_html(
            '<span style="padding:6px 12px;border-radius:8px;'
            'background:{};color:white;font-weight:bold;">{}</span>',
            color,
            grade
        )

    grade_badge.short_description = "Grade"


    # 🎯 Probability Progress Bar
    def probability_bar(self, obj):
        percent = int(obj.probability() * 100)

        return format_html(
            """
            <div style="width:120px;background:#eee;border-radius:5px;">
                <div style="width:{}%;background:#007bff;color:white;
                text-align:center;border-radius:5px;">
                {}%
                </div>
            </div>
            """,
            percent,
            percent
        )

    probability_bar.short_description = "Probability"
