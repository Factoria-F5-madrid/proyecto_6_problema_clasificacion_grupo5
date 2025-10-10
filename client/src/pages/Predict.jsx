// client/src/pages/Predict.jsx
import React, { useState } from "react";
import { predictPassenger } from "../services/predictPassengerServices";

/*
 Predict page: form collects required inputs, calls service, shows result.
 The fields here are examples — adapt to the model's expected features.
*/
export default function Predict() {
  const [form, setForm] = useState({
    Gender: "Male",
    Age: 30,
    FlightDistance: 500,
    CabinService: 3 // example rating
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: isNaN(value) ? value : Number(value) }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      // This calls your client/src/services/predictPassengerServices.js
      const res = await predictPassenger(form);
      setResult(res); // assume backend returns an object like {satisfaction: "satisfied", probability: 0.87}
    } catch (err) {
      setError(err.message || "Failed to predict");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page predict-page">
      <h2>Passenger Satisfaction Predictor</h2>
      <p>Fill the fields below and press Predict. The model will return the satisfaction prediction.</p>

      <form onSubmit={handleSubmit} className="predict-form">
        <label>
          Gender
          <select name="Gender" value={form.Gender} onChange={handleChange}>
            <option>Male</option>
            <option>Female</option>
          </select>
        </label>

        <label>
          Age
          <input name="Age" type="number" value={form.Age} onChange={handleChange} min="0" />
        </label>

        <label>
          Flight Distance (km)
          <input name="FlightDistance" type="number" value={form.FlightDistance} onChange={handleChange} min="0" />
        </label>

        <label>
          Cabin Service Rating (1-5)
          <input name="CabinService" type="number" value={form.CabinService} onChange={handleChange} min="1" max="5" />
        </label>

        <div className="form-actions">
          <button type="submit" className="btn" disabled={loading}> {loading ? "Predicting..." : "Predict"} </button>
        </div>
      </form>

      {error && <div className="box error">{error}</div>}

      {result && (
        <div className="box result">
          <h3>Prediction</h3>
          <p><strong>Satisfaction:</strong> {result.satisfaction ?? result.result ?? JSON.stringify(result)}</p>
          {result.probability && <p><strong>Confidence:</strong> {(result.probability*100).toFixed(1)}%</p>}
        </div>
      )}
    </section>
  );
}
