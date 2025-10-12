// client/src/services/predictPassengerServices.js

// Replace base URL if your backend runs elsewhere
const BASE_URL = "http://localhost:8000";

/*
 predictPassenger:
 - sends JSON POST to /predict
 - expects JSON response like { satisfaction: "satisfied", probability: 0.9 }
*/
export async function predictPassenger(data) {
  const res = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || "Prediction request failed");
  }
  return res.json();
}
