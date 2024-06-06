// function addTicket(section) {
//     const ticketTitle = prompt("Enter ticket title:");
//     const ticketDescription = prompt("Enter ticket description:");
//     const ticketOwner = section === 'critical-tickets' ? prompt("Enter ticket owner:") : null;

//     if (ticketTitle && ticketDescription) {
//         const ticketSection = document.querySelector(`.${section}`);
//         const newTicket = document.createElement('div');
//         newTicket.className = 'ticket';

//         const ticketHeader = document.createElement('div');
//         ticketHeader.className = 'ticket-header';
//         ticketHeader.innerText = ticketTitle;

//         const ticketDesc = document.createElement('div');
//         ticketDesc.className = 'ticket-description';
//         ticketDesc.innerText = ticketDescription;

//         newTicket.appendChild(ticketHeader);
//         newTicket.appendChild(ticketDesc);

//         if (ticketOwner) {
//             const ticketOwnerElem = document.createElement('div');
//             ticketOwnerElem.className = 'ticket-owner';
//             ticketOwnerElem.innerText = ticketOwner;
//             newTicket.appendChild(ticketOwnerElem);
//         }

//         ticketSection.insertBefore(newTicket, ticketSection.querySelector('button'));
//     }
// }

// function addKanbanTask(columnId) {
//     const taskTitle = prompt("Enter task title:");
//     if (taskTitle) {
//         const column = document.getElementById(columnId);
//         const newTask = document.createElement('div');
//         newTask.className = 'kanban-tasks';
//         newTask.innerText = taskTitle;
//         column.appendChild(newTask);
//     }
// }

$(document).ready(function() {
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

// Drop the item
function drop(event) {
    event.preventDefault();
    const data = event.dataTransfer.getData("text");
    const task = document.getElementById(data);
    event.target.appendChild(task);
}

// Show input box to add a new task
function showInputBox(columnId) {
    const inputBox = document.querySelector(`#new-task-${columnId}`).parentElement;
    inputBox.style.display = 'flex';
}

// Add a new task
function addTask(columnId) {
    const input = document.getElementById(`new-task-${columnId}`);
    const taskText = input.value;
    if (taskText.trim() !== "") {
        const newTask = document.createElement('div');
        newTask.className = 'kanban-task';
        newTask.id = `${columnId}-${new Date().getTime()}`;
        newTask.draggable = true;
        newTask.ondragstart = drag;
        newTask.innerText = taskText;
        document.getElementById(columnId).appendChild(newTask);
        input.value = "";
        input.parentElement.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const addTaskButtons = document.querySelectorAll('.add-task-button');
    addTaskButtons.forEach(button => {
        button.addEventListener('click', function() {
            const columnId = button.parentElement.nextElementSibling.id;
            showInputBox(columnId);
        });
    });

    const addBtnSolid = document.querySelectorAll('.add-btn.solid');
    addBtnSolid.forEach(button => {
        button.addEventListener('click', function() {
            const columnId = button.previousElementSibling.id.replace('new-task-', '');
            addTask(columnId);
        });
    });

    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            button.parentElement.style.display = 'none';
        });
    });
});
