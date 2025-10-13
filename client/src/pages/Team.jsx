// client/src/pages/Team.jsx
import React from "react";

/*
 Team page styled with Tailwind to match Home.
*/

const members = [
  {
    name: "Teo Ramos",
    role: "Frontend lead — UI, UX, visual design.",
    initials: "TR",
    linkedin: "https://www.linkedin.com/in/teo-ramos-ruano/"
  },
  {
    name: "Yeder Pimentel Tapia",
    role: "Backend & model integration.",
    initials: "YP",
    linkedin: "https://www.linkedin.com/in/yeder-pimentel/"
  },
  {
    name: "Alfonso Bermúdez Torres",
    role: "Data scientist — Scrum master.",
    initials: "AB",
    linkedin: "https://www.linkedin.com/in/alfonsobermudeztorres/"
  },
  {
    name: "Maribel Gutiérrez Ramírez",
    role: "Project manager & data analyst.",
    initials: "MG",
    linkedin: "https://www.linkedin.com/in/maribel-guti%C3%A9rrez-ram%C3%ADrez/"
  }
];

export default function Team() {
  return (
    <section className="min-h-[60vh] py-2 px-6 md:px-12">
      <div className="max-w-[1100px] mx-auto">
        {/* Header */}
        <header className="mb-10 text-center md:text-left">
          <h2 className="text-3xl md:text-4xl font-extrabold text-[#114665] leading-tight">
            Meet the Team
          </h2>
          <p className="mt-2 text-xl  text-gray-600">
            We are Group 5 — building better flight comfort tools and data-driven experiences.
          </p>
        </header>

        {/* Team Grid */}
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {members.map((m) => (
            <article
              key={m.name}
              className="group bg-white/90 p-6 rounded-2xl shadow-md hover:shadow-xl transition-all duration-200 flex flex-col justify-between"
            >
              <div>
                {/* Avatar with initials */}
                <div
                  className="flex items-center justify-center w-14 h-14 rounded-lg text-white text-lg font-semibold mb-4 mx-auto md:mx-0"
                  style={{
                    background:
                      "linear-gradient(180deg, rgba(99,185,255,1), rgba(46,142,230,1))"
                  }}
                >
                  {m.initials}
                </div>

                {/* Name and Role */}
                <h3 className="text-lg font-semibold text-[#0b2534] text-center md:text-left">
                  {m.name}
                </h3>
                <p className="mt-1 text-sm text-gray-600 text-center md:text-left">
                  {m.role}
                </p>
              </div>

              {/* Action Buttons */}
              <div className="mt-5 flex flex-col items-center md:items-start gap-3">
                <a
                  href={m.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#EAF4FF] text-[#1666B3] text-sm font-medium hover:bg-[#D0EAFF] transition-colors"
                >
                  View profile
                </a>
              </div>
            </article>
          ))}
        </div>

        {/* Footer note */}
        <div className="mt-10 text-center text-sm text-gray-650">
          Grupo 5 — Factoria F5 Bootcamp IA
        </div>
      </div>
    </section>
  );
}
