// client/src/pages/Database.jsx
import React from "react";

/*
 Database page styled with Tailwind to match Home.
 Placeholder table that looks polished; replace with dynamic data fetching later.
*/

export default function Database() {
  // placeholder rows (replace by fetched data later)
  const rows = [
    { id: "PX001", gender: "Male", age: 35, distance: 1200, satisfaction: "neutral or dissatisfied" },
    { id: "PX002", gender: "Female", age: 28, distance: 300, satisfaction: "satisfied" },
    { id: "PX003", gender: "Male", age: 42, distance: 760, satisfaction: "satisfied" }
  ];

  return (
    <section className="py-6 px-6 md:px-12">
      <div className="max-w-[1100px] mx-auto">
        <header className="mb-6">
          <h2 className="text-3xl font-extrabold text-[#114665]">Dataset: Airline Passenger Satisfaction</h2>
          <p className="mt-2 text-sm text-gray-600">
            Preview of the dataset. In production, this table will be backed by the API with pagination and filters.
          </p>
        </header>

        <div className="bg-white/90 rounded-2xl shadow-md overflow-hidden">
          <div className="flex items-center justify-between p-4 border-b">
            <div>
              <h3 className="text-base font-semibold text-[#0b2534]">Preview</h3>
              <p className="text-xs text-gray-500">Showing recent examples (static placeholder)</p>
            </div>
            <div>
              <button className="px-3 py-1 rounded-md bg-[#2E8EE6] text-white text-sm font-medium hover:bg-[#1666B3] transition">
                Refresh
              </button>
            </div>
          </div>

          <div className="p-4">
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-left text-xs text-gray-500 uppercase">
                    <th className="px-3 py-2">PassengerId</th>
                    <th className="px-3 py-2">Gender</th>
                    <th className="px-3 py-2">Age</th>
                    <th className="px-3 py-2">FlightDistance</th>
                    <th className="px-3 py-2">Satisfaction</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((r, idx) => (
                    <tr
                      key={r.id}
                      className={`border-t ${idx % 2 === 0 ? "bg-white" : "bg-gray-50"}`}
                    >
                      <td className="px-3 py-3 font-medium text-[#114665]">{r.id}</td>
                      <td className="px-3 py-3 text-gray-700">{r.gender}</td>
                      <td className="px-3 py-3">{r.age}</td>
                      <td className="px-3 py-3">{r.distance}</td>
                      <td className="px-3 py-3">
                        <span
                          className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${
                            r.satisfaction === "satisfied"
                              ? "bg-green-100 text-green-800"
                              : "bg-yellow-100 text-yellow-800"
                          }`}
                        >
                          {r.satisfaction}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-4 flex justify-between items-center">
              <div className="text-xs text-gray-500">Total rows: {rows.length}</div>
              <div className="text-xs">
                <button className="px-3 py-1 rounded-md bg-white border text-[#1666B3] text-sm">Export CSV</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
