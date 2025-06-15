const apiBase = "/workouts";
const token = localStorage.getItem("access_token");

function addExercise() {
  const container = document.getElementById("exercises");
  const index = container.children.length;
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
  const title = document.getElementById("title").value;
  const category = document.getElementById("category").value;
  const is_favorite = document.getElementById("is_favorite").checked;

  const exercises = [];
  document.querySelectorAll("#exercises .exercise").forEach((el) => {
    exercises.push({
      exercise_name: el.querySelector(".exercise_name").value,
      sets: parseInt(el.querySelector(".sets").value),
      reps: parseInt(el.querySelector(".reps").value),
      duration: parseInt(el.querySelector(".duration").value),
    });
  });

  const payload = { title, category, is_favorite, exercises };
  const res = await fetch(apiBase + "/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    alert("Workout created!");
    loadWorkouts();
  } else {
    alert("Failed to create workout");
  }
});

async function loadWorkouts() {
  const res = await fetch(apiBase + "/", {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  const list = document.getElementById("workoutList");
  list.innerHTML = "";
  data.forEach((w) => {
    const item = document.createElement("li");
    item.innerHTML = `
      <strong>${w.title}</strong> (${w.category})
      <button onclick="deleteWorkout(${w.id})">Delete</button>
      <button onclick="toggleFavorite(${w.id})">Favorite: ${w.is_favorite}</button>
      <button onclick="repeatWorkout(${w.id})">Repeat</button>
    `;
    list.appendChild(item);
  });
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

// Init
loadWorkouts();
