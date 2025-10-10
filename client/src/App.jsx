// client/src/App.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./layout/Layout";
import Home from "./pages/Home";
import Database from "./pages/Database";
import Predict from "./pages/Predict";
import Team from "./pages/Team";

/*
  App defines top-level routes. Using Layout wraps pages with Nav + Footer.
  If you want nested routes or protected routes later, add them here.
*/
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="database" element={<Database />} />
        <Route path="predict" element={<Predict />} />
        <Route path="team" element={<Team />} />
        {/* Redirect unknown paths to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
