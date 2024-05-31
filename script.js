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
