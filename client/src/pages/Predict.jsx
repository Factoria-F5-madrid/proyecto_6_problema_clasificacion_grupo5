// client/src/pages/Predict.jsx
import React, { useState } from "react";
import { predictPassenger } from "../services/predictPassengerServices";

/*
 Predict page (minimal): only the fields you requested.
 Sends exactly the same JSON keys you used in Postman.
*/

export default function Predict() {
  const [form, setForm] = useState({
    passenger_id: "PX002",
    gender: "female",
    age: 32,
    inflight_wifi_service: 1,
    online_boarding: 1,
    checkin_service: 0,
    baggage_handling: 5,
    seat_comfort: 5,
    inflight_service: 5,
    cleanliness: 1,
    type_of_travel: "Business travel",
    customer_type: "Disloyal Customer",
    class_type: "Business"
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // fields that must be numeric
  const numericFields = new Set([
    "age",
    "inflight_wifi_service",
    "online_boarding",
    "checkin_service",
    "baggage_handling",
    "seat_comfort",
    "inflight_service",
    "cleanliness"
  ]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const parsed = numericFields.has(name) ? (value === "" ? "" : Number(value)) : value;
    setForm(prev => ({ ...prev, [name]: parsed }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      // Build payload exactly as keys in form
      const payload = {};
      for (const [k, v] of Object.entries(form)) {
        // send null for empty strings to match backend optional fields
        payload[k] = v === "" ? null : v;
      }

      const res = await predictPassenger(payload);
      const uiResult = {
        satisfaction: res.satisfaction ?? res.predicted_label ?? null,
        probability: (res.predicted_proba ?? res.probability ?? null),
        raw: res
      };
      setResult(uiResult);
    } catch (err) {
      // normalize possible error shapes
      const msg = err?.message ?? String(err);
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page predict-page p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold mb-2">Passenger Satisfaction Predictor</h2>
      <p className="mb-4 text-sm text-gray-600">
        Fill the form and press <strong>Predict</strong>. This will submit the exact JSON used in Postman.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4 bg-white p-4 rounded shadow">
        <div className="grid grid-cols-2 gap-4">
          <label className="flex flex-col">
            Passenger ID
            <input name="passenger_id" value={form.passenger_id} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Gender
            <select name="gender" value={form.gender} onChange={handleChange} className="mt-1 p-2 border rounded">
              <option value="male">male</option>
              <option value="female">female</option>
              <option value="other">other</option>
            </select>
          </label>

          <label className="flex flex-col">
            Age
            <input name="age" type="number" min="0" value={form.age} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Type of travel
            <select name="type_of_travel" value={form.type_of_travel} onChange={handleChange} className="mt-1 p-2 border rounded">
              <option>Business travel</option>
              <option>Personal travel</option>
            </select>
          </label>

          <label className="flex flex-col">
            Customer Type
            <select name="customer_type" value={form.customer_type} onChange={handleChange} className="mt-1 p-2 border rounded">
              <option>Loyal Customer</option>
              <option>Disloyal Customer</option>
            </select>
          </label>

          <label className="flex flex-col">
            Class Type
            <select name="class_type" value={form.class_type} onChange={handleChange} className="mt-1 p-2 border rounded">
              <option>Eco</option>
              <option>Eco Plus</option>
              <option>Business</option>
              <option>First</option>
            </select>
          </label>
        </div>

        <hr />

        <div className="grid grid-cols-2 gap-4">
          <label className="flex flex-col">
            Inflight Wifi Service (1-5)
            <input name="inflight_wifi_service" type="number" min="0" max="5" value={form.inflight_wifi_service} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Online Boarding (1-5)
            <input name="online_boarding" type="number" min="0" max="5" value={form.online_boarding} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Checkin Service (1-5)
            <input name="checkin_service" type="number" min="0" max="5" value={form.checkin_service} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Baggage Handling (1-5)
            <input name="baggage_handling" type="number" min="0" max="5" value={form.baggage_handling} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Seat Comfort (1-5)
            <input name="seat_comfort" type="number" min="0" max="5" value={form.seat_comfort} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Inflight Service (1-5)
            <input name="inflight_service" type="number" min="0" max="5" value={form.inflight_service} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>

          <label className="flex flex-col">
            Cleanliness (1-5)
            <input name="cleanliness" type="number" min="0" max="5" value={form.cleanliness} onChange={handleChange} className="mt-1 p-2 border rounded" />
          </label>
        </div>

        <div className="mt-4 flex gap-2">
          <button type="submit" className="btn px-4 py-2 bg-blue-600 text-white rounded" disabled={loading}>
            {loading ? "Predicting..." : "Predict"}
          </button>
        </div>
      </form>

      {error && <div className="box error mt-4 p-3 bg-red-50 border border-red-200 text-red-700">{error}</div>}

      {result && (
        <div className="box result mt-4 p-4 bg-green-50 border border-green-200 rounded">
          <h3 className="text-lg font-semibold">Prediction</h3>
          <p><strong>Satisfaction:</strong> {result.satisfaction}</p>
          {typeof result.probability === "number" && (
            <p><strong>Confidence:</strong> {(result.probability * 100).toFixed(1)}%</p>
          )}
          <details className="mt-2">
            <summary className="text-sm text-gray-600">Raw response</summary>
            <pre className="text-xs mt-1">{JSON.stringify(result.raw, null, 2)}</pre>
          </details>
        </div>
      )}
    </section>
  );
}
