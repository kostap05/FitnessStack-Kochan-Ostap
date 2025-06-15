document.getElementById("getExercisesBtn").addEventListener("click", async () => {
  const muscle = document.getElementById("muscleSelect").value;
  const list = document.getElementById("exerciseList");
  list.innerHTML = "";

  if (!muscle) {
    alert("Please select a muscle group!");
    return;
  }

  try {
    const res = await fetch(`/external/suggested-exercises?muscle=${encodeURIComponent(muscle)}`);
    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }
    const data = await res.json();
    if (data.exercises.length === 0) {
      list.innerHTML = "<p>No exercises found.</p>";
      return;
    }

    data.exercises.forEach(ex => {
      const card = document.createElement("div");
      card.className = "exercise-card";
      card.innerHTML = `
        <img src="${ex.gifUrl}" alt="${ex.name}" />
        <h3>${ex.name}</h3>
        <p><strong>Body Part:</strong> ${ex.bodyPart}</p>
        <p><strong>Equipment:</strong> ${ex.equipment}</p>
        <p><strong>Instructions:</strong> ${ex.instructions}</p>
      `;
      list.appendChild(card);
    });
  } catch (err) {
    console.error(err);
    list.innerHTML = "<p>Failed to load exercises.</p>";
  }
});
