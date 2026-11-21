// Finding things on the page by their id (their name tag in the HTML).
const tbody = document.getElementById("applications-body");
const emptyMessage = document.getElementById("empty-message");
const dialog = document.getElementById("add-dialog");
const form = document.getElementById("add-form");
const formTitle = document.getElementById("form-title");
const submitButton = document.getElementById("submit-button");
const formError = document.getElementById("form-error");

// The form fields, in one list, so filling and reading them is one loop.
const FIELDS = ["company", "role", "location", "deadline", "status", "link", "notes"];

// null when adding a new application, or the id of the one being edited.
let editingId = null;


// (a) + (c): ask the API for the list, then build one table row per application.
function loadApplications() {
    fetch("/api/applications")
        .then(response => response.json())
        .then(data => {
            tbody.innerHTML = "";               // empty the table before refilling it
            emptyMessage.hidden = data.length > 0;
            data.forEach(application => {
                tbody.appendChild(makeRow(application));
            });
        });
}


// Builds one <tr> for one application.
function makeRow(application) {
    const row = document.createElement("tr");
    row.className = "status-" + application.status;   // the CSS colours rows by this

    row.appendChild(makeCell(application.company));
    row.appendChild(makeRoleCell(application));
    row.appendChild(makeCell(application.location));
    row.appendChild(makeCell(application.deadline));

    const statusCell = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = application.status;
    statusCell.appendChild(badge);
    row.appendChild(statusCell);

    row.appendChild(makeCell(application.notes));

    const actions = document.createElement("td");
    actions.className = "actions";
    actions.appendChild(makeButton("Edit", () => openEdit(application)));
    actions.appendChild(makeButton("Delete", () => deleteApplication(application)));
    row.appendChild(actions);

    return row;
}


function makeCell(text) {
    const cell = document.createElement("td");
    cell.textContent = text || "";        // empty fields (null) show as blank
    return cell;
}


// The role is shown as a link when the application has one.
function makeRoleCell(application) {
    const cell = document.createElement("td");
    if (application.link) {
        const a = document.createElement("a");
        a.href = safeUrl(application.link);
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = application.role;
        cell.appendChild(a);
    } else {
        cell.textContent = application.role;
    }
    return cell;
}


// Only allow web links, so a link like "javascript:..." can't run code.
function safeUrl(link) {
    if (link.startsWith("http://") || link.startsWith("https://")) {
        return link;
    }
    return "https://" + link;
}


function makeButton(label, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", onClick);
    return button;
}


// Opening the pop-up, empty, to add a new application.
function openAdd() {
    editingId = null;
    form.reset();
    formTitle.textContent = "New application";
    submitButton.textContent = "Add";
    formError.hidden = true;
    dialog.showModal();
}


// Opening the same pop-up, filled in with one application's values, to edit it.
function openEdit(application) {
    editingId = application.id;
    FIELDS.forEach(field => {
        document.getElementById(field).value = application[field] || "";
    });
    formTitle.textContent = "Edit application";
    submitButton.textContent = "Save";
    formError.hidden = true;
    dialog.showModal();
}


// (b): the form sends its data to the API.
form.addEventListener("submit", event => {
    event.preventDefault();                // stop the browser reloading the page

    // Read every field into one object, like {"company": "Shell", ...}.
    const body = {};
    FIELDS.forEach(field => {
        const value = document.getElementById(field).value.trim();
        body[field] = value === "" ? null : value;   // empty box -> null in the database
    });

    // Adding is POST to the list address; editing is PUT to that one id's address.
    const url = editingId === null ? "/api/applications" : "/api/applications/" + editingId;
    const method = editingId === null ? "POST" : "PUT";

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)             // the object turned into JSON text
    })
        .then(response => response.json().then(reply => ({ok: response.ok, reply})))
        .then(({ok, reply}) => {
            if (ok) {
                dialog.close();
                loadApplications();            // redraw the table with the change
            } else {
                formError.textContent = reply.message;   // e.g. "Invalid status!" from a 400
                formError.hidden = false;
            }
        });
});


function deleteApplication(application) {
    if (!confirm("Delete " + application.company + " - " + application.role + "?")) {
        return;
    }
    fetch("/api/applications/" + application.id, {method: "DELETE"})
        .then(() => loadApplications());
}


document.getElementById("open-add").addEventListener("click", openAdd);
document.getElementById("cancel-add").addEventListener("click", () => dialog.close());

loadApplications();
