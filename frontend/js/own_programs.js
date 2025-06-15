const apiBase = "/own-programs";
const token = localStorage.getItem("access_token");

let editingProgramId = null;

document.getElementById("programForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("programName").value.trim();
  const description = document.getElementById("programDescription").value.trim();

  const days = [];
  document.querySelectorAll(".day").forEach(dayEl => {
    const dayName = dayEl.querySelector(".dayName").value.trim();
    const exercises = [];
    dayEl.querySelectorAll(".exercise").forEach(exEl => {
      const exercise_name = exEl.querySelector(".exercise_name").value.trim();
      const sets = parseInt(exEl.querySelector(".sets").value);
      const reps = parseInt(exEl.querySelector(".reps").value);
      exercises.push({ exercise_name, sets, reps });
    });
    days.push({ day_name: dayName, exercises });
  });

  const payload = { name, description, days };

  let res;
  if (editingProgramId) {
    res = await fetch(`${apiBase}/${editingProgramId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
  } else {
    res = await fetch(`${apiBase}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
  }

  if (res.ok) {
    alert(editingProgramId ? "Program updated!" : "Program created!");
    document.getElementById("programForm").reset();
    document.getElementById("daysContainer").innerHTML = "";
    editingProgramId = null;
    loadPrograms();
  } else {
    alert("Failed to save program");
  }
});

function addDay() {
  const container = document.getElementById("daysContainer");
  const dayDiv = document.createElement("div");
  dayDiv.className = "day";
  dayDiv.innerHTML = `
    <input type="text" class="dayName" placeholder="Day Name" required />
    <div class="exercisesContainer"></div>
    <button type="button" onclick="addExercise(this)">Add Exercise</button>
  `;
  container.appendChild(dayDiv);
}

function addExercise(btn) {
  const exercisesContainer = btn.previousElementSibling;
  const exDiv = document.createElement("div");
  exDiv.className = "exercise";
  exDiv.innerHTML = `
    <input type="text" class="exercise_name" placeholder="Exercise Name" required />
    <input type="number" class="sets" placeholder="Sets" required />
    <input type="number" class="reps" placeholder="Reps" required />
  `;
  exercisesContainer.appendChild(exDiv);
}

async function loadPrograms() {
  const res = await fetch(apiBase + "/", {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  renderPrograms(data);
}

function renderPrograms(data) {
  const list = document.getElementById("programList");
  list.innerHTML = "";
  data.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${p.name}</strong>: ${p.description}
      <button onclick="editProgram(${p.id})">Edit</button>
      <button onclick="deleteProgram(${p.id})">Delete</button>
    `;
    list.appendChild(li);
  });
}

async function editProgram(id) {
  const res = await fetch(`${apiBase}/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    const p = await res.json();
    document.getElementById("programName").value = p.name;
    document.getElementById("programDescription").value = p.description;

    const container = document.getElementById("daysContainer");
    container.innerHTML = "";
    p.days.forEach(day => {
      const dayDiv = document.createElement("div");
      dayDiv.className = "day";
      dayDiv.innerHTML = `
        <input type="text" class="dayName" placeholder="Day Name" value="${day.day_name}" required />
        <div class="exercisesContainer"></div>
        <button type="button" onclick="addExercise(this)">Add Exercise</button>
      `;
      const exercisesContainer = dayDiv.querySelector(".exercisesContainer");
      day.exercises.forEach(ex => {
        const exDiv = document.createElement("div");
        exDiv.className = "exercise";
        exDiv.innerHTML = `
          <input type="text" class="exercise_name" placeholder="Exercise Name" value="${ex.exercise_name}" required />
          <input type="number" class="sets" placeholder="Sets" value="${ex.sets}" required />
          <input type="number" class="reps" placeholder="Reps" value="${ex.reps}" required />
        `;
        exercisesContainer.appendChild(exDiv);
      });
      container.appendChild(dayDiv);
    });

    editingProgramId = id;
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else {
    alert("Failed to load program");
  }
}

async function deleteProgram(id) {
  if (!confirm("Delete this program?")) return;
  const res = await fetch(`${apiBase}/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    loadPrograms();
  } else {
    alert("Failed to delete program");
  }
}

loadPrograms();
