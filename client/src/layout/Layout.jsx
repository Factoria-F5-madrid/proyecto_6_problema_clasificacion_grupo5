// client/src/layout/Layout.jsx
import React from "react";
import { Outlet } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";

/*
 Layout comp: common UI that wraps pages.
 - Nav stays at the top
 - Outlet renders the current route's page
 - Footer at the bottom
*/
export default function Layout() {
  return (
    <div className="app-root">
      <Nav />
      <main className="container">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
