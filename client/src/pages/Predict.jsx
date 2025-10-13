import React, { useState } from "react";
import { predictPassenger } from "../services/predictPassengerServices";

/*
 Predict page (compact & wide): same logic, improved responsive design
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
    setForm((prev) => ({ ...prev, [name]: parsed }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const payload = {};
      for (const [k, v] of Object.entries(form)) {
        payload[k] = v === "" ? null : v;
      }

      const res = await predictPassenger(payload);
      const uiResult = {
        satisfaction: res.satisfaction ?? res.predicted_label ?? null,
        probability: res.predicted_proba ?? res.probability ?? null,
        raw: res
      };
      setResult(uiResult);
    } catch (err) {
      setError(err?.message ?? String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="flex justify-center">
      <div className="w-full max-w-6xl bg-white/80 backdrop-blur-sm p-4 rounded-2xl shadow-lg">
        <h2 className="text-3xl font-bold text-[#114665] mb-2 text-center">
          Passenger Satisfaction Predictor
        </h2>
        <p className="mb-6 text-sm text-gray-600 text-center">
          Rellene el formulario y pulse <strong>Predict</strong>.
        </p>

        {/* FORM */}
        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-4 gap-4 text-sm"
        >
          {/* BASIC INFO */}
          <label className="flex flex-col">
            Passenger ID
            <input
              name="passenger_id"
              value={form.passenger_id}
              onChange={handleChange}
              className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-300"
            />
          </label>

          <label className="flex flex-col">
            Gender
            <select
              name="gender"
              value={form.gender}
              onChange={handleChange}
              className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm"
            >
              <option value="male">male</option>
              <option value="female">female</option>
              <option value="other">other</option>
            </select>
          </label>

          <label className="flex flex-col">
            Age
            <input
              name="age"
              type="number"
              min="0"
              value={form.age}
              onChange={handleChange}
              className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm"
            />
          </label>

          <label className="flex flex-col">
            Type of travel
            <select
              name="type_of_travel"
              value={form.type_of_travel}
              onChange={handleChange}
              className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm"
            >
              <option>Business travel</option>
              <option>Personal travel</option>
            </select>
          </label>

          <label className="flex flex-col">
            Customer Type
            <select
              name="customer_type"
              value={form.customer_type}
              onChange={handleChange}
              className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm"
            >
              <option>Loyal Customer</option>
              <option>Disloyal Customer</option>
            </select>
          </label>

          <label className="flex flex-col">
            Class Type
            <select
              name="class_type"
              value={form.class_type}
              onChange={handleChange}
              className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm"
            >
              <option>Eco</option>
              <option>Eco Plus</option>
              <option>Business</option>
              <option>First</option>
            </select>
          </label>

          {/* NUMERIC RATINGS */}
          {[
            "inflight_wifi_service",
            "online_boarding",
            "checkin_service",
            "baggage_handling",
            "seat_comfort",
            "inflight_service",
            "cleanliness"
          ].map((field) => (
            <label key={field} className="flex flex-col">
              {field
                .replaceAll("_", " ")
                .replace(/\b\w/g, (l) => l.toUpperCase())}{" "}
              (1-5)
              <input
                name={field}
                type="number"
                min="0"
                max="5"
                value={form[field]}
                onChange={handleChange}
                className="mt-1 px-2 py-1 border border-gray-300 rounded-md text-sm"
              />
            </label>
          ))}

          {/* BUTTON */}
          <div className="col-span-4 flex justify-center mt-4">
            <button
              type="submit"
              className="px-6 py-2 bg-[#114665] text-white rounded-lg font-semibold hover:bg-[#0b2534] transition-all"
              disabled={loading}
            >
              {loading ? "Predicting..." : "Predict"}
            </button>
          </div>
        </form>

        {/* ERROR */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* RESULT */}
        {result && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded">
            <h3 className="text-lg font-semibold text-green-800 mb-1">
              Prediction
            </h3>
            <p>
              <strong>Satisfaction:</strong>{" "}
              {result.satisfaction === "0"
                ? "Neutral or Dissatisfied"
                : result.satisfaction === "1"
                ? "Satisfied"
                : result.satisfaction}
            </p>
            {typeof result.probability === "number" && (
              <p>
                <strong>Confidence:</strong>{" "}
                {(result.probability * 100).toFixed(1)}%
              </p>
            )}
            <details className="mt-2 text-sm text-gray-600">
              <summary className="cursor-pointer">Raw response</summary>
              <pre className="text-xs mt-1 overflow-auto max-h-40">
                {JSON.stringify(result.raw, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </section>
  );
}
