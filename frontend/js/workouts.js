const apiBase = "/workouts";
const token = localStorage.getItem("access_token");


let editingWorkoutId = null;


function addExercise() {
  const container = document.getElementById("exercises");
  const html = `
    <div class="exercise">
      <input type="text" placeholder="Exercise Name" class="exercise_name" required />
      <input type="number" placeholder="Sets" class="sets" required />
      <input type="number" placeholder="Reps" class="reps" required />
      <input type="number" placeholder="Duration (min)" class="duration" required />
    </div>
  `;
  container.insertAdjacentHTML("beforeend", html);
}


document.getElementById("workoutForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("editingWorkoutId в submit:", editingWorkoutId);
  const title = document.getElementById("title").value.trim();
  const category = document.getElementById("category").value.trim();
  const is_favorite = document.getElementById("is_favorite").checked;

  const exercises = [];
  const exerciseElements = document.querySelectorAll("#exercises .exercise");

  if (exerciseElements.length === 0) {
    alert("Add at least one exercise!");
    return;
  }

  for (const el of exerciseElements) {
    const name = el.querySelector(".exercise_name").value.trim();
    const sets = el.querySelector(".sets").value;
    const reps = el.querySelector(".reps").value;
    const duration = el.querySelector(".duration").value;

    if (!name || !sets || !reps || !duration) {
      alert("Fill in all exercise fields!");
      return;
    }

    exercises.push({
      exercise_name: name,
      sets: parseInt(sets),
      reps: parseInt(reps),
      duration: parseInt(duration),
    });
  }

  const payload = { title, category, is_favorite, exercises };

  let res;

  if (editingWorkoutId) {
    console.log("Отправляем PUT запрос");
    res = await fetch(`${apiBase}/${editingWorkoutId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
  } else {
    console.log("Отправляем POST запрос");
    res = await fetch(apiBase + "/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
  }

  if (res.ok) {
    alert(editingWorkoutId ? "Workout updated!" : "Workout created!");
    document.getElementById("workoutForm").reset();
    document.getElementById("exercises").innerHTML = "";
    editingWorkoutId = null;
    loadWorkouts();
  } else {
    alert("Failed to save workout");
  }
});


function renderWorkouts(data) {
  const list = document.getElementById("workoutList");
  list.innerHTML = "";
  data.forEach((w) => {
    const item = document.createElement("li");
    item.innerHTML = `
      <strong>${w.title}</strong> (${w.category}) - 
      <em>${w.total_duration} min, ${w.total_calories.toFixed(0)} kcal</em>
      <button onclick="editWorkout(${w.id})">Edit</button>
      <button onclick="deleteWorkout(${w.id})">Delete</button>
      <button onclick="toggleFavorite(${w.id})">Favorite: ${w.is_favorite}</button>
      <button onclick="repeatWorkout(${w.id})">Repeat</button>
    `;
    list.appendChild(item);
  });
}


async function loadWorkouts() {
  const res = await fetch(apiBase + "/", {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  renderWorkouts(data);
}


async function editWorkout(id) {
  const res = await fetch(`${apiBase}/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    const w = await res.json();
    document.getElementById("title").value = w.title;
    document.getElementById("category").value = w.category;
    document.getElementById("is_favorite").checked = w.is_favorite;


    const container = document.getElementById("exercises");
    container.innerHTML = "";
    w.exercises.forEach(ex => {
      const html = `
        <div class="exercise">
          <input type="text" placeholder="Exercise Name" class="exercise_name" value="${ex.exercise_name}" required />
          <input type="number" placeholder="Sets" class="sets" value="${ex.sets}" required />
          <input type="number" placeholder="Reps" class="reps" value="${ex.reps}" required />
          <input type="number" placeholder="Duration (min)" class="duration" value="${ex.duration}" required />
        </div>
      `;
      container.insertAdjacentHTML("beforeend", html);
    });
    console.log("Status:", res.status);
    console.log("Response text:", await res.clone().text());

    editingWorkoutId = id;
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else {
    alert("Failed to load workout");
  }
}


async function filterWorkouts() {
  const category = document.getElementById("filterCategory").value.trim();
  const res = await fetch(apiBase + "/?category=" + encodeURIComponent(category), {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  renderWorkouts(data);
}


async function loadFavorites() {
  const res = await fetch(apiBase + "/favorites/", {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  renderWorkouts(data);
}


async function deleteWorkout(id) {
  if (!confirm("Delete this workout?")) return;
  const res = await fetch(apiBase + "/" + id, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    loadWorkouts();
  } else {
    alert("Failed to delete");
  }
}


async function toggleFavorite(id) {
  const res = await fetch(apiBase + "/" + id + "/favorite", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    loadWorkouts();
  } else {
    alert("Failed to toggle favorite");
  }
}

async function repeatWorkout(id) {
  const res = await fetch(apiBase + "/" + id + "/repeat", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    loadWorkouts();
  } else {
    alert("Failed to repeat workout");
  }
}

loadWorkouts();
