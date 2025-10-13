// client/src/App.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./layout/Layout";
import Home from "./pages/Home";
import Database from "./pages/Database";
import Predict from "./pages/Predict";
import Team from "./pages/Team";
import Splash from "./pages/Splash";

export default function App() {
  return (
    <Routes>
      {/* Splash solo se muestra al entrar a la raíz "/" */}
      <Route path="/" element={<Splash />} />

      {/* Todas las demás páginas dentro del Layout */}
      <Route path="/" element={<Layout />}>
        <Route path="home" element={<Home />} />
        <Route path="database" element={<Database />} />
        <Route path="predict" element={<Predict />} />
        <Route path="team" element={<Team />} />
        {/* Redirige cualquier ruta desconocida a home */}
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Route>
    </Routes>
  );
}
