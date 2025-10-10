// client/src/pages/Database.jsx
import React from "react";

/*
 Database page: summary + small preview.
 In production you'd fetch paginated data from backend; here we show a placeholder table.
*/
export default function Database() {
  return (
    <section className="page">
      <h2>Dataset: Airline Passenger Satisfaction</h2>
      <p>
        This page should show a preview of <code>airline_passenger_satisfaction.csv</code>.
        Ideally you fetch it from the backend and implement pagination + filters.
      </p>

      {/* Placeholder table - replace with real data fetching */}
      <div className="table-preview">
        <table>
          <thead>
            <tr>
              <th>PassengerId</th>
              <th>Gender</th>
              <th>Age</th>
              <th>FlightDistance</th>
              <th>Satisfaction</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>1</td><td>Male</td><td>35</td><td>1200</td><td>neutral or dissatisfied</td></tr>
            <tr><td>2</td><td>Female</td><td>28</td><td>300</td><td>satisfied</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  );
}
