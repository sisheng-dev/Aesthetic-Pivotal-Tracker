$(document).ready(function () {
    $('#calendar').fullCalendar({
        defaultView: 'month',
        editable: true,
        events: [
            {
                title: 'Meeting',
                start: '2024-05-30T10:30:00',
                end: '2024-05-30T12:30:00'
            },
            {
                title: 'Meeting #2 idk',
                start: '2024-05-31T12:00:00'
            }
        ]
    });
});

// Allow items to be dropped in the columns
function allowDrop(event) {
    event.preventDefault();
}

// Drag the item
function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

// Drop the item and update status
function drop(event) {
    event.preventDefault();
    const data = event.dataTransfer.getData("text");
    const task = document.getElementById(data);
    const targetColumn = event.target.closest('.drag-item-list');

    if (targetColumn && task) {
        targetColumn.appendChild(task);

        let newStatus;
        if (targetColumn.id === 'to-do-content') {
            newStatus = 0;
        } else if (targetColumn.id === 'in-progress-content') {
            newStatus = 1;
        } else if (targetColumn.id === 'done-content') {
            newStatus = 2;
        }

        fetch(`/update-task-status/${task.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ status: newStatus })
        })
            .then(response => {
                if (response.ok) {
                    console.log('Task status updated successfully.');
                } else {
                    console.log('Failed to update task status.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });

    }
}

// Toggle dropdown content
function toggleDropdown(event) {
    const dropdownContent = event.target.nextElementSibling;
    dropdownContent.classList.toggle("show");
}

// Show input box to add a new task
function showInputBox(columnId) {
    const inputBox = document.querySelector(`#new-task-${columnId}`).parentElement;
    inputBox.style.display = 'flex';

}

function hideInputBox(columnId) {
    const inputBox = document.querySelector(`#new-task-${columnId}`).parentElement;
    inputBox.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const addTaskButtons = document.querySelectorAll('.add-task-button');
    addTaskButtons.forEach(button => {
        button.addEventListener('click', function () {
            const columnId = button.parentElement.nextElementSibling.id;
            showInputBox(columnId);
        });
    });

    const addBtnSolid = document.querySelectorAll('.add-btn.solid');
    addBtnSolid.forEach(button => {
        button.addEventListener('click', function () {
            const columnId = button.previousElementSibling.id.replace('new-task-', '');
            addTask(columnId);
        });
    });

    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            button.parentElement.style.display = 'none';
        });
    });
});


function deleteTask(taskId) {
    fetch('/delete-task/' + taskId, {
        method: 'POST',
    })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        });
}

// Show the edit form
function showEditForm(taskId) {
    const card = document.getElementById(taskId);
    const title = card.querySelector('.task-title');
    const description = card.querySelector('.task-description');
    const deadline = card.querySelector('.task-deadline');
    const form = card.querySelector('.edit-task-form');

    title.style.display = 'none';
    description.style.display = 'none';
    deadline.style.display = 'none';
    form.style.display = 'block';
}

// Hide the edit form and show original task details
function hideEditForm(taskId) {
    const card = document.getElementById(taskId);
    const title = card.querySelector('.task-title');
    const description = card.querySelector('.task-description');
    const deadline = card.querySelector('.task-deadline');
    const form = card.querySelector('.edit-task-form');

    title.style.display = 'block';
    description.style.display = 'block';
    deadline.style.display = 'block';
    form.style.display = 'none';
}

// Add event listeners for confirm and cancel buttons
document.addEventListener('DOMContentLoaded', function () {
    const editForms = document.querySelectorAll('.edit-task-form');
    editForms.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const taskId = form.parentElement.id;
            const formData = new FormData(form);

            fetch(`/edit-task/${taskId}`, {
                method: 'POST',
                body: formData,
            }).then(response => {
                if (response.ok) {
                    response.json().then(data => {
                        const card = document.getElementById(taskId);
                        card.querySelector('.task-title').innerText = data.taskTitle;
                        card.querySelector('.task-description').innerText = data.taskDescription;
                        card.querySelector('.task-deadline').innerText = data.taskDeadline;
                        hideEditForm(taskId);
                    });
                }
            });
        });
    });
});

function getCSRFToken() {
    return document.querySelector('input[name="csrf_token"]').value;
}

function startTimer(description, projectTitle, taskTitle) {
    fetch('/start_timer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            description: description,
            project_id: projectTitle,
            tags: [taskTitle]
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Timer started successfully!');
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to start timer.');
        });
}
function stopTimer() {
    if (currentTimerId === null) {
        alert('No timer is running.');
        return;
    }

    fetch('/stop_timer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            time_entry_id: currentTimerId
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            alert('Timer stopped successfully!');
            currentTimerId = null;  // Clear the timer ID
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Failed to stop timer.');
        });
}