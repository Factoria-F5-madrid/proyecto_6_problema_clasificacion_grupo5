// client/src/services/predictPassengerServices.js

const BASE_URL = "http://localhost:8000"; // ajusta si tu backend está en otro host/puerto

export async function predictPassenger(data) {
  const res = await fetch(`${BASE_URL}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const txt = await res.text();
    // try parse json error
    try {
      const j = JSON.parse(txt);
      throw new Error(j.detail ? JSON.stringify(j.detail) : txt);
    } catch {
      throw new Error(txt || "Prediction request failed");
    }
  }

  return res.json();
}
