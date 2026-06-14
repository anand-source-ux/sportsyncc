import streamlit as st
import pandas as pd
import os
import qrcode
from datetime import date
import plotly.express as px

# -------------------------
# APP CONFIG
# -------------------------
st.set_page_config(
    page_title="Sports Facility Management",
    page_icon="🏆",
    layout="wide"
)

# -------------------------
# FILE SETUP
# -------------------------

os.makedirs("qr_codes", exist_ok=True)

if not os.path.exists("users.csv"):
    pd.DataFrame({
        "Username": ["student1", "coach1"],
        "Password": ["1234", "1234"],
        "Role": ["Student", "Coach"]
    }).to_csv("users.csv", index=False)

if not os.path.exists("bookings.csv"):
    pd.DataFrame(columns=[
        "BookingID",
        "Student",
        "Sport",
        "Date",
        "Time"
    ]).to_csv("bookings.csv", index=False)

if not os.path.exists("attendance.csv"):
    pd.DataFrame(columns=[
        "BookingID",
        "Student",
        "Sport",
        "Status"
    ]).to_csv("attendance.csv", index=False)

if not os.path.exists("progress.csv"):
    pd.DataFrame(columns=[
        "Student",
        "Sport",
        "Score",
        "Feedback"
    ]).to_csv("progress.csv", index=False)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🏆 Sports Hub")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Student Login",
        "Coach Login",
        "Slot Booking",
        "Attendance",
        "Progress Tracker",
        "Analytics"
    ]
)

# -------------------------
# HOME
# -------------------------

if menu == "Home":

    st.title("🏆 Sports Facility Management System")

    st.markdown("""
    ### Features

    ✅ Student Login

    ✅ Coach Login

    ✅ Slot Booking

    ✅ QR Code Generation

    ✅ Attendance Tracking

    ✅ Progress Tracking

    ✅ Coach Feedback

    ✅ Analytics Dashboard
    """)

# -------------------------
# STUDENT LOGIN
# -------------------------

elif menu == "Student Login":

    st.title("🎓 Student Login")

    users = pd.read_csv("users.csv")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login Student"):

        match = users[
            (users["Username"] == username) &
            (users["Password"] == password) &
            (users["Role"] == "Student")
        ]

        if len(match) > 0:
            st.success("Login Successful")
            st.session_state["student"] = username
        else:
            st.error("Invalid Credentials")

# -------------------------
# COACH LOGIN
# -------------------------

elif menu == "Coach Login":

    st.title("🏅 Coach Login")

    users = pd.read_csv("users.csv")

    username = st.text_input("Coach Username")
    password = st.text_input("Coach Password", type="password")

    if st.button("Login Coach"):

        match = users[
            (users["Username"] == username) &
            (users["Password"] == password) &
            (users["Role"] == "Coach")
        ]

        if len(match) > 0:
            st.success("Coach Login Successful")
            st.session_state["coach"] = username
        else:
            st.error("Invalid Credentials")

# -------------------------
# SLOT BOOKING
# -------------------------

elif menu == "Slot Booking":

    st.title("📅 Sports Slot Booking")

    sports = [
        "Gymnasium",
        "Swimming",
        "Basketball",
        "Football",
        "Snooker",
        "Table Tennis",
        "Tennis",
        "Cricket"
    ]

    student = st.text_input("Student Name")

    sport = st.selectbox("Sport", sports)

    booking_date = st.date_input(
        "Booking Date",
        min_value=date.today()
    )

    time_slot = st.selectbox(
        "Time Slot",
        [
            "06:00 AM",
            "07:00 AM",
            "08:00 AM",
            "04:00 PM",
            "05:00 PM",
            "06:00 PM"
        ]
    )

    if st.button("Book Slot"):

        bookings = pd.read_csv("bookings.csv")

        booking_id = f"BK{len(bookings)+1}"

        row = pd.DataFrame({
            "BookingID": [booking_id],
            "Student": [student],
            "Sport": [sport],
            "Date": [booking_date],
            "Time": [time_slot]
        })

        bookings = pd.concat(
            [bookings, row],
            ignore_index=True
        )

        bookings.to_csv(
            "bookings.csv",
            index=False
        )

        qr = qrcode.make(booking_id)

        qr_path = f"qr_codes/{booking_id}.png"

        qr.save(qr_path)

        st.success(
            f"Booking Successful! ID: {booking_id}"
        )

        st.image(
            qr_path,
            width=250,
            caption="Show this QR at entry"
        )

    st.subheader("Current Bookings")

    st.dataframe(
        pd.read_csv("bookings.csv"),
        use_container_width=True
    )

# -------------------------
# ATTENDANCE
# -------------------------

elif menu == "Attendance":

    st.title("📱 Attendance")

    booking_id = st.text_input(
        "Enter Booking ID"
    )

    if st.button("Mark Attendance"):

        bookings = pd.read_csv("bookings.csv")

        match = bookings[
            bookings["BookingID"] == booking_id
        ]

        if len(match) > 0:

            attendance = pd.read_csv(
                "attendance.csv"
            )

            row = pd.DataFrame({
                "BookingID": [booking_id],
                "Student": [match.iloc[0]["Student"]],
                "Sport": [match.iloc[0]["Sport"]],
                "Status": ["Present"]
            })

            attendance = pd.concat(
                [attendance, row],
                ignore_index=True
            )

            attendance.to_csv(
                "attendance.csv",
                index=False
            )

            st.success("Attendance Marked")

        else:
            st.error("Booking ID Not Found")

    st.subheader("Attendance Records")

    st.dataframe(
        pd.read_csv("attendance.csv"),
        use_container_width=True
    )

# -------------------------
# PROGRESS TRACKER
# -------------------------

elif menu == "Progress Tracker":

    st.title("📈 Progress Tracker")

    student = st.text_input("Student")

    sport = st.selectbox(
        "Sport",
        [
            "Gymnasium",
            "Swimming",
            "Basketball",
            "Football",
            "Snooker",
            "Table Tennis",
            "Tennis",
            "Cricket"
        ]
    )

    score = st.slider(
        "Performance Score",
        0,
        100,
        50
    )

    feedback = st.text_area(
        "Coach Feedback"
    )

    if st.button("Save Progress"):

        progress = pd.read_csv(
            "progress.csv"
        )

        row = pd.DataFrame({
            "Student": [student],
            "Sport": [sport],
            "Score": [score],
            "Feedback": [feedback]
        })

        progress = pd.concat(
            [progress, row],
            ignore_index=True
        )

        progress.to_csv(
            "progress.csv",
            index=False
        )

        st.success(
            "Progress Saved"
        )

    st.subheader("Progress Records")

    st.dataframe(
        pd.read_csv("progress.csv"),
        use_container_width=True
    )

# -------------------------
# ANALYTICS
# -------------------------

elif menu == "Analytics":

    st.title("📊 Analytics Dashboard")

    bookings = pd.read_csv(
        "bookings.csv"
    )

    if len(bookings) > 0:

        fig = px.histogram(
            bookings,
            x="Sport",
            title="Sports Facility Usage"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    attendance = pd.read_csv(
        "attendance.csv"
    )

    st.subheader(
        "Attendance Records"
    )

    st.dataframe(
        attendance,
        use_container_width=True
    )

    progress = pd.read_csv(
        "progress.csv"
    )

    if len(progress) > 0:

        fig2 = px.bar(
            progress,
            x="Student",
            y="Score",
            color="Sport",
            title="Performance Scores"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )