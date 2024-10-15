// Get elements
const modal = document.getElementById("modal");
const closeModal = document.querySelector(".close");
const markRedBtn = document.getElementById("markRed");
const monthYearDisplay = document.getElementById("monthYear");
const prevMonthBtn = document.getElementById("prevMonth");
const nextMonthBtn = document.getElementById("nextMonth");

let selectedDate = null;
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

// List of available dates for demonstration purposes
const availableDates = [
    { day: 5, month: 9, year: 2024 },
    { day: 15, month: 9, year: 2024 },
    { day: 25, month: 9, year: 2024 }
];

// Function to generate the calendar for the selected month and year
function generateCalendar(month, year) {
    const calendarElement = document.getElementById("calendar");
    calendarElement.innerHTML = ""; // Clear previous content

    // Get the first day of the month
    const firstDay = new Date(year, month, 1).getDay();
    // Get the number of days in the month
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Display the current month and year
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    monthYearDisplay.textContent = `${monthNames[month]} ${year}`;

    // Generate empty spaces for the days of the week before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement("div");
        calendarElement.appendChild(emptyDiv);
    }

    // Generate the days in the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dateElement = document.createElement("div");
        dateElement.classList.add("date");

        // Check if the date is available
        const isAvailable = availableDates.some(
            (d) => d.day === day && d.month === month && d.year === year
        );

        if (isAvailable) {
            dateElement.addEventListener("click", () => openModal(day));
        } else {
            dateElement.classList.add("disabled");
        }

        dateElement.textContent = day;
        calendarElement.appendChild(dateElement);
    }
}

// Open modal
function openModal(date) {
    selectedDate = date;
    modal.style.display = "flex";
}

// Close modal
closeModal.addEventListener("click", () => {
    modal.style.display = "none";
});

// Mark date as red
markRedBtn.addEventListener("click", () => {
    const dateElements = document.querySelectorAll(".date");

    // Find the selected date and mark it red
    dateElements.forEach((dateEl) => {
        if (parseInt(dateEl.textContent) === selectedDate) {
            dateEl.style.backgroundColor = "red";
        }
    });

    modal.style.display = "none";
});

// Navigate months
prevMonthBtn.addEventListener("click", () => {
    if (currentMonth === 0) {
        currentMonth = 11;
        currentYear--;
    } else {
        currentMonth--;
    }
    generateCalendar(currentMonth, currentYear);
});

nextMonthBtn.addEventListener("click", () => {
    if (currentMonth === 11) {
        currentMonth = 0;
        currentYear++;
    } else {
        currentMonth++;
    }
    generateCalendar(currentMonth, currentYear);
});

// Initialize calendar for the current month and year
generateCalendar(currentMonth, currentYear);

